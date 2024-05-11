import random
import math

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890abcdefghijklmnopqrstuvwxyz'

from lib.location import Location
from lib.location import LOCATION_TYPES
from lib import text
from lib import names
from lib import encounter
from lib.constants import get as constant
from lib.colortext import colorprint as print
from lib.colortext import colorinput as input
from lib.colortext import getColorStr as getColorStr
from lib.colortext import resetColor as resetColor
from lib.colortext import getColor as getColor

MAP = {}
MAP_STR = ''
W,H = 48,24
AVG = math.sqrt( (W) ** 2 + (H) ** 2  )
LOCATIONS = []
TRAVELLING = []
UNIQUE_NPC = {}

ENCOUNTER_THRESHOLD = AVG/8

def convertToIndex(x,y):
    return y * (W-1) + x

def get(x,y):
    return MAP[ y * (W-1) + x ]

def set(x,y, v):
    MAP[ y * (W-1) + x ] = v

def check(x,y):
    try:
        return MAP[ y * (W-1) + x ]
    except:
        return False

def buildMap(location, journal):
    global MAP_STR
    MAP_STR = ' '

    for x in range(W):
        MAP_STR += '_'

    MAP_STR += getColorStr('  MAP LEGEND:\n', color='white') + resetColor()

    for y in range(H):
        MAP_STR += '|'
        for x in range(W):
            hit = False
            for i, loc in enumerate(LOCATIONS):
                if loc.x == x and loc.y == y:
                    hit = True
                    if loc == location:
                        MAP_STR = MAP_STR[:-1]
                        MAP_STR += getColorStr('*', color='yellow') + resetColor()
                    else:
                        for entry in journal:
                            if entry.location == loc:
                                MAP_STR = MAP_STR[:-1]
                                MAP_STR += getColorStr('!', color='yellow') + resetColor()
                    if loc.type == 0:
                        MAP_STR += getColorStr(ALPHABET[i], color='cyan')
                    elif loc.type == 1:
                        MAP_STR += getColorStr(ALPHABET[i], color='green')
                    elif loc.type == 2:
                        MAP_STR += getColorStr(ALPHABET[i], color='white')
                    elif loc.type == 3:
                        MAP_STR += getColorStr(ALPHABET[i], color='red')
                    elif loc.type == 4:
                        MAP_STR += getColorStr(ALPHABET[i], color='blue')
                    else:
                        MAP_STR += getColorStr(ALPHABET[i], color='magenta')
                    MAP_STR += resetColor()
                    break
            if not hit:
                MAP_STR += ' '
        MAP_STR += '|'

        if y < len(LOCATIONS):
            loc = LOCATIONS[y]
            if loc.type == 0:
                MAP_STR += getColor('cyan')
            elif loc.type == 1:
                MAP_STR += getColor('green')
            elif loc.type == 2:
                MAP_STR += getColor('white')
            elif loc.type == 3:
                MAP_STR += getColor('red')
            elif loc.type == 4:
                MAP_STR += getColor('blue')
            else:
                MAP_STR += getColor('magenta')

            MAP_STR += ' ' + ALPHABET[y] + ': ' + loc.getShortDescription()
            if loc == location:
                MAP_STR += getColorStr(' *(Current Location)*', color='yellow') + resetColor()
            MAP_STR += resetColor()
        MAP_STR += '\n'

    MAP_STR += ' '

    for x in range(W):
        MAP_STR += '_'

    if len(LOCATIONS) > H:
        MAP_STR += '  ' + ALPHABET[H] + ': ' + LOCATIONS[H].getShortDescription()

        for y in range(H + 1, len(LOCATIONS)):
            MAP_STR += '\n'
            MAP_STR += ' ' * (W + 2)
            MAP_STR += ' ' + ALPHABET[y] + ': ' + LOCATIONS[y].getShortDescription()


def printMap(location, journal):
    buildMap(location, journal)
    print(MAP_STR)

def serializeMap():
    data = '[LOCATIONS]\n'
    for loc in LOCATIONS:
        pass

def getUniqueNPC(id):
    return UNIQUE_NPC[id]

def setUniqueNPC(id, npc):
    UNIQUE_NPC[id] = npc
    return npc

def getLocation(name):
    try:
        return LOCATIONS[name]
    except:
        return False

def newLocation(x,y, name, type):
    loc = Location(x,y, name, type)
    set(x,y, loc)
    LOCATIONS.append(loc)
    return loc

def newRandomLocation(type):
    x, y = 0 ,0

    while x < 2 or y < 2:
        x = random.randint(2, W - 2)
        y = random.randint(2, H - 2)
        for location in LOCATIONS:
            if ( location.x - 2 <= x <= location.x + 2 ) and (location.y - 2 <= y <= location.y + 2):
                x = 0
                y = 0

    name = names.getRandom('town')

    while True:
        hit = False
        for location in LOCATIONS:
            if name == location.name:
                name = names.getRandom('town')
                hit = True
        if not hit:
            break


    location = newLocation(x,y, name, type)

    if type <= 2:
        if random.randint(0,1) == 1:
            location.addLandmark('Fountain')
        if random.randint(0,1) == 1:
            location.addLandmark('Blacksmith')
        if random.randint(0,1) == 1:
            location.addLandmark('Market')
        if random.randint(0,1) == 1:
            location.addLandmark('Church')
        if random.randint(0,1) == 1:
            location.addLandmark('Farm')
        if random.randint(0,2) == 1:
            location.addLandmark('MagesGuild')

    if type <= 1:
        if random.randint(0,1) == 1:
            location.addLandmark('Barracks')
        if random.randint(0,1) == 1:
            location.addLandmark('Keep')
        if random.randint(0,1) == 1:
            location.addLandmark('Walls')
        if random.randint(0,1) == 1:
            location.addLandmark('Camp')
    if type == 0:
        location.addLandmark('Jail')
        location.addLandmark('Tournament')

    if type == 3:
        if random.randint(0,1) == 1:
            location.addLandmark('Cemetery')
        if random.randint(0,1) == 1:
            location.addLandmark('Camp')
        if random.randint(0,1) == 1:
            location.addLandmark('RiverTown')

    if type == 4:
        location.addLandmark('Farm')
        location.addLandmark('FlourMill')
        if random.randint(0,1) == 1:
            location.addLandmark('Cemetery')
        if random.randint(0,1) == 1:
            location.addLandmark('Camp')
        if random.randint(0,1) == 1:
            location.addLandmark('RiverTown')

    if type == 5:
        location.addLandmark('RiverWilderness')

    if location.type == 0:
        location.addRandomPerson(4, 'noble1').setLootList('villager1')

    for landmark in location.landmarks:
        if landmark.name == 'Blacksmith':
            location.addRandomPerson(1).setLootList('blacksmith1')
        elif landmark.name == 'Market':
            location.addRandomPerson(2).setLootList('shopGeneral1')
        elif landmark.name == 'Farm':
            location.addRandomPerson(3).setLootList('villager1')
        elif landmark.name == 'Church':
            location.addRandomPerson(7).setLootList('villager1')
        elif landmark.name == 'Tournament':
            location.addRandomPerson(9, 'tournament1').setLootList('villager1')
        elif landmark.name == 'MagesGuild':
            location.addRandomPerson(11, 'wizard1').setLootList('villager1')
        elif landmark.name == 'Jail':
            location.addRandomPerson(10, 'sheriff1').setLootList('villager1')

    for i in range(random.randint(1,3)):
        location.addRandomPerson(0).setLootList('villager1')

    return location

def setRandomMap(scale):
    cities = random.randint(1, scale // 7 + 1)
    towns  = random.randint(1, scale // 5 + 1)
    villages  = random.randint(1, scale // 3 + 1)
    inns = random.randint(1, scale // 5 + 1)
    farms = random.randint(1, scale // 5 + 1)
    caves = random.randint(1, scale // 5 + 1)

    for i in range(cities + 1):
        newRandomLocation(0)

    for i in range(towns + 1):
        newRandomLocation(1)

    for i in range(villages + 1):
        newRandomLocation(2)

    for i in range(inns + 1):
        newRandomLocation(3)

    for i in range(farms + 1):
        newRandomLocation(4)

    for i in range(caves + 1):
        newRandomLocation(5)

    for loc in LOCATIONS:
        if loc.type == 0:
            UNIQUE_NPC['Earl'] = loc.addRandomPerson(12, 'earl1')
            UNIQUE_NPC['Earl'].setTraits()
            UNIQUE_NPC['Earl'].setLootList('villager1')
            UNIQUE_NPC['Steward'] = loc.addRandomPerson(14)
            UNIQUE_NPC['Steward'].setTraits()
            UNIQUE_NPC['Steward'].setLootList('villager1')
            UNIQUE_NPC['Constable'] = loc.addRandomPerson(15)
            UNIQUE_NPC['Constable'].setTraits()
            UNIQUE_NPC['Constable'].setLootList('villager1')
            break

def getAllLocations():
    return LOCATIONS

def updateLocations():
    for location in reversed(LOCATIONS):
        location.update()

def verifyLocations():
    for location in reversed(LOCATIONS):
        if location.remove:
            LOCATIONS.remove(location)

#SEARCH RELATED
def getAllByNPC(player, name):
    locations = []
    travelling = []
    x, y = player.getPosition()

    name = name.lower()

    for location in LOCATIONS:
        for person in location.people:
            if name in person.name.lower():
                dist = math.sqrt( (location.x - x) ** 2 + (location.y - y) ** 2)
                locations.append((location, dist, person.name))

    for entry in TRAVELLING:
        npc = entry[0]
        if name in npc.name.lower():
            travelling.append(entry)


    def sortLocation(v):
        return v[1]

    locations.sort(key=sortLocation, reverse=True)

    return locations, travelling

def getPersonByRef(npc):
    for location in LOCATIONS:
        for person in location.people:
            if person == npc:
                return person

def getPersonByName(name):
    for location in LOCATIONS:
        for person in location.people:
            if person.name == name:
                return person

def getNearestByLocationType(player, type):
    locations = []
    x, y = player.getPosition()

    for location in LOCATIONS:
        if location.getType() == type:
            dist = math.sqrt( (location.x - x) ** 2 + (location.y - y) ** 2)
            locations.append((location, dist))

    def sortLocation(v):
        return v[1]

    locations.sort(key=sortLocation, reverse=True)

    if len(locations) > 0:
        return locations.pop()

def getNearestByProfessionType(player, type):
    locations = []
    x, y = player.getPosition()

    for location in LOCATIONS:
        for npc in location.people:
            if npc.getType() == type:
                dist = math.sqrt( (location.x - x) ** 2 + (location.y - y) ** 2)
                locations.append((location, dist))
                break

    def sortLocation(v):
        return v[1]
    locations.sort(key=sortLocation, reverse=True)
    if len(locations) > 0:
        return locations.pop()

def getNearestByLandmarkType(player, type):
    locations = []
    x, y = player.getPosition()

    for location in LOCATIONS:
        for landmark in location.landmarks:
            if landmark.name == type:
                dist = math.sqrt( (location.x - x) ** 2 + (location.y - y) ** 2)
                locations.append((location, dist))
                break

    def sortLocation(v):
        return v[1]

    locations.sort(key=sortLocation, reverse=True)

    if len(locations) > 0:
        return locations.pop()

def checkRandomEncounter(player, inventory, dist):
    while dist > ENCOUNTER_THRESHOLD:
        roll = random.randint(0, int(dist) + 1)
        if roll > ENCOUNTER_THRESHOLD:
            enc = encounter.getRandom()
            enc(player, inventory)
        if player.health[0] <= 0:
            return False
        dist -= roll
    return True

#TRAVELLING
def updateTravelling(player):
    for loc in LOCATIONS:
        for npc in reversed(loc.people):
            if npc.type == 0 or npc.type == 3:
                if npc.home == loc:
                    if player.clock.time >= npc.endStay:
                        entry = getNearestByLocationType(npc, LOCATION_TYPES[random.randint(0, 1)])
                        if not entry or entry[0] == loc:
                            entry = getNearestByLocationType(npc, LOCATION_TYPES[random.randint(2, 4)])
                        time = player.clock.time + entry[1]
                        npc.endStay = player.clock.time + time + random.randint(48, 96)
                        TRAVELLING.append((npc, entry[0], time))
                        loc.people.remove(npc)
                elif player.clock.time >= npc.endStay:
                    loc = npc.home
                    time = player.clock.time + loc.getDistance(loc)
                    npc.endStay = player.clock.time + time + random.randint(96, 168)
                    TRAVELLING.append((npc, loc, time))
                    loc.people.remove(npc)

    for entry in reversed(TRAVELLING):
        if player.clock.time >= entry[2]:
            npc = entry[0]
            loc = entry[1]
            npc.location = loc
            loc.people.append(npc)
            TRAVELLING.remove(entry)

def showTeleportMain(player, inventory, location, clock):
    continueMove = True

    while continueMove:
        print()
        print(text.get('titleTeleport'), color='blue')
        print(text.get('moveMenu'), color='white')
        clock.printDescription()
        print(text.get('locationCurrent', [player.name, location.getShortDescription() ]), color='blue')

        for i,loc in enumerate(LOCATIONS):
            dist = location.getDistance(loc)
            diff = dist/AVG
            if loc.type == 0:
                print(f'  {i}: {loc.getShortDescription()}', color='cyan')
            elif loc.type == 1:
                print(f'  {i}: {loc.getShortDescription()}', color='green')
            elif loc.type == 2:
                print(f'  {i}: {loc.getShortDescription()}', color='white')
            elif loc.type == 3:
                print(f'  {i}: {loc.getShortDescription()}', color='red')
            elif loc.type == 4:
                print(f'  {i}: {loc.getShortDescription()}', color='blue')
            else:
                print(f'  {i}: {loc.getShortDescription()}', color='magenta')


        select = None

        while not select:
            print()
            select = input(text.get('selection2'), color='cyan').lower()

            if select == 'b':
                return False
            else:
                try:
                    select = LOCATIONS[int(select)]
                except:
                    print(text.get('invalidSelection'), color='red')
                    select = None

        select2 = None

        while not select2:
            dist = location.getDistance(select)
            diff = dist/AVG
            cost = diff * constant('magicTeleportBaseCost')
            cost = int(cost)

            if player.mana[0] >= cost:
                print(text.get('magicTeleportCost', [cost, select.name]))

                select2 = input().lower()

                if select2 == 'y' or select2 == 'yes':
                    player.setPosition(select.x, select.y)

                    print()
                    print(text.get('magicTeleportSuccess', [player.name]))

                    print(text.get('moveArrive', [player.name, select.name, clock.getTimeOfDay() ]))

                    input(text.get('continue'))

                    return select
                elif select2 == 'n' or select2 == 'no':
                    print()
                else:
                    print(text.get('invalidSelection'))
            else:
                print(text.get('magicTeleportFail', [player.name, select.name]))
                input(text.get('continue'))
                select2 = True

def showMoveMain(player, inventory, location, clock):
    continueMove = True
    
    while continueMove:
        print()
        print(text.get('titleMove'), color='blue')
        clock.printDescription()
        print(text.get('locationCurrent', [player.name, location.getShortDescription() ]), color='blue')
        print(text.get('moveMenu'), color='white')
        
        for i,loc in enumerate(LOCATIONS):
            dist = location.getDistance(loc)
            diff = dist/AVG

            if loc.type == 0:
                print(f'  {i}: {loc.getShortDescription()}', color='cyan', end=' ')
            elif loc.type == 1:
                print(f'  {i}: {loc.getShortDescription()}', color='green', end=' ')
            elif loc.type == 2:
                print(f'  {i}: {loc.getShortDescription()}', color='white', end=' ')
            elif loc.type == 3:
                print(f'  {i}: {loc.getShortDescription()}', color='red', end=' ')
            elif loc.type == 4:
                print(f'  {i}: {loc.getShortDescription()}', color='blue', end=' ')
            else:
                print(f'  {i}: {loc.getShortDescription()}', color='magenta', end=' ')
            
            if diff <= 0:
                print('(Current Location)', color='yellow')
            elif diff < 0.1:
                print('(Really Close)', color='white')
            elif diff < 0.25:
                print('(Close)', color='white')
            elif diff < 0.5:
                print('(Far)', color='white')
            else:
                print('(Really Far)', color='white')

        select = False
        
        while not select:
            print()
            select = input(text.get('selection2'), color='cyan').lower()
            
            if select == 'b':
                return False
            else:
                try:
                    select = LOCATIONS[int(select)]
                except:
                    print(text.get('invalidSelection'),color='red')
                    select = None
        
        select2 = None
        
        while not select2:
            dist = location.getDistance(select) / player.moveSpeed
            dist = round(dist, 1)
            
            print(text.get('moveConfirm', [dist]), color='cyan')
            
            select2 = input().lower()
            
            if select2 == 'y' or select2 == 'yes':
                if checkRandomEncounter(player, inventory, dist):
                    player.setPosition(select.x, select.y)
                    player.addTravelTime(dist)

                    print()
                    print(text.get('moveArrive', [player.name, select.name, clock.getTimeOfDay() ]), color='blue')

                    input(text.get('continue'), color='cyan')

                return select
            elif select2 == 'n' or select2 == 'no':
                print()
            else:
                print(text.get('invalidSelection'), color='red')

def getRandomLocation():
    return LOCATIONS[random.randint(0, len(LOCATIONS)-1)]
