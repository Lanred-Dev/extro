import pygame
import sys
import typing


class Engine:
    delta: float = 0
    screen: pygame.Surface
    clock: pygame.time.Clock
    fps: int = 60
    __update_callbacks: dict[str, typing.Callable[[], None]] = {}
    __running: bool = True

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))
        self.clock = pygame.time.Clock()

    def start(self):
        while self.__running:
            self.__tick()

        self.quit()

    def __tick(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__running = False

        self.screen.fill((0, 0, 0))

        for updater in list(self.__update_callbacks.values()):
            updater()

        pygame.display.flip()
        self.delta = self.clock.tick(self.fps) / 1000

    def register_updater(self, id: str, function: typing.Callable[[], None]):
        self.__update_callbacks[id] = function

    def unregister_updater(self, id: str):
        self.__update_callbacks.pop(id, None)

    def quit(self):
        pygame.quit()
        sys.exit()


engine = Engine()
