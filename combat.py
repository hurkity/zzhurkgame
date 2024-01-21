import pygame
import random
from cons import *

pygame.init()

class Character(pygame.sprite.Sprite):
    def __init__(self, name, hp, power):
        #self.group = game.all_users
        #pygame.sprite.Sprite.__init__(self, self.group)
        self.name = name
        self.hp = hp #i think i need to add them all together and replace or something idk how to turn it into one from four objects
        self.power = power
    
    
class Team:
    def __init__(self):
        self.characters = []
        c1 = Character('s', 100, pow1)
        c2 = Character('as', 100, pow2)
        c3 = Character('f', 100, pow3)
        c4 = Character('w', 100, pow4)
        self.characters.append(c1)
        self.characters.append(c2)
        self.characters.append(c3)
        self.characters.append(c4)
        self.trust = {c1.name + ' ' + c2.name: trust[0], 
                      c1.name + ' ' + c3.name: trust[1],
                      c1.name + ' ' + c4.name: trust[2],
                      c2.name + ' ' + c3.name: trust[3],
                      c2.name + ' ' + c4.name: trust[4],
                      c3.name + ' ' + c4.name: trust[5]
                      }
        
    @property
    def hp(self):
        hp = 0
        for chars in self.characters:
            hp += chars.hp
        return hp
    
    def attack(self, c1, c2):
        print ("player: %i" % self.hp)
        print ("%s and %s attacking" %(c1.name, c2.name))
        trust = 0
        key = c1.name + ' ' + c2.name
        key2 = c2.name + ' ' + c1.name
        if key in self.trust:
            trust = self.trust[key]
        else:
            trust = self.trust[key2]
        damage = c1.power * c2.power * trust
        return damage

    def update(self, damage):
        eachdamage = damage/len(self.characters)
        for character in self.characters:
            character.hp -= eachdamage
            if character.hp <= 0:
                print ("game over")


class Computer(pygame.sprite.Sprite):
    def __init__(self, name, hp, power, escape):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.hp = hp
        self.power = power
        self.escape = escape

    def attack(self):
        print ("enemy: %i" % self.hp)
        print ("enemy attacking")
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