import pyray
from typing import TYPE_CHECKING

from extro.internal.utils.InstanceRegistry import InstanceRegistry
import extro.internal.InstanceManager as InstanceManager
import extro.services.Timing as TimingService

if TYPE_CHECKING:
    from extro.utils.Timeout import Timeout

timeouts: InstanceRegistry = InstanceRegistry("Timing System")


def update():
    TimingService.delta = pyray.get_frame_time()

    for instance_id in timeouts.instances[:]:
        instance: "Timeout" = InstanceManager.instances[instance_id]  # type: ignore

        if not instance._is_running:
            continue

        instance._elapsed += TimingService.delta

        if instance._elapsed >= instance.delay:
            instance._is_running = False
            instance.on_finish.fire()
