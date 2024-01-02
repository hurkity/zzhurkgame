#start screen gyap
import sys
from os import path
from objs import *
import pygame
from cons import *
import buttons as b


class Game:
  def __init__(self):
    pygame.init()
    self.dis = pygame.display.set_mode((800, 500))
    pygame.display.set_caption('Start Screen')
    self.clock = pygame.time.Clock()
    pygame.key.set_repeat(500, 100)
    self.load_data()
    self.displaytext = False

  def load_data(self):
    folder = path.dirname(__file__)
    self.mapdata = []
    with open(path.join(folder, 'map.txt'), 'rt') as f:
      for line in f:
        self.mapdata.append(line)

  def new(self):
    self.all_sprites = pygame.sprite.Group()
    self.obstruction = pygame.sprite.Group()
    self.interactable = pygame.sprite.Group()
    for i, row in enumerate(tilemap):
      for j, value in enumerate(row):
        if value == '1':
          Wall(self, j, i)
        elif value == 'p':
          self.player = Player(self, j, i)
        elif value == '2':
          Interactable(self, j, i)
    """for x in range (15,30): #gyap
      Wall(self, x, 10) #gyap
    for x in range (20,25): #gyap
      Wall(self, 10, x) #gyap
    for thing in self.map.tmxdata.objects:
      if thing.name == 'player':
        self.player = Player(self, thing.x, thing.y)"""

    self.camera = Camera(diswidth, disheight) #gyap

  def newtwo(self):
    self.all_buttons = pygame.sprite.Group()
    pygame.display.flip()

  def run(self):
    self.game_over = False
    while not self.game_over:
      self.dt = self.clock.tick(60) / 1000
      self.rupdate()
      self.draw()
      self.events()
    pygame.quit()

  def runtwo(self):
    self.game_over = False
    while not self.game_over:
      self.dt = self.clock.tick(60) / 1000
      self.drawtwo()
    pygame.quit()

  def quit(self):
    sys.exit()

  def rupdate(self):
    self.all_sprites.update()
    self.camera.update(self.player)

  def grid(self):
    for y in range (0, disheight, tilesize):
      pygame.draw.line(self.dis, (black), (0, y), (diswidth, y))
    for x in range (0, diswidth, tilesize):
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

  def drawtwo(self):
    self.dis.fill(white)
    self.all_buttons.draw(self.dis)

  def draw(self):
    self.drawbg(white)
    self.grid()
    self.all_sprites.draw(self.dis)
    if self.displaytext == True:
      self.displaymytext()
    '''for sprit in self.all_sprites:
     self.dis.blit(sprit.image, self.camera.apply(sprit))'''
    #for x in list:
      #dis.blit()#find an efficient way to compare x as and integer to object position in a list
    pygame.display.flip()

  def displaymytext(self):
    self.dis.blit(cs.text, cs.textRect)
    pygame.display.update()

  def events(self):
    #while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.quit()
        if event.type == pygame.KEYDOWN:
            play_pos = (self.player.x, self.player.y, self.displaytext)
            if event.key == pygame.K_a:
              self.player.move(xchange = -block_speed)
              print (self.player.x)
            elif event.key == pygame.K_d:
              self.player.move(xchange = block_speed)
            elif event.key == pygame.K_w:
              self.player.move(ychange = -block_speed)
            elif event.key == pygame.K_s:
              self.player.move(ychange = block_speed)
            
        elif event.type == pygame.KEYUP:
          self.player.move()

  def textappear(self, string, colour, background):
    char = ''
    for i in range(len(string)):
      char += string[i]
      text = font.render(char, True, colour)
      textrect = text.get_rect(center = (200, 400))
      self.dis.blit(background, (0, 0)) #gyap
      self.dis.blit(text, textrect) #gyap
      pygame.display.update()
      pygame.time.wait(100)

  def text(self, string, font, colour, x, y):
    text = font.render(string, True, colour)
    textrect = text.get_rect(topleft = (x, y))
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
    #while True:
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
    #gamestart.newtwo()
    #gamestart.runtwo()
    #gamestart.mainmenu()
    gamestart.new()
    gamestart.run()

    pygame.display.update()
    gamestart.clock.tick(60)
main()
