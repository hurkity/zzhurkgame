import pygame
import cons as cs
from pygame import mixer

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


class Player(pygame.sprite.Sprite):

    def __init__(self, game, x, y):
        self.group = game.all_sprites, game.playergroup
        pygame.sprite.Sprite.__init__(self, self.group)
        self.game = game
        self._currentsprite = 0

        self.frontsprites = [] #animation loop throughh
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

        self.leftsprites = [] #same but for left facing
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

        self.rightsprites = [] #etc
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
        self.direction = None

        self.x = x
        self.y = y
        self.freeze = False
        self.cutscene = False
        self.cutsceneend = False
        self.directions = []

        self.player_speed = 250

        #object interaction schturrrrff
        self.status = "free"
        self.keytype = -1
        self.rect = self.image.get_rect(topleft = (self.x, self.y))

    @property
    def currentsprite(self): #for bugs during cutscene with movement
        return self._currentsprite
    @currentsprite.setter
    def currentsprite(self, value):
        self._currentsprite = value
        if value is None:
            raise Exception("none")

    def get_keys(self): #player movement
        direction = None
        if self.cutscene: #if in a cutscene, the movement doesn't depend on keys
            self.velocity.x = 0
            self.velocity.y = 0
            if len(self.directions) > 0:
                direction = self.directions[0]
                if direction == 'left':
                    self.position.x -= cs.block_speed
                    self.velocity.x = -self.player_speed/2
                elif direction == 'right':
                    self.position.x += cs.block_speed
                    self.velocity.x = self.player_speed/2
                elif direction == 'fwd':
                    self.position.y += cs.block_speed
                    self.velocity.y = self.player_speed/2
                elif direction == 'bwd':
                    self.position.y -= cs.block_speed
                    self.velocity.y = -self.player_speed/2
                elif direction is None:
                    direction = self.direction
                self.directions.pop(0)
                return direction
            else:
                self.cutsceneend = True
        else: #if not in cutscene, it doesnt depend on keys!
            self.velocity = vc(0, 0)
            if self.game.interactivity == False and self.game.frozen == False:
                keez = pygame.key.get_pressed()
                if keez[pygame.K_LEFT] or keez[pygame.K_a]:
                    direction = "left"
                    self.velocity.x = -self.player_speed
                elif keez[pygame.K_RIGHT] or keez[pygame.K_d]:
                    direction = "right"
                    self.velocity.x = self.player_speed
                elif keez[pygame.K_DOWN] or keez[pygame.K_s]:
                    direction = "fwd"
                    self.velocity.y = self.player_speed
                elif keez[pygame.K_UP] or keez[pygame.K_w]:
                    direction = "bwd"
                    self.velocity.y = -self.player_speed
        return direction

    def getanigroup(self): #animation. the sprite group is passed from here
        if self.direction in ['left', 'right', 'fwd', 'bwd']:
            return self.sprites_group[self.direction]
        else:
            return self.sprites_group['bwd']

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

    def holding(self, target): #picking uyp objects
        self.keytype = target.type
        target.rect.center = self.rect.midbottom
        return True

    def dropped(self): #dropping objects
        for x in self.game.text:
            if x.type == self.keytype:
                self.keytype = -1
                x.rect.topleft = x.topleft
                pygame.sprite.Sprite.add(x, self.game.obstruction)



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
        self.inside = self.game.text, self.game.interactable, self.game.obstruction
        pygame.sprite.Sprite.__init__(self, self.inside)
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.hit_rect = self.rect
        self.font = cs.objfont
        self.image = pygame.image.load('graphics/tree.png').convert_alpha()
        match type:
            case 0:
                self.image = pygame.image.load('graphics/key.png').convert_alpha()
            case 1:
                self.image = pygame.image.load('graphics/jorhny.png').convert_alpha()
            case 2:
                self.image = pygame.image.load('graphics/evangeline.png').convert_alpha()
            case 3:
                self.image = pygame.image.load('graphics/ivy.png').convert_alpha()
            case 4:
                self.image = pygame.image.load('graphics/louise.png').convert_alpha()
            case 5:
                self.image = pygame.image.load('graphics/mittens.png').convert_alpha()
            case 6:
                self.image = pygame.image.load('graphics/bunny.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.rect.width,
                                                         self.rect.height))
        self.text = self.font.render(str(cs.Text[self.type][self.game.textindex].strip("[],")), True, cs.white)
        self.textimage = pygame.Surface((cs.diswidth, 0.2 * cs.disheight),
                                        pygame.SRCALPHA)
        self.textimage.fill(cs.translucent_black)
        self.textrect = self.textimage.get_rect()
        self.textrect.x = 0
        self.textrect.y = cs.diswidth * 0.8
        self.topleft = (self.rect.x, self.rect.y)
    def displaymytextbetter(self):
        self.game.dis.blit(self.textimage, self.textrect)
        self.game.dis.blit(self.text, self.textrect)
        self.game.dis.blit(cs.pressetoclose, cs.etocloserect)
        if len(cs.Text[self.type]) - 1 > self.game.textindex:
            self.game.dis.blit(cs.entertocontinue, cs.textRect3)
        self.text = self.font.render(str(cs.Text[self.type][self.game.textindex].strip("[],")), True, cs.white)
        pygame.display.update()

    def displaymytext(self):
        self.game.dis.blit(cs.text, cs.textRect)
        self.game.dis.blit(cs.textSecondLine, cs.textSecondLineRect)
        pygame.display.update()
    #def displaymytextbetter(self, index):
   #     pass

    def displaymytextbetter(self):
        self.game.dis.blit(self.textimage, self.textrect)
        self.game.dis.blit(self.text, self.textrect)
        self.game.dis.blit(cs.pressetoclose, cs.etocloserect)
        if len(cs.Text[self.type]) - 1 > self.game.textindex:
            self.game.dis.blit(cs.entertocontinue, cs.textRect3)
        self.text = self.font.render(str(cs.Text[self.type][self.game.textindex].strip("[],")), True, cs.white)
        pygame.display.update()

    def displaymytext(self):
        self.game.dis.blit(cs.text, cs.textRect)
        self.game.dis.blit(cs.textSecondLine, cs.textSecondLineRect)
        pygame.display.update()
    #def displaymytext(self):
    #    self.game.dis.blit(cs.text, cs.textRect)
   #     self.game.dis.blit(cs.textSecondLine, cs.textSecondLineRect)
   #     pygame.display.update()

    '''def displaytextani(self, string_list, txtcolour, font):
        # if not self.textrunning:
        if self.string >= len(string_list):
            return

        self.camera.freeze = True
        for sprite in self.all_sprites:
            sprite.freeze = True
        
        # playerx = self.player.position.x
        # playery = self.player.position.y
        
        pygame.draw.rect(self.map_img, cs.black, pygame.Rect(self.x - 250, self.y + 150, 500, 100))
        
        current_string = string_list[self.string][:self.letter]
        text_surface = font.render(current_string, True, txtcolour)
        text_rect = text_surface.get_rect(topleft=(self.x - 200, self.y + 180))
        self.map_img.blit(text_surface, text_rect)

        if self.letter > len(string_list[self.string]) - 1:
            self.string += 1
            self.letter = 0
            if self.string >= len(string_list):
                self.textrunning = False
                return
            
        self.letter += 1
        pygame.display.update()
        pygame.display.flip()
        self.clock.tick(15)
'''

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
        self.text = self.font.render(cs.LockText[text_id], True, cs.white)
        self.textimage = pygame.Surface((cs.diswidth, 0.2 * cs.disheight),
                                        pygame.SRCALPHA)
        self.textimage.fill(cs.translucent_black)
        self.textrect = self.textimage.get_rect()
        self.textrect.x = 0
        self.textrect.y = cs.diswidth * 0.8

    def displaymytextbetter(self):
        self.game.dis.blit(self.textimage, self.textrect)
        self.game.dis.blit(self.text, self.textrect)
        self.game.dis.blit(cs.text2, cs.textRect2)
        if len(cs.Text[self.type]) - 1 > self.game.textindex:
            self.game.dis.blit(cs.text3, cs.textRect3)
        self.text = self.font.render(str(cs.Text[self.type][self.game.textindex].strip("[],")), True, cs.white)
        pygame.display.update()

    def displaymytext(self):
        self.game.dis.blit(cs.text, cs.textRect)
        self.game.dis.blit(cs.textSecondLine, cs.textSecondLineRect)
        pygame.display.update()
    def unlocked(self, key, changetarget):
        self.image = changetarget.image
        pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        pygame.sprite.Sprite.remove(self, self.game.obstruction)
        self.game.player.status = "free"
        self.game.interactivibee = False
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
        self.text = self.font.render(cs.LockText[text_id], True, cs.white)
        self.textimage = pygame.Surface((cs.diswidth, 0.2 * cs.disheight),
                                        pygame.SRCALPHA)
        self.textimage.fill(cs.translucent_black)
        self.textrect = self.textimage.get_rect()
        self.textrect.x = 0
        self.textrect.y = cs.diswidth * 0.8


class Arrows(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height, type):
        self.game = game
        self.type = type
        self.inside = self.game.arrows
        pygame.sprite.Sprite.__init__(self, self.inside)
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y
        self.hit_rect = self.rect
        #self.image = pygame.image.load('graphics/arrowtopright.png').convert_alpha()
        #i hope you're not checking for efficiency here because i am REALLY tweakin out now
        match self.type:
            case 1:
                self.image = pygame.image.load('graphics/frog.png').convert_alpha()
            case 2:
                self.image = pygame.image.load('graphics/bird.png').convert_alpha()
            case 3:
                self.image = pygame.image.load('graphics/bunny.png').convert_alpha()
            case 4:
                self.image = pygame.image.load('graphics/squirrel.png').convert_alpha()
            case 5:
                self.image = pygame.image.load('graphics/arrowtopright.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.rect.width,
                                                         self.rect.height))
class TextAni(object):
    def __init__(self):
        self.string_list = None
        self.x = 0
        self.y = 0
        self.string = 0
        self.letter = 0
        self.textrunning = False
        self.textplaying = False
        self.cleanup_func = None

    def playsound(self, sound, vol):
        mixer.music.load(sound)
        mixer.music.set_volume(vol)
        mixer.music.play()
        
    def start_display(self, string_list, x, y, font, colour, cleanup_func=None):
        self.string_list = [f"{str} " + ' ' * 10000 for str in string_list]
        self.string = 0
        self.letter = 0
        self.x = x
        self.y = y
        self.font = font
        self.colour = colour
        self.cleanup_func = cleanup_func

        self.textrunning = True
        self.textplaying = True

    def stop_display(self):
        self.textrunning = False
        self.textplaying = False

    def is_displaying(self):
        return self.textrunning

    def skip_line(self):
        if self.string < len(self.string_list):
            self.letter = len(self.string_list[self.string]) - 1

    def update(self, map_img, vol):
        if not self.textplaying:
            return
        if self.string >= len(self.string_list):
            return

        # self.camera.freeze = True
        #for sprite in self.all_sprites:
            #sprite.freeze = True
        if self.letter > len(self.string_list[self.string]) - 1:
            #pygame.time.delay(1000)
            self.string += 1
            self.letter = 0
            if self.string >= len(self.string_list):
                self.textrunning = False
                return False
        if self.letter == 0:
            self.playsound('sounds/typing.mp3', vol)
        if self.letter == 20:
            mixer.music.stop()
        pygame.draw.rect(map_img, cs.black, pygame.Rect(self.x, self.y, 500, 100))

        current_string = self.string_list[self.string][:self.letter]
        text_surface = self.font.render(current_string, True, self.colour)
        text_rect = text_surface.get_rect(topleft=(self.x + 7, self.y + 30))
        map_img.blit(text_surface, text_rect)

        self.letter += 1
        pygame.display.update()
        pygame.display.flip()
        pygame.time.Clock().tick(30)
        return True

    def cleanup(self):
        mixer.music.stop()
        if self.cleanup_func is None:
            return
        self.cleanup_func()
        self.cleanup_func = None
