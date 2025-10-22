from typing import TYPE_CHECKING
from enum import Enum, auto, IntFlag

import extro.internal.InstanceManager as InstanceManager
from extro.shared.Coord import CoordType
import extro.internal.systems.Collision as CollisionSystem
import extro.internal.ComponentManager as ComponentManager

if TYPE_CHECKING:
    from extro.instances.core.components.Transform import Transform
    from extro.instances.core.components.Hierarchy import Hierarchy


class TransformUpdateType(Enum):
    POSITION = auto()
    ROTATION = auto()
    SIZE = auto()


class TransformDirtyFlags(IntFlag):
    POSITION = auto()
    SIZE = auto()
    ROTATION = auto()


def recalculate_position(
    transform: "Transform",
    hierarchy: "Hierarchy | None",
):
    new_x: float = 0
    new_y: float = 0

    match transform._position.type:
        case CoordType.RELATIVE if hierarchy and hierarchy._parent is not None:
            parent_x, parent_y, parent_width, parent_height = (
                ComponentManager.transforms[hierarchy._parent]._bounding
            )
            new_x = parent_x + (parent_width * transform._position.x)
            new_y = parent_y + (parent_height * transform._position.y)
        case _:
            new_x, new_y = transform._position.to_tuple()

    width, height = transform._actual_size
    offset_x, offset_y = transform._position_offset
    transform._actual_position = (
        new_x - (width * transform._anchor.x) + offset_x,
        new_y - (height * transform._anchor.y) + offset_y,
    )

    recalculate_bounding(transform)
    transform.on_update.fire(TransformUpdateType.POSITION)


def recalculate_bounding(
    transform: "Transform",
):
    width, height = transform._actual_size
    x, y = transform._actual_position
    transform._bounding = (
        x - transform._position_offset[0],
        y - transform._position_offset[1],
        width,
        height,
    )


def recalculate_size(
    transform: "Transform",
    hierarchy: "Hierarchy | None",
):
    new_x = transform._size.absolute_x * transform._scale.x
    new_y = transform._size.absolute_y * transform._scale.y

    if (
        transform._size.type == CoordType.RELATIVE
        and hierarchy
        and hierarchy._parent is not None
    ):
        _, _, parent_width, parent_height = ComponentManager.transforms[
            hierarchy._parent
        ]._bounding
        new_x *= parent_width
        new_y *= parent_height

    transform._actual_size = (new_x, new_y)

    # No `recalculate_bounding` here because `recalculate_position`, which should be called after this function, calls it


def update():
    transforms = ComponentManager.transforms.items()

    # Do an initial pass to calculate if any children need updating due to parent changes
    for instance_id, transform in transforms:
        hierarchy = ComponentManager.hierarchies.get(instance_id)

        if not hierarchy:
            continue

        if not transform.has_flag(TransformDirtyFlags.SIZE) and not transform.has_flag(
            TransformDirtyFlags.POSITION
        ):
            continue

        for child_id in hierarchy._children:
            child_transform = ComponentManager.transforms.get(child_id)

            if not child_transform:
                continue

            child_transform._flags |= transform._flags

    for instance_id, transform in transforms:
        if transform._flags == 0:
            continue

        hierarchy = ComponentManager.hierarchies.get(instance_id)

        # if/else because size change requires position to be recalculated
        if transform.has_flag(TransformDirtyFlags.SIZE):
            recalculate_size(transform, hierarchy)

            # If the instance has a `Drawable` component the transform needs to be offset by half (because the render origin is in the center)
            if ComponentManager.drawables.get(instance_id):
                transform._position_offset = (
                    transform._actual_size[0] / 2,
                    transform._actual_size[1] / 2,
                )

            recalculate_position(transform, hierarchy)
        elif transform.has_flag(TransformDirtyFlags.POSITION):
            recalculate_position(transform, hierarchy)

        transform.clear_flags()

        collider = ComponentManager.colliders.get(instance_id)
        if collider:
            CollisionSystem.on_transform_change(collider, transform)
