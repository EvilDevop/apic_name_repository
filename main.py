import pygame
import sys

FPS = 60


pygame.init()
pygame.display.set_mode((1336, 788))
clock = pygame.time.Clock()


pygame.display.update()


while True:


    clock.tick(FPS)

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()


    pygame.display.update()