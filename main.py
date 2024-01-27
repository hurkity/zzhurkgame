# start screen gyap
import sys
import math
import json
from os import path
from objs import *
import pygame
from pygame import QUIT, Rect
from pygame import mixer
import os
curdir = path.dirname(__file__)
os.chdir(curdir)
from cons import *
import buttons as b
from tilemap import *
from combat import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        mixer.init()
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
        #self.textplaying = False
        self.attackingstate = False
        self.charstate = False
        self.selected = [False, False, False, False]
        self.chosen = []
        self.enemyattacking = False
        self.escaped = False
        self.start = False
        self.string = 0
        self.letter = 0
        self.textrunning = False
        self.volume = 0.3
        self.sevolume = 0.3
        self.settingstate = False
        self.string_list = []
        self.font = None
        self.colour = None
        self.selected2 = None
        self.scroll = 0
        self.text_ani = TextAni()
        self.start_playing = False
        self.tutorial_start = False
        self.tutorial_start2 = False
        self.cutindex = None
        self.indexcounter = 26

    def load_data(self):
        folder = path.dirname(__file__)
        img_folder = path.join(folder, 'graphics')
        map_folder = path.join(folder, 'tilemaps')
        print("Index: " + str(self.mapindex) + "; Map len: "
              + str(len(cs.mapchange)))
        self.map = TiledMap(path.join(map_folder, cs.mapchange[self.mapindex]))
        print(len(cs.mapchange))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pygame.image.load(
            path.join(img_folder, 'mcfront.png')).convert_alpha()
        self.player_imgfrontleft = pygame.image.load(
            path.join(img_folder, 'mcfrontleft.png')).convert_alpha()
        self.player_imgfrontright = pygame.image.load(
            path.join(img_folder, 'mcfrontright.png')).convert_alpha()
        self.player_imgleft = pygame.image.load(
            path.join(img_folder, 'mcleft.png')).convert_alpha()
        self.player_imgleftleft = pygame.image.load(
            path.join(img_folder, 'mcleftleft.png')).convert_alpha()
        self.player_imgleftright = pygame.image.load(
            path.join(img_folder, 'mcleftright.png')).convert_alpha()
        self.player_imgright = pygame.image.load(
            path.join(img_folder, 'mcright.png')).convert_alpha()
        self.player_imgrightleft = pygame.image.load(
            path.join(img_folder, 'mcrightleft.png')).convert_alpha()
        self.player_imgrightright = pygame.image.load(
            path.join(img_folder, 'mcrightright.png')).convert_alpha()
        self.player_imgback = pygame.image.load(
            path.join(img_folder, 'mcback.png')).convert_alpha()
        self.player_imgbackleft = pygame.image.load(
            path.join(img_folder, 'mcbackleft.png')).convert_alpha()
        self.player_imgbackright = pygame.image.load(
            path.join(img_folder, 'mcbackright.png')).convert_alpha()

        self.painterimg = pygame.image.load('graphics/personality.png')
        self.painterimg = pygame.transform.scale(self.painterimg, (100, 100))


    def striptype(self, stripped):
        return int(stripped.strip())
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
        self.arrows = pygame.sprite.Group()

        for layerobject in self.map.tmxdata.objects:

            if layerobject.name == 'player' and len(self.all_sprites) == 0:
                self.player = Player(self, layerobject.x, layerobject.y) #playerspawn

            elif layerobject.name == 'house':
                Obstacle(self, layerobject.x, layerobject.y,
                         layerobject.width, layerobject.height) #obstructionspawn, use this for walls and stuff

            elif layerobject.name == 'interactablehitbox':
                InteractableBox(self, self.striptype(layerobject.type), layerobject.x, #keyhitbox
                                layerobject.y, layerobject.width,
                                layerobject.height)

            elif layerobject.name == 'textdisplay':
                if self.indexcounter == 27:
                    TextDisplay(self, 218 + int(layerobject.type) * 25,
                            885, layerobject.width,
                            layerobject.height, self.striptype(layerobject.type)) #key spawn
                else:
                    TextDisplay(self, layerobject.x,
                                layerobject.y, layerobject.width,
                                layerobject.height, self.striptype(layerobject.type)) #key spawn

            elif layerobject.name == 'teleport':
                Teleport(self, self.striptype(layerobject.type),
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

            elif layerobject.name == 'arrow':
                Arrows(self,
                       layerobject.x, layerobject.y, layerobject.width,
                       layerobject.height, self.striptype(layerobject.type))
        self.draw_debug = False
        self.interactivity = False #text interactivity
        self.frozen = False #its just like interactivity but i need to use it
        self.interactivibee = False #pickup interactivity
        self.camera = View(self.map.width, self.map.height)

        self.team = Team()

        self.enemies = []
        for enemy in enemies:
            obj_enemy = Computer(enemy['name'], enemy['hp'], enemy['pow'], True, enemy['map'], enemy['x'], enemy['y'], enemy['pic'])
            self.enemies.append(obj_enemy)

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

    def prequit(self):
        pos = [self.player.position.x, self.player.position.y]
        return pos

    def rupdate(self):
        self.all_sprites.update()
        direction = self.player.direction
        #print([self.player.position.x, self.player.position.y])
        self.camera.update(self.player)
        return direction

    def drawbg(self, colour):
        self.dis.fill(colour)

    def startscreen(self, event): #just the opening screen with the car going down

        gameover = False
        currentime = 0
        num = 7
        #self.playsound('sounds/car.mp3')
        while not gameover and currentime < 10000:
            if event.type == QUIT:
                gameover = True
                self.quit()

            for i in range(0, tiles):
                self.dis.blit(bg, (i*diswidth + self.scroll, 0))

                num -= 0.01
                self.scroll -= num #slows down until it comes to stop

                if abs(self.scroll) > diswidth:
                    self.scroll = 0

                self.dis.blit(truck, truckrect) #gyap
                if event.type == smokeappear:
                    self.dis.blit(smoke, smokerect) #gyap

                if currentime in range(9080, 10020):
                    pygame.time.delay(3000)
                    pygame.mixer.stop()
                    x = self.player.position.x - 250
                    y = self.player.position.y + 160
                    self.camera.freeze = True
                    for sprite in self.all_sprites:
                        sprite.freeze = True
                    self.text_ani.start_display(bigtext1, x, y, font2, white,
                                                cleanup_func = self.start_tutorial)

                    if event.type == pygame.KEYDOWN:
                        self.tutorial(event)

                currentime = pygame.time.get_ticks()
                self.clock.tick(80) #gyap
                pygame.display.update()

    def start_tutorial(self):
        self.tutorial_start = True

    def tutorial(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                self.camera.freeze = False
                for sprite in self.all_sprites:
                    sprite.freeze = False
                self.map_img = self.map.make_map()
                self.tutorial_start = False
                pygame.time.delay(2000)


    def movementani(self, direction):

        for sprite in self.all_sprites:
            if direction == None: #when no movement 
                self.dis.blit(sprite.image, self.camera.implement(sprite))
            elif direction == 'l':
                self.map_img.blit(sprite.imageleft, sprite.rectleft)
                break
            elif direction == 'r':
                self.map_img.blit(sprite.imageright, self.camera.implement(sprite))
                break
            elif direction == 'b':
                self.map_img.blit(sprite.imageback, sprite.rectback)
                break
            elif direction == 'f':
                self.map_img.blit(sprite.image, sprite.rectfront)
                break

            else:
                anigroup = sprite.getanigroup() #to HERE (check objs player class get keys method)
                self.dis.blit(anigroup[sprite.currentsprite], self.camera.implement(
                    sprite)) #for animation yep
                sprite.currentsprite += 1 #loooop
                pygame.time.wait(100)
                if sprite.currentsprite > len(anigroup) - 1:
                    sprite.currentsprite = 0 #reset

            if self.draw_debug:
                pygame.draw.rect(self.dis, cs.blue,
                                self.camera.implement_rect(sprite.hit_rect), 1)

    def playsound(self, sound):
        mixer.music.load(sound)
        mixer.music.set_volume(self.volume)
        mixer.music.play()

    def cutsceneend(self):
        self.player.player_speed = 250
        cutscenes[self.cutindex]['done'] = True
        self.map_img = self.map.make_map()

        pygame.display.update()
        self.player.cutscene = False
        self.player.cutsceneend = False

    def cutscene(self, movement, text, index):
        if index == 6:
            x = self.player.position.x - 410
            y = self.player.position.y + 310
        if index == 7:
            x = self.player.position.x - 250
            y = self.player.position.y + 100
        if index == 15: 
            x = self.player.position.x - 230
            y = self.player.position.y + 150
        if index == 22: 
            x = self.player.position.x - 230
            y = self.player.position.y + 150
        else:
            x = self.player.position.x - 250
            y = self.player.position.y + 150
        
        if text != None:
            self.text_ani.start_display(text, x, y, font2, white, cleanup_func = self.cleanup)

        self.player.player_speed = 100
        self.player.cutscene = True
        self.player.directions = movement[:]

    def draw(self, direction):
        self.dis.blit(self.map_img, self.camera.implement_rect(self.map_rect))
        #if cs.cutscenes[self.indexcounter]['index'] ==
        if not self.combatstate:
            for x in self.text:
                if x.type == self.player.keytype:
                    self.player.holding(x)

            for x in self.text:
                self.dis.blit(x.image, self.camera.implement_rect(x.rect))

            for x in self.locks:
                self.dis.blit(x.image, self.camera.implement_rect(x.rect))

            for x in self.arrows:
                self.dis.blit(x.image, self.camera.implement_rect(x.rect))
            # .all_sprites.draw(self.dis)

            self.movementani(direction)

            if self.draw_debug:
                for x in self.obstruction:
                    pygame.draw.rect(self.dis, cs.blue,
                                     self.camera.implement_rect(x.hit_rect), 1)

            self.checkobjinter()
            self.checklockinter()
            self.checkpickups()

            if self.player.status == "carrying":
                self.inneractivibee()


            arghhss = pygame.sprite.spritecollideany(self.player, self.teleport)
            if arghhss is not None:
                self.mapindex = arghhss.type
                self.load_data()
                self.new()
                '''
            for sprit in self.all_sprites:
                self.dis.blit(sprit.image, self.camera.apply(sprit))'''
            # for x in list:
            # dis.blit()#find an efficient way to compare x as and integer to object position in a list

        pygame.display.flip()

    def checkpickups(self):
        if self.player.status == "carrying":
            self.dis.blit(cs.droptext, cs.droptextRect)
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
                                        lock.unlocked(textdis, lc) #WHY IS THIS NOT WORKING

    def checklockinter(self):
        c = pygame.sprite.spritecollideany(self.player, self.interactablelox)
        if self.interactivibee:
            if c is not None:
                for aye in self.locks:
                    if aye.type == c.type:
                        #self.player.keytype = aye.type
                        pygame.sprite.Sprite.remove(aye,
                                                    self.obstruction)

    def checkobjinter(self):
        grr = pygame.sprite.spritecollideany(self.player, self.interactablebox)
        if grr is not None:
            for erm in self.text:
                if erm.type == grr.type:
                    if self.interactivity:
                        erm.displaymytextbetter()
                    elif self.interactivibee:
                        if self.player.keytype == erm.type:
                            pygame.sprite.Sprite.remove(erm,
                                                        self.obstruction)
                    else:
                        erm.displaymytext()

    def drawborder(self, rect, colour):
        pygame.draw.rect(self.map_img, colour, pygame.Rect(rect.x - 2, rect.y - 2, rect.width + 4, rect.height + 4))
        pygame.display.flip()

    def combat(self):
        self.escaped = False
        x = self.player.position.x - 250
        y = self.player.position.y + 150
        self.text_ani.start_display(combattext1, x, y, font, green, cleanup_func = None)
        self.combatstate = True
        self.camera.freeze = True
        for sprite in self.all_sprites:
            sprite.freeze = True

        x = self.player.position.x
        y = self.player.position.y
        self.combatbg = pygame.image.load('graphics/combatbg.jpg').convert()
        self.combatbg = pygame.transform.scale(self.combatbg, (diswidth, disheight))
        self.map_img.blit(self.combatbg, (x - 250, y - 250))
        self.map_img.blit(self.enemyimg, (x - 50, y))
        self.map_img.blit(self.painterimg, (x + 100, y + 50))

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
                    self.string_list = escapetext

                    self.combatstate = False
                    self.camera.freeze = False
                    for sprite in self.all_sprites:
                        sprite.freeze = False #releasing the little man
                    pygame.time.delay(1000)
                    self.escaped = True
                    self.map_img = self.map.make_map()
                    self.text_ani.start_display(["You ran away..."], x - 250, y + 150, font, red, cleanup_func=self.cleanup)

                else:
                    self.attackingstate = True
                    self.map_img = self.map.make_map()
                    self.map_img.blit(self.combatbg, (x - 250, y - 250))
                    self.map_img.blit(self.enemyimg, (x - 50, y))
                    self.map_img.blit(self.painterimg, (x + 100, y + 50))

                    pygame.display.flip()
                    self.drawtext("You lost your advantage!", font, red, x - 180, y + 200)
                    self.drawtext("%s attacks first!" %(self.enemy.name), font, red, x - 160, y + 220)
                    pygame.display.flip()

                    self.enemyattacking = True
                    self.charstate = True

            elif self.attackbutton.hover(mousepos) and not self.attackingstate:
                x = self.player.position.x - 250
                y = self.player.position.y + 150
                self.attackingstate = True
                self.chosen = []
                self.text_ani.start_display(["CHOOSE TWO CHARACTERS: "], x, y, font, green, cleanup_func = None)
                self.selected = [False, False, False, False]
                self.map_img = self.map.make_map()
                self.map_img.blit(self.combatbg, (x - 250, y - 250))
                self.map_img.blit(self.enemyimg, (x - 50, y))
                self.map_img.blit(self.painterimg, (x + 100, y + 50))
                self.charstate = True

    def combatstage2(self, event):
        self.charstate = True
        x = self.player.position.x
        y = self.player.position.y

        for i in range(4):
            self.drawborder(self.buttons[i], black)

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
                if len(self.chosen) < 2 and 0 not in self.chosen:
                    self.selected[0] = True
                    self.chosen.append(0)
            if self.c2attack.hover(mousepos) and 1 not in self.chosen:
                if len(self.chosen) < 2:
                    self.selected[1] = True
                    self.chosen.append(1)
            if self.c3attack.hover(mousepos) and 2 not in self.chosen:
                if len(self.chosen) < 2:
                    self.selected[2] = True
                    self.chosen.append(2)
            if self.c4attack.hover(mousepos) and 3 not in self.chosen:
                if len(self.chosen) < 2:
                    self.selected[3] = True
                    self.chosen.append(3)
            if len(self.chosen) == 2:
                damage = self.team.attack(self.team.characters[self.chosen[0]], self.team.characters[self.chosen[1]])
                self.enemy.update(damage)
                pygame.time.delay(2000)
                text_list = ["%s AND %s ATTACK" %(charas[self.chosen[0]]['name'], charas[self.chosen[1]]['name']),
                        "DEAL %i DAMAGE" % damage]
                x = self.player.position.x - 250
                y = self.player.position.y + 150
                if self.enemy.hp > 0:
                    self.enemyattacking = True
                    self.text_ani.start_display(text_list, x, y, font, yellow, cleanup_func=self.switch_enemy_attack)

                else:
                    self.escaped = True
                    self.combatstate = False
                    self.camera.freeze = False
                    for sprite in self.all_sprites:
                        sprite.freeze = False #releasing the little man
                    self.map_img = self.map.make_map()
                    self.charstate = False
                    self.team.add_maxhp(self.team.hp)
                    self.team.reset_hp()
                    self.enemy.resethp(self.enemy.hp)
                    self.attackingstate = False
                    text_list.append("YOU WIN!")
                    self.text_ani.start_display(text_list, x, y, font, yellow, cleanup_func=self.cleanup)


    def enemyattack(self, enemy):
        x = self.player.position.x - 250
        y = self.player.position.y + 150
        damage = enemy.attack()
        self.team.update(damage)
        pygame.time.delay(2000)
        self.enemyattacking = False
        self.selected = [False, False, False, False]
        self.chosen = []

        if self.team.hp <= 0:
            self.text_ani.start_display(combattextlose, x, y, font, yellow, cleanup_func=self.cleanup)
            self.charstate = False
            self.enemyattacking = False
            self.combatstate = False
            self.escaped = True
            self.camera.freeze = False
            for sprite in self.all_sprites:
                sprite.freeze = False #releasing the little man
            self.map_img = self.map.make_map()
            self.team.reset_hp()
            self.enemy.resethp(self.enemy.hp)
            self.attackingstate = False



    def healthbar(self, enemymaxhp):
        x = self.player.position.x
        y = self.player.position.y

        if self.team.hp > self.team.max_hp * 0.75:
            playerhealth = green
        elif self.team.hp > self.team.max_hp * 0.4:
            playerhealth = yellow
        elif self.team.hp <= self.team.max_hp * 0.4:
            playerhealth = red

        pygame.draw.rect(self.map_img, black, pygame.Rect(x + 98, y + 68, 104, 24), 20)
        widthplayer = int(100 * self.team.hp / self.team.max_hp)
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

    def cleanup(self):
        self.map_img = self.map.make_map()
        self.camera.freeze = False
        for sprite in self.all_sprites:
            sprite.freeze = False

    def switch_enemy_attack(self):
        self.enemyattacking = True

    def events(self):
        if not self.player.cutscene:
            if not self.player.cutsceneend:
                for cut in cutscenes:
                    if self.indexcounter == cut['index']:
                        if not cut['done'] and self.mapindex == cut['map'] and self.start:
                            if abs(self.player.position.x - cut['x']) < 50 and abs(self.player.position.y - cut['y']) < 50:
                                self.cutscene(cut['movement'], cut['text'], cut['index'])
                                self.cutindex = cut['index']
                                print (self.indexcounter)
                                self.indexcounter += 1
                                if cut['colour'] == yellow:
                                    self.text_ani.colour = yellow
                                else:
                                    self.text_ani.colour = white
            else:
                self.player.cutscene = False
        else:
            if self.player.cutsceneend:
                self.cutsceneend()
                self.map_img = self.map.make_map()

        if not self.player.cutscene: #specifically for cutscene 7 which is when you pick up the key
            if self.player.keytype == 0 and not cutscenes[7]['done'] and self.indexcounter == cutscenes[7]['index']:
                self.cutindex = cutscenes[7]['index']
                self.indexcounter += 1
                if self.indexcounter == 27:
                        enemies.append({"name": "FINAL MUTATION", "hp": 10000, "pow": 200, "map": 2, "x": 250, "y": 700, "pic": "graphics/monster.png"})

                self.cutscene(cutscenes[7]['movement'], cutscenes[7]['text'], cutscenes[7]['index'])
                if cutscenes[7]['colour'] == yellow:
                    self.text_ani.colour = yellow
                else:
                    self.text_ani.colour = white
            else:
                self.player.cutscene = False
        else:
            if self.player.cutsceneend:
                self.cutsceneend()
                self.map_img = self.map.make_map()

        if self.combatstate: 
            self.camera.freeze = True
            for sprite in self.all_sprites: 
                sprite.freeze = True

        if not self.escaped:
            for enemy in self.enemies:
                if enemy.map == self.mapindex and self.start:
                    if abs(self.player.position.x - enemy.x) < 50 and abs(self.player.position.y - enemy.y) < 50:
                        if not self.combatstate:
                            self.enemy = enemy
                            self.enemyimg = pygame.image.load(self.enemy.pic)
                            self.enemyimg = pygame.transform.scale(self.enemyimg, (100, 100))
                            self.combat()

        else:
            inrange = False
            for enemy in self.enemies:
                if enemy.map == self.mapindex and self.start:
                    if abs(self.player.position.x - enemy.x) < 60 or abs(self.player.position.y - enemy.y) < 60:
                        inrange = True
                        break
            
            if not inrange:
                self.escaped = False
            self.map_img = self.map.make_map()
            self.combatstate = False

        if self.text_ani.is_displaying():
            self.player.direction = None
            self.camera.freeze = True
            for sprite in self.all_sprites:
                sprite.freeze = True

            displaying = self.text_ani.update(self.map_img)
        else:
            if not self.combatstate:
                self.camera.freeze = False
                for sprite in self.all_sprites:
                    sprite.freeze = False
            self.text_ani.cleanup()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if self.enemyattacking:
                self.enemyattack(self.enemy)
                self.healthbar(self.enemy.maxhp)
                continue
            if self.charstate:
                self.combatstage2(event)
                self.healthbar(self.enemy.maxhp)
                continue
            if self.combatstate:
                #self.textrunning = True
                self.combatevent(event)
                # continue

            if not self.start and not self.settingstate:
                self.frozen = True
                self.mainmenu(event)
                continue
            if self.settingstate:
                self.settings(event)
                continue
            if self.start:
                self.frozen = False

            if self.tutorial_start:
                self.tutorial(event)
            if self.tutorial_start2:
                self.tutorial2(event)

            if event.type == pygame.KEYDOWN:
                # play_pos = (self.player.x, self.player.y, self.displaytext)
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_m: 
                    if not self.combatstate and not self.text_ani.textplaying:
                        self.start = False
                        self.mainmenu(event)
                if event.key == pygame.K_q:
                    print ([self.player.position.x, self.player.position.y])
                if event.key == pygame.K_t: #GYAP
                    x = self.player.position.x - 250
                    y = self.player.position.y + 150
                    self.camera.freeze = True
                    self.text_ani.start_display(stringlist, x, y, font, white, self.cleanup)
                if event.key == pygame.K_SPACE:
                    if self.text_ani.is_displaying():
                        self.text_ani.skip_line()
                    else:
                        self.map_img = self.map.make_map()

                if event.key == pygame.K_j:
                    self.draw_debug = not self.draw_debug # originally a function meant to show objects heh

                if self.player.status == "carrying":
                    if event.key == pygame.K_g:
                        self.interactivibee = False
                        self.player.dropped()
                        self.player.status = "free"


                abc = pygame.sprite.spritecollideany(self.player,
                                                     self.interactablebox)
                if abc is not None:
                    if self.player.status == "free":
                        if event.key == pygame.K_e:
                            self.interactivity = not self.interactivity
                            self.textindex = 0
                if abc is not None:
                    if event.key == pygame.K_RETURN:
                        if len(cs.Text[abc.type]) - 1 > self.textindex:
                            self.textindex += 1
                if abc is not None:
                    if event.key == pygame.K_p:
                        self.interactivibee = not self.interactivibee
                        self.player.status = "carrying"
                        self.player.keytype = abc.type




                '''if event.key == pygame.K_d:
              self.player.move(xchange = block_speed)
            if event.key == pygame.K_w:
              self.player.move(ychange = -block_speed)
            if event.key == pygame.K_s:
              self.player.move(ychange = block_speed)'''

            # elif event.type == pygame.KEYUP:
            #  self.player.move()

    def drawtext(self, string, font, colour, x, y):
        text = font.render(string, True, colour)
        textrect = text.get_rect(topleft=(x, y))
        self.map_img.blit(text, textrect)

    def start_game(self):
        self.start_playing = True

    def newgame(self, event):
        pygame.display.set_caption("New Game")

        self.map_img = self.map.make_map()

        self.startscreen(event)

        self.cutscenestate = True

        pygame.display.flip()
        self.start = True

        if event.type == QUIT:
            self.quit()

    def contgame(self, event):
        pygame.display.set_caption("Continue Game")
        self.map_img = self.map.make_map()
        pygame.display.flip()

        self.start = True
        if event.type == QUIT:
            self.quit()

    def settings(self, event):
        mousepos = list(pygame.mouse.get_pos())
        mousepos[0] -= self.camera.x
        mousepos[1] -= self.camera.y
        x = self.player.position.x
        y = self.player.position.y

        pygame.display.set_caption("Settings")
        self.map_img.fill(black)
        pygame.display.flip()

        self.settingstate = True
        if event.type == QUIT:
            self.quit()

        audiobutton = b.Button(x - 200, y - 200, black)
        systembutton = b.Button(x, y - 200, black)
        self.drawborder(audiobutton, white)
        self.drawborder(systembutton, white)

        audiobutton.draw(self.map_img)
        systembutton.draw(self.map_img)

        audiocol = white
        systemcol = white
        if self.selected2 == "AUDIO":
            audiocol = red
        elif self.selected2 == "SYSTEM":
            systemcol = red
        self.drawtext("AUDIO", font, audiocol, x - 170, y - 180)
        self.drawtext("SYSTEM", font, systemcol, x + 30, y - 180)

        self.back = b.Button(x + 150, y + 200, white)
        self.drawtext("BACK", font, red, x + 150, y + 200)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back.hover(mousepos):
                self.settingstate = False
                self.mainmenu(event)

        if audiobutton.hover(mousepos) and self.selected2 != "AUDIO":
            self.drawtext("AUDIO", font, red, x - 170, y - 180)
        elif systembutton.hover(mousepos) and self.selected2 != "SYSTEM":
            self.drawtext("SYSTEM", font, red, x + 30, y - 180)

        yvols = [y - 50, y - 65, y - 80, y - 95]
        vols = []
        self.vol1 = b.Button2(x, yvols[0], white, 50)
        self.vol2 = b.Button2(x + 40, yvols[1], white, 80)
        self.vol3 = b.Button2(x + 80, yvols[2], white, 110)
        self.vol4 = b.Button2(x + 120, yvols[3], white, 140)
        vols.append(self.vol1)
        vols.append(self.vol2)
        vols.append(self.vol3)
        vols.append(self.vol4)

        yvols2 = [y + 100, y + 85, y + 70, y + 55]
        vols2 = []
        self.vol5 = b.Button2(x, yvols2[0], white, 50)
        self.vol6 = b.Button2(x + 40, yvols2[1], white, 80)
        self.vol7 = b.Button2(x + 80, yvols2[2], white, 110)
        self.vol8 = b.Button2(x + 120, yvols2[3], white, 140)
        vols2.append(self.vol5)
        vols2.append(self.vol6)
        vols2.append(self.vol7)
        vols2.append(self.vol8)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.vol1.hover(mousepos):
                self.volume = 0
            if self.vol2.hover(mousepos):
                self.volume = 0.2
            if self.vol3.hover(mousepos):
                self.volume = 0.4
            if self.vol4.hover(mousepos):
                self.volume = 0.6

            if self.vol5.hover(mousepos):
                self.sevolume = 0
            if self.vol6.hover(mousepos):
                self.sevolume = 0.2
            if self.vol7.hover(mousepos):
                self.sevolume = 0.4
            if self.vol8.hover(mousepos):
                self.sevolume = 0.6

        #audio buttons
        self.bgvol = b.Button(x - 200, y - 50, black)
        self.sevol = b.Button(x - 200, y + 100, black)
        #system buttons
        self.loadfile = b.Button(x - 200, y - 50, black)
        self.exitgame = b.Button(x - 200, y + 100, black)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if audiobutton.hover(mousepos):
                self.selected2 = "AUDIO"
                self.map_img = self.map.make_map()
                self.map_img.fill(black)
            if systembutton.hover(mousepos):
                self.selected2 = "SYSTEM"
                self.map_img = self.map.make_map()
                self.map_img.fill(black)

        if self.selected2 == "AUDIO":
            self.drawborder(self.bgvol, white)
            self.bgvol.draw(self.map_img)
            self.drawborder(self.sevol, white)
            self.sevol.draw(self.map_img)
            self.drawtext("BGM VOL", font, red, x - 180, y - 30)
            self.drawtext("SE VOL", font, red, x - 180, y + 120)
            self.drawtext("BACK", font, red, x + 150, y + 200)

            for vol in range(4):
                vols[vol].draw(self.map_img)
            for vol2 in range(4):
                vols2[vol2].draw(self.map_img)


            if event.type == pygame.MOUSEBUTTONDOWN:
                if systembutton.hover(mousepos):
                    self.selected2 = "SYSTEM"
                if self.back.hover(mousepos):
                    self.selected2 = None

        if self.selected2 == "SYSTEM":
            self.drawborder(self.loadfile, white)
            self.loadfile.draw(self.map_img)
            self.drawborder(self.exitgame, white)
            self.exitgame.draw(self.map_img)
            self.drawtext("LOAD FILE", font, red, x - 194, y - 30)
            self.drawtext("EXIT GAME", font, red, x - 194, y + 120)
            self.drawtext("BACK", font, red, x + 150, y + 200)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if audiobutton.hover(mousepos):
                    self.selected2 = "AUDIO"
                if self.back.hover(mousepos):
                    self.selected2 = None
                if self.exitgame.hover(mousepos):
                    self.quit()


    def mainmenu(self, event):
        self.map_img.fill(white)
        self.settingstate = False
        #self.camera.freeze = True
        #for sprite in self.all_sprites:
            #sprite.freeze = True

        x = self.player.position.x
        y = self.player.position.y
        mousepos = list(pygame.mouse.get_pos())
        mousepos[0] -= self.camera.x
        mousepos[1] -= self.camera.y

        button1 = b.Button(x + x1, y1 + y, colour1)
        self.drawborder(button1, black)
        button1.draw(self.map_img)
        button2 = b.Button(x + x2, y2 + y, colour2)
        self.drawborder(button2, black)
        button2.draw(self.map_img)
        button3 = b.Button(x + x3, y3 + y, colour3)
        self.drawborder(button3, black)
        button3.draw(self.map_img)

        self.drawtext(string1, font, black, x + x1 + 10, y1 + y + 10)
        self.drawtext(string2, font, black, x + x2 + 10, y2 + y + 10)
        self.drawtext(string3, font, black, x + x3 + 10, y3 + y + 10)

        if button1.hover(mousepos):
            self.drawtext(string1, font, red, x + x1 + 10, y1 + y + 10)
        elif button2.hover(mousepos):
            self.drawtext(string2, font, red, x + x2 + 10, y2 + y + 10)
        elif button3.hover(mousepos):
            self.drawtext(string3, font, red, x + x3 + 10, y3 + y + 10)


        if event.type == QUIT:
            self.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button1.hover(mousepos):
                self.newgame(event)
            elif button2.hover(mousepos):
                self.contgame(event)
            elif button3.hover(mousepos):
                self.settings(event)


def main():
    gamestart = Game()
    while True:
        # gamestart.mainmenu() i tried making this code run but idk what the texts are lol
        gamestart.new()
        gamestart.run()

        pygame.display.update()
        gamestart.clock.tick(60)


main()
