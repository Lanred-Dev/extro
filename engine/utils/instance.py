from engine.instances import Instance
import typing

InstanceType = typing.TypeVar("InstanceType", bound=Instance)


def createInstance(instance_cls: typing.Type[InstanceType]) -> InstanceType:
    """Create and initialize an instance of the given class."""
    instance = instance_cls()
    instance.init()
    return instance
