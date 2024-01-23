import pygame
import math

pygame.init()
pygame.font.init()
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

x1 = -175
y1 = 100
colour1 = white

x2 = -75
y2 = 175
colour2 = white

x3 = 25
y3 = 100
colour3 = white

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
dis = pygame.display.set_mode((diswidth, disheight))
bg = pygame.image.load('graphics/background.jpg').convert_alpha()
bg = pygame.transform.scale(bg, (499, 499))
bgwidth = bg.get_width()
white1 = pygame.image.load('graphics/white.jpg').convert_alpha()
truck = pygame.image.load('graphics/unnamed.jpg').convert_alpha()
truck = pygame.transform.scale(truck, (50, 50))
smoke = pygame.image.load('graphics/painter.jpg').convert_alpha()
smoke = pygame.transform.scale(smoke, (15, 15))

truckrect = truck.get_rect(center = (250, 400))
smokerect = smoke.get_rect(center = (235, 420))
scroll = 0
tiles = math.ceil(diswidth/bgwidth) + 1 #should be 2 (round up)
smokeappear, t = pygame.USEREVENT+1, 3000
pygame.time.set_timer(smokeappear, t)

string4 = "woahh oh woahh"
objfont = pygame.font.Font('public-pixel-font/PublicPixel.ttf', 16)
font = pygame.font.Font('public-pixel-font/PublicPixel.ttf', 16)
font2 = pygame.font.Font('public-pixel-font/PublicPixel.ttf', 8)
font3 = pygame.font.Font('public-pixel-font/PublicPixel.ttf', 12)

text = font.render("'e' to interact with the object!", True, green, blue)
textSecondLine = font.render("'p' to pick up the object!", True, green, blue)
text2 = font2.render("press 'e' again to close", True, white)
text3= font2.render("press enter to continue", True, white)



Text = [  # font.render("bjdndkjnf", True, green),
        ["first object description", "first object des2", "first object des3"],
        ["second object description", "second object des2"],
        ["third object description"]]

LockText = [  # font.render("bjdndkjnf", True, green),
        "first lock description",
        "second lock description",
        "third lock description"]
textRect = text.get_rect(center = (diswidth/2, disheight/10))
textSecondLineRect = text.get_rect(center = (diswidth/2, disheight/10 +
                                             textRect.height))
textRect2 = text2.get_rect(bottomright = (diswidth, disheight))
textRect3 = text2.get_rect(bottomright = (textRect2.left - 20, textRect2.bottom))

#textRect1 = text1.get_rect()

#textRect1.center = (250, 400)

#part2
tilesize = 16
gridwidth = int(diswidth/tilesize)
gridheight = int(disheight/tilesize)

block_speed = 1
player_speed = 250


mapchange = [
        'bettertestmap.tmx',
        'betterbettertestmap.tmx',
        'bettertestmap3.tmx'
]


playerhptotal = 400

name1 = "name"
pow1 = 20

name2 = "err"
pow2 = 15

name3 = "ooh"
pow3 = 25

name4 = "aah"
pow4 = 10

targname = "gart"
targpow = 80
targhp = 20000

targhpcopy = 20000
trust = [5, 7, 8, 8, 5, 7]

fontbold = pygame.font.SysFont('public-pixel-font/PublicPixel.ttf', 25, bold = True)

stringlist = ["blah blah", "blah"]
combattext1 = ["You've been ambushed!", "What would you like to do?"]
escapetext = ["You ran away..."]
escapetext2 = ["You can't run!"]
combattext2 = ["Choose your first character: "]
combattext3 = ["Choose your second character: "]

testtext = ["shblawg"]

bigtext1 = ["3: Ohhh my goodness… My entire body hurts…", 
"4: Right?",
"4: How did people back in the day handle these car rides?", 
"1: Hey 2, is this the right place?", 
"2: According to my calculations, we've reached at our", 
"2: destination.",
"2: ...Although, I may not be the most accurate GPS.", 
"2: I really hope we weren’t misled…", 
"4: We’d better not have been!!!", 
"4: IF I WENT THROUGH THAT JUST FOR IT TO BE THE WRONG PLACE", 
"4: I'M GONNA- ",
"1: I’m sick of your voice.", 
"3: Yeah 4, we’re the ones who suffered.", 
"2: Quit arguing everyone!",
"2: Let’s head inside already.", 
"2: Looks like the reception is just through the front door."]

instructions1 = ["INSTRUCTIONS:",
"Welcome to x! Press W, A, S, D to control your movement."]

instructions2 = ["Good, now try interacting with this x using the E key!", 
"E will be your key for interacting with everything."]

instructions3 = ["That's about it! It's a simple game.",
"Head on over to the hotel now."]

instructions4 = ["4: Alright, let’s go have some fun!", 
"2: Wait wait wait no.", 
"They forgot to give us our hotel room key???", 
"Are you kidding me?!?!", 
"3: That totally sucks. I guess let’s go look for it?", 
"NARRATOR: Oops haha! I completely forgot to give you the key.", 
"Well, I left it down the hall, so go ahead and pick it up as your first quest."]

instructions5 = ["Perfect, you found the key! Now, head on over to the hotel."]

hotel1 = ["4: Wow. This place is GORGEOUS!", 
"1: You’re being way too generous. There are cobwebs EVERYWHERE!", 
"3: Yeah… I can feel the spiders creeping up my body already… eugh.", 
"2: Insightful commentary, now let’s go talk to the receptionist."]

hotel2 = ["RECEPTIONIST: Hello, how can I help you?",
"2: Hi, we’d like to check in.", 
"RECEPTIONIST: Alright, just give me one moment.", 
"... tap tap tap…", 
"It’s been a long time since we’ve had new visitors...", 
"...but we’re happy to have you guys! Especially since… well…", 
"In any case, welcome to x!", 
"I’ll have your bags and all moved up to your rooms when they’re ready.", 
"So feel free to spend some time exploring the town."]

