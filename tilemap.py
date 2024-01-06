import pygame
import pytmx

import cons as cs
class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * cs.tilesize
        self.height = self.tilewidth * cs.tilesize

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha = True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, platform):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        platform.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface
class View:
    def __init__(self, width, height):
        self.view = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def implement(self, thing):
        return thing.rect.move(self.view.topleft)

    def implement_rect(self, rect):
        return rect.move(self.view.topleft)
    def update(self, target):
        x = -target.rect.x + int(cs.diswidth/2)
        y = -target.rect.y + int(cs.disheight/2)

        #edgehitting
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - cs.diswidth), x)
        y = max(-(self.height - cs.disheight), y)
        self.view = pygame.Rect(x, y, self.width, self.height)
