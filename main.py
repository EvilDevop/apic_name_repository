import pygame
import sys


class Map_ya:
    def __init__(self):
        super(Map_ya, self).__init__()
        self.img = pygame.image.load("data/test.png")

    def render(self):
        a = self.img.get_rect(bottomright=(875, 650))
        screen.blit(self.img, a)

FPS = 60
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((1200, 750))
pygame.display.set_caption('epic_map')

all_sprites = pygame.sprite.Group()

sprite_pole = pygame.sprite.Sprite()
sprite_pole.image = pygame.image.load("data/background_img.jpg")
sprite_pole.rect = sprite_pole.image.get_rect()
all_sprites.add(sprite_pole)
sprite_pole.rect.x = 0
sprite_pole.rect.y = 0

map_ya = Map_ya()


class App:
    def __init__(self, list_but, map):
        super(App, self).__init__()
        self.list_but = list_but
        self.map = map

    def render(self):
        map_ya.render()

    def on_click(self, cell):
        print(cell)


app = App([], [])

while True:
    clock.tick(FPS)

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit()
        elif i.type == pygame.MOUSEBUTTONDOWN:
            app.on_click(i.pos)

    all_sprites.draw(screen)
    app.render()
    pygame.display.update()