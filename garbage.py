'''def startscreen(self):
  gameover = False
  while not gameover: 
    for i in range(0, cs.tiles):
      cs.dis.blit(cs.bg, (i*cs.bgwidth + cs.scroll, 0))

    cs.scroll -= 5

    if abs(cs.scroll) > cs.diswidth:
      scroll = 0

    for event in pygame.event.get():
         if event.type == QUIT:
             gameover = True

         elif event.type == pygame.MOUSEBUTTONDOWN:
            textappear(cs.string1, cs.black, cs.white)

    dis.blit(cs.truck, cs.truckrect) #gyap
    if event.type == cs.smokeappear:
      dis.blit(cs.smoke, cs.smokerect) #gyap

    clock.tick(60) #gyap
    pygame.display.update()'''

'''objs.NPC1.rect.move_ip(cs.xchange, cs.ychange)
cs.white1.blit(objs.NPC1.image, objs.NPC1.rect)
cs.white1.blit(objs.NPC2.image, objs.NPC2.rect)'''

'''class NPC(pygame.sprite.Sprite):
  def __init__(self, x, y, image):
    pygame.sprite.Sprite.__init__(self)
    self.image = image
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)

npcs = pygame.sprite.Group()
NPC1 = NPC(200, 375, pygame.image.load('introsprites/npc1.webp'))
NPC2 = NPC(300, 375, pygame.image.load('introsprites/npc2.png'))
npcs.add(NPC1)
npcs.add(NPC2)'''