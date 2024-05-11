import random

from lib import mapper
from lib import character
from lib import text
from lib import items
from lib import dialogue
from lib import trade
from lib import magic
from lib import theft
from lib import quest
from lib import encounter
from lib.time import Clock
from lib.constants import get as constant
from lib import hunt
from lib import saver

from lib.colortext import colorprint as print
from lib.colortext import colorinput as input
from lib.colortext import lightMode

#lightMode()

from lib.dialogues import villager1
from lib.dialogues import bounty1
from lib.dialogues import noble1
from lib.dialogues import tournament1
from lib.dialogues import wizard1
from lib.dialogues import sheriff1
from lib.dialogues import earl1

print(text.get('title'), color='blue')
print(text.get('titleImg'), color='white')
print(text.get('author'))

PLAYER = None
INVENTORY = None
LOCATION = None
CLOCK = None

#items.printItems()

while True:
    PLAYER = None
    INVENTORY = None
    mapper.setRandomMap(16)
    LOCATION = mapper.getRandomLocation()
    CLOCK = Clock(constant('timeStart'))

    character.addPremade(CLOCK, 'Grom', 'm', 'Barbarian', 100, 12, [45, 60, 11, 3, 10, 24, 10, 11, 15, 11])
    character.addPremade(CLOCK, 'Zora', 'f', 'Fighter', 75, 20, [55, 45, 25, 16, 20, 15, 10, 22, 23, 62])
    character.addPremade(CLOCK, 'Roland', 'm', 'Mage', 46, 75, [30, 11, 23, 11, 67, 55, 14, 11, 24, 31])
    character.addPremade(CLOCK, 'Katherine', 'f', 'Thief', 60, 20, [55, 15, 50, 60, 20, 15, 70, 67, 35, 22])
    character.addPremade(CLOCK, 'Strider', 'm', 'Ranger', 67, 32, [46, 23, 77, 42, 10, 32, 30, 15, 18, 23])

    print()
    print(text.get('titleMain'), color='blue', style=5)
    print(text.get('mainMenu'), color='white')
    select = input(text.get('selection'), color='cyan').lower()
    
    if select == 'n':
        print()
        print(text.get('introNewGame'), color='blue')
        
        while not PLAYER:
            print(text.get('characterNewMenu'), color='white')
            select = input(text.get('selection'), color='cyan')
            if select == '0':
                PLAYER = character.showCreateCharacterMain(CLOCK)
            elif select == '1':
                premades = character.getAllPremade()
                
                for i,premade in enumerate(premades):
                    print('\nPre-made', str(i) + ':', color='magenta')
                    premade.printCharacter()
                
                while True:
                    select = input('\nEnter selection for pre-made character:\n', color='cyan')
                    try:
                        PLAYER = premades[ int(select) ]
                        break
                    except:
                        print(text.get('invalidSelection'), color='red')
                
                while True:
                    select = input(text.get('confirmCharacter', [PLAYER.name]), color='cyan')
                    
                    if select == 'y':
                        break
                    elif select == 'n':
                        PLAYER = None
                        break
                    else:
                        print(text.get('invalidSelection'), color='red')
            else:
                print(text.get('invalidSelection'), color='red')

        PLAYER.setPosition(LOCATION.x, LOCATION.y)
        
        INVENTORY = items.Inventory()
        INVENTORY.equipItem(56)
        INVENTORY.equipItem(2)
        INVENTORY.equipItem(108)

        for i in range(25):
            INVENTORY.addItem(129)
        INVENTORY.addItem(129)
        INVENTORY.addItem(130)
        INVENTORY.addItem(131)
        INVENTORY.addItem(41)
        INVENTORY.addItem(218)

        INVENTORY.setGold(random.randint(75,125))

        PLAYER.armor  = INVENTORY.getTotalArmor()
        PLAYER.damage = INVENTORY.getTotalDamage()
        PLAYER.weight = INVENTORY.getTotalWeight()
        PLAYER.speed  = INVENTORY.getTotalSpeed(PLAYER.weight)
        PLAYER.moveSpeed = INVENTORY.getMoveSpeed(PLAYER.weight)

        mapMenu = True

        print(text.get('storyIntro', [PLAYER.name, PLAYER.pronoun, LOCATION.name]), color='white')
        input(text.get('continue'), color='cyan')
        
        while mapMenu:
            print()
            print(text.get('titleMap'), color='blue')
            mapper.printMap(LOCATION, quest.getJournal())
            print(text.get('locationCurrent', [PLAYER.name, LOCATION.getShortDescription() ]), color='blue')
            CLOCK.printDescription()
            print('HP:', PLAYER.health, color='red', end=' ')
            print('MP:', PLAYER.mana, color='blue')
            PLAYER.printHungerAndExhaustion()

            if PLAYER.bounty > 0:
                print(f'Bounty: {PLAYER.bounty}', color='yellow')

            print(text.get('mapMenu'), color='white')
            
            select = input(text.get('selection'), color='cyan').lower()
            if select == 'c':
                print()
                print(text.get('titleCharacter'), color='blue')
                PLAYER.printCharacter()
                input(text.get('continue'), color='cyan')
            elif select == 'i':
                items.showInventoryMain(PLAYER, INVENTORY)
                PLAYER.armor  = INVENTORY.getTotalArmor()
                PLAYER.damage = INVENTORY.getTotalDamage()
                PLAYER.weight = INVENTORY.getTotalWeight()
                PLAYER.speed  = INVENTORY.getTotalSpeed(PLAYER.weight)
                PLAYER.moveSpeed = INVENTORY.getMoveSpeed(PLAYER.weight)
            elif select == 'r':
                LOCATION.showRest(PLAYER, INVENTORY)
            elif select == 'l':
                print()
                print(text.get('titleLook'), color='blue')
                if LOCATION:
                    LOCATION.printFullDescription(CLOCK)
                else:
                    print(text.get('descNothing'))
                input(text.get('continue'), color='cyan')
            elif select == 'n':
                loc = mapper.showMoveMain(PLAYER, INVENTORY, LOCATION, CLOCK)
                if loc:
                    LOCATION = loc
            elif select == 'm':
                magic.showMagicMain(PLAYER, INVENTORY)
            elif select == 'h':
                hunt.showHuntMain(PLAYER, INVENTORY, LOCATION)
            elif select == 't':
                print()
                print(text.get('titleTalk'), color='blue')
                if LOCATION:
                    print('Location:', LOCATION.name, color='blue')
                    if len(LOCATION.people) > 0:
                        print(text.get('lookPeople'))
                        for i,npc in enumerate(LOCATION.people):
                            print(' ', str(i) + ':', npc.getDescription(), end='', color='white' )
                            if npc.sleep[1] < CLOCK.getHours() < npc.sleep[0]:
                                print()
                            else:
                                print('(unavailable)', color='yellow')
                        
                        select = None
                        
                        while not select:
                            select = input(text.get('selection2'), color='cyan')

                            if select == 'b':
                                pass
                            else:
                                try:
                                    select = LOCATION.people[ int(select) ]
                                    if select.sleep[1] < CLOCK.getHours() < select.sleep[0]:
                                        response = dialogue.showDialogueMain(select.dialogue, select, PLAYER, INVENTORY, LOCATION)

                                        if response == 'trade':
                                            trade.showTradeMain(select, PLAYER, INVENTORY)
                                    else:
                                        print(text.get('npcUnavailable', [select.name]), color='yellow')
                                        select = None
                                except:
                                    print(text.get('invalidSelection'), color='red')
                                    select = None
                        
                #input(text.get('continue'), color='cyan')
            elif select == 's':
                loc = theft.showStealMain(CLOCK, LOCATION, PLAYER, INVENTORY)
                if loc:
                    LOCATION = loc
            elif select == 'j':
                quest.showJournalMain(PLAYER)
            elif select == 'q':
                mapMenu = False
            else:
                print(text.get('invalidSelection'), color='red')

            quest.showJournalUpdate(PLAYER)
            LOCATION.checkHostility(PLAYER, INVENTORY)
            LOCATION.checkBounty(PLAYER, INVENTORY)
            PLAYER.updateExperience()

            mapper.verifyLocations()
            mapper.updateTravelling(PLAYER)

            loc = PLAYER.updateTeleport(INVENTORY, LOCATION, CLOCK)
            if loc:
                LOCATION = loc
            elif PLAYER.updateConjure(INVENTORY):
                enc = encounter.getRandomConjure()
                enc(PLAYER, INVENTORY)
            elif PLAYER.updateDuplicate(INVENTORY):
                pass

            if PLAYER.health[0] <= 0:
                print(text.get('death', [PLAYER.name, PLAYER.pronoun[1]]), color='red')
                input(text.get('continue'), color='cyan')
                mapMenu = False
            else:
                if CLOCK.checkTimeAcc():
                    mapper.updateLocations()

                if PLAYER.status == 'jail':
                    PLAYER.status = None
                    theft.showJailMain(0, PLAYER, INVENTORY)
                elif PLAYER.exhaustion >= constant('playerExhaustionThreshold'):
                    time = random.randint(1, 4)

                    PLAYER.addRestTime(time, time * 0.5)
                    if PLAYER.hunger < constant('playerStarveThreshold'):
                        PLAYER.addMana(time * 5)
                        PLAYER.addHealth(time * 5)

                    print(text.get('characterExhaustion', [PLAYER.name]), color='red')
                    print(text.get('restComplete', [PLAYER.name, time, CLOCK.getTimeOfDay()]), color='blue')
                    input(text.get('continue'), color='cyan')

    elif select == 'l':
        print(text.get('unbuilt'))
    elif select == 'o':
        print(text.get('unbuilt'))
    elif select == 'a':
        print()
        print(text.get('about'), color='white')
        input(text.get('continue'), color='cyan')
    elif select == 'q':
        break
