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
        self.textindex = 0
        self.cutscenestate = False
        self.textplaying = False
        self.attackingstate = False
        self.charstate = False
        self.selected = [False, False, False, False]
        self.chosen = []
        self.enemyattacking = False

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
        self.painterimg = pygame.image.load('graphics/personality.png')
        self.painterimg = pygame.transform.scale(self.painterimg, (100, 100))


    def striptype(self, stripped):
        return int(stripped.strip("'"))
    def new(self):
        self.all_sprites = pygame.sprite.Group()  # all sprites
        self.obstruction = pygame.sprite.Group()  # blocks movement in collicase
        self.interactable = pygame.sprite.Group()  # obsolete class hate this
        self.interactablebox = pygame.sprite.Group()  # prompts interaction without actually colliding with objects you can't go through
        self.text = pygame.sprite.Group()  # group for sprites that need to display text
        self.playergroup = pygame.sprite.GroupSingle()  # single group for player
        self.teleport = pygame.sprite.Group()  # moves player from map to map
        self.locks = pygame.sprite.Group()  # destination corresponding to the objects the player picks up
        self.interactablelox = pygame.sprite.Group()
        self.lockchange = pygame.sprite.Group()
        '''for i, row in enumerate(self.map.data):
      for j, value in enumerate(row):
        if value == '1':
          Wall(self, j, i)
        elif value == 'p':
          self.player = Player(self, j, i)
        elif value == '2':
          Interactable(self, j, i) old tilemap stuff
          InteractableBox(self, j, i)'''
        for layerobject in self.map.tmxdata.objects:

            if layerobject.name == 'player':
                self.player = Player(self, layerobject.x, layerobject.y) #playerspawn

            elif layerobject.name == 'house':
                Obstacle(self, layerobject.x, layerobject.y,
                         layerobject.width, layerobject.height) #obstructionspawn, use this for walls and stuff

            elif layerobject.name == 'interactablehitbox':
                InteractableBox(self, self.striptype(layerobject.type), layerobject.x, #keyhitbox
                                layerobject.y, layerobject.width,
                                layerobject.height)

            elif layerobject.name == 'textdisplay':
                TextDisplay(self, layerobject.x,
                            layerobject.y, layerobject.width,
                            layerobject.height, self.striptype(layerobject.type)) #key spawn

            elif layerobject.name == 'teleport':
                Teleport(self, layerobject.type,
                         layerobject.x, layerobject.y, layerobject.width,
                         layerobject.height) #teleport spawn

            elif layerobject.name == 'lock':
                Lock(self,
                     layerobject.x, layerobject.y, layerobject.width, #spawn a lock object and a lockchange object in the same spot
                     layerobject.height, self.striptype(layerobject.type),
                     self.striptype(layerobject.type))
                Lockchange(self,
                           layerobject.x, layerobject.y, layerobject.width,
                           layerobject.height, self.striptype(layerobject.type),
                           self.striptype(layerobject.type))

            elif layerobject.name == 'interactablehitlox':
                InteractableLox(self, self.striptype(layerobject.type), layerobject.x, #lock hit box
                                layerobject.y, layerobject.width,
                                layerobject.height)

        self.draw_debug = False
        self.interactivity = False #text interactivity
        self.interactivibee = False #pickup interactivity
        self.camera = View(self.map.width, self.map.height)

        self.team = Team()

        self.enemy = Computer(targname, targhp, targpow, False)

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


    def cutsceneend(self, event):
        x = self.player.position.x - 250
        y = self.player.position.y - 50
        self.textani(event, (x, y), stringlist, font, white)
        pygame.display.update()
        self.player.cutscene = False
        self.player.cutsceneend = False

    def cutscene(self): 
        self.player.cutscene = True
        self.player.directions = ['left', 'left', 'left', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd']
            
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
            # .all_sprites.draw(self.dis)

            self.movementani(direction)

            if self.draw_debug:
                for x in self.obstruction:
                    pygame.draw.rect(self.dis, cs.blue,
                                     self.camera.implement_rect(x.hit_rect), 1)

            self.checkobjinter()
            self.checklockinter()

            if self.player.status == "carrying":
                self.inneractivibee()

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

    def inneractivibee(self):
        a = pygame.sprite.spritecollideany(self.player, self.interactablelox)
        if a is not None: #checking specific box
            if self.player.keytype == a.type: #if the key the player is carrying matches hitbox type
                for lock in self.locks: #lock object check
                    if lock.type == a.type: #if lock object type is equal to hitbox object type
                        for lc in self.lockchange: #if lockchange type is equal to yada yada
                            if lc.type == lock.type:
                                for textdis in self.text:
                                    if textdis.type == lc.type:
                                        lock.unlocked(textdis, lc, self.player) #WHY IS THIS NOT WORKING

    def checklockinter(self):
        c = pygame.sprite.spritecollideany(self.player, self.interactablelox)
        if self.interactivibee:
            if c is not None:
                for aye in self.locks:
                    if aye.type == c.type:
                        self.player.keytype = aye.type
                        pygame.sprite.Sprite.remove(aye,
                                                    self.obstruction)

    def checkobjinter(self):
        b = pygame.sprite.spritecollideany(self.player, self.interactablebox)
        if b is not None:
            for interactable in self.text:
                if interactable.type == b.type:
                    if self.interactivity:
                        interactable.displaymytextbetter(self.textindex)
                    elif self.interactivibee:
                        self.player.keytype = interactable.type
                        pygame.sprite.Sprite.remove(interactable,
                                                    self.obstruction)
                    else:
                        self.displaymytext()

    def displaymytext(self):
        self.dis.blit(cs.text, cs.textRect)
        self.dis.blit(cs.textSecondLine, cs.textSecondLineRect)
        pygame.display.update()

    def combat(self):
        self.combatstate = True
        self.camera.freeze = True
        for sprite in self.all_sprites:
            sprite.freeze = True
        
        x = self.player.position.x
        y = self.player.position.y
        self.combatbg = pygame.image.load('graphics/combatbg.jpg').convert()
        self.combatbg = pygame.transform.scale(self.combatbg, (diswidth, disheight))
        self.map_img.blit(self.combatbg, (x - 250, y - 240))
        self.map_img.blit(self.enemyimg, (x - 50, y))
        self.map_img.blit(self.painterimg, (x + 100, y + 100))
        
        escapex = x - 200
        escapey = y - 140
        attackx = x + 50
        attacky = y - 140
        self.escapebutton = b.Button(escapex, escapey, black) #first screen; two choices are escape or attack
        self.attackbutton = b.Button(attackx, attacky, white)
        self.escapebutton.draw(self.map_img)
        self.attackbutton.draw(self.map_img)
        self.drawtext("Escape...", font, white, x - 190, y - 120)
        self.drawtext("Attack!", font, black, x + 60, y - 120)
        
        #attacks happen in pairs, choose two characters to create a combo attack that deals damage based on power + trust
        self.c1attack = b.Button(x - 180, y - 170, white) 
        self.c2attack = b.Button(x + 70, y - 170, white)
        self.c3attack = b.Button(x - 180, y - 70, white)
        self.c4attack = b.Button(x + 70, y - 70, white)

        self.buttons = []
        self.buttons.append(self.escapebutton)
        self.buttons.append(self.attackbutton)
        self.buttons.append(self.c1attack)
        self.buttons.append(self.c2attack)
        self.buttons.append(self.c3attack)
        self.buttons.append(self.c4attack)

    def combatevent(self, event):
        x = self.player.position.x
        y = self.player.position.y
        if event.type == QUIT: 
            self.quit()
        if event.type == pygame.MOUSEMOTION:
            mousepos = list(pygame.mouse.get_pos())
            mousepos[0] -= self.camera.x
            mousepos[1] -= self.camera.y
            if self.escapebutton.hover(mousepos) and not self.attackingstate:
                self.drawtext("Escape...", font, grey, x - 190, y - 120)
            elif not self.escapebutton.hover(mousepos) and not self.attackingstate:
                self.drawtext("Escape...", font, white, x - 190, y - 120)
            if self.attackbutton.hover(mousepos) and not self.attackingstate:
                self.drawtext("Attack!", font, red, x + 60, y - 120)
            elif not self.attackbutton.hover(mousepos) and not self.attackingstate:
                self.drawtext("Attack!", font, black, x + 60, y - 120)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousepos = list(pygame.mouse.get_pos())
            mousepos[0] -= self.camera.x
            mousepos[1] -= self.camera.y
            if self.escapebutton.hover(mousepos) and not self.attackingstate:
                if self.enemy.escape: #escapability depends on if enemy is part of the main quest
                    print ("escaping")
                    self.combatstate = False
                    self.camera.freeze = False
                    for sprite in self.all_sprites:
                        sprite.freeze = False #releasing the little man
                    self.drawtext("You ran away...", fontbold, red, 250, 400) #fix textani later
                    pygame.time.delay(1000)
                    #direction = self.rupdate()
                    self.map_img = self.map.make_map()
                    #self.draw(direction)
                else:
                    self.dis.blit(self.combatbg, (0, 0))
                    self.drawtext("Unable to escape!", font, red, 200, 400)
                    pygame.time.delay(1000)
                    
                    self.map_img = self.map.make_map()
                    self.map_img.blit(self.combatbg, (x - 250, y - 240))
                    self.map_img.blit(self.enemyimg, (x - 50, y))
                    self.map_img.blit(self.painterimg, (x + 100, y + 100))

                    self.drawtext("You lost your advantage! %s attacks first!" %(self.enemy.name), fontbold, red, 200, 400)
                    self.enemyattacking = True
                        
            elif self.attackbutton.hover(mousepos) and not self.attackingstate:
                print ("attacking")
                self.attackingstate = True
                self.chosen = []
                self.selected = [False, False, False, False]
                self.map_img = self.map.make_map()
                self.map_img.blit(self.combatbg, (x - 250, y - 240))
                self.map_img.blit(self.enemyimg, (x - 50, y))
                self.map_img.blit(self.painterimg, (x + 100, y + 100))
                self.charstate = True

    def combatstage2(self, event):
        self.charstate = True
        x = self.player.position.x
        y = self.player.position.y
        self.c1attack.draw(self.map_img)
        self.c2attack.draw(self.map_img)
        self.c3attack.draw(self.map_img)
        self.c4attack.draw(self.map_img)

        charas = [{"name": name1,
                   "x": x - 180,
                   "y": y - 160},
                   {"name": name2,
                    "x": x + 70,
                    "y": y - 160},
                   {"name": name3,
                    "x": x - 180,
                    "y": y - 60},
                   {"name": name4,
                   "x": x + 70,
                   "y": y - 60}
                  ]
        
        i = 0
            
        for chara in charas:
            if self.selected[i]:
                colour1 = red
            else:
                colour1 = black
            i += 1
            self.drawtext(chara["name"], font, colour1, chara["x"], chara["y"])

        mousepos = list(pygame.mouse.get_pos())
        mousepos[0] -= self.camera.x
        mousepos[1] -= self.camera.y

        if event.type == pygame.MOUSEMOTION:
            if self.c1attack.hover(mousepos) and not self.selected[0]:
                self.drawtext(name1, font, blue, x - 180, y - 160)
            if self.c2attack.hover(mousepos) and not self.selected[1]:
                self.drawtext(name2, font, red, x + 70, y - 160)
            if self.c3attack.hover(mousepos) and not self.selected[2]:
                self.drawtext(name3, font, green, x - 180, y - 60)
            if self.c4attack.hover(mousepos) and not self.selected[3]:
                self.drawtext(name4, font, orange, x + 70, y - 60)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.c1attack.hover(mousepos):
                if len(self.chosen) < 2:
                    self.selected[0] = True
                    self.chosen.append(0)
            if self.c2attack.hover(mousepos):
                if len(self.chosen) < 2:
                    self.selected[1] = True
                    self.chosen.append(1)
            if self.c3attack.hover(mousepos):
                if len(self.chosen) < 2:
                    self.selected[2] = True
                    self.chosen.append(2)
            if self.c4attack.hover(mousepos):
                if len(self.chosen) < 2:
                    self.selected[3] = True
                    self.chosen.append(3)
            if len(self.chosen) == 2:
                print ("%i and %i attack" %(self.chosen[0], self.chosen[1]))
                damage = self.team.attack(self.team.characters[self.chosen[0]], self.team.characters[self.chosen[1]])
                self.enemy.update(damage)
                pygame.time.delay(2000)
                if self.enemy.hp > 0:
                    self.enemyattacking = True
                else:
                    print ("uou woinin")
                    self.combatstate = False
                    self.camera.freeze = False
                    for sprite in self.all_sprites:
                        sprite.freeze = False #releasing the little man
                    self.map_img = self.map.make_map()
                    self.charstate = False

            
    def enemyattack(self, enemy):
        damage = enemy.attack()
        print ("enemy damage: %i" % damage)
        self.team.update(damage)
        pygame.time.delay(2000)
        self.enemyattacking = False
        self.selected = [False, False, False, False]
        self.chosen = []
        
        if self.team.hp <= 0:
            print ("you lose")
            self.charstate = False
            self.enemyattacking = False
            self.combatstate = False
            self.camera.freeze = False
            for sprite in self.all_sprites:
                sprite.freeze = False #releasing the little man
            self.map_img = self.map.make_map()


    def healthbar(self, enemymaxhp):
        x = self.player.position.x 
        y = self.player.position.y

        if self.team.hp > 300:
            playerhealth = green
        elif self.team.hp > 150 and self.team.hp <= 300:
            playerhealth = yellow
        elif self.team.hp <= 150:
            playerhealth = red
        
        pygame.draw.rect(self.map_img, black, pygame.Rect(x + 98, y + 68, 104, 24), 20)
        widthplayer = int(self.team.hp / 4)
        heightplayer = 20
        pygame.draw.rect(self.map_img, playerhealth, pygame.Rect(x + 100, y + 70, widthplayer, heightplayer))

        if self.enemy.hp > int(enemymaxhp / 3) * 2:
            enemyhealth = green
        elif self.enemy.hp > int(enemymaxhp / 3) and self.enemy.hp <= int(enemymaxhp / 3) * 2:
            enemyhealth = yellow 
        elif self.enemy.hp <= int(enemymaxhp / 3):
            enemyhealth = red
        
        pygame.draw.rect(self.map_img, black, pygame.Rect(x - 52, y - 12, 104, 24), 20)
        widthenemy = self.enemy.hp/enemymaxhp * 100
        heightenemy = 20
        pygame.draw.rect(self.map_img, enemyhealth, pygame.Rect(x - 50, y - 10, widthenemy, heightenemy))

        pygame.display.flip()

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
            if self.enemyattacking:
                self.enemyattack(self.enemy)
                continue
            if self.charstate:
                self.combatstage2(event)
                self.healthbar(targhpcopy)
                continue
            if self.combatstate:
                self.combatevent(event)
                continue


            if event.type == pygame.KEYDOWN:
                # play_pos = (self.player.x, self.player.y, self.displaytext)
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_SPACE:
                    self.combat()
                if event.key == pygame.K_j:
                    self.draw_debug = not self.draw_debug
                if pygame.sprite.spritecollideany(self.player,
                                                  self.interactablebox):
                    if self.player.status == "free":
                        if event.key == pygame.K_e:
                            self.interactivity = not self.interactivity
                            self.textindex = 0
                if pygame.sprite.spritecollideany(self.player,
                                                  self.interactablebox):
                    if event.key == pygame.K_p:
                        self.interactivibee = not self.interactivibee
                        self.player.status = "carrying"
                        for y in self.interactablelox:
                            if pygame.sprite.collide_rect(self.player, y):
                                self.player.keytype = y.type
                abc = pygame.sprite.spritecollideany(self.player,
                                                     self.interactablebox)
                if abc is not None:
                    if event.key == pygame.K_RETURN:
                        if len(cs.Text[abc.type]) - 1 > self.textindex:
                            self.textindex += 1

                '''if event.key == pygame.K_d:
              self.player.move(xchange = block_speed)
            if event.key == pygame.K_w:
              self.player.move(ychange = -block_speed)
            if event.key == pygame.K_s:
              self.player.move(ychange = block_speed)'''

            # elif event.type == pygame.KEYUP:
            #  self.player.move()

    def textani(self, event, tuple, string_list, font, txtcolour):
        self.textplaying = True
        string = 0
        letter = 0
        running = True
        x, y = tuple
        while running:
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

    def texttwo(self, string, font, colour, x,
                y):  # probably easier to use for combat
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
        # gamestart.mainmenu() i tried making this code run but idk what the texts are lol
        gamestart.new()
        gamestart.run()

        pygame.display.update()
        gamestart.clock.tick(60)


main()
