import pygame
from enum import Enum


class LogType(Enum):
    ERROR = ("Error", pygame.Color(255, 0, 0))
    INFO = ("Info", pygame.Color(255, 255, 255))
    WARNING = ("Warning", pygame.Color(100, 100, 0))


class Console:
    def __init__(self):
        self.__is_active: bool = False
        self.__history: list[list[str | pygame.Color]] = []
        self.__surface: pygame.Surface | None = None
        self.__max_history_size: int = 1
        self.__font: pygame.font.Font = pygame.font.SysFont("arial", 15)

    def handle_input(self, event: pygame.event.Event):
        if event.key == pygame.K_F10:
            self.__is_active = not self.__is_active

    def log(self, text: str, type: LogType = LogType.INFO):
        [type_text, type_color] = type.value
        self.__history.insert(0, [type_text, type_color, text])

    def tick(self, screen: pygame.Surface):
        screen_size = (screen.get_width(), screen.get_height())
        [_text_width, text_height] = self.__font.size("1")
        self.__max_history_size = int(screen_size[1] / text_height)

        if not self.__is_active:
            return

        if not isinstance(self.__surface, pygame.Surface):
            self.__surface = pygame.Surface(screen_size, pygame.SRCALPHA)

        self.__surface.fill(pygame.Color(0, 0, 0, 225))
        screen.blit(self.__surface, (0, 0))

        for index, (type, color, text) in enumerate(self.__history.copy()):
            if index >= self.__max_history_size:
                return

            text_surface = self.__font.render(f"[{type}]: {text}", True, color)
            screen.blit(text_surface, (0, screen_size[1] - (text_height * (index + 1))))


console = Console()
