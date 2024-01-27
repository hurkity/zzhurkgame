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
objfont = pygame.font.Font('public-pixel-font/PublicPixel.ttf', 10)
font = pygame.font.Font('public-pixel-font/PublicPixel.ttf', 16)
font2 = pygame.font.Font('public-pixel-font/PublicPixel.ttf', 8)
font3 = pygame.font.Font('public-pixel-font/PublicPixel.ttf', 12)

text = font.render("'e' to interact with the object!", True, green, blue)
textSecondLine = font.render("'p' to pick up the object!", True, green, blue)
droptext = font.render("'g' to drop the object!", True, white)
pressetoclose = font2.render("press 'e' again to close", True, white)
entertocontinue= font2.render("press enter to continue", True, white)



Text = [  # font.render("bjdndkjnf", True, green),
        ["A rusty old key.", "Looks like it opens some large doors."],
        ["", "second object des2"],
        ["third object description"],
        ["fourth object description"],
        ["fifth object description"],
        ["sixth object description"]]

LockText = [  # font.render("bjdndkjnf", True, green),
        "first lock description",
        "second lock description",
        "third lock description"]
textRect = text.get_rect(center = (diswidth/2, disheight/10))
droptextRect = droptext.get_rect(center = (diswidth/2, disheight/10))
textSecondLineRect = text.get_rect(center = (diswidth/2, disheight/10 +
                                             textRect.height))
etocloserect = pressetoclose.get_rect(bottomright = (diswidth, disheight))
textRect3 = pressetoclose.get_rect(bottomright = (etocloserect.left - 20, etocloserect.bottom))

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
        'tuto.tmx',
        'hotel.tmx',
        'town.tmx',
        'forest.tmx'
]


playerhptotal = 400

name1 = "EMCY"
pow1 = 20

name2 = "AMY"
pow2 = 15

name3 = "EMILY"
pow3 = 25

name4 = "ADAM"
pow4 = 10

targname1 = "gart"
targpow1 = 80
targhp1 = 2000

enemies = [
    {"name": "gart", "hp": 2000, "pow": 100, "map": 0, "x": 900, "y": 900, "pic": "graphics/cookiemonster.png"},
    {"name": "gart", "hp": 2000, "pow": 100, "map": 0, "x": 1250, "y": 280, "pic": "graphics/monster.png"},
    {"name": "gart", "hp": 2000, "pow": 100, "map": 3, "x": 850, "y": 130, "pic": "graphics/cookiemonster.png"},
    {"name": "gart", "hp": 2000, "pow": 100, "map": 3, "x": 124, "y": 340, "pic": "graphics/cookiemonster.png"}


]


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


#act 1

bigtext1 = ["EMILY: Ohhh my goodness… My entire body hurts…",
"ADAM: Right?",
"ADAM: How did people back in the day handle these car rides?",
"EMCY: Hey AcadAmy, is this the right place?",
"AMY: According to my calculations, we've reached our",
"AMY: destination.",
"AMY: ...Although, I may not be the most accurate GPS.",
"AMY: I really hope we weren’t misled…",
"ADAM: We’d better not have been!!!",
"ADAM: IF ALL THAT WAS TO END UP AT THE WRONG PLACE",
"ADAM: I'M GONNA- ",
"EMCY: I’m sick of your voice.",
"EMILY: Yeah Adumb, we’re the ones who suffered.",
"AMY: Quit arguing everyone!",
"AMY: Let’s head inside already.",
"AMY: Looks like the reception is just through the front door."]

instructions1 = ["INSTRUCTIONS:",
"Welcome to BOAR-DOM!",
"Press W, A, S, D to control your movement."]

instructions2 = ["Now try interacting with this x using the E key!",
"E will be your key for interacting with everything."]

instructions3 = ["Press M to see the menu screen."]

instructions4 = ["That's about it! It's a simple game.",
"Head DOWN over to the hotel now."]

instructions5 = ["ADAM: Alright, let’s go have some fun!",
"AMY: Wait wait wait no.",
"They forgot to give us our hotel room key???",
"Are you kidding me?!?!",
"EMILY: That totally sucks. I guess let’s go look for it?"]

instructions6 = ["NARRATOR: Oops! I completely forgot to give you the key.",
"I left it on the top right of the map, go ahead and take it."]

instructions7 = ["NARRATOR: Perfect, you found the key!",
"Now, head on over to the hotel on the TOP of the map."]

hotel1 = ["ADAM: Wow. This place is GORGEOUS!",
"EMCY: You're just completely lying Adumb.",
"There are cobwebs EVERYWHERE!",
"EMILY: Yeah…",
"I can feel spiders creeping up my body already… eugh.",
"AMY: C'mon, let’s go talk to the receptionist."]

hotel2 = ["RECEPTIONIST: Hello, how can I help you?",
"2: Hi, we’d like to check in.",
"RECEPTIONIST: Alright, just give me one moment.",
"... tap tap tap…",
"It’s been a long time since we’ve had new visitors...",
"...but we’re happy to have you guys!",
"Especially since… well…",
"In any case, welcome to BOAR-DOM!",
"I’ll have your bags and all moved up to your rooms.",
"So feel free to spend some time exploring the town.", 
"If you head UP and RIGHT, you'll find the door."]

cutscene1 = ["TOUR GUIDE: “Well, here we are!",
"ALL: ...",
"TOUR GUIDE: ...",
"TOUR GUIDE: Well…",
"If you have any questions, let me know."]

louisedia = ["LOUISE: Ahh.. young ones…",
"LOUISE: You’re new here.",
"LOUISE: It’s been a while since I’ve seen anyone",
"born after the Chilly War.",
"ADAM: ..??? Chilly War???",
"LOUISE: Kids nowadays.",
"LOUISE: I’ve lost my cat, Mittens.",
"LOUISE: It would mean so much",
"if you could help me find her…",
"My legs just aren't what they used to be…",
"ADAM: Of course we can help you! It’s just that-",
"LOUISE: Never mind..",
"I wouldn’t want to bother you children…",
"Go on, have some fun."]

evangelinedia = ["EVANGELINE: “Hello!!!",
"EVANGELINE: “Oh.. you’re wondering what I do?",
"EVANGELINE: Well..",
"Recently I’ve been working on an experiment",
"which involves genetically modifying creatures,",
"causing them to mutate rather oddly...",
"I don’t want to bore you though.",
"AMY: Wow… that’s so interesting.",
"AMY: I really aspire to be like you in the future!",
"EVANGELINE: Really? Well… I appreciate the sentiment."
"EVANGELINE: “You all should run off now, and..",
"be careful around these parts."]

ivydia = ["IVY: Oh, hey kids! Are you guys new here?",
"EMILY: Mhm!",
"Do you know anything interesting about BOAR-DOM?",
"IVY: Hmmm.. let’s see.",
"IVY: Well, there’s been a lot of tension",
"between us neighbours lately.",
"IVY: I personally have been hurt by",
"how my PLANTS are being TRAMPLED!",
"EMILY: THAT’S TERRIBLE!",
"I’d be so sad if that happened to my plants…",
"IVY: I’m a crop vendor",
"and every night for the last few weeks,",
"IVY: my crops have gotten absolutely destroyed.",
"IVY: I’m losing so much… it’s such a shame really.",
"IVY: But while you’re here",
"don’t concern yourself with my problems!",
"Try to enjoy yourselves",
"Even though there’s absolutely nothing to do..."]

jorhnydia = ["JORHNY: I’m so exhausted…",
"JORHNY: Oh. Kids.",
"I’m sure you guys have a lot of fun. And money.",
"JORHNY: Anyways. How can I help you guys?",
"EMCY: We’re just exploring the town, we just got here.",
"EMCY: Anything interesting going on?",
"JORHNY: “I wish. BOAR-DOM is boaring as FLEEP.",
"JORHNY: And broke too.",
"I’ve been working hard to move out but being a florist,",
"Let’s just say I don’t make a dime,"
"at least compared to Ekon Mulch."
"EMCY: ... Ekon Mulch??",
"JORHNY: WOW.",
"YOU’VE NEVER HEARD OF THE MAN HIMSELF,",
"EKON MULCH?!?!?!",
"He’s my hero; he’s rich, and smart",
"and… I wish I could be him.",
"JORHNY: Anyhoo, I’m gonna get back to work now.",
"You kids have fun… while you can…"]

cutscene2 = ["EMILY: This really sucks…",
"Everyone hates each other here!",
"AMY: Yeah..",
"It's quite upsetting to see such a divided community.",
"Maybe there’s something we can do to help out?",
"ADAM: DEFINITELY! IT'S HORRIBLE!!!"]

prequest = ["NARRATOR: Here's something you can do.",
"How about you chat with Louise?"]

louise2 = ["ADAM: LOUISEEE WE'RE BACKKK",
"LOUISE: Hello Adam.. What brings you back here?",
"EMILY: WE WANT TO HELP YOU!",
"EMILY: Hearing about your cats made me so sad..",
"LOUISE: I appreciate it children.",
"LOUISE: If you insist on helping me,",
"The forest is where MITTENS is most likely to be."]

quest1 = ["QUEST added: Find Louise’s Cat!"]

#act 2

forest1 = ["ADAM: Huff… Huff… Are you… puff… kidding me?",
"How far do we… need to run?",
"EMILY: STOP WHINING! If you’re weak just say so!",
"EMCY: Cut it out Emoly,",
"maybe Mittens is hiding deeper in the forest?",
"EMCY: We’ve gotta be careful though, it seems dangerous there.",
"AMY: o..ohhh… do we really need to go in there?",
"EMILY: Don’t be afraid AcadAmy! :D",
"I’ll be right with you the WHOLE time!",
"AMY: ... Okay, let's go."]

forest2 = ["AMY: ... this is so odd.",
"EMILY: I’m starting to get really freaked out..",
"can we leave?",
"ADAM: GUUUYYYSSSSS. We can’t give up!",
"ADAM: This is for a sweet elderly lady, c’mon!",
"EMCY: Adumb is right. Let’s take the bowl and keep going.",
"EMCY: Maybe if we follow these PATHS,"
"it’ll lead us to Mittens."]

cutscene3 = ["EMCY: Jorhny? Is that you?",
"JORHNY: KITTY!!!!! KITTY KITTY?!?!",
"JORHNY: OH, hey kids!",
"JORHNY: You startled me…",
"What are you doing out here?",
"EMCY: We’re looking for a cat named Mittens.",
"EMCY: She belongs to Louise, one of your neighbours."
"JORHNY: “What a coincidence!",
"JORHNY: I’m looking for a cat as well,",
"Though I don’t know her name.",
"JORHNY: ...",
"EMCY: ...",
"EMILY: ...",
"ADAM: ...",
"ADAM: Is she a nice kitty?",
"AMY: ARE YOU GUYS ACTUALLY DUMB???",
"AMY: The obvious conclusion",
"is that they are the same cat!",
"AMY: How many cats in this town could possibly go",
"missing at once??",
"AMY: There’s only so many people living here."
"JORHNY: I’d never really thought of that.",
"I’ve been feeding this cat for months thinking",
"it was a stray since she LOVED to run out to the forest.",
"No wonder Louise gives me a dirty look when we meet.",
"JORHNY: Does she think I’m trying to steal her cat?",
"EMCY: Jorhny, that is pretty odd.",
"EMCY: If I were her, I’d be pretty freaked out too.",
"EMILY: Yeah…",
"Don’t you feel kinda weird doing that Jorhny?",
"ADAM: Even I wouldn’t stoop that low,",
"feeding a cat you don’t even know JORHNY?",
"JORHNY: Well I can’t help it, she was so cute!",
"Well, since we’re looking for the same cat,",
"let’s search together, yes?"]

party = ["JORHNY HAS JOINED YOUR PARTY."]

#act 3
forest3 = ["...: MEOW!",
"JORHNY: You guys heard that right?",
"EMILY: MITTENS??? MITTTEEEENNNNNSSSS?!?!?",
"ADAM: MITTENS!!!!!",
"WE’RE COMING FOR YOUUUUU!!!!!!",
"AMY: Stop yelling! You’re gonna scare her."]
#mittens blit


forest4 = ["EMCY: I guess there wasn’t any need to worry after all.",
"JORHNY: Oh great heavens! Let’s head home Mittens.",
"??: GRAAHHAGGHGH",
"ALL: ?!?!?!",
"ADAM: That doesn’t sound good, does it…",
"EMILY: THAT SO DOES NOT SOUND GOOD!",
"AMY: Jorhny.. you should stay here.",
"EMCY: Let’s see what it is before panicking…",
"NARRATOR: Head to the right"]

postfight = ["ADAM: What was that…?",
"EMCY: This town gets odder and odder.",
"EMILY: I am DEEPLY AFRAID!",
"AMY: Stop that, Emoly.",
"EMILY: Sorry.",
"ADAM: Are we just glazing over what just happened",
"like it’s normal?",
"EMCY: Yeah, well….",
"Let’s go back and find Louise, I guess…"
]

town = ["IVY: Look what you’ve done, old lady!",
"Your cats have run all over my crops! Again!",
"LOUISE: Mittens would do no such thing… ",
"if she’s even still here, that is!",
#(Sees players)
"OH! MITTENS! Thank you so much!",
"IVY: Ugh, that’s that, I guess.",
"Just make sure you keep",
"a better watch on your cats, Louise.",
"LOUISE: I’m telling you,",
"Mittens would do no such thing…"
"IVY: Whatever, whatever.",
"Say, EMCY, could you go get me my shovel?",
"I need to take out all the dead plants in my field"]
#quest added: find Ivy’s shovel!

shovel = ["EMCY: Here’s your shovel, Ivy.",
"IVY: Oh, hey Emcy! Thanks, man."]

finalfight = ["ADAM: Oh, everyone’s here. What’s happening?",
"Are we having an outdoor party?",
"Wait, can parties be outdoor, or are those all barbecues…",
"what’s the overlap here….",
"LOUISE: Hmph. Personally, I’m not too concerned,",
"but apparently Evangeline has something she wants to tell us.",
"EVANGELINE: YES! SOMETHING SUPER URGENT!",
"The sensors in my lab just went off, which means…",
"things are about to get real bad!",
"JORHNY: Wait, what!? What do you mean, Evangeline?",
"EVANGELINE: Ugh, JORHNY,",
"That means that my mutations have",
"TOTALLY hypermutated",
"and are really dangerous right now!",
"EVANGELINE: ...",
"And, um, they’re also in your field.",
"JORHNY: WHAT!? I — I mean.",
"Totally cool, Evangeline, ahaha.",
"Nothing a guy like me can’t handle, eheheh.",
"AMY: Why are you acting like that? Stop that at once.",
"IVY: Okay, what say we all go over to the field and…",
"The new kids can try to fight it off?",
"LOUISE: Mittens likes this!",
"JORHNY: Oh, yeah.. you coming with, Evangeline?",
"EVANGELINE: What would this town do without me?"]

#final act
ending1 = ["NARRATOR: and so… they resolved the issue.",
"The kids were finally free to enjoy their vacation,",
"and Evangeline also came to some very important conclusions",
"First, her mutations had held Mittens hostage in the forest,",
"Second, they were the ones tearing up Ivy’s crops and eating them,",
"and that third,",
"the vegetable seeds were spread in Jorhny’s flowers",
"due to the creatures… well… defecating in the fields."]

ending2 = ["And why were the creatures so insistent on",
"doing it in Jorhny’s fields?",
"Well, they were attracted to the flower fields",
"because they were made of flowers!",
"Due to the qualities of the pollen of the flowers that Jorhny,"
"had left in Evangeline’s lab,",
"her experiment had gotten a lot more lively… literally!"]

ending3 = ["Well, when the residents of Boardom",
"cleared up their misunderstandings,",
"everyone hugged and made up.",
"Except for Mittens, who went immediately to taunt her previous captors.",
"The sludge was definitely not happy about that."]

cutscenes = [{'x': 827,
                'y': 879,
                'movement': ['bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd'],
                'index': 0,
                'map': 0,
                'text': bigtext1,
               'colour': white,
                'done': False},
                {'x': 827,
                'y': 779,
                'movement': ['left', 'left', 'left', 'left', 'left', None, None, None, 'fwd', 'fwd', 'fwd', 'fwd', 'fwd', None, None, None, 'right', 'right', 'right', 'right', 'right', None, None, None, 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', None, None, None],
                'index': 1,
                'map': 0,
                'text': instructions1,
               'colour': yellow,
                'done': False},
                {'x': 827,
                'y': 679,
                'movement': [None],
                'index': 2,
                'map': 0,
                'text': instructions2,
               'colour': yellow,
                'done': False},
                {'x': 827,
                'y': 579,
                'movement': [None],
                'index': 3,
                'map': 0,
                'text': instructions3,
               'colour': yellow,
                'done': False},
                {'x': 827,
                'y': 529,
                'movement': ['left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', None, None, None, 'fwd', 'fwd', 'fwd', 'fwd', 'fwd', None, None, None, 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', None, None, None, 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', None, None, None],
                'index': 4,
                'map': 0,
                'text': instructions4,
               'colour': yellow,
                'done': False},
                {'x': 827,
                'y': 479,
                'movement': ['bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd'],
                'index': 5,
                'map': 0,
                'text': instructions5,
               'colour': white,
                'done': False},
                {'x': 827,
                'y': 429,
                'movement': [None],
                'index': 6,
                'map': 0,
                'text': instructions6,
               'colour': yellow,
                'done': False},
                {'x': 0,
                'y': 0,
                'movement': [None],
                'index': 7,
                'map': 0,
                'text': instructions7,
               'colour': yellow,
                'done': False},
                {'x': 980,
               'y': 700, 
               'movement': ['right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd'],
               'index': 8,
               'map': 1,
               'text': hotel1,
               'colour': white,
               'done': False}, 
               {'x': 1100, 
                'y': 700, 
                'movement': [None],
                'index': 9,
                'map': 1,
                'text': hotel2,
               'colour': white,
                'done': False},
                {'x': 948,
                'y': 1060,
                'movement': ['bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd'],
                'index': 10,
                'map': 2,
                'text': None,
               'colour': white,
                'done': False},
                {'x': 948,
                'y': 920,
                'movement': [None],
                'index': 11,
                'map': 2,
                'text': cutscene1,
               'colour': white,
                'done': False},
                {'x': 948,
                'y': 860,
                'movement': ['right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'up', 'up', 'up', 'up', 'up', 'up', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right'],
                'index': 12,
                'map': 2,
                'text': None,
               'colour': white,
                'done': False},
                {'x': 1080,
                'y': 860,
                'movement': [],
                'index': 13,
                'map': 2,
                'text': louisedia,
               'colour': white,
                'done': False},
                {'x': 500,
                'y': 850,
                'movement': ['left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd'],
                'index': 14,
                'map': 2,
                'text': None,
               'colour': white,
                'done': False},
                {'x': 230,
                'y': 830,
                'movement': [],
                'index': 15,
                'map': 2,
                'text': jorhnydia,
               'colour': white,
                'done': False},
                {'x': 550,
                'y': 550,
                'movement': ['left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd','bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left', 'left'],
                'index': 16,
                'map': 2,
                'text': None,
               'colour': white,
                'done': False},
                {'x': 440,
                'y': 360,
                'movement': [None],
                'index': 17,
                'map': 2,
                'text': evangelinedia,
               'colour': white,
                'done': False},
                {'x': 1100, #change
                'y': 400, #change
                'movement': [None],
                'index': 18,
                'map': 2,
                'text': ivydia,
               'colour': white,
                'done': False},
                {'x': 500, 
                'y': 700, 
                'movement': ['fwd', 'fwd', 'fwd', 'fwd', 'fwd', 'fwd', 'fwd'],
                'index': 19,
                'map': 2,
                'text': cutscene2,
               'colour': white,
                'done': False},
                {'x': 500, 
                'y': 800, 
                'movement': [None],
                'index': 20,
                'map': 2,
                'text': prequest,
               'colour': yellow,
                'done': False},
                {'x': 1080, 
                'y': 860, 
                'movement': ['bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd', 'bwd'],
                'index': 21,
                'map': 2,
                'text': louise2,
               'colour': white,
                'done': False},
                {'x': 1080, 
                'y': 900, 
                'movement': [None],
                'index': 22,
                'map': 2,
                'text': quest1,
               'colour': yellow,
                'done': False},
                {'x': 180, 
                'y': 800, 
                'movement': [None],
                'index': 23,
                'map': 3,
                'text': forest1,
               'colour': white,
                'done': False},
                {'x': 520, 
                'y': 320, 
                'movement': ['right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'up', 'up', 'up', 'up', 'up', 'up', 'up', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right',],
                'index': 24,
                'map': 3,
                'text': forest2,
               'colour': white,
                'done': False},
                {'x': 420, 
                'y': 320, 
                'movement': ['right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right'],
                'index': 25,
                'map': 3,
                'text': None,
               'colour': white,
                'done': False},
                {'x': 520, 
                'y': 320, 
                'movement': [],
                'index': 26,
                'map': 3,
                'text': cutscene3,
               'colour': white,
                'done': False}, 
                {'x': 520, 
                'y': 320, 
                'movement': [],
                'index': 27,
                'map': 3,
                'text': party,
               'colour': yellow,
                'done': False},
                {'x': 1220, 
                'y': 560, 
                'movement': ['fwd', 'fwd', 'fwd', 'fwd', 'fwd', 'fwd', 'fwd', 'fwd', 'fwd', 'fwd'],
                'index': 28,
                'map': 3,
                'text': forest3,
               'colour': white,
                'done': False},
]
