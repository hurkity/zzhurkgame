
class ActManager:
    def __init__(self, game):

class Act:
    def __init__(self, game):
        self.dialogue = [[]]
    def draw(self):
class ActOne(Act):
    def __init__(self, game):
        self.dialogue = [[3, "Ohhh my goodness… My entire body hurts…"],
                         [4, "Right? How did people back in the day handle these crazy long car rides?"],
                         [1, "Hey Amy, is this the right place?"],
                         [2, "According to my calculations, we have arrived at our destination. Although… I may not be the most accurate GPS… I sure hope we weren’t misled…"],
                         [4, "We’d better not have been!!! IF I WENT THROUGH ALL THAT JUST FOR US TO BE IN THE WRONG PLACE, I’M GONNA--"],
                         [3, "I'm sick of your voice, Adam."],
                         [2, "Yeah Adam, we're the ones who suffered through hearing your voice the whole time."],
                         [1, "Quit arguing everyone! Let’s head inside already, looks like the reception is just through the front door."],
                         []]

    def dialogue(self, startindex, endindex):

