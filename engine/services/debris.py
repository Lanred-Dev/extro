from utils.types import Destroyable
import threading


def debris(instance: Destroyable, duration: float):
    """Schedule deletion of an instance after a given duration."""
    timer = threading.Timer(duration, instance.destroy)
    timer.start()
