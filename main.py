# start screen gyap
import sys
import math
from os import path
from objs import *
import pygame
from pygame import QUIT, Rect
from pygame import mixer
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
        self.textplaying = False
        self.attackingstate = False
        self.charstate = False
        self.selected = [False, False, False, False]
        self.chosen = []
        self.enemyattacking = False
        self.start = False
        self.string = 0
        self.letter = 0
        self.textrunning = False
        self.volume = 0.5
        self.settingstate = False
        self.string_list = []
        self.font = None
        self.colour = None
        self.selected2 = None
        self.vol1col = white
        self.vol2col = white
        self.vol3col = white
        self.vol4col = black
        self.scroll = 0
        self.text_ani = TextAni()
        self.start_playing = False
        self.tutorial_start = False

    def load_data(self):
        folder = path.dirname(__file__)
        img_folder = path.join(folder, 'graphics')
        map_folder = path.join(folder, 'tilemaps')
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
                InteractableBox(self, layerobject.type, layerobject.x, #keyhitbox
                                layerobject.y, layerobject.width,
                                layerobject.height)

            elif layerobject.name == 'textdisplay':
                TextDisplay(self, layerobject.x,
                            layerobject.y, layerobject.width,
                            layerobject.height, layerobject.type) #key spawn

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

    def drawbg(self, colour):
        self.dis.fill(colour)

    def startscreen(self, event):

        gameover = False
        currentime = 0
        num = 7
        #self.playsound('sounds/car.mp3')
        while not gameover and currentime < 1000:
            if event.type == QUIT:
                gameover = True
                self.quit()

            for i in range(0, tiles):
                self.dis.blit(bg, (i*diswidth + self.scroll, 0))

                num -= 0.01
                self.scroll -= num

                if abs(self.scroll) > diswidth:
                    self.scroll = 0

                self.dis.blit(truck, truckrect) #gyap
                if event.type == smokeappear:
                    self.dis.blit(smoke, smokerect) #gyap

                if currentime in range(0, 1000):
                    pygame.time.delay(3000)
                    pygame.mixer.stop()
                    x = self.player.position.x - 250
                    y = self.player.position.y + 160
                    text_list = bigtext1
                    self.camera.freeze = True
                    for sprite in self.all_sprites:
                        sprite.freeze = True
                    self.text_ani.start_display(text_list, x, y, font2, white, \
                                                cleanup_func = self.start_tutorial)

                    #self.cleanup()
                    print ("??")
                    if event.type == pygame.KEYDOWN:
                        self.tutorial(event)

                currentime = pygame.time.get_ticks()
                self.clock.tick(80) #gyap
                pygame.display.update()

    def start_tutorial(self):
        print ("Asdasd")
        x = self.player.position.x - 250
        y = self.player.position.y + 160
        self.text_ani.start_display(instructions1, x, y, font2, yellow, cleanup_func = self.start_game)
        self.tutorial_start = True

    def tutorial(self, event):
        x = self.player.position.x - 250
        y = self.player.position.y + 160
        currentime = 0
        running = True
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                while running:
                    self.camera.freeze = False
                    for sprite in self.all_sprites:
                        sprite.freeze = False
                    print (currentime)
                    currentime = pygame.time.get_ticks()
                    self.clock.tick(80)
                    pygame.display.update()
                    if currentime > 5000:
                        running = False
                        self.text_ani.start_display(instructions2, x, y, font2, yellow, cleanup_func = None)
                        self.camera.freeze = True
                        for sprite in self.all_sprites:
                            sprite.freeze = True
                #self.text_ani.start_display(instructions3, x, y, font2, yellow, cleanup_func = self.start_game)

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

    def playsound(self, sound):
        mixer.music.load(sound)
        mixer.music.set_volume(self.volume)
        mixer.music.play()

    def cutsceneend(self):
        x = self.player.position.x - 250
        y = self.player.position.y - 50
        self.string_list = testtext
        self.textplaying = True
        self.textrunning = True
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
                        self.mapindex = self.striptype(x.type)
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
                                        lock.unlocked(textdis, lc) #WHY IS THIS NOT WORKING

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
        grr = pygame.sprite.spritecollideany(self.player, self.interactablebox)
        if grr is not None:
            for erm in self.text:
                if erm.type == grr.type:
                    if self.interactivity:
                        erm.displaymytextbetter(self.textindex)
                    elif self.interactivibee:
                        self.player.keytype = erm.type
                        pygame.sprite.Sprite.remove(erm,
                                                    self.obstruction)
                    else:
                        erm.displaymytext()

    def drawborder(self, rect, colour):
        pygame.draw.rect(self.map_img, colour, pygame.Rect(rect.x - 2, rect.y - 2, rect.width + 4, rect.height + 4))
        pygame.display.flip()

    def starttextani(self):
        #self.playsound('sounds/typing.mp3')
        self.string = 0
        self.letter = 0
        self.textrunning = True
        self.textplaying = True
        self.camera.freeze = True
        for sprite in self.all_sprites:
            sprite.freeze = True

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
        self.buttons.append(self.c1attack)
        self.buttons.append(self.c2attack)
        self.buttons.append(self.c3attack)
        self.buttons.append(self.c4attack)

    def combatevent(self, event):
        x = self.player.position.x
        y = self.player.position.y
        self.string_list = combattext1
        self.font = font
        self.colour = white
        self.textrunning = True
        self.textplaying = True

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
                    self.string_list = escapetext

                    self.combatstate = False
                    self.camera.freeze = False
                    for sprite in self.all_sprites:
                        sprite.freeze = False #releasing the little man
                    pygame.time.delay(1000)
                    self.map_img = self.map.make_map()
                    self.text_ani.start_display(["You ran away..."], x - 250, y + 150, font, red, cleanup_func=self.cleanup)

                else:
                    self.attackingstate = True
                    self.map_img = self.map.make_map()
                    self.map_img.blit(self.combatbg, (x - 250, y - 240))
                    self.map_img.blit(self.enemyimg, (x - 50, y))
                    self.map_img.blit(self.painterimg, (x + 100, y + 100))

                    self.string_list = combattext2
                    self.textrunning = True
                    self.textplaying = True

                    #self.drawtext("Unable to escape!", font, red, x - 130, y + 180)
                    pygame.display.flip()
                    self.drawtext("You lost your advantage!", font, red, x - 180, y + 200)
                    self.drawtext("%s attacks first!" %(self.enemy.name), font, red, x - 160, y + 220)
                    pygame.display.flip()

                    self.enemyattacking = True
                    self.charstate = True

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
                damage = self.team.attack(self.team.characters[self.chosen[0]], self.team.characters[self.chosen[1]])
                self.enemy.update(damage)
                pygame.time.delay(2000)
                text_list = ["Attacking enemy.",
                        "%s and %s attack" %(charas[self.chosen[0]]['name'], charas[self.chosen[1]]['name']),
                        "%i damage" % damage]
                x = self.player.position.x - 250
                y = self.player.position.y + 150
                if self.enemy.hp > 0:
                    self.enemyattacking = True
                    self.text_ani.start_display(text_list, x, y, font, yellow, cleanup_func=self.swith_enemy_attack)

                else:
                    print ("uou woinin")
                    self.combatstate = False
                    self.camera.freeze = False
                    for sprite in self.all_sprites:
                        sprite.freeze = False #releasing the little man
                    self.map_img = self.map.make_map()
                    self.charstate = False
                    text_list.append("You win!")
                    self.text_ani.start_display(text_list, x, y, font, yellow, cleanup_func=self.cleanup)


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

    def cleanup(self):
        self.map_img = self.map.make_map()
        self.camera.freeze = False
        for sprite in self.all_sprites:
            sprite.freeze = False

    def swith_enemy_attack(self):
        self.enemyattacking = True

    def events(self):
        if not self.player.cutscene:
            if not self.player.cutsceneend:
                if abs(self.player.position.x - 500) < 50 and abs(self.player.position.y - 500) < 50:
                    self.cutscene()
        else:
            if self.player.cutsceneend:
                print ("Asd")
                self.cutsceneend()

        '''if not self.textplaying:
            if self.textrunning:
                self.textrunning = False
                self.camera.freeze = False
                for sprite in self.all_sprites:
                    sprite.freeze = False
                    
                if not self.combatstate:  
                    self.map_img = self.map.make_map()'''

        if self.text_ani.is_displaying():
            displaying = self.text_ani.update(self.map_img)
            if not displaying:
                self.text_ani.cleanup()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if self.enemyattacking:
                self.enemyattack(self.enemy)
                self.healthbar(targhpcopy)
                continue
            if self.charstate:
                self.combatstage2(event)
                self.healthbar(targhpcopy)
                continue
            if self.combatstate:
                self.textrunning = True
                self.combatevent(event)
                # continue

            if not self.start and not self.settingstate:
                self.mainmenu(event)
                continue
            if self.settingstate:
                self.settings(event)
                continue

            if self.tutorial_start:
                self.tutorial(event)

            if event.type == pygame.KEYDOWN:
                # play_pos = (self.player.x, self.player.y, self.displaytext)
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_SPACE: #temporary
                    if not self.combatstate:
                        x = self.player.position.x - 250
                        y = self.player.position.y + 150
                        self.combat()
                        self.text_ani.start_display(combattext1, x, y, font, green, cleanup_func = None)
                if event.key == pygame.K_m: #temporary
                    self.playsound('sounds/typing.mp3')
                if event.key == pygame.K_t: #GYAP
                    x = self.player.position.x - 250
                    y = self.player.position.y + 150
                    self.camera.freeze = True
                    self.text_ani.start_display(stringlist, x, y, font, white, self.cleanup)
                if event.key == pygame.K_p:
                    #self.map_img = self.map.make_map()
                    if self.text_ani.is_displaying():
                        self.text_ani.skip_line()
                    else:
                        self.map_img = self.map.make_map()
                if event.key == pygame.K_RETURN:
                    if self.textplaying and not self.textrunning:
                        self.map_img = self.map.make_map()
                        self.camera.freeze = False
                        for sprite in self.all_sprites:
                            sprite.freeze = False
                        self.textplaying = False
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

    def drawtext(self, string, font, colour, x, y):
        text = font.render(string, True, colour)
        textrect = text.get_rect(topleft=(x, y))
        self.map_img.blit(text, textrect)

    def texttwo(self, string, font, colour, x,
                y):  # probably easier to use for combat
        text = font.render(string, True, colour)
        textrect = text.get_rect(center=(x, y))
        self.dis.blit(text, textrect)

    def start_game(self):
        self.start_playing = True

    def newgame(self, event):
        pygame.display.set_caption("New Game")

        self.map_img = self.map.make_map()

        self.startscreen(event)

        self.cutscenestate = True

        pygame.display.flip()
        print('new game')
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

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.vol1.hover(mousepos):
                self.volume = 0
            if self.vol2.hover(mousepos):
                self.volume = 0.2
            if self.vol3.hover(mousepos):
                self.volume = 0.4
            if self.vol4.hover(mousepos):
                self.volume = 0.6
        print (self.volume)

        self.vol1 = b.Button2(x, yvols[0], self.vol1col, 50)
        self.vol2 = b.Button2(x + 40, yvols[1], self.vol1col, 80)
        self.vol3 = b.Button2(x + 80, yvols[2], self.vol1col, 110)
        self.vol4 = b.Button2(x + 120, yvols[3], self.vol4col, 140)

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
                self.drawborder(vols[vol], white)
                vols[vol].draw(self.map_img)

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
