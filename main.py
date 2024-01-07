# start screen gyap
import sys
from os import path
from objs import *
import pygame
from pygame import QUIT
from cons import *
import buttons as b
from tilemap import *


class Game:
    def __init__(self):
        pygame.init()
        self.dis = pygame.display.set_mode((cs.diswidth, cs.disheight))
        pygame.display.set_caption('get me out of heeaarraahh')
        self.clock = pygame.time.Clock()
        # pygame.key.set_repeat(500, 100)
        self.load_data()
        # self.displaytext = False

    def load_data(self):
        folder = path.dirname(__file__)
        img_folder = path.join(folder, 'graphics')
        map_folder = path.join(folder, 'tilemaps')
        self.map = TiledMap(path.join(map_folder, 'bettertestmap.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pygame.image.load(path.join(img_folder, 'sunnysprite.png')).convert_alpha()
        self.player_imgfrontleft = pygame.image.load(path.join(img_folder, 'sunnyfrontleft.png')).convert_alpha()
        self.player_imgfrontright = pygame.image.load(path.join(img_folder, 'sunnyfrontright.png')).convert_alpha()
        self.player_imgleft = pygame.image.load(path.join(img_folder, 'sunnyleft.png')).convert_alpha()
        self.player_imgleftleft = pygame.image.load(path.join(img_folder, 'sunnyleftleft.png')).convert_alpha()
        self.player_imgleftright = pygame.image.load(path.join(img_folder, 'sunnyleftright.png')).convert_alpha()
        self.player_imgright = pygame.image.load(path.join(img_folder, 'sunnyright.png')).convert_alpha()
        self.player_imgrightleft = pygame.image.load(path.join(img_folder, 'sunnyrightleft.png')).convert_alpha()
        self.player_imgrightright = pygame.image.load(path.join(img_folder, 'sunnyrightright.png')).convert_alpha()
        self.player_imgback = pygame.image.load(path.join(img_folder, 'sunnyback.png')).convert_alpha()
        self.player_imgbackleft = pygame.image.load(path.join(img_folder, 'sunnybackleft.png')).convert_alpha()
        self.player_imgbackright = pygame.image.load(path.join(img_folder, 'sunnybackright.png')).convert_alpha()


    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.obstruction = pygame.sprite.Group()
        self.interactable = pygame.sprite.Group()
        self.interactablebox = pygame.sprite.Group()
        self.text = pygame.sprite.Group()
        self.playergroup = pygame.sprite.GroupSingle()
        '''for i, row in enumerate(self.map.data):
      for j, value in enumerate(row):
        if value == '1':
          Wall(self, j, i)
        elif value == 'p':
          self.player = Player(self, j, i)
        elif value == '2':
          Interactable(self, j, i)
          InteractableBox(self, j, i)'''
        for layerobject in self.map.tmxdata.objects:
            if layerobject.name == 'player':
                self.player = Player(self, layerobject.x, layerobject.y)
            elif layerobject.name == 'house':
                Obstacle(self, layerobject.x, layerobject.y,
                         layerobject.width, layerobject.height)
            elif layerobject.name == 'interactablehitbox':
                InteractableBox(self, layerobject.type, layerobject.x, layerobject.y, layerobject.width, layerobject.height)

            elif layerobject.name == 'textdisplay':
                TextDisplay(self, layerobject.type, int(layerobject.type.strip("'")))

        self.draw_debug = False
        self.interactivity = False
        self.camera = View(self.map.width, self.map.height)

    def run(self):
        self.game_over = False
        while not self.game_over:
            self.dt = self.clock.tick(60) / 1000
            self.events()
            direction = self.rupdate()
            self.draw(direction)
        pygame.quit()

    def quit(self):
        sys.exit()

    def rupdate(self):
        self.all_sprites.update()
        direction = self.player.direction
        #direction = []
        #for sprite in self.all_sprites:
            #direction.append(sprite)
        self.camera.update(self.player)
        return direction

    def grid(self):
        for y in range(0, disheight, tilesize):
            pygame.draw.line(self.dis, (black), (0, y), (diswidth, y))
        for x in range(0, diswidth, tilesize):
            pygame.draw.line(self.dis, (black), (x, 0), (x, disheight))

    def drawbg(self, colour):
        self.dis.fill(colour)

    '''def createtilemap(self):
    for i, row in enumerate(tilemap):
      for j, value in enumerate(row):
        if value == '1':
          Wall(self, j, i)
        elif value == 'p':
          self.player = Player(self, j, i)'''

    def movementani(self, direction):
        for sprite in self.all_sprites:
            if direction == None:
                self.dis.blit(sprite.image, self.camera.implement(sprite))
                break
            anigroup = sprite.getanigroup()
            self.dis.blit(anigroup[sprite.currentsprite], self.camera.implement(sprite)) #make a method for this lol
            sprite.currentsprite += 1
            pygame.time.wait(100)
            if sprite.currentsprite > len(anigroup) - 1:
                sprite.currentsprite = 0
            
            if self.draw_debug:
                pygame.draw.rect(self.dis, cs.blue,
                                 self.camera.implement_rect(sprite.hit_rect), 1)

    def draw(self, direction):
        # self.drawbg(white)
        # self.grid()
        self.dis.blit(self.map_img, self.camera.implement_rect(self.map_rect))
        # self.all_sprites.draw(self.dis) changed w camera

        self.movementani(direction)

        if self.draw_debug:
            for x in self.obstruction:
                pygame.draw.rect(self.dis, cs.blue,
                                 self.camera.implement_rect(x.hit_rect), 1)

        if pygame.sprite.spritecollideany(self.player, self.interactablebox):
            for y in self.interactablebox:
                if pygame.sprite.collide_rect(self.player, y):
                    for interactable in self.text:
                        if interactable.type == y.type:
                            self.displaymytext(interactable)

        '''for sprit in self.all_sprites:
     self.dis.blit(sprit.image, self.camera.apply(sprit))'''
        # for x in list:
        # dis.blit()#find an efficient way to compare x as and integer to object position in a list
        pygame.display.flip()

    def displaymytext(self, target):
        self.dis.blit(cs.text, cs.textRect)
        if self.interactivity:
            self.dis.blit(target.image, target.rect)
            self.dis.blit(target.text, target.rect)
            self.player.interacting = True
        pygame.display.update()



    def events(self):
        # while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                # play_pos = (self.player.x, self.player.y, self.displaytext)
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_j:
                    self.draw_debug = not self.draw_debug
                if event.key == pygame.K_e:
                    self.interactivity = not self.interactivity
                    self.player.interacting = not self.player.interacting
                '''if event.key == pygame.K_d:
              self.player.move(xchange = block_speed)
            if event.key == pygame.K_w:
              self.player.move(ychange = -block_speed)
            if event.key == pygame.K_s:
              self.player.move(ychange = block_speed)'''

            # elif event.type == pygame.KEYUP:
            #  self.player.move()

    def textani(self, tuple, string_list, font, txtcolour):
        string = 0
        letter = 0
        running = True
        x, y = tuple
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        string = (string + 1) % len(string_list)
                        letter = 0

            self.dis.fill(black)
            current_string = string_list[string][:letter + 1]
            text_surface = font.render(current_string, True, txtcolour)
            text_rect = text_surface.get_rect(topleft=(x, y))
            self.dis.blit(text_surface, text_rect)
            letter += 1

            pygame.display.flip()
            self.clock.tick(30)

    '''def text(self, string, font, colour, x, y):
        text = font.render(string, True, colour)
        textrect = text.get_rect(topleft=(x, y))
        self.dis.blit(text, textrect)'''

    def newgame(self):
        while True:
            pygame.display.set_caption("New Game")
            self.dis.fill(black)
            self.text(newgametext, font, white, 300, 250)
            pygame.display.flip()

    def contgame(self):
        while True:
            pygame.display.set_caption("Continue Game")
            self.dis.fill(black)
            self.text(conttext, font, white, 300, 250)
            pygame.display.flip()

    def settings(self):
        while True:
            pygame.display.set_caption("Settings")
            self.dis.fill(black)
            self.text(settingstext, font, white, 300, 250)
            pygame.display.flip()

    def mainmenu(self):
        # while True:
        mousepos = pygame.mouse.get_pos()
        button1 = b.Button(x1, y1, colour1)
        button1.draw(self.dis)
        button2 = b.Button(x2, y2, colour2)
        button2.draw(self.dis)
        button3 = b.Button(x3, y3, colour3)
        button3.draw(self.dis)

        self.text(string1, font, black, x1 + 8, y1 + 12)
        self.text(string2, font, black, x2 + 8, y2 + 12)
        self.text(string3, font, black, x3 + 8, y3 + 12)

        if button1.hover(mousepos):
            self.text(string1, font, grey, x1 + 8, y1 + 12)
        elif button2.hover(mousepos):
            self.text(string2, font, grey, x2 + 8, y2 + 12)
        elif button3.hover(mousepos):
            self.text(string3, font, grey, x3 + 8, y3 + 12)

        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1.hover(mousepos):
                    self.newgame()
                elif button2.hover(mousepos):
                    self.contgame()
                elif button3.hover(mousepos):
                    self.settings()


def main():
    gamestart = Game()
    while True:
        gamestart.new()
        gamestart.run()

        pygame.display.update()
        gamestart.clock.tick(60)


main()
