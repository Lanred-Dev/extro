from enum import Enum, auto, IntFlag

from extro.shared.Coord import Coord
import extro.internal.systems.Collision as CollisionSystem
import extro.internal.ComponentManager as ComponentManager


class TransformUpdateType(Enum):
    POSITION = auto()
    ROTATION = auto()
    SIZE = auto()


class TransformDirtyFlags(IntFlag):
    POSITION = auto()
    SIZE = auto()
    ROTATION = auto()


def update():
    transforms = ComponentManager.transforms.items()

    # Do an initial pass to calculate if any children need updating due to parent changes
    for instance_id, transform in transforms:
        hierarchy = ComponentManager.hierarchies.get(instance_id)

        if (
            not hierarchy
            or not transform.has_flag(TransformDirtyFlags.SIZE)
            and not transform.has_flag(TransformDirtyFlags.POSITION)
        ):
            continue

        for child_id in hierarchy._children:
            child_transform = ComponentManager.transforms.get(child_id)

            if not child_transform:
                continue

            child_transform._flags |= transform._flags

    for instance_id, transform in transforms:
        if transform.is_empty():
            continue

        hierarchy = ComponentManager.hierarchies.get(instance_id)
        recompute_position: bool = transform.has_flag(TransformDirtyFlags.POSITION)

        # if/else because size change requires position to be recalculated
        if transform.has_flag(TransformDirtyFlags.SIZE):
            new_x = transform._size.absolute_x * transform._scale.x
            new_y = transform._size.absolute_y * transform._scale.y

            if (
                transform._size.type == Coord.CoordType.RELATIVE
                and hierarchy
                and hierarchy._parent is not None
            ):
                _, _, parent_width, parent_height = ComponentManager.transforms[
                    hierarchy._parent
                ]._bounding
                new_x *= parent_width
                new_y *= parent_height

            transform._actual_size[0] = new_x
            transform._actual_size[1] = new_y

            # If the instance has a `Drawable` component the transform needs to be offset by half (because the render origin is in the center)
            if ComponentManager.drawables.get(instance_id):
                transform._position_offset[0] = new_x / 2
                transform._position_offset[1] = new_y / 2

            recompute_position = True

        if recompute_position:
            new_x: float = 0
            new_y: float = 0

            match transform._position.type:
                case Coord.CoordType.RELATIVE if (
                    hierarchy and hierarchy._parent is not None
                ):
                    parent_x, parent_y, parent_width, parent_height = (
                        ComponentManager.transforms[hierarchy._parent]._bounding
                    )
                    new_x = parent_x + (parent_width * transform._position.x)
                    new_y = parent_y + (parent_height * transform._position.y)
                case _:
                    new_x = transform._position.absolute_x
                    new_y = transform._position.absolute_y

            width, height = transform._actual_size
            offset_x, offset_y = transform._position_offset
            transform._actual_position[0] = (
                new_x - (width * transform._anchor.x) + offset_x
            )
            transform._actual_position[1] = (
                new_y - (height * transform._anchor.y) + offset_y
            )

            width, height = transform._actual_size
            x, y = transform._actual_position
            transform._bounding[0] = x - transform._position_offset[0]
            transform._bounding[1] = y - transform._position_offset[1]
            transform._bounding[2] = width
            transform._bounding[3] = height

            transform.on_update.fire(TransformUpdateType.POSITION)

        transform.clear_flags()

        collider = ComponentManager.colliders.get(instance_id)
        if collider:
            CollisionSystem.on_transform_change(collider, transform)


def recalculate_normalized_coords():
    for transform in ComponentManager.transforms.values():
        if transform._position.type == Coord.CoordType.NORMALIZED:
            transform._position._set_using_normalized(
                transform._position.x, transform._position.y
            )
            transform.add_flag(TransformDirtyFlags.POSITION)

        if transform._size.type == Coord.CoordType.NORMALIZED:
            transform._size._set_using_normalized(transform._size.x, transform._size.y)
            transform.add_flag(TransformDirtyFlags.SIZE)
