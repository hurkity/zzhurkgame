import pygame
import cons as cs

vc = pygame.math.Vector2

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


class Camera:  # dont think we need this anymore wait i lied ehhhh did i though gyap

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
        self.group = game.all_sprites, game.playergroup
        pygame.sprite.Sprite.__init__(self, self.group)
        self.game = game
        self.currentsprite = 0

        self.frontsprites = []
        self.image = game.player_img
        self.imagefrontleft = game.player_imgfrontleft
        self.imagefrontright = game.player_imgfrontright

        self.image = pygame.transform.scale(self.image, (32, 32))
        self.imagefrontleft = pygame.transform.scale(self.imagefrontleft, (32, 32))
        self.imagefrontright = pygame.transform.scale(self.imagefrontright, (32, 32))

        self.frontsprites.append(self.image)
        self.frontsprites.append(self.imagefrontleft)
        self.frontsprites.append(self.image)
        self.frontsprites.append(self.imagefrontright)

        self.leftsprites = []
        self.imageleft = game.player_imgleft
        self.imageleftleft = game.player_imgleftleft
        self.imageleftright = game.player_imgleftright

        self.imageleft = pygame.transform.scale(self.imageleft, (32, 32))
        self.imageleftleft = pygame.transform.scale(self.imageleftleft, (32, 32))
        self.imageleftright = pygame.transform.scale(self.imageleftright, (32, 32))

        self.leftsprites.append(self.imageleft)
        self.leftsprites.append(self.imageleftleft)
        self.leftsprites.append(self.imageleft)
        self.leftsprites.append(self.imageleftright)

        self.rightsprites = []
        self.imageright = game.player_imgright
        self.imagerightleft = game.player_imgrightleft
        self.imagerightright = game.player_imgrightright

        self.imageright = pygame.transform.scale(self.imageright, (32, 32))
        self.imagerightleft = pygame.transform.scale(self.imagerightleft, (32, 32))
        self.imagerightright = pygame.transform.scale(self.imagerightright, (32, 32))

        self.rightsprites.append(self.imageright)
        self.rightsprites.append(self.imagerightleft)
        self.rightsprites.append(self.imageright)
        self.rightsprites.append(self.imagerightright)

        self.backsprites = []
        self.imageback = game.player_imgback
        self.imagebackleft = game.player_imgbackleft
        self.imagebackright = game.player_imgbackright

        self.imageback = pygame.transform.scale(self.imageback, (32, 32))
        self.imagebackleft = pygame.transform.scale(self.imagebackleft, (32, 32))
        self.imagebackright = pygame.transform.scale(self.imagebackright, (32, 32))

        self.backsprites.append(self.imageback)
        self.backsprites.append(self.imagebackleft)
        self.backsprites.append(self.imageback)
        self.backsprites.append(self.imagebackright)

        self.sprites_group = {"fwd": self.frontsprites, "left": self.leftsprites, "right": self.rightsprites,
                              "bwd": self.backsprites}

        self.velocity = vc(0, 0)
        self.position = vc(x, y)
        self.rect = self.image.get_rect()
        self.rectleft = self.imageleft.get_rect()
        self.rectright = self.imageright.get_rect()
        self.rectback = self.imageback.get_rect()
        self.vx, self.vy = 0, 0
        self.hit_rect = cs.playerhitrect
        self.direction = 0

        self.x = x
        self.y = y
        self.freeze = False
        self.cutscene = False
        self.cutsceneend = False
        self.directions = []

        #object interaction schturrrrff
        self.status = "free"
        self.keytype = None
        self.interactivity = False
        # self.rect = self.image.get_rect(topleft = (self.x, self.y))

    def get_keys(self):
        if self.cutscene:
            if len(self.directions) > 0:
                direction = self.directions[0]
                if direction == 'left':
                    self.position.x -= cs.block_speed
                    self.velocity.x = -cs.player_speed/2
                elif direction == 'right':
                    self.position.x += cs.block_speed
                    self.velocity.x = cs.player_speed/2
                elif direction == 'fwd':
                    self.position.y += cs.block_speed
                    self.velocity.y = cs.player_speed/2
                elif direction == 'bwd':
                    self.position.y -= cs.block_speed
                    self.velocity.y = -cs.player_speed/2
                self.directions.pop(0)
                print (self.directions)
                return direction
            else:
                self.cutsceneend = True
        direction = None
        self.velocity = vc(0, 0)
        if self.game.interactivity == False:
            keez = pygame.key.get_pressed()
            if keez[pygame.K_LEFT] or keez[pygame.K_a]:
                direction = "left"
                self.velocity.x = -cs.player_speed
            elif keez[pygame.K_RIGHT] or keez[pygame.K_d]:
                direction = "right"
                self.velocity.x = cs.player_speed
            elif keez[pygame.K_DOWN] or keez[pygame.K_s]:
                direction = "fwd"
                self.velocity.y = cs.player_speed
            elif keez[pygame.K_UP] or keez[pygame.K_w]:
                direction = "bwd"
                self.velocity.y = -cs.player_speed
        return direction

    def getanigroup(self):
        if self.direction == None:
            return None
        return self.sprites_group[self.direction]

    def collicase(self, axis):
        if axis == 'x':
            collision = pygame.sprite.spritecollide(self, self.game.obstruction,
                                                    False)
            if collision:
                if self.velocity.x > 0:
                    self.position.x = collision[0].rect.left - self.rect.width
                if self.velocity.x < 0:
                    self.position.x = collision[0].rect.right
                self.velocity.x = 0
                self.rect.x = self.position.x
        if axis == 'y':
            collision = pygame.sprite.spritecollide(self, self.game.obstruction,
                                                    False)
            if collision:
                if self.velocity.y > 0:
                    self.position.y = collision[0].rect.top - self.rect.height
                if self.velocity.y < 0:
                    self.position.y = collision[0].rect.bottom
                self.velocity.y = 0
                self.rect.y = self.position.y

    def holding(self, target):
        self.keytype = target.type
        target.rect.center = self.rect.midbottom
        return True


    def update(self):
        if self.freeze:
            return
        self.direction = self.get_keys()
        self.position += self.velocity * self.game.dt
        self.rect.x = self.position.x
        self.collicase('x')
        self.rect.y = self.position.y
        self.collicase('y')
        return self.direction


'''class Background(pygame.sprite.Sprite):
  def __init__(self, x, y, layers):
    #chat does it need layers im confused
    self.group = layers.all_layers #hurk does this mean that each layer and by layer i just mean like map element will be an object? im fricking lost no right yeah yeah yeah no im chilling
    self.layers = layers
    self.image = pygame.Surface(im lost)
    self.x = x
    self.y = y'''


class Interactable(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.inside = self.game.all_sprites, self.game.obstruction, \
            self.game.interactable
        pygame.sprite.Sprite.__init__(self, self.inside)
        self._layer = cs.object_layer
        self.x = x
        self.y = y
        self.image = pygame.image.load('graphics/tree.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.x * cs.tilesize
        self.rect.y = self.y * cs.tilesize


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


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self.game = game
        self.inside = self.game.obstruction
        pygame.sprite.Sprite.__init__(self, self.inside)
        self.rect = pygame.Rect(x, y, width, height)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y


class InteractableBox(pygame.sprite.Sprite):
    def __init__(self, game, type, x, y, w, h):
        self.game = game
        self.type = type
        self.inside = self.game.interactablebox
        pygame.sprite.Sprite.__init__(self, self.inside)
        # self._layer = cs.object_layer
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        # self.image = pygame.Surface((18, 18), pygame.SRCALPHA, 32)
        self.rect.x = self.x
        self.rect.y = self.y

class InteractableLox(pygame.sprite.Sprite):
    def __init__(self, game, type, x, y, w, h):
        self.game = game
        self.type = type
        self.inside = self.game.interactablelox
        pygame.sprite.Sprite.__init__(self, self.inside)
        # self._layer = cs.object_layer
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        # self.image = pygame.Surface((18, 18), pygame.SRCALPHA, 32)
        self.rect.x = self.x
        self.rect.y = self.y

class Teleport(pygame.sprite.Sprite):
    def __init__(self, game, type, x, y, w, h):
        self.game = game
        self.inside = self.game.teleport
        pygame.sprite.Sprite.__init__(self, self.inside)
        # self._layer = cs.object_layer
        self.type = type
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        # self.image = pygame.Surface((18, 18), pygame.SRCALPHA, 32)
        self.rect.x = self.x
        self.rect.y = self.y


class TextDisplay(pygame.sprite.Sprite):  # textbox appearing to describe objects

    def __init__(self, game, x, y, width, height, type):
        self.game = game
        self.type = type
        self.inside = self.game.text, self.game.obstruction
        pygame.sprite.Sprite.__init__(self, self.inside)
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.hit_rect = self.rect
        self.font = cs.objfont
        self.image = pygame.image.load('graphics/tree.png').convert_alpha()
        self.text = cs.font.render(cs.Text[self.type][self.game.textindex], True, cs.white)
        self.textimage = pygame.Surface((cs.diswidth, 0.2 * cs.disheight),
                                        pygame.SRCALPHA)
        self.textimage.fill(cs.translucent_black)
        self.textrect = self.textimage.get_rect()
        self.textrect.x = 0
        self.textrect.y = cs.diswidth * 0.8

    def displaymytextbetter(self, index):
        self.game.dis.blit(self.textimage, self.textrect)
        self.game.dis.blit(self.text, self.textrect)
        self.game.dis.blit(cs.text2, cs.textRect2)
        self.game.dis.blit(cs.text3, cs.textRect3)
        self.text = cs.font.render(cs.Text[self.type][self.game.textindex], True, cs.white)
        pygame.display.update()

    def displaymytext(self):
        self.game.dis.blit(cs.text, cs.textRect)
        self.game.dis.blit(cs.textSecondLine, cs.textSecondLineRect)
        pygame.display.update()



class Lock(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, type, text_id):
        self.game = game
        self.type = type
        self.inside = self.game.locks, self.game.obstruction
        pygame.sprite.Sprite.__init__(self, self.inside)
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.hit_rect = self.rect
        self.font = cs.objfont
        self.image = pygame.image.load('graphics/truck.png').convert()
        self.image = pygame.transform.scale(self.image, (self.rect.width,
                                                         self.rect.height))
        self.text = cs.font.render(cs.LockText[text_id], True, cs.white)
        self.textimage = pygame.Surface((cs.diswidth, 0.2 * cs.disheight),
                                        pygame.SRCALPHA)
        self.textimage.fill(cs.translucent_black)
        self.textrect = self.textimage.get_rect()
        self.textrect.x = 0
        self.textrect.y = cs.diswidth * 0.8

    def unlocked(self, key, changetarget, player):
        self.image = changetarget.image
        pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        pygame.sprite.Sprite.remove(self, self.game.obstruction)
        player.status = "free"
        key.kill()

class Lockchange(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, type, text_id):
        self.game = game
        self.type = type
        self.inside = self.game.lockchange
        pygame.sprite.Sprite.__init__(self, self.inside)
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.hit_rect = self.rect
        self.font = cs.objfont
        self.image = pygame.image.load('graphics/painter.jpg').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.text = cs.font.render(cs.LockText[text_id], True, cs.white)
        self.textimage = pygame.Surface((cs.diswidth, 0.2 * cs.disheight),
                                        pygame.SRCALPHA)
        self.textimage.fill(cs.translucent_black)
        self.textrect = self.textimage.get_rect()
        self.textrect.x = 0
        self.textrect.y = cs.diswidth * 0.8

