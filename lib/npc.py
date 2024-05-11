import random

from lib import loot
from lib import dialogue as talk
from lib import entities
from lib.constants import get as constant
from lib.colortext import colorprint as print
from lib.colortext import colorinput as input
from lib.colortext import colorstr

              #0          #1            #2           #3         #4      #5       #6           #7        #8      #9                   #10        #11       #12      #13              #14        #15
NPC_TYPES = ('Villager', 'Blacksmith', 'Shopkeeper', 'Farmer', 'Lord', 'Bandit', 'Merchant', 'Priest', 'Guard', 'Tournament Master', 'Sheriff', 'Wizard', 'Earl', 'Stable Master', 'Steward', 'Constable')

NPC_TRAITS = ('merciless', 'courageous', 'intelligent', 'valiant', 'insane', 'neurotic', 'mad', 'sharp', 'strong', 'inventive', 'forceful', 'calculating', 'thin', 'brave')

class NPC:
    def __init__(self, name, type, gender, location=None, dialogue='villager1'):
        self.name  = name
        self.type  = type
        self.items = []
        self.lootList = 'villager1'
        self.gold  = random.randint(0, 100)
        self.dialogue = talk.getDialogue(dialogue)
        self.mood = random.randint(5, 100)
        self.opinion = random.randint(0, 30)
        self.sleep = [random.randint(20, 22), random.randint(5, 8)]
        self.setGender(gender)
        self.takesBribe = False
        self.location = location
        self.home = location
        self.endStay = constant('timeStart') + random.randint(96, 168)
        self.givesQuest = random.randint(0, 2) == 1
        self.questType = random.randint(0, 3)
        self.quest = None
        self.battle = None
        self.traits = None
        self.hasMet = False
        self.canApproach = None

        if random.randint(0, 1) == 1:
            self.takesBribe = True

        if random.randint(0, 3) == 1:
            self.givesQuest = True
        
    def getType(self):
        try:
            return NPC_TYPES[self.type]
        except:
            return 'Unknown'

    def setTraits(self):
        self.traits = []
        for i in range(random.randint(1, 3)):
            trait = random.choice(NPC_TRAITS)
            while trait in self.traits:
                trait = random.choice(NPC_TRAITS)
            self.traits.append(trait)

    def getPosition(self):
        return self.location.x, self.location.y

    def getOpponent(self, bounty=True):
        opponent = entities.Creature(self.name, 100, 10, 25, 8, 0, 'villager1', 'not much.')
        opponent.bounty = bounty
        return opponent

    def getOpponentAddon(self):
        return entities.Creature('Guard', 150, 15, 35, 8, 0, 'villager1', 'not much.')

    def getDescription(self):
        return colorstr(self.name + ' (' + self.getType() + ')', 'white')

    def getMoodDescription(self):
        if self.mood < 25:
            return 'angry'
        elif self.mood < 50:
            return 'discontent'
        elif self.mood < 75:
            return 'neutral'
        else:
            return 'happy'

    def getOpinionDescription(self):
        if self.opinion < -50:
            return 'hostile'
        elif self.opinion < -15:
            return 'distrusting'
        elif self.opinion < 15:
            return 'neutral'
        elif self.opinion < 50:
            return 'trusting'
        elif self.opinion >= 50:
            return 'friendly'

    def setPronouns(self, first, second, third):
        self.pronoun = [first, second, third]

    def setGender(self, gender=None):
        if gender == 'm' or gender == 'male':
            self.gender = 'Male'
            self.setPronouns('he', 'his', 'him')
        elif gender == 'f' or gender == 'female':
            self.gender = 'Female'
            self.setPronouns('she', 'her', 'her')
        elif gender == 'p' or gender == 'plural':
            self.gender = 'Plural'
            self.setPronouns('they', 'their', 'them')
        else:
            self.gender = 'None'
            self.setPronouns('it', 'its', 'it')
    
    def addGold(self, i):
        self.gold += i
    
    def setGold(self, i):
        self.gold = i
    
    def addItem(self, i):
        self.items.append(i)

    def addOpinion(self, v):
        self.opinon = min(100, max(-100, self.opinion + v))
    
    def removeItem(self, i):
        self.items.remove(i)
        
    def setItems(self, items):
        self.items = items

    def updateLootList(self):
        lootList = loot.get( self.lootList )

        self.items.clear()
        self.gold = lootList.getGold()

        for item in lootList.getItems():
            self.items.append(item)
        
    def setLootList(self, lootListName, update=True):
        self.lootList = lootListName

        if update:
            self.updateLootList()
