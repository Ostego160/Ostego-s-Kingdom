import math
import random

from lib.npc import NPC
from lib import text
from lib import names
from lib import battle
from lib.constants import get as constant
from lib import encounter

from lib.colortext import colorprint as print
from lib.colortext import colorinput as input
from lib.colortext import colorstr

LANDMARK = {}
LOCATION_TYPES = ('City', 'Town', 'Village', 'Inn', 'Farm', 'Cave', 'Hideout', 'Forest', 'Grassland', 'Mountain', 'River')
REST_QUALITY = (1, .8, .7, 1, .5, .5, .5, .5, .5, .5)

class Landmark():
    def __init__(self, name):
        self.name = name
        self.desc = text.get('landmark' + name)
    
    def getDescription(self):
        return self.desc

class Location:
    def __init__(self, x,y, name, type ):
        self.x = x
        self.y = y
        self.name = name
        self.people = []
        self.landmarks = []
        self.type = type
        self.remove = None

    def getType(self):
        return LOCATION_TYPES[self.type]
    
    def getDistance(self, location):
        return math.sqrt( (location.x - self.x) ** 2 + (location.y - self.y) ** 2  )
    
    def addPerson(self, *args):
        npc = NPC(*args)
        self.people.append(npc)
        return npc

    def addRandomPerson(self, NPCtype=0, dialogue='villager1'):
        gender = 'm'
        name = None

        roll = random.randint(0,1)

        if roll:
            gender = 'f'
            name = names.getRandom('NPCfemale')
        else:
            name = names.getRandom('NPCmale')

        npc = NPC(name, NPCtype, gender, self, dialogue)

        self.people.append(npc)

        return npc

    def lowerPeopleOpinion(self, v):
        for npc in self.people:
            npc.opinion -= int(v)
        
    def addLandmark(self, name):
        self.landmarks.append( LANDMARK[name] )
        
    def getShortDescription(self):
        return self.name + ' (' + LOCATION_TYPES[self.type] + ')'
        
    def getDescription(self):
        try:
            return text.get('desc' + LOCATION_TYPES[self.type])
        except:
            print(text.get('errorLocation'))
            return ''

    def update(self):
        for npc in self.people:
            npc.mood = random.randint(10,100)

            if not npc.quest:
                npc.givesQuest = random.randint(0, 3) == 1
                npc.questType = random.randint(0, 3)

            npc.updateLootList()

    def checkHostility(self, player, inventory):
        opponents = []
        banditOnly = True

        for npc in self.people:
            if npc.battle or npc.opinion <= -100:
                opponent = npc.getOpponent()
                opponents.append(opponent)
                if npc.type != 5:
                    banditOnly = False
                    player.addBounty(constant('bountyAssault'))
                    for i in range(random.randint(1, 2)):
                        opponents.append(npc.getOpponentAddon())
                else:
                    opponent.bounty = False

                npc.battle = None

        if len(opponents) > 0:
            if not banditOnly:
                for npc in self.people:
                    npc.opinion -= random.randint(35, 50)
                    npc.mood -= random.randint(35, 50)
                    if npc.opinion <= -50:
                        opponents.append(npc.getOpponentAddon())

                print(text.get('locationHostility', [player.name, self.name]))
                input(text.get('continue'))

            battle.showBattleMain(player, inventory, opponents)

            for opponent in opponents:
                if opponent.health[0] <= 0:
                    for npc in reversed(self.people):
                        if opponent.name == npc.name:
                            self.people.remove(npc)
                            break

    def checkBounty(self, player, inventory):
        if self.type <= 3 and player.bounty > 0:
            chance = -player.weight / 2 + player.skills[3] / 2 - player.bounty / 250
            chance *= 100
            chance = int(chance) + random.randint(-10, 10)
            if chance >= 50:
                print(text.get('stealBountyEvade', [player.name]))
                input(text.get('continue'))
            else:
                enc = encounter.getRandomBounty()
                enc(player, inventory)
    
    def printFullDescription(self, clock):
        bul = text.get('formatBullet')
        print()
        print(bul + 'Location:', self.name, color='white')
        print(bul, end='')
        clock.printDescription()
        print(bul + 'Description:', color='white')
        print(self.getDescription())
        print(bul + 'People:', color='white')
        for person in self.people:
            print(f'{person.getDescription()} - {person.gender} (looks {person.getMoodDescription()})', color='yellow')
            print(f'  Has a {person.getOpinionDescription()} opinion of you.')
            if person.quest:
                print(f'  (?) You have a quest from {person.name}.')
            elif person.givesQuest:
                print(f'  (!) Has a quest for you.', color='green')
        print(bul + 'Observations:', color='white')
        if len(self.landmarks) > 0:
            for landmark in self.landmarks:
                print(landmark.getDescription())
        else:
            print(text.get('landmarkNothing'))

    def showRest(self, player, inventory, quality=None, wilderness=False):
        while True:
            time = input(text.get('restMenu'), color='cyan').lower()
            if time == 'b':
                return False
            try:
                time = int(time)
            except:
                print(text.get('invalidSelection'), color='red')

            if isinstance(time, int):
                if time <= 0:
                    print(text.get('restShort'), color='red')
                elif time > 24:
                    print(text.get('restLong'), color='red')
                else:
                    hasMeat = False

                    for i in inventory.bag:
                        if i == 129:
                            hasMeat = True
                            break
                    if hasMeat:
                        continueCook = True
                        while continueCook:
                            count = inventory.bag.count(129)
                            print(text.get('locationCookMeat', [player.name, count]))
                            select = input(text.get('locationCook'), color='cyan').lower()
                            continueCookCount = False
                            try:
                                select = int(select)
                                continueCookCount = True
                            except:
                                print(text.get('invalidSelection'), color='red')

                            if isinstance(select, int):
                                if select > count:
                                    print(text.get('invalidSelection'), color='red')

                                elif select > 0 and continueCookCount:
                                    for i in range(select):
                                        if 129 in inventory.bag:
                                            inventory.bag.remove(129)
                                            inventory.bag.append(130)
                                    print(text.get('locationCookComplete', [player.name, select]), color='blue')
                                    continueCook = False
                                else:
                                    continueCook = False

                    if not quality:
                        quality = REST_QUALITY[self.type]

                    player.addRestTime(time, time * quality)

                    if player.checkHungerAndExhaustion():
                        player.addMana(time * 10 * quality)
                        player.addHealth(time * 10 * quality)

                    restLevel = ''
                    if quality == 1:
                        restLevel = colorstr('excellent', color='green')
                    elif quality > .8:
                        restLevel = colorstr('great', color='green')
                    elif quality > .6:
                        restLevel = colorstr('average', color='yellow')
                    elif quality > .4:
                        restLevel = colorstr('poor', color='yellow')
                    else:
                        restLevel = colorstr('poor', color='red')

                    if wilderness:
                        print(text.get('restQuality', [self.name + ' Wilderness', restLevel]))
                    else:
                        print(text.get('restQuality', [self.name, restLevel]))

                    print(text.get('restComplete', [player.name, time, player.clock.getTimeOfDay()]), color='blue')
                    input(text.get('continue'), color='cyan')
                    return True

LANDMARK['Fountain'] = Landmark('Fountain')
LANDMARK['Camp'] = Landmark('Camp')
LANDMARK['Walls'] = Landmark('Walls')
LANDMARK['Keep'] = Landmark('Keep')
LANDMARK['FarmerCart'] = Landmark('FarmerCart')
LANDMARK['Blacksmith'] = Landmark('Blacksmith')
LANDMARK['FlourMill'] = Landmark('FlourMill')
LANDMARK['Tournament']= Landmark('Tournament')
LANDMARK['Church']= Landmark('Church')
LANDMARK['RiverTown']= Landmark('RiverTown')
LANDMARK['RiverWilderness']= Landmark('RiverWilderness')
LANDMARK['Farm']= Landmark('Farm')
LANDMARK['Cemetery']= Landmark('Cemetery')
LANDMARK['Barracks']= Landmark('Barracks')
LANDMARK['Market']= Landmark('Market')
LANDMARK['Jail']= Landmark('Jail')
LANDMARK['MagesGuild'] = Landmark('MagesGuild')

