import random

from lib import text
from lib import items
from lib import battle
from lib import entities
from lib import mapper
from lib import encounter
from lib import magic
from lib.constants import get as constant
from lib.colortext import colorprint as print
from lib.colortext import colorinput as input
from lib.colortext import colorstr

def showFightMain(player, inventory):
    while True:
        select = input(text.get('stealFailFight', [player.name]), color='cyan')

        if select == 'y' or select == 'yes':
            chance = -player.weight / 64 + player.skills[3] / 2 - player.bounty / 2000
            chance *= 100
            chance = int(chance) + random.randint(-10, 10)
            if chance >= 50:
                print(text.get('stealBountyEvade', [player.name]), color='blue')
            else:
                enc = encounter.getRandomGuard()
                enc(player, inventory)
            return True
        elif select == 'n' or select == 'no':
            return False
        else:
            print(text.get('invalidSelection'), color='red')

def showJailMain(value, player, inventory):
    player.addBounty(value)

    if showFightMain(player, inventory):
        if player.health[0] > 0:
            return

    jailInventory = items.Inventory()
    jailInventory.spells = inventory.spells
    jailInventory.equipItem(54)
    jailInventory.equipItem(106)

    player.armor  = jailInventory.getTotalArmor()
    player.damage = jailInventory.getTotalDamage()
    player.weight = jailInventory.getTotalWeight()
    player.speed  = jailInventory.getTotalSpeed(player.weight)

    dur = value * 2 + player.bounty
    fineMin = min(int(value/2), int(inventory.gold/2))
    fineMax = min(value, inventory.gold)
    fine = random.randint(fineMin, fineMax)
    location, dist = mapper.getNearestByLandmarkType(player, 'Jail')
    player.clock.add(dist)
    player.setPosition(location.x, location.y)
    inventory.gold -= fine
    player.setHunger(0)
    player.setExhaustion(0)

    print(text.get('stealJailStart', [location.name, dur // 24]), color='white')
    print(text.get('stealJailClothes', [player.name]), color='blue')
    print(text.get('stealJailFine', [fine]), color='yellow')
    input(text.get('continue'), color='cyan')

    while dur > 0:
        time = random.randint(24, 72)
        time = min(time, dur)

        roll = random.randint(0, 1)

        if roll == 0:
            print(text.get('stealJailUneventful', [time // 24]), color='blue')
        elif roll == 1:
            print(text.get('stealJailEventful', [time // 24]), color='blue')
            enc = encounter.getRandomJail()
            enc(player, jailInventory)

        if player.health[0] <= 0:
            print(text.get('stealJailDeath'), color='red')
            input(text.get('continue'), color='cyan')
            return

        dur -= time
        player.addHealth(time)
        player.addMana(time)

        while True:
            print()
            print(text.get('titleJail'), color='blue')
            print(text.get('stealJailRemaining', [player.name, dur // 24]), color='white')
            print(text.get('stealJailLocation', [player.name, location.name]), color='blue')
            print(text.get('stealJailMenu', [player.skills[3]]), color='white')
            select = input(text.get('selection'), color='cyan').lower()

            player.clock.add(time)

            if select == 'c':
                print()
                print(text.get('titleCharacter'), color='blue')
                player.printCharacter()
                input(text.get('continue'), color='cyan')
            elif select == 'i':
                items.showInventoryMain(player, jailInventory)
                player.armor  = jailInventory.getTotalArmor()
                player.damage = jailInventory.getTotalDamage()
                player.weight = jailInventory.getTotalWeight()
                player.speed  = jailInventory.getTotalSpeed(player.weight)
            elif select == 'm':
                magic.showMagicMain(player, jailInventory)
                loc = player.updateTeleport(inventory, location, player.clock)
                if loc:
                    return loc
            elif select == 'e':

                roll = random.randint(int(player.skills[3]/2), player.skills[3])
                if roll >= 50:
                    player.addBounty(constant('bountyEscape'))
                    print(text.get('stealJailEscapeSuccess', [player.name]), color='blue')
                    input(text.get('continue'), color='cyan')
                    return location
                else:
                    mod = random.randint(72, 240)
                    dur += mod
                    print(text.get('stealJailEscapeFail', [player.name]), color='yellow')
                    print(text.get('stealJailLonger', [player.name, mod // 24]), color='red')
                    input(text.get('continue'), color='cyan')

            elif select == 'w':
                break
            else:
                print(text.get('invalidSelection'), color='red')

    player.armor  = inventory.getTotalArmor()
    player.damage = inventory.getTotalDamage()
    player.weight = inventory.getTotalWeight()
    player.speed  = inventory.getTotalSpeed(player.weight)

    for i in jailInventory.bag:
        inventory.addItem(i)

    print(text.get('stealJailComplete', [player.name, player.pronoun[1]]), color='white')

    inventory.gold -= player.bounty
    inventory.gold = max(0, inventory.gold)

    player.bounty = 0

    input(text.get('continue'), color='cyan')
    return location

def showBribeMain(value, npc, player, inventory):
    if npc.takesBribe:
        print(text.get('stealBribe', [npc.name]), color='blue')
        bribe = value * 2.5 - value * (npc.mood / 100) - value * (npc.opinion / 100)
        bribe = int(bribe)

        if inventory.gold >= bribe:
            continueBribe = True
            while continueBribe:
                confirm = input(text.get('stealBribe2', [bribe]), color='cyan').lower()
                if confirm == 'y' or confirm == 'yes':
                    inventory.gold -= bribe
                    npc.gold += bribe
                    print(text.get('stealBribeComplete', [npc.name, bribe]), color='red')
                    continueBribe = None
                    input(text.get('continue'), color='cyan')
                elif confirm == 'n' or confirm == 'no':
                    continueBribe = None
                    player.addBount(constant('bountyTheft'))
                    return showJailMain(value, player, inventory)
                else:
                    print(text.get('invalidSelection'), color='red')
        else:
            print(text.get('stealBribeFail2', [player.name, npc.name]), color='red')
            input(text.get('continue'), color='cyan')
            return showJailMain(value, player, inventory)
    else:
        print(text.get('stealBribeFail1', [player.name, npc.name]), color='yellow')
        input(text.get('continue'), color='cyan')
        return showJailMain(value, player, inventory)

def showStealMain(clock, location, player, inventory):
    print(text.get('titleSteal'), color='blue')
    continueSteal = True
    while continueSteal:
        print()

        continueSelectPerson = True
        while continueSelectPerson:
            for i, person in enumerate(location.people):
                if person.sleep[1] < clock.getHours() < person.sleep[0]:
                    print(f'{i}: {person.name} - Pickpocket {player.skills[6]}', color='white')
                else:
                    print(f'{i}: {person.name} - Lockpick {player.skills[7]}', color='white')

            person = None
            select = input(text.get('selection2'), color='cyan').lower()

            if select == 'b':
                continueSelectPerson = None
                continueSteal = None
            else:
                try:
                    person = location.people[int(select)]
                except:
                    print(text.get('invalidSelection'), color='red')

                if person:
                    print(f'\n{person.name} items:', color='white')
                    for i, v in enumerate(person.items):
                        item = items.getItem(v)
                        print(f'  {i}: {item.getColorString()}', color='white')
                    print(f'  {len(person.items)}:', end='', color='white')
                    print(f'Gold {person.gold}', color='yellow')

                continueSelectItem = True

                while continueSelectItem:
                    item = None
                    select = input(text.get('selection2'), color='cyan').lower()

                    if select == 'b':
                        item = None
                        continueSelectItem = None
                    else:
                        try:
                            select = int(select)
                        except:
                            item = None
                            print(text.get('invalidSelection'), color='red')

                        if select == len(person.items):
                            continueConfirm = True
                            while continueConfirm:
                                gold = 0

                                if person.sleep[1] < clock.getHours() < person.sleep[0]:
                                    print(text.get('stealPickpocket', ['gold coins']), color='blue')
                                    gold = random.randint(0, min(5 + player.skills[6], person.gold))
                                else:
                                    print(text.get('stealLockpick', ['gold coins']), color='blue')
                                    gold = random.randint(0, min(5 + player.skills[7], person.gold))

                                itemName = str(gold) + ' gold coins'
                                confirm = input().lower()

                                if confirm == 'y' or confirm == 'yes':
                                    chance = 0
                                    if person.sleep[1] < clock.getHours() < person.sleep[0]:
                                        chance = player.skills[6] / 128 - gold / 256 + player.skills[3] / 256
                                    else:
                                        chance = player.skills[7] / 128 - gold / 256 + player.skills[3] / 256
                                    chance *= 100
                                    chance += random.randint(-8, 8)

                                    if chance >= 50:
                                        print(text.get('stealComplete', [player.name, itemName]), color='blue')
                                        person.gold -= gold
                                        inventory.gold += gold
                                    elif chance >= 25:
                                        print(text.get('stealFail1', [player.name, itemName]), color='yellow')
                                    else:
                                        print(text.get('stealFail2', [player.name, itemName, person.name]), color='red')
                                        mod = min(25, int(gold / 2))
                                        person.opinion -= mod
                                        person.mood -= mod
                                        location.lowerPeopleOpinion(mod)
                                        return showBribeMain(gold, person, player, inventory)

                                    input(text.get('continue'), color='cyan')

                                    continueSelectItem = None
                                    continueConfirm = None
                                elif confirm == 'n' or confirm == 'no':
                                    continueSelectItem = None
                                    continueConfirm = None
                                else:
                                    print(text.get('invalidSelection'), color='red')
                        else:
                            try:
                                item = items.getItem(person.items[select])
                            except:
                                item = None
                                print(text.get('invalidSelection'), color='red')

                            if item:
                                continueConfirm = True
                                while continueConfirm:
                                    if person.sleep[1] < clock.getHours() < person.sleep[0]:
                                        print(text.get('stealPickpocket', [item.name]), color='blue')
                                    else:
                                        print(text.get('stealLockpick', [item.name]), color='blue')
                                    confirm = input().lower()

                                    if confirm == 'y' or confirm == 'yes':
                                        chance = 0
                                        if person.sleep[1] < clock.getHours() < person.sleep[0]:
                                            chance = player.skills[6] / 128 - item.weight / 32 - item.value / 1000 + player.skills[3] / 256
                                        else:
                                            chance = player.skills[7] / 128 - item.weight / 32 - item.value / 1000 + player.skills[3] / 256
                                        chance *= 100
                                        chance += random.randint(-8, 8)

                                        if chance >= 50:
                                            print(text.get('stealComplete', [player.name, item.name]), color='blue')
                                            inventory.bag.append( person.items.pop(int(select)) )
                                        elif chance >= 25:
                                            print(text.get('stealFail1', [player.name, item.name]), color='yellow')
                                        else:
                                            print(text.get('stealFail2', [player.name, item.name, person.name]), color='red')
                                            roll = random.randint( int(player.skills[9]/2), player.skills[9])
                                            if roll > item.value / 5:
                                                print(text.get('stealSpeech', [player.name, player.pronoun[1]]), color='white')
                                            else:
                                                mod = min(25, int(item.value / 2))
                                                person.opinion -= mod
                                                person.mood -= mod
                                                location.lowerPeopleOpinion(mod)
                                                return showBribeMain(item.value, person, player, inventory)

                                        input(text.get('continue'))

                                        continueSelectItem = None
                                        continueConfirm = None
                                    elif confirm == 'n' or confirm == 'no':
                                        continueSelectItem = None
                                        continueConfirm = None
                                    else:
                                        print(text.get('invalidSelection'), color='red')

