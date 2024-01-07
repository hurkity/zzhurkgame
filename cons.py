import pygame


pygame.init()
black = (0, 0, 0)
blue = (0, 0, 128)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)
orange = (255, 128, 0)
pink = (255, 192, 203)
light_blue = (173, 216, 230)
dark_blue = (0, 0, 139)
light_green = (144, 238, 144)
dark_green = (0, 100, 0)
grey = (127, 127, 127)
translucent_black = (0, 0, 0, 128)

floor_layer = 0
object_layer = 1
player_layer = 2

playerhitrect = pygame.Rect(0, 0, 15, 15)

text1 = "Start"
text2 = "Settings"
text3 = "Quit"

width = 150
height = 50

x1 = 100
y1 = 300
colour1 = yellow

x2 = 350
y2 = 300
colour2 = green

x3 = 600
y3 = 300
colour3 = orange

#font = pygame.font.SysFont("comicsans", 35)

string1 = "NEW GAME"
string2 = "CONTINUE"
string3 = "SETTINGS"

newgametext = "New Game raaahhh"
conttext = "Imagine you are in your previous game haha"
settingstext = "Switch up your settings!"


#part1
diswidth = 500
disheight = 500


'''bg = pygame.image.load('graphics/background.jpg').convert_alpha()
bg = pygame.transform.scale(bg, (1023, 768))
bgwidth = bg.get_width()
white1 = pygame.image.load('graphics/white.jpg').convert_alpha()
truck = pygame.image.load('graphics/unnamed.jpg').convert_alpha()
truck = pygame.transform.scale(truck, (100, 100))
smoke = pygame.image.load('graphics/painter.jpg').convert_alpha()
smoke = pygame.transform.scale(smoke, (25, 25))

truckrect = truck.get_rect(center = (400, 375))
smokerect = smoke.get_rect(center = (325, 420))
scroll = 0
tiles = math.ceil(diswidth/bgwidth) + 1 #should be 2 (round up)
smokeappear, t = pygame.USEREVENT+1, 3000
pygame.time.set_timer(smokeappear, t)'''

string4 = "woahh oh woahh"
objfont = pygame.font.Font('public-pixel-font/PublicPixel.ttf', 16)
font = pygame.font.Font('public-pixel-font/PublicPixel.ttf', 16)
text = font.render("'e' to interact with the object!", True, green, blue)
Text = [  # font.render("bjdndkjnf", True, green),
        "first object description",
        "second object description",
        "third object description"]
textRect = text.get_rect(center = (diswidth/2, disheight/10))
#textRect1 = text1.get_rect()

#textRect1.center = (250, 400)

#part2
tilesize = 16
gridwidth = int(diswidth/tilesize)
gridheight = int(disheight/tilesize)

block_speed = 1
player_speed = 300


mapchange = [
        'bettertestmap.tmx',
        'betterbettertestmap.tmx'
]
