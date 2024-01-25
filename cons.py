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
player_speed2 = 100


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
combattextlose = ["You lose..."]

testtext = ["shblawg", "asdasd"]
cutscenetest = ['left', 'left', 'left', 'right', 'right', 'right', 'right', 'right']
cutscenes = [{'x': 500, 'y': 600, 'movement': ['left', 'left', 'left', 'right', 'right', 'right', 'right', 'right']}]

#act 1

bigtext1 = ["EMILY: Ohhh my goodness… My entire body hurts…", 
"ADAM: Right?",
"ADAM: How did people back in the day handle these car rides?", 
"EMCY: Hey 2, is this the right place?", 
"AMY: According to my calculations, we've reached at our", 
"AMY: destination.",
"AMY: ...Although, I may not be the most accurate GPS.", 
"AMY: I really hope we weren’t misled…", 
"ADAM: We’d better not have been!!!", 
"ADAM: IF I WENT THROUGH THAT JUST FOR IT TO BE THE WRONG PLACE", 
"ADAM: I'M GONNA- ",
"EMCY: I’m sick of your voice.", 
"EMILY: Yeah 4, we’re the ones who suffered.", 
"AMY: Quit arguing everyone!",
"AMY: Let’s head inside already.", 
"AMY: Looks like the reception is just through the front door."]

instructions1 = ["INSTRUCTIONS:",
"Welcome to x! Press W, A, S, D to control your movement."]

instructions2 = ["Now try interacting with this x using the E key!", 
"E will be your key for interacting with everything."]

instructions3 = ["That's about it! It's a simple game.",
"Head on over to the hotel now."]

instructions4 = ["4: Alright, let’s go have some fun!", 
"2: Wait wait wait no.", 
"They forgot to give us our hotel room key???", 
"Are you kidding me?!?!", 
"3: That totally sucks. I guess let’s go look for it?", 
"NARRATOR: Oops! I completely forgot to give you the key.", 
"I left it down the hall, so go ahead and pick it up."]

instructions5 = ["Perfect, you found the key!", 
"Now, head on over to the hotel."]

hotel1 = ["4: Wow. This place is GORGEOUS!", 
"1: You’re being way too generous. There are cobwebs EVERYWHERE!", 
"3: Yeah… I can feel spiders creeping up my body already… eugh.", 
"2: Insightful commentary, now let’s go talk to the receptionist."]

hotel2 = ["RECEPTIONIST: Hello, how can I help you?",
"2: Hi, we’d like to check in.", 
"RECEPTIONIST: Alright, just give me one moment.", 
"... tap tap tap…", 
"It’s been a long time since we’ve had new visitors...", 
"...but we’re happy to have you guys! Especially since… well…", 
"In any case, welcome to x!", 
"I’ll have your bags and all moved up to your rooms.", 
"So feel free to spend some time exploring the town."]

cutscene1 = ["TOUR GUIDE: “Well, here we are! Welcome to x!", 
"1+2+3+4: ...", 
"TOUR GUIDE: ...", 
"TOUR GUIDE: Well… If you have any questions, let me know."]

louisedia = ["LOUISE: Ahh.. young ones…", 
"LOUISE: You’re new here.", 
"LOUISE: It’s been a while since I’ve seen anyone", 
"born after the Chilly War.", 
"4: ..??? Chilly War???", 
"LOUISE: Kids nowadays.", 
"LOUISE: I’ve lost my cat, Mittens.", 
"LOUISE: It would mean so much if you could help me find her…", 
"LOUISE: My legs just aren't what they used to be…", 
"4: Of course we can help you! It’s just that-", 
"LOUISE: Never mind.. I wouldn’t want to bother you children…", 
"Go on, have some fun."]

evangelinedia = ["EVANGELINE: “Hello!!!", 
"EVANGELINE: “Oh.. you’re wondering what I do?", 
"EVANGELINE: Well.. recently I’ve been working on an experiment", 
"which involves genetically modifying a series of creatures,", 
"causing them to mutate rather oddly...", 
"I don’t want to bore you though.", 
"2: Wow… that’s so interesting.",
"2: I really aspire to be like you in the future!",
"EVANGELINE: Really? Well… I appreciate the sentiment."
"EVANGELINE: “You all should run off now, and..", 
"be careful around these parts."]

ivydia = ["IVY: Oh, hey kids! Are you guys new here?", 
"EMILY: Mhm! Do you know anything interesting about BOAR-DOM?", 
"IVY: Hmmm.. let’s see.", 
"IVY: Well, there’s been a lot of tension between us neighbours lately.", 
"IVY: I personally have been hurt by how my PLANTS are being TRAMPLED!", 
"EMILY: THAT’S TERRIBLE! I’d be so sad if that happened to my plants…", 
"IVY: I’m a crop vendor, and every night for the last few weeks,", 
"IVY: my crops have gotten absolutely destroyed.", 
"IVY: I’m losing so much… it’s such a shame really.", 
"IVY: But while you’re here, don’t concern yourself with my problems!", 
"Try to enjoy yourselves, even though there’s absolutely nothing to do..."]

jorhnydia = ["JORHNY: I’m so exhausted…", 
"JORHNY: Oh. Kids. I’m sure you guys have a lot of fun. And money.", 
"JORHNY: Anyways. How can I help you guys?", 
"EMCY: We’re just exploring the town, we just got here.", 
"EMCY: Anything interesting going on?", 
"JORHNY: “I wish. BOAR-DOM is boaring as FLEEP. And broke too.",  
"I’ve been working hard to move out but being a florist,", 
"let’s just say I don’t make a dime compared to Ekon Mulch."
"EMCY: ... Ekon Mulch??", 
"JORHNY: WOW.",
"YOU’VE NEVER HEARD OF THE MAN HIMSELF, EKON MULCH?!?!?!", 
"He’s my hero; he’s rich, and smart, and… I wish I could be him.", 
"JORHNY: Anyhoo, I’m gonna get back to work now.", 
"You kids have fun… while you can…"]

cutscene2 = ["EMILY: This really sucks… everyone hates each other here!", 
"AMY: Yeah.. it's quite upsetting to see such a divided community.", 
"Maybe there’s something we can do to help out?"
"ADAM: DEFINITELY! IT'S HORRIBLE!!!"
"EMCY: Alright then, let’s start with Louise then.", 
"She seemed so upset.", 
"NARRATOR: QUEST added: Find Louise’s Cat!"]

#act 2

forest1 = ["ADAM: Huff… Huff… Are you… puff… kidding me?", 
"How far do we… need to run?", 
"EMILY: STOP WHINING! If you’re weak just say so!", 
"EMCY: ANYWAYS… Maybe Mittens is hiding somewhere in the forest?", 
"EMCY: We’ve gotta be careful though, it seems dangerous there.", 
"AMY: o..ohhh… do we really need to go in there?", 
"EMILY: Don’t be afraid! :D", 
"I’ll be right with you the WHOLE time, you can always count on me!", 
"AMY: ... Okay, let's go."]

forest2 = ["AMY: ... this is so odd.", 
"EMILY: I’m starting to get really freaked out.. can we leave?", 
"ADAM: GUUUYYYSSSSS. We can’t give up!", 
"ADAM: This is for a sweet elderly lady, c’mon!", 
"EMCY: He’s right. Let’s take the bowl and keep going.", 
"EMCY: Maybe if we follow these FOOTPRINTS, it’ll lead us to Mittens."]

cutscene3 = ["EMCY: Jorhny? Is that you?", 
"JORHNY: KITTY!!!!! KITTY KITTY?!?!", 
"JORHNY: OH, hey kids!", 
"JORHNY: You startled me… what are you doing out here?", 
"EMCY: We’re looking for a cat named Mittens.", 
"EMCY: She belongs to Louise, one of your neighbours."
"JORHNY: “What a coincidence!", 
"JORHNY: I’m looking for a cat as well, though I don’t know her name.", 
"JORHNY: ...", 
"EMCY: ...", 
"EMILY: ...", 
"ADAM: ...", 
"ADAM: Is she a nice kitty?", 
"AMY: ARE YOU GUYS ACTUALLY DUMB????", 
"AMY: The obvious conclusion is that they are the same cat!", 
"AMY: How many cats in this town could possibly go", 
"missing at once??", 
"AMY: There’s only so many people living here."
"JORHNY: I’d never really thought of that.", 
"JORHNY: I’ve been feeding this cat for months thinking", 
"it was a stray since she LOVED to run out to the forest.",
"JORHNY: No wonder Louise gives me a dirty look when we meet.", 
"JORHNY: Does she think I’m trying to steal her cat?", 
"EMCY: Jorhny, that is pretty odd.", 
"EMCY: If I were her, I’d be pretty freaked out too.",
"EMILY: Yeah… don’t you feel kinda weird doing that Jorhny?", 
"ADAM: Even I wouldn’t stoop that low,",
"feeding a cat you don’t even know JORHNY?",
"JORHNY: Well I can’t help it, she was so cute!", 
"Well, since we’re looking for the same cat,",
"let’s search together, yes?"]

#act 3

