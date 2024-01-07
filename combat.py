import pygame
import random

pygame.init()

class UserTurnBased(pygame.sprite.Sprite):
    def __init__(self, game, name, hp, power):
        self.group = game.all_players
        pygame.sprite.Sprite.__init__(self, self.group)
        self.game = game
        self.name = name
        self.hp = hp #i think i need to add them all together and replace or something idk how to turn it into one from four objects
        self.power = power
    
    def attack(self, partner, trust):
        damage = self.power * partner.power * trust #trust on scale of 1-5 i think
        return damage
    
    #make a bunch of methods for animations for each pair
    def update(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            print ("Game Over") #make death screen + reset from save?
    

class TargetTurnBased(pygame.sprite.Sprite): #refers to computer
    def __init__(self, name, hp, power):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.hp = hp
        self.power = power

    def attack(self):
        damage = self.power
        return damage
    
    def skill(self):
        chosenskill = random.randint(1, 3)
        if chosenskill == 1:
            damage = self.power * 0.8
        elif chosenskill == 2:
            damage = self.power * 1.2
        elif chosenskill == 3:
            damage == self.power * 1.5
    
    def update(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            print ("You win!")