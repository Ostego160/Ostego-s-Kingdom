import random
from lib.constants import get as constant
from lib.colortext import colorprint as print
from lib.colortext import colorinput as input
from lib.colortext import colorstr

class EntityType:
    icon = 'E'
    
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name
        
    def getDescription(self):
        return self.desc
    
    def setDescription(self, desc):
        self.desc = desc
        
class Creature(EntityType):
    icon = 'C'
    
    def __init__(self, name, max_health, min_damage, max_damage, speed, hostility, lootList, desc):
        self.type      = 'creature'
        self.name      = name
        self.health    = [max_health, max_health]
        self.damage    = [min_damage, max_damage]
        self.speed     = [speed, speed]
        self.hostility = hostility or 0
        self.lootList  = lootList
        self.desc      = desc
        self.status    = None
        self.bounty    = False

    def clone(self):
        creature = Creature(self.name, self.health[1], self.damage[0], self.damage[1], self.speed[0])
        creature.health[0] = self.health[0]
        return creature
    
    def getDamage(self):
        return self.damage[0]
    
    def setDamage(self, v):
        self.damage[0] = max(0, min(v, self.damage[1]))

    def addDamage(self, v):
        self.damage[0] = max(0, min(self.damage[0] + v, self.damage[1]))

    def getDamageMax(self):
        return self.damage[1]

    def setDamageMax(self, v):
        self.damage[1] = max(0, min(v, constant('creatureDamageMax')))

    def addDamageMax(self, v):
        self.damage[1] = max(0, min(self.damage[1] + v, constant('creatureDamageMax')))
    
    def getHealth(self):
        return self.health[0]
    
    def setHealth(self, v):
        self.health[0] = max(0, min(v, self.health[1]))

    def addHealth(self, v):
        self.health[0] = max(0, min(self.health[0] + v, self.health[1]))

    def getHealthMax(self):
        return self.health[1]

    def setHealthMax(self, v):
        self.health[1] = max(0, min(constant('creatureHealthMax'), v))

    def addHealthMax(self, v):
        self.health[1] += v
        self.health[1] = max(0, min(constant('creatureHealthMax'), self.health[1]))
        self.addHealth(v)
    
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
    
    def printBasic(self):
        print(self.name, color='white')
        print('  Health:', self.health[0], '/', self.health[1], color='red')
        print('  Damage:', self.damage[0], '-', self.damage[1], color='blue')
    
    def printBattleInfo(self, i):
        if self.health[0] <= 0:
            print(str(i) + ': ' + self.name,color='white')
            print(' HP: DEAD', color='red')
        else:
            print(str(i) + ': ' + self.name, color='white')
            print(' HP:', self.health, color='red')

def getLeveledCreatureEasy(player, name, lootList='bandit1'):
    l = player.level
    h = random.randint(50, 65)
    s = random.randint(8,10)
    return Creature(name, h + (l * 10), 5 + l, 15 + 2 * int(l / 2), s, 0, lootList, 'not much.')

def getLeveledCreatureNormal(player, name, lootList='bandit1'):
    l = player.level
    h = random.randint(70, 85)
    s = random.randint(9,10)
    return Creature(name, h + (l * 12), 8 + l, 18 + 2 * int(l / 2), s, 0, lootList, 'not much.')

def getLeveledCreatureHard(player, name, lootList='bandit1'):
    l = player.level
    h = random.randint(90, 105)
    s = random.randint(9,10)
    return Creature(name, h + (l * 12), 10 + l, 20 + 2 * int(l / 2), s, 0, lootList, 'not much.')

def getLeveledCreatureVeryHard(player, name, lootList='bandit1'):
    l = player.level
    h = random.randint(120, 135)
    s = random.randint(9,11)
    return Creature(name, h + (l * 12), 12 + l, 25 + 2 * int(l / 2), s, 0, lootList, 'not much.')
