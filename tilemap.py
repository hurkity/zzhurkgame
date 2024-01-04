import pygame
from cons import *
class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line)
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * tilesize
        self.height = self.tilewidth * tilesize


class View:
    def __init__(self, width, height):
        self.view = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def implement(self, thing):
        return thing.rect.move(self.view.topleft)

    def update(self, target):
        x = -target.rect.x + int(width/2)
        y = -target.rect.y + int(height/2)
        self.camera = pygame.Rect(x, y, self.width, self.height)
