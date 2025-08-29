from typing import Callable, Any

class Signal:
    __subscribers: list[Callable[..., None]]

    def __init__(self):
        self.__subscribers = []

    def connect(self, callback: Callable[..., None]):
        self.__subscribers.append(callback)

    def fire(self, *args: Any, **kwargs: Any):
        for subscriber in self.__subscribers:
            subscriber(*args, **kwargs)