import random
from lib.constants import get as constant
from lib import text
from lib import encounter
from lib import items
from lib import character
from lib import magic
from lib import quest
from lib import mapper
from lib import loot

from lib.colortext import colorprint as print
from lib.colortext import colorinput as input
from lib.colortext import colorstr

FISH_LOCATIONS = ('large river', 'small river', 'creek', 'large lake', 'small lake', 'pond', 'waterfall', 'marsh', 'cottage in the woods')

def showHuntForage(player, inventory):
    continueForage = True

    while continueForage:
        time = random.randint(30, 180)
        time = round(time / 60, 1)
        player.addTime(time)
        print(text.get('huntForageIntro', [player.name, time]), color='blue')
        input(text.get('continue'), color='cyan')

        roll = random.randint(0,12)

        if roll < 3:
            print(text.get('huntForageFail',[player.name]), color='yellow')
        else:
            i = 129
            if roll == 4:
                i = 131
            elif roll == 5:
                i = 132
            elif roll == 6:
                i = 133
            elif roll == 7:
                i = 134
            elif roll == 8:
                i = 136
            elif roll == 9:
                i = 137
            elif roll == 10:
                i = 138
            elif roll == 11:
                i = 139
            elif roll == 12:
                i = 140
            elif roll == 13:
                i = 191
            elif roll == 14:
                i = 196
            item = items.getItem(i)
            count = random.randint(1,3)
            print(text.get('huntForageFind', [player.name, count, item.name]), color='blue')
            for num in range(count):
                inventory.bag.append(i)

        while True:
            select = input(text.get('huntForageContinue', [player.name]), color='cyan').lower()

            if select == 'y' or select == 'yes':
                break
            elif select == 'n' or select == 'no':
                print(text.get('huntForageComplete', [player.name, player.pronoun[1]]))
                input(text.get('continue'), color='cyan')
                continueForage = False
                break
            else:
                print(text.get('invalidSelection'), color='red')

def showHuntFish(player, inventory):
    if not 218 in inventory.bag:
        print(text.get('huntFishPoleFail', [player.name]), color='yellow')
        input(text.get('continue'), color='cyan')
        return

    locType = random.choice(FISH_LOCATIONS)
    hookBait = False
    fishQuantity = random.randint(0, 10)

    def checkBait():
        if hookBait:
            print(text.get('huntFishBait'), color='blue')
        else:
            print(text.get('huntFishNoBait'), color='yellow')

    def checkFishLevel():
        if fishQuantity <= 0:
            print(text.get('huntFishLevel0'))
            return True
        elif fishQuantity <= 3:
            print(text.get('huntFishLevel0'))
        elif fishQuantity <= 5:
            print(text.get('huntFishLevel1'))
        elif fishQuantity <= 7:
            print(text.get('huntFishLevel2'))
        else:
            print(text.get('huntFishLevel3'))

    print(text.get('huntFishIntro', [player.name, player.pronoun[1]]), color='blue')
    print(text.get('huntFishLocation', [player.name, locType]), color='white')
    input(text.get('continue'), color='cyan')

    continueFish = True
    while continueFish:
        print(text.get('huntFishLocation', [player.name, locType]), color='white')
        checkBait()
        checkFishLevel()
        print(text.get('huntFishCastMenu'), color='white')
        select = input(text.get('selection'), color='cyan').lower()

        if select == 'b':
            if hookBait:
                inventory.bag.append(129)
            return
        elif select == 'h':
            if 129 in inventory.bag:
                while True:
                    confirm = input(text.get('huntFishBaitConfirm'), color='cyan').lower()
                    if confirm == 'y' or confirm == 'yes':
                        hookBait = True
                        inventory.bag.remove(129)
                        break
                    elif confirm == 'n' or confirm == 'no':
                        break
                    else:
                        print(text.get('invalidSelection'), color='red')
            else:
                print(text.get('huntFishBaitFail',[player.name]), color='yellow')
                input(text.get('continue'), color='cyan')
        elif select == 'c':
            if hookBait:
                print(text.get('huntFishCast', [player.name]), color='white')
                dist = random.randint(5, 25)
                print(text.get('huntFishCast2', [dist]), color='blue')
                input(text.get('continue'), color='cyan')

                continueCast = True
                while continueCast:
                    print(text.get('huntFishLocation', [player.name, locType]), color='white')
                    checkBait()
                    checkFishLevel()
                    print(text.get('huntFishWaitMenu'), color='white')
                    select = input(text.get('selection'))
                    if select == 'b':
                        continueCast = False
                    elif select == 'r':
                        print(text.get('huntFishCast', [player.name]), color='white')
                        dist = random.randint(5, 25)
                        print(text.get('huntFishCast2', [dist]), color='blue')
                        input(text.get('continue'), color='cyan')
                    elif select == 'w':
                        time = random.randint(5, 60)
                        time = round(time / 60, 1)
                        player.addTime(time)
                        print(text.get('huntFishWait', [player.name, player.pronoun[1], time]))
                        input(text.get('continue'), color='cyan')
                        roll = random.randint(0, 25)
                        if roll < 3:
                            print(text.get('huntFishEscape'), color='red')
                            input(text.get('continue'), color='cyan')
                            hookBait = False
                            continueCast = False
                        elif dist >= roll:
                            print(text.get('huntFishBite', [player.name]), color='white')
                            inventory.applyLootList(player, loot.get('trap2'))
                            continueCast = False
                        else:
                            print(text.get('huntFishNoBite'), color='yellow')
                            input(text.get('continue'), color='cyan')
                    else:
                        print(text.get('invalidSelection'), color='red')
            else:
                print(text.get('huntFishNoBait'), color='yellow')
                input(text.get('continue'), color='cyan')
        elif select == 'n':
            while True:
                confirm = input(text.get('huntFishMove'), color='cyan').lower()
                if confirm == 'y' or confirm == 'yes':
                    locType = random.choice(FISH_LOCATIONS)
                    fishQuantity = random.randint(0, 10)
                    print(text.get('huntFishMoveDone', [player.name, locType]))
                    break
                elif confirm == 'n' or confirm == 'no':
                    break
                else:
                    print(text.get('invalidSelection'), color='red')
        else:
            print(text.get('invalidSelection'), color='red')

def showHuntTrap(player, inventory, traps):
    trapSizes = ('small', 'medium', 'large')
    lootLists = (
        loot.get('trap1'),
        loot.get('trap2'),
        loot.get('trap3')
    )

    def addTrap(size=1):
        player.clock.time += (size + 1)
        print(text.get('huntTrapTime2', [player.name, size + 1, trapSizes[size]]), color='yellow')
        time = player.clock.time + random.randint(3, 48)
        traps.append((time, size))
        input(text.get('continue'), color='cyan')

    continueTrap = True

    while continueTrap:
        if len(traps) == 1:
            print(text.get('huntTrapCount1'), color='blue')
        else:
            print(text.get('huntTrapCount', [len(traps)]), color='blue')

        print(text.get('huntTrapMenu'), color='white')

        select = input(text.get('selection2'), color='cyan').lower()

        if select == 'b':
            return
        elif select == 'c':
            count = 0
            time = 0.0
            complete = []
            for trap in reversed(traps):
                count += 1
                time += 0.5
                if player.clock.time >= trap[0]:
                    complete.append(trap)
                    traps.remove(trap)
            player.addTime(time)

            print(text.get('huntTrapTime', [time, count]), color='yellow')

            if len(complete) > 0:

                exp = 0
                gold = 0
                stuff = []

                for trap in complete:
                    lootList = lootLists[trap[1]]
                    exp   += lootList.getExp()
                    gold  += lootList.getGold()
                    stuff += lootList.getItems()

                player.addExperience(exp)
                inventory.addGold(gold)
                for i in stuff:
                    inventory.addItem(i)

                print(text.get('huntTrapComplete', [player.name, exp, gold]), color='yellow')

                for i in stuff:
                    item = items.getItem(i)
                    print(f'  {item.getColorString()}')
            else:
                print(text.get('huntTrapFail'), color='red')

            input(text.get('continue'), color='cyan')

            print(text.get('huntTrapActive'), color='blue')
            for i, trap in enumerate(traps):
                size = trapSizes[trap[1]]
                print(f'  {i}: {size}')
            input(text.get('continue'), color='cyan')
        elif select == 's':

            while True:
                print(text.get('huntTrapSetupMenu'), color='white')

                select = input(text.get('selection2'), color='cyan').lower()

                if select == 'b':
                    break
                elif select == '0':
                    addTrap(0)
                elif select == '1':
                    addTrap(1)
                elif select == '2':
                    addTrap(2)
                else:
                    print(text.get('invalidSelection'), color='red')

        elif select == 'd':
            while True:
                print(text.get('huntTrapActive'), color='white')
                for i, trap in enumerate(traps):
                    size = trapSizes[trap[1]]
                    print(f'  {i}: {size}', color='white')

                select = input(text.get('huntTrapDismantle'), color='cyan').lower()

                trap = None

                if select == 'b':
                    break
                else:
                    try:
                        trap = traps[int(select)]
                    except:
                        print(text.get('invalidSelection'), color='red')

                if trap:
                    size = trapSizes[trap[1]]
                    traps.remove(trap)
                    print(text.get('huntTrapDismantleComplete', [player.name, size]), color='blue')
        else:
            print(text.get('invalidSelection'), color='red')

def showHuntPrey(player, inventory):
    if inventory.primary > 0:
        item = items.getItem(inventory.primary)
        if item.type == 'weapon':
            if item.skill != 'Ranged':
                print(text.get('huntUnavailable', [player.name]), color='red')
                input(text.get('continue'), color='cyan')
                return
        else:
            print(text.get('huntUnavailable', [player.name]), color='red')
            input(text.get('continue'), color='cyan')
            return
    else:
        print(text.get('huntUnavailable', [player.name]), color='red')
        input(text.get('continue'), color='cyan')
        return

    continueHunt = True
    while continueHunt:
        print()

        roll = random.randint(1, 100)

        roll += (player.skills[2] + player.skills[3]) / 2

        time = random.randint(4,12)
        time = round(time / 6, 1)

        player.addTime(time)

        print(text.get('huntPreyTime', [player.name, time]), color='yellow')

        if roll <= constant('huntChanceFailure'):
            print(text.get('huntPreyFailure'), color='red')
            input(text.get('continue'), color='cyan')
        elif roll <= constant('huntChanceFailure') + constant('huntChanceEncounter'):
            enc = encounter.getRandomHunt()
            enc(player, inventory)
        else:
            enc = encounter.getRandomHuntSuccess()
            enc(player, inventory)

        while True:
            select = input(text.get('huntPreyContinue', [player.name]), color='cyan').lower()

            if select == 'y' or select == 'yes':
                break
            elif select == 'n' or select == 'no':
                print(text.get('huntPreyComplete', [player.name, player.pronoun[1], player.clock.getTimeOfDay()]), color='blue')
                input(text.get('continue'), color='cyan')
                return
            else:
                print(text.get('invalidSelection'), color='red')

def showHuntMain(player, inventory, location):
    traps = []

    print(text.get('huntIntro', [player.name, location.name]), color='blue')
    input(text.get('continue'), color='cyan')

    continueHunt = True

    while continueHunt:
        print()
        print(text.get('titleHunt'), color='blue')
        print(text.get('locationCurrent', [player.name, location.name + ' Wilderness' ]), color='blue')
        player.clock.printDescription()
        print('HP:', player.health, color='red', end=' ')
        print('MP:', player.mana, color='blue')
        player.printHungerAndExhaustion()

        if player.bounty > 0:
            print(f'Bounty: {player.bounty}', color='yellow')

        print(text.get('huntMenu'), color='white')
        select = input(text.get('selection'), color='cyan')

        if select == 'c':
            print()
            print(text.get('titleCharacter'), color='blue')
            player.printCharacter()
            input(text.get('continue'), color='cyan')
        elif select == 'i':
            items.showInventoryMain(player, inventory)
            player.armor  = inventory.getTotalArmor()
            player.damage = inventory.getTotalDamage()
            player.weight = inventory.getTotalWeight()
            player.speed  = inventory.getTotalSpeed(player.weight)
            player.moveSpeed = inventory.getMoveSpeed(player.weight)
        elif select == 'm':
            magic.showMagicMain(player, inventory)
        elif select == 'r':
            location.showRest(player, inventory, 0.6, True)
        elif select == 'f':
            showHuntFish(player, inventory)
        elif select == 't':
            showHuntTrap(player, inventory, traps)
        elif select == 'h':
            showHuntPrey(player, inventory)
        elif select == 's':
            showHuntForage(player, inventory)
        elif select == 'q':
            print(text.get('huntComplete', [player.name, player.pronoun[1], location.name]), color='blue')
            input(text.get('continue'), color='cyan')
            return

        quest.showJournalUpdate(player)
        player.updateExperience()

        mapper.verifyLocations()
        mapper.updateTravelling(player)

        loc = player.updateTeleport(inventory, location, player.clock)
        if loc:
            return loc
        elif player.updateConjure(inventory):
            enc = encounter.getRandomConjure()
            enc(player, inventory)
        elif player.updateDuplicate(inventory):
            pass

        if player.health[0] <= 0:
            return
        elif player.clock.checkTimeAcc():
            mapper.updateLocations()


