import pygame
from engine.instances import Part
from engine import engine
from engine.utils.instance import createInstance

part1 = createInstance(Part)
part1.set_global_position(100, 100)
part1.set_color(255, 0, 0)
part1.set_global_size(100, 100)

pygame.display.set_caption("Ghost Librarian")
engine.start()
