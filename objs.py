import pygame
import cons as cs

objlist = []
pygame.init()


class Map:

  def __init__(self, file):
    self.data = []
    with open(file, 'rt') as f:
      for x in f:
        self.data.append(x)
    self.tilewidth = len(self.data[0])
    self.tileheight = len(self.data)
    self.width = self.tilewidth * cs.tilesize
    self.height = self.tileheight * cs.tilesize


class Camera: #dont think we need this anymore wait i lied ehhhh did i though gyap

  def __init__(self, width, height):
    self.camera = pygame.Rect(0, 0, width, height)
    self.width = width
    self.height = height

  def apply(self, object):
    return object.rect.move(self.camera.topleft)

  def update(self, gart):
    x = -gart.rect.x + cs.diswidth / 2
    y = -gart.rect.y + cs.disheight / 2
    x = min(0, x)
    y = min(0, y)
    x = max(-(self.width - cs.diswidth), x)
    y = max(-(self.height - cs.disheight), y)
    self.camera = pygame.Rect(x, y, self.width, self.height)


class Player(pygame.sprite.Sprite):

  def __init__(self, game, x, y):
    self.group = game.all_sprites
    pygame.sprite.Sprite.__init__(self, self.group)
    self.game = game
    self.image = pygame.Surface((cs.tilesize, cs.tilesize))
    self.image.fill(cs.black)
    self.rect = self.image.get_rect()
    self.x = x
    self.y = y
    #self.rect = self.image.get_rect(topleft = (self.x, self.y))

  def move(self, xchange=0, ychange=0):
    if not self.collicase(xchange, ychange):
      self.x += xchange
      self.y += ychange

  def collicase(self, xchange=0, ychange=0):
    for bigolwall in self.game.obstruction:
      if bigolwall.x == self.x + xchange and bigolwall.y == self.y + ychange:
        if isinstance(bigolwall, Interactable):
          self.game.displaytext = True
        return True
    return False



  def update(self):
    self.rect.x = self.x * cs.tilesize
    self.rect.y = self.y * cs.tilesize

'''class Background(pygame.sprite.Sprite):
  def __init__(self, x, y, layers):
    #chat does it need layers im confused
    self.group = layers.all_layers #hurk does this mean that each layer and by layer i just mean like map element will be an object? im fricking lost no right yeah yeah yeah no im chilling
    self.layers = layers
    self.image = pygame.Surface(im lost)
    self.x = x
    self.y = y'''


class Wall(pygame.sprite.Sprite):
  def __init__(self, game, x, y):
    self.game = game
    self.inside = self.game.all_sprites, self.game.obstruction
    pygame.sprite.Sprite.__init__(self, self.inside)
    self._layer = cs.object_layer
    self.x = x
    self.y = y
    self.width = cs.tilesize
    self.height = cs.tilesize
    self.image = pygame.Surface((self.width, self.height))
    self.image.fill(cs.blue)
    self.rect = self.image.get_rect()
    self.rect.x = self.x * cs.tilesize
    self.rect.y = self.y * cs.tilesize

class Interactable(pygame.sprite.Sprite):
  def __init__(self, game, x, y):
    self.game = game
    self.inside = self.game.all_sprites, self.game.obstruction, self.game.interactable
    pygame.sprite.Sprite.__init__(self, self.inside)
    self._layer = cs.object_layer
    self.x = x
    self.y = y
    self.image = pygame.image.load('graphics/tree.png').convert_alpha()
    self.rect = self.image.get_rect()
    self.rect.x = self.x * cs.tilesize
    self.rect.y = self.y * cs.tilesize






class Obstacle(pygame.sprite.Sprite):
  def __init__(self, game, x, y, width, height):
    self.groups = self.game.all_sprites, self.game.obstruction
    pygame.sprite.Sprite().__init__(self, self.groups)
    self.game = game
    self.rect = pygame.Rect(x, y, width, height)
    self.x = x
    self.y = y
    self.rect.x = x * cs.tilesize
    self.rect.y = y * cs.tilesize
