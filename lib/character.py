import random

from lib import entities
from lib import text
from lib import mapper
from lib import magic
from lib.constants import get as constant
from lib.colortext import colorprint as print

from lib.colortext import colorprint as print
from lib.colortext import colorinput as input
from lib.colortext import colorstr

SKILLS = ['One Handed', 'Two Handed', 'Ranged', 'Sneak', 'Fire Magic', 'Nature Magic', 'Pickpocket', 'Lockpicking', 'Barter', 'Speech']
PREMADE = []

def showLevelUpMain(player):
    print(text.get('characterLevelUp', [player.name]), color='white')
    input(text.get('continue'), color='cyan')

    print(f'H: Health - {player.health}', color='red')
    print(f'M: Mana - {player.mana}', color='blue')
    for i in range( len(SKILLS) ):
        print(f'{i}: {SKILLS[i]} - {player.skills[i]}', color='white')

    skills = []
    skillNames = []

    print(text.get('characterLevelUpSkills'), color='white')
    while len(skills) < 3:
        skill = input().lower()
        if skill == 'h':
            skills.append(skill)
            skillNames.append('Health')
        elif skill == 'm':
            skillNames.append('Mana')
            skills.append(skill)
        else:
            try:
                skill = int(skill)

                if 0 <= skill < len(SKILLS):
                    skills.append(skill)
                    skillNames.append(SKILLS[skill])
                else:
                    print(text.get('invalidSelection'), color='red')
            except:
                print(text.get('invalidSelection'), color='red')

    for skill in skills:
        if skill == 'h':
            player.addHealthMax(3)
        elif skill == 'm':
            player.addManaMax(3)
        else:
            player.addSkill(skill, 3)

    player.addHealthMax(3)
    player.addManaMax(3)

    print(text.get('characterLevelUpComplete', [player.name, skillNames[0], skillNames[1], skillNames[2]]), color='white')
    player.printCharacter()
    input(text.get('continue'), color='cyan')

class Player(entities.Creature):
    def __init__(self, clock, name, gender, role, health, mana, skills):
        self.clock  = clock
        self.name   = name
        self.setGender(gender)
        self.role   = role
        self.level  = 0
        self.exp    = 0.0
        self.armor  = 0.0
        self.damage = [0.0, 0.0]
        self.weight = 0.0
        self.speed  = [0.0, 0.0]
        self.moveSpeed = 1
        self.health = [health, health]
        self.mana   = [mana, mana]
        self.skills = skills
        self.position = [0, 0]
        self.status = None
        self.bounty = 0
        self.hunger = 0
        self.exhaustion = 0

        self.arenaChampion = False

    def addTime(self, v):
        self.clock.add(v)
        self.addHunger(v)
        self.addExhaustion(v)

    def addTravelTime(self, v):
        self.clock.add(v)
        self.addHunger(int(v/2))
        self.addExhaustion(int(v/2))

    def addRestTime(self, v, rest):
        self.clock.add(v)
        self.addHunger(int(v / 1.5))
        self.addExhaustion(-int(rest * 1.5))

    def setDamageMax(self, v):
        self.damage[1] = max(0, min(v, constant('playerDamageMax')))

    def addDamageMax(self, v):
        self.damage[1] = max(0, min(self.damage[1] + v, constant('playerDamageMax')))

    def setHealthMax(self, v):
        self.health[1] = max(0, min(constant('playerHealthMax'), v))

    def addHealthMax(self, v):
        self.health[1] += v
        self.health[1] = max(0, min(constant('playerHealthMax'), self.health[1]))
        self.addHealth(v)

    def getMana(self):
        return self.mana[0]

    def setMana(self, v):
        self.mana[0] = max(0, min(v, self.mana[1]))

    def addMana(self, v):
        self.mana[0] = max(0, min(self.mana[0] + v, self.mana[1]))

    def getManaMax(self):
        return self.mana[1]

    def setManaMax(self, v):
        self.mana[1] = max(0, min(constant('playerManaMax'), v))

    def addManaMax(self, v):
        self.mana[1] += v
        self.mana[1] = max(0, min(constant('playerManaMax'), self.mana[1]))
        self.addMana(v)

    def addExperience(self, i):
        self.exp += i

    def addSkill(self, i, v):
        self.skills[i] = max(0, min(constant('playerSkillMax'), self.skills[i] + v))
    
    def setSkill(self, i, v):
        self.skills[i] = max(0, min(constant('playerSkillMax'), v))
    
    def setSkills(self, skills):
        self.skills = skills

    def setBounty(self, v):
        self.bounty = max(0, v)

    def addBounty(self, v):
        print(text.get('bounty', [self.name, self.pronoun[1], v]), color='yellow')
        self.bounty = max(0, self.bounty + v)

    def setHunger(self, v):
        self.hunger = max(0, v)

    def addHunger(self, v):
        threshold = constant('playerStarveThreshold')

        if self.hunger + v >= threshold:
            diff = self.hunger + v - threshold
            self.hunger = threshold
            self.addHealth(-diff)
            print(text.get('characterStarving', [self.name]), color='red')
            input(text.get('continue'), color='cyan')
        else:
            self.hunger = max(0, self.hunger + v)

    def setExhaustion(self, v):
        self.exhaustion = min(max(0, v), constant('playerExhaustionThreshold'))

    def addExhaustion(self, v):
        self.exhaustion = min(max(0, self.exhaustion + v), constant('playerExhaustionThreshold'))

    def checkHungerAndExhaustion(self):
        return self.hunger < constant('playerStarveThreshold') and self.exhaustion < constant('playerExhaustionThreshold')
        
    def printCharacter(self):
        print('Name:', self.name, color='yellow')
        print('Level:', self.level, ' Exp:', f"{self.exp:.1f}", color='white')
        print('Gender:', self.gender, ' Role:', self.role, color='white')
        print('Health:', self.health, color = 'red')
        print('Mana:', self.mana, color='blue')
        print('Damage:', self.damage, color='white')
        print('Armor:', f"{self.armor:.1f}", ' Weight:', f"{self.weight:.1f}", color='white')
        print(f'Combat Speed: {self.speed[0]}, Move Speed: {self.moveSpeed}', color='white')
        print('Skills:', color='white')
        print('  One Handed:', self.skills[0], color='white')
        print('  Two Handed:', self.skills[1], color='white')
        print('  Ranged:', self.skills[2], color='white')
        print('  Sneak:', self.skills[3], color='white')
        print('  Fire Magic:', self.skills[4], color='white')
        print('  Nature Magic:', self.skills[5], color='white')
        print('  Pickpocket:', self.skills[6], color='white')
        print('  Lockpicking:', self.skills[7], color='white')
        print('  Barter:', self.skills[8], color='white')
        print('  Speech:', self.skills[9], color='white')
    
    def printCharacterBasic(self):
        print(self.name, color='white')
        print('  Health:', self.health, color='red')
        print('  Mana:', self.mana, color='blue')
        print('  Damage:', self.damage, color='white')
    
    def printSkills(self):
        for i,skill in enumerate(SKILLS):
            print('', skill + ':', self.skills[i], color='white')

    def printHungerAndExhaustion(self):
        hunger = colorstr('well fed', 'green')
        exhaustion = colorstr('well rested', 'green')
        if self.hunger >= constant('playerStarveThreshold'):
            hunger = colorstr('STARVING TO DEATH', 'red')
        elif self.hunger >= 24:
            hunger = colorstr('starving', 'red')
        elif self.hunger >= 12:
            hunger = colorstr('hungry', 'yellow')
        elif self.hunger >= 6:
            hunger = colorstr('peckish', 'green')

        if self.exhaustion >= 24:
            exhaustion = colorstr('exhausted', 'red')
        elif self.exhaustion >= 12:
            exhaustion = colorstr('tired', 'yellow')
        elif self.exhaustion >= 6:
            exhaustion = colorstr('refreshed', 'green')

        print(f'{self.name} is {hunger}', colorstr('and', 'blue'), exhaustion, color='blue')
    
    def getPosition(self):
        return self.position[0], self.position[1]
    
    def setPosition(self, x,y):
        self.position[0] = x
        self.position[1] = y

    def updateExperience(self):
        exp = (self.level + 1) * 100 + (self.level * 50)
        if self.exp > exp:
            self.level += 1
            self.exp -= exp
            showLevelUpMain(self)

    def updateTeleport(self, inventory, location, clock):
        if self.status == 'teleport':
            self.status = None
            return mapper.showTeleportMain(self, inventory, location, clock)

    def updateConjure(self, inventory):
        if self.status == 'conjure':
            self.status = None
            return magic.showMagicConjure(self, inventory)

    def updateDuplicate(self, inventory):
        if self.status == 'duplicate':
            self.status = None
            return magic.showMagicDuplicate(self, inventory)

def printSkills(skills):
        for i,skill in enumerate(SKILLS):
            print(f'  {skill}: {skills[i]}', color='white')
            
def getAllPremade():
    return PREMADE

def getPremade(i):
    return PREMADE[i]

def addPremade(*args):
    PREMADE.append(Player(*args))

def showCreateCharacterMain(clock):
    print()
    print(text.get('titleCharacterCreation'), color='blue')
    
    confirmCharacter = False
    
    while confirmCharacter != True:
        char = {'level':0, 'exp':0, 'armor':0.0, 'damage':0.0, 'weight':0.0, 'speed':0.0}
        
        name = input(text.get('selectName'), color='cyan')
        
        while True:
            gender = input(text.get('selectGender'), color='cyan').lower()
            break
        
        roles = ('Fighter', 'Barbarian', 'Ranger', 'Bard', 'Thief', 'Mage', 'Druid', 'Spellsword')
        
        role = None
        
        while not role:
            print('\nAvailable Roles:', color='white')
            for i,role in enumerate(roles):
                print(f'  {i}: {role.capitalize()}', color='white')
            select = input(text.get('selection'), color='cyan').lower()
            try:
                role = roles[int(select)]
            except:
                print(text.get('invalidSelection'), color='red')
            
            print(text.get('role' + role), color='white')
                
            select = None
            
            while not select:
                print(text.get('selectRole', [role]), color='cyan')
                select = input().lower()
                
                if select == 'y' or select == 'yes':
                    print()
                elif select == 'n' or select == 'no':
                    role = None
                else:
                    print(text.get('invalidSelection'), color='red')
                    select = None
        
        confirmSkills = False
        skills = []
        health = 0
        mana = 0

        while confirmSkills != True:
            print('\nRolling skills...', color='blue')
            
            skills = [
                random.randint(5,50),
                random.randint(5,50),
                random.randint(5,50),
                random.randint(5,50),
                random.randint(5,50),
                random.randint(5,50),
                random.randint(5,50),
                random.randint(5,50),
                random.randint(5,50),
                random.randint(5,50)
            ]
            
            health = random.randint(25,50)
            mana = random.randint(10,50)
            
            if role == 'Fighter':
                skills[0] += 10
                skills[1] += 5
                skills[2] += 5
            elif role == 'Barbarian':
                health += 10
                skills[1] += 10
            elif role == 'Ranger':
                skills[2] += 10
                skills[0] += 5
                skills[3] += 5
            elif role == 'Bard':
                skills[8] += 10
                skills[9] += 10
            elif role == 'Thief':
                skills[3] += 10
                skills[6] += 5
                skills[7] += 5
            elif role == 'Mage':
                mana += 10
                health -= 10
                skills[4] += 10
                skills[5] += 10
            elif role == 'Druid':
                mana += 5
                skills[1] += 5
                skills[5] += 10
            elif role == 'Spellsword':
                mana += 5
                skills[0] += 10
                skills[4] += 5

            print(colorstr(f'Health: {health}','red'), colorstr(f'Mana: {mana}','blue'))
            
            printSkills(skills)
            
            while True:
                select = input(text.get('confirmSkills'), color='cyan').lower()
                
                if select == 'y':
                    confirmSkills = True
                    break
                elif select == 'n':
                    break
        while True:
            print()
            print(text.get('selectSkills'), color='cyan')
            for i in range( len(SKILLS) ):
                print(f'  {i}: {SKILLS[i]}', color='white')
                
            skill1 = int(input())
            skill2 = int(input())
            skill3 = int(input())
            
            if 0 <= skill1 <= 9 and 0 <= skill2 <= 9 and 0 <= skill3 <= 9:
                skills[skill1] += 10
                skills[skill2] += 10
                skills[skill3] += 10
                break
            else:
                print(text.get('invalidSelection'), color='red')
        player = Player(clock, name, gender, role, health, mana, skills)
        
        player.printCharacter()
        
        print(text.get('confirmCharacter', [name]), color='cyan')
        
        select = input().lower()
        
        if select == 'y':
            confirmCharacter = True
            return player
