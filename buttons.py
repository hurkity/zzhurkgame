import pygame

class Button:
  def __init__(self, x, y, colour):
    self.x = x
    self.y = y
    self.width = 150
    self.height = 50
    self.colour = colour
    self.image = pygame.Surface([self.width, self.height])
    self.image.fill(self.colour)
    self.rect = self.image.get_rect(topleft = (self.x, self.y))

  def draw(self, surface):
    pygame.draw.rect(surface, self.colour, pygame.Rect(self.x, self.y, self.width, self.height))

  def hover(self, position):
    if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
      return True
  
  def invalid(self):
    x = pygame.image.load('graphics/x.png').convert_alpha()
    self.blit(x)