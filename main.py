# start screen gyap
import sys
import math
from os import path
from objs import *
import pygame
from pygame import QUIT, Rect
from cons import *
import buttons as b
from tilemap import *
from combat import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.dis = pygame.display.set_mode((diswidth, disheight))
        pygame.display.set_caption('get me out of heeaarraahh')
        self.clock = pygame.time.Clock()
        # pygame.key.set_repeat(500, 100)
        self.mapindex = 0
        self.load_data()
        # self.displaytext = False
        self.combatstate = False
        self.cutscenestate = False

    def load_data(self):
        folder = path.dirname(__file__)
        img_folder = path.join(folder, 'graphics')
        map_folder = path.join(folder, 'tilemaps')
        self.map = TiledMap(path.join(map_folder, cs.mapchange[self.mapindex]))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pygame.image.load(
            path.join(img_folder, 'sunnysprite.png')).convert_alpha()
        self.player_imgfrontleft = pygame.image.load(
            path.join(img_folder, 'sunnyfrontleft.png')).convert_alpha()
        self.player_imgfrontright = pygame.image.load(
            path.join(img_folder, 'sunnyfrontright.png')).convert_alpha()
        self.player_imgleft = pygame.image.load(
            path.join(img_folder, 'sunnyleft.png')).convert_alpha()
        self.player_imgleftleft = pygame.image.load(
            path.join(img_folder, 'sunnyleftleft.png')).convert_alpha()
        self.player_imgleftright = pygame.image.load(
            path.join(img_folder, 'sunnyleftright.png')).convert_alpha()
        self.player_imgright = pygame.image.load(
            path.join(img_folder, 'sunnyright.png')).convert_alpha()
        self.player_imgrightleft = pygame.image.load(
            path.join(img_folder, 'sunnyrightleft.png')).convert_alpha()
        self.player_imgrightright = pygame.image.load(
            path.join(img_folder, 'sunnyrightright.png')).convert_alpha()
        self.player_imgback = pygame.image.load(
            path.join(img_folder, 'sunnyback.png')).convert_alpha()
        self.player_imgbackleft = pygame.image.load(
            path.join(img_folder, 'sunnybackleft.png')).convert_alpha()
        self.player_imgbackright = pygame.image.load(
            path.join(img_folder, 'sunnybackright.png')).convert_alpha()

        self.enemyimg = pygame.image.load('graphics/cookiemonster.png')
        self.enemyimg = pygame.transform.scale(self.enemyimg, (100, 100))

    def new(self):
        self.all_sprites = pygame.sprite.Group()  # all sprites
        self.obstruction = pygame.sprite.Group()  # blocks movement in collicase
        self.interactable = pygame.sprite.Group()  # obsolete class hate this
        self.interactablebox = pygame.sprite.Group()  # prompts interaction without actually colliding with objects you can't go through
        self.text = pygame.sprite.Group()  # group for sprites that need to display text
        self.playergroup = pygame.sprite.GroupSingle()  # single group for player
        self.teleport = pygame.sprite.Group()  # moves player from map to map
        self.locks = pygame.sprite.Group()  # destination corresponding to the objects the player picks up
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
                InteractableBox(self, layerobject.type, layerobject.x,
                                layerobject.y, layerobject.width,
                                layerobject.height)
            elif layerobject.name == 'textdisplay':
                TextDisplay(self, layerobject.x,
                            layerobject.y, layerobject.width,
                            layerobject.height, layerobject.type,
                            int(layerobject.type.strip("'")))
            elif layerobject.name == 'teleport':
                Teleport(self, layerobject.type,
                         layerobject.x, layerobject.y, layerobject.width, layerobject.height)
            elif layerobject.name == 'lock':
                Lock(self,
                     layerobject.x, layerobject.y, layerobject.width,
                     layerobject.height, int(layerobject.type.strip("'")),
                     int(layerobject.type.strip("'")))
            elif layerobject.name == 'interactablehitlox':
                InteractableLox(self, layerobject.type, layerobject.x,
                                layerobject.y, layerobject.width,
                                layerobject.height)


        self.draw_debug = False
        self.interactivity = False
        self.interactivibee = False
        self.camera = View(self.map.width, self.map.height)

        self.team = Team()

        self.enemy = Computer(targname, targhp, targpow, True)

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
        # direction = []
        # for sprite in self.all_sprites:
        # direction.append(sprite)
        self.camera.update(self.player)
        return direction

    '''def grid(self):
        for y in range(0, disheight, tilesize):
            pygame.draw.line(self.dis, cs.black, (0, y), (diswidth, y))
        for x in range(0, diswidth, tilesize):
            pygame.draw.line(self.dis, (black), (x, 0), (x, disheight))'''

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
            self.dis.blit(anigroup[sprite.currentsprite], self.camera.implement(
                sprite))  
            sprite.currentsprite += 1
            pygame.time.wait(100)
            if sprite.currentsprite > len(anigroup) - 1:
                sprite.currentsprite = 0

            if self.draw_debug:
                pygame.draw.rect(self.dis, cs.blue,
                                 self.camera.implement_rect(sprite.hit_rect), 1)
                                 
    def blitdirection(self, sprites): #sprites is dict key = char, value = direction
        for sprite in sprites:
            if sprites[sprite] == "left":
                self.map_img.blit(sprite.imageleft, sprite.rectleft)
            elif sprites[sprite] == "right":
                self.map_img.blit(sprite.imageright, sprite.rectright)
            elif sprites[sprite] == "front":
                self.map_img.blit(sprite.imagefront, sprite.rectfront)
            elif sprites[sprite] == "back":
                self.map_img.blit(sprite.imageback, sprite.rectback)

    def healthbar(self, enemy):
        return None

    #call like self.combat(enemyimg, self.enemy) from new
    def combat(self, enemyimg, enemy):
        self.combatstate = True
        self.camera.freeze = True
        for sprite in self.all_sprites:
            sprite.freeze = True
        
        self.combatbg = pygame.image.load('graphics/combatbg.jpg').convert()
        self.combatbg = pygame.transform.scale(self.combatbg, (diswidth, disheight))
        self.map_img.blit(self.combatbg, (0, 0))
        self.map_img.blit(enemyimg, (250, 250))
        
        #oh bluther i gotta use buttons this is so freaked 
        self.escapebutton = b.Button(100, 100, black) #first screen; two choices are escape or attack
        self.attackbutton = b.Button(350, 100, white)
        self.escapebutton.draw(self.map_img)
        self.attackbutton.draw(self.map_img)
        self.drawtext("Escape...", font, white, 120, 100)
        self.drawtext("Attack!", font, black, 370, 100)
        
        #attacks happen in pairs, choose two characters to create a combo attack that deals damage based on power + trust
        self.c1attack = b.Button(100, 80, green) 
        self.c2attack = b.Button(350, 80, orange)
        self.c3attack = b.Button(100, 180, blue)
        self.c4attack = b.Button(350, 180, red)

        self.buttons = []
        self.buttons.append(self.escapebutton)
        self.buttons.append(self.attackbutton)
        self.buttons.append(self.c1attack)
        self.buttons.append(self.c2attack)
        self.buttons.append(self.c3attack)
        self.buttons.append(self.c4attack)

        gameover = False
        '''for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
            if event.type == pygame.MOUSEMOTION:
                mousepos = pygame.mouse.get_pos()
                print (mousepos)
                if self.escapebutton.hover(mousepos):
                    self.drawtext("Escape...", font, grey, 120, 100)
                elif self.attackbutton.hover(mousepos):
                    self.drawtext("Attack!", font, red, 370, 100)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.escapebutton.hover(mousepos):
                    if enemy.escape: #escapability depends on if enemy is part of the main quest
                        self.dis.blit(self.map_img, self.map_rect)
                    else:
                        self.drawtext("Unable to escape!", font, red, 200, 100)
                        pygame.time.delay(500)
                        self.drawtext("You lost your advantage! %s attacks first!" %(enemy.name))
                        damage = enemy.attack()

                        totalhp = 0
                        for user in self.users: #set hp for user
                            totalhp += user.hp

                            totalhp -= damage
                            print ("You lost %i HP!" (damage)) #lazy

                            while not gameover: #this wont work lol
                                self.users.attack()
                                enemy.update()
                                enemy.attack()
                                self.users.update()
                            
                elif self.attackbutton.hover(mousepos):
                    self.map_img.blit(self.combatbg)
                    self.c1attack.draw(self.dis)
                    self.drawtext("CHARACTER1", font, red, 120, 180)
                    self.c2attack.draw(self.dis)
                    self.drawtext("CHARACTER2", font, blue, 370, 180)
                    self.c3attack.draw(self.dis)
                    self.drawtext("CHARACTER3", font, orange, 120, 80)
                    self.c4attack.draw(self.dis)
                    self.drawtext("CHARACTER4", font, green, 370, 80)

                    if self.c1attack.hover(mousepos):
                        self.drawtext("CHARACTER1", fontbold, red, 120, 350)
                    elif self.c2attack.hover(mousepos):
                        self.drawtext("CHARACTER2", fontbold, blue, 370, 350)
                    elif self.c3attack.hover(mousepos):
                        self.drawtext("CHARACTER3", fontbold, orange, 120, 450)
                    elif self.c4attack.hover(mousepos):
                        self.drawtext("CHARACTER4", fontbold, green, 370, 450)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.c1attack.hover(mousepos):
                            sys.quit()
                            return 1
                        elif self.c2attack.hover(mousepos):
                            return 2
                        elif self.c3attack.hover(mousepos):
                            return 3
                        elif self.c4attack.hover(mousepos):
                            return 4'''

    def combat2(self, enemyimg, enemy):
        firstattack = self.combat(enemyimg, enemy)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            
    def cutsceneend(self):
        x = self.player.position.x - 250
        y = self.player.position.y - 50
        self.textani((x, y), stringlist, font, white)
        pygame.display.update()
        self.player.cutscene = False
        self.player.cutsceneend = False

    def cutscene(self): 
        self.player.cutscene = True
        self.player.directions = ['left', 'left', 'left', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd']


        #for guy in turns:
            #how to get direction in here lol what the heck!
            #also movementani has to take in the sprite thats moving
            #dict gives which sprite of four move as key and how much as value
            #call movementani as it goes
            #self.movementani()
            
    def draw(self, direction):
        self.dis.blit(self.map_img, self.camera.implement_rect(self.map_rect))
        if not self.combatstate:

            for x in self.text:
                if x.type == self.player.keytype:
                    self.player.holding(x)

            for x in self.text:
                self.dis.blit(x.image, self.camera.implement_rect(x.rect))

            for x in self.locks:
                self.dis.blit(x.image, self.camera.implement_rect(x.rect))
            #.all_sprites.draw(self.dis)

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
                                if self.interactivity:
                                    self.displaymytextbetter(interactable)
                                elif self.interactivibee:
                                    self.player.keytype = interactable.type
                                    pygame.sprite.Sprite.remove(interactable,
                                                                self.obstruction)

                                else:
                                    self.displaymytext(interactable)

            if pygame.sprite.spritecollideany(self.player, self.teleport):
                for x in self.teleport:
                    if pygame.sprite.collide_rect(self.player, x):
                        self.mapindex = int(x.type.strip("'"))
                    self.load_data()
                    self.new()
                '''
            for sprit in self.all_sprites:
                self.dis.blit(sprit.image, self.camera.apply(sprit))'''
            # for x in list:
            # dis.blit()#find an efficient way to compare x as and integer to object position in a list
        pygame.display.flip()

    def displaymytextbetter(self, target):
        self.dis.blit(target.textimage, target.textrect)
        self.dis.blit(target.text, target.textrect)
        self.dis.blit(cs.text2, cs.textRect2)

        pygame.display.update()

    def displaymytext(self, target):
        self.dis.blit(cs.text, cs.textRect)
        self.dis.blit(cs.textSecondLine, cs.textSecondLineRect)
        pygame.display.update()

    def combatevent(self, event):
        if event.type == QUIT:
            self.quit()
        if event.type == pygame.MOUSEMOTION:
            mousepos = pygame.mouse.get_pos()
            print (mousepos)
            if self.escapebutton.hover(mousepos):
                self.drawtext("Escape...", font, grey, 120, 100)
            elif self.attackbutton.hover(mousepos):
                self.drawtext("Attack!", font, red, 370, 100)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousepos = pygame.mouse.get_pos()
            if self.escapebutton.hover(mousepos):
                if self.enemy.escape: #escapability depends on if enemy is part of the main quest
                    print ("asdasd")
                    self.combatstate = False
                    self.camera.freeze = False
                    for sprite in self.all_sprites:
                        sprite.freeze = False #releasing the little man
                    self.drawtext("You ran away...", fontbold, red, 250, 400)
                    self.combatbg.blit(self.map_img, self.camera.implement_rect(self.map_rect))
                    direction = self.rupdate()
                    self.draw(direction)
                    #self.escapebutton.delete()
                else:
                    self.dis.blit(self.combatbg, (0, 0))
                    self.drawtext("Unable to escape!", font, red, 200, 400)
                    pygame.time.delay(1000)
                    
                    self.dis.blit(self.combatbg, (0, 0))
                    self.drawtext("You lost your advantage! %s attacks first!" %(self.enemy.name), fontbold, red, 200, 400)
                    damage = self.enemy.attack()

                    totalhp = 0
                    '''for user in self.users: #set hp for user
                        totalhp += user.hp

                        totalhp -= damage
                        print ("You lost %i HP!" (damage)) #lazy'''
                        
            elif self.attackbutton.hover(mousepos):
                print ("asd")
                self.combatbg.blit(self.combatbg, (0, 0))
                self.c1attack.draw(self.combatbg)
                self.drawtext("CHARACTER1", font, red, 120, 80)
                self.c2attack.draw(self.combatbg)
                self.drawtext("CHARACTER2", font, blue, 370, 80)
                self.c3attack.draw(self.dis)
                self.drawtext("CHARACTER3", font, orange, 120, 180)
                self.c4attack.draw(self.dis)
                self.drawtext("CHARACTER4", font, green, 370, 180)

                if self.c1attack.hover(mousepos):
                    self.drawtext("CHARACTER1", fontbold, blue, 120, 80)
                elif self.c2attack.hover(mousepos):
                    self.drawtext("CHARACTER2", fontbold, red, 370, 80)
                elif self.c3attack.hover(mousepos):
                    self.drawtext("CHARACTER3", fontbold, green, 120, 180)
                elif self.c4attack.hover(mousepos):
                    self.drawtext("CHARACTER4", fontbold, orange, 370, 180)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.c1attack.hover(mousepos):
                        return 1
                    elif self.c2attack.hover(mousepos):
                        return 2
                    elif self.c3attack.hover(mousepos):
                        return 3
                    elif self.c4attack.hover(mousepos):
                        return 4
    def events(self):
        # while True:
        if not self.player.cutscene:
            if not self.player.cutsceneend:
                if abs(self.player.position.x - 500) < 50 and abs(self.player.position.y - 500) < 50:
                    self.cutscene()
        else:
            if self.player.cutsceneend:
                print ("Asd")
                self.cutsceneend()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if self.combatstate:
                self.combatevent(event)
                continue

            if event.type == pygame.KEYDOWN:
                # play_pos = (self.player.x, self.player.y, self.displaytext)
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_SPACE:
                    self.combat(self.enemyimg, self.enemy)
                if event.key == pygame.K_j:
                    self.draw_debug = not self.draw_debug
                if pygame.sprite.spritecollideany(self.player,
                                                  self.interactablebox):
                    if event.key == pygame.K_e:
                        self.interactivity = not self.interactivity
                        self.player.interacting = not self.player.interacting
                if pygame.sprite.spritecollideany(self.player,
                                                  self.interactablebox):
                    if event.key == pygame.K_p:
                        self.interactivibee = not self.interactivibee
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

            pygame.draw.rect(self.map_img, black, pygame.Rect(x, y, 500, 100))
            current_string = string_list[string][:letter + 1]
            text_surface = font.render(current_string, True, txtcolour)
            text_rect = text_surface.get_rect(topleft=(x, y))
            self.map_img.blit(text_surface, text_rect)
            letter += 1

            pygame.display.update()
            pygame.display.flip()
            self.clock.tick(30)

    def drawtext(self, string, font, colour, x, y):
        text = font.render(string, True, colour)
        textrect = text.get_rect(topleft=(x, y))
        self.map_img.blit(text, textrect)

    def texttwo(self, string, font, colour, x, y): #probably easier to use for combat
        text = font.render(string, True, colour)
        textrect = text.get_rect(center=(x, y))
        self.dis.blit(text, textrect)

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

        text(string1, font, black, x1 + 8, y1 + 12)
        text(string2, font, black, x2 + 8, y2 + 12)
        text(string3, font, black, x3 + 8, y3 + 12)

        if button1.hover(mousepos):
            text(string1, font, grey, x1 + 8, y1 + 12)
        elif button2.hover(mousepos):
            text(string2, font, grey, x2 + 8, y2 + 12)
        elif button3.hover(mousepos):
            text(string3, font, grey, x3 + 8, y3 + 12)

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
        #gamestart.mainmenu() i tried making this code run but idk what the texts are lol
        gamestart.new()
        gamestart.run()

        pygame.display.update()
        gamestart.clock.tick(60)


main()
