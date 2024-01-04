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
    self.vx, self.vy = 0, 0
    self.x = x * cs.tilesize
    self.y = y * cs.tilesize
    #self.rect = self.image.get_rect(topleft = (self.x, self.y))

  def get_keys(self):
    self.vx, self.vy = 0, 0
    keez = pygame.key.get_pressed()
    if keez[pygame.K_LEFT] or keez[pygame.K_a]:
      self.vx = -cs.player_speed
    elif keez[pygame.K_RIGHT] or keez[pygame.K_d]:
      self.vx = cs.player_speed
    elif keez[pygame.K_DOWN] or keez[pygame.K_s]:
      self.vy = cs.player_speed
    elif keez[pygame.K_UP] or keez[pygame.K_w]:
      self.vy = -cs.player_speed



  def collicase(self, axis):
    if axis == 'x':
      collision = pygame.sprite.spritecollide(self, self.game.obstruction, False)
      if collision:
        if self.vx > 0:
          self.x = collision[0].rect.left - self.rect.width
        if self.vx < 0:
          self.x = collision[0].rect.right
        self.vx = 0
        self.rect.x = self.x
    if axis == 'y':
      collision = pygame.sprite.spritecollide(self, self.game.obstruction, False)
      if collision:
        if self.vy > 0:
          self.y = collision[0].rect.top - self.rect.height
        if self.vy < 0:
          self.y = collision[0].rect.bottom
        self.vy = 0
        self.rect.y = self.y




  def update(self):
    self.get_keys()
    self.x += self.vx * self.game.dt
    self.y += self.vy * self.game.dt
    self.rect.x = self.x
    self.collicase('x')
    self.rect.y = self.y
    self.collicase('y')

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

class InteractableBox(pygame.sprite.Sprite):
  def __init__(self, game, x, y):
    self.game = game
    self.inside = self.game.all_sprites, self.game.interactablebox
    pygame.sprite.Sprite.__init__(self, self.inside)
    self._layer = cs.object_layer
    self.x = x
    self.y = y
    self.image = pygame.Surface((18, 18), pygame.SRCALPHA, 32)
    self.rect = self.image.get_rect()
    self.rect.x = self.x * cs.tilesize - 1
    self.rect.y = self.y * cs.tilesize - 1







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
