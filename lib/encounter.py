from lib import entities
from lib import battle
from lib import text
from lib import items
from lib.npc import NPC
from lib import dialogue
from lib import names
from lib import theft
from lib.constants import get as constant
from lib import loot

from lib.colortext import colorprint as print
from lib.colortext import colorinput as input
from lib.colortext import colorstr

import random

def encounter1(player, inventory):
    l = player.level + 1
    creature1 = entities.Creature('Bandit', 50 + (l*15), 2 * l, 15 + 2 * int(l/2), 8, 0, 'bandit1', 'not much.')
    creature2 = entities.Creature('Bandit', 50 + (l*15), 2 * l, 15 + 2 * int(l/2), 8, 0, 'bandit1', 'not much.')
    print(text.get('encounterBandit2'), color='white')
    input(text.get('continue'), color='cyan')
    battle.showBattleMain(player, inventory, [creature1, creature2])

def encounter2(player, inventory):
    l = player.level + 1
    creature1 = entities.Creature('Wild Dog', 35 * l, 2 * l, 10 + 2 * int(l/2), 9, 0, 'animal1', 'not much.')
    creature2 = entities.Creature('Mongrel', 40 * l, 2 * l, 12 + 2 * int(l/2), 9, 0, 'animal1', 'not much.')
    print(text.get('encounterDog1'), color='white')
    input(text.get('continue'), color='cyan')
    battle.showBattleMain(player, inventory, [creature1, creature2])
    
def encounter3(player, inventory):
    l = player.level + 1
    creature1 = entities.Creature('Horseman Bandit', 60 * l, 2 * l, 15 + 2 * int(l/2), 9, 0, 'bandit1', 'not much.')
    print(text.get('encounterBandit1'), color='white')
    input(text.get('continue'), color='cyan')
    battle.showBattleMain(player, inventory, [creature1])

def encounter4(player, inventory):
    l = player.level + 1
    creature1 = entities.Creature('Viking', 50 * l, 2 * l, 15 + 2 * int(l/2), 9, 0, 'bandit1', 'not much.')
    creature2 = entities.Creature('Viking Leader', 60 * l, 2 * l, 20 + 2 * int(l/2), 9, 0, 'bandit1', 'not much.')
    creature3 = entities.Creature('Viking', 50 * l, 2 * l, 15 + 2 * int(l/2), 9, 0, 'bandit1', 'not much.')
    print(text.get('encounterViking1'), color='white')
    input(text.get('continue'), color='cyan')
    battle.showBattleMain(player, inventory, [creature1, creature2, creature3])

def encounter5(player, inventory):
    print(text.get('encounterMonster1'), color='white')
    input(text.get('continue'), color='cyan')
    creature1 = entities.Creature('Minotaur', 75, 5, 15, 8, 0, 'bandit1', 'not much.')
    battle.showBattleMain(player, inventory, [creature1])

def encounter6(player, inventory):
    creature1 = entities.Creature('Stag', 35, 5, 8, 9, 0, 'animal1', 'not much.')
    print(text.get('encounterAnimal1', [creature1.name]), color='white')
    input(text.get('continue'), color='cyan')
    battle.showBattleMain(player, inventory, [creature1])

def encounter7(player, inventory):
    creature1 = entities.Creature('Boar', 35, 5, 10, 9, 0, 'animal1', 'not much.')
    print(text.get('encounterAnimal1', [creature1.name]), color='white')
    input(text.get('continue'), color='cyan')
    battle.showBattleMain(player, inventory, [creature1])

def encounter8(player, inventory):
    creature1 = entities.Creature('Boar', 25, 5, 10, 9, 0, 'animal1', 'not much.')
    creature2 = entities.Creature('Boar', 35, 5, 10, 9, 0, 'animal1', 'not much.')
    creature3 = entities.Creature('Boar', 25, 5, 10, 9, 0, 'animal1', 'not much.')
    print(text.get('encounterAnimal2', [creature1.name]), color='white')
    input(text.get('continue'), color='cyan')
    battle.showBattleMain(player, inventory, [creature1, creature2, creature3])

def encounter9(player, inventory):
    creature1 = entities.Creature('Bandit', 25, 5, 10, 9, 0, 'bandit1', 'not much.')

    print(text.get('encounterBandit3', [creature1.name]), color='white')
    input(text.get('continue'), color='cyan')
    battle.showBattleMain(player, inventory, [creature1])

def encounter10(player, inventory):
    creature1 = entities.Creature('Bandit', 25, 5, 10, 9, 0, 'bandit1', 'not much.')
    creature2 = entities.Creature('Bandit', 25, 5, 10, 9, 0, 'bandit1', 'not much.')

    print(text.get('encounterBandit4'), color='white')
    input(text.get('continue'), color='cyan')
    battle.showBattleMain(player, inventory, [creature1, creature2])

#HUNT
def encounterHunt1(player, inventory):
    creature1 = entities.getLeveledCreatureEasy(player, 'Rabid Badger', 'animal1')
    creature2 = entities.getLeveledCreatureEasy(player, 'Rabid Badger', 'animal1')
    creature3 = entities.getLeveledCreatureEasy(player, 'Rabid Badger', 'animal1')

    print(text.get('encounterHunt1', [player.name]), color='white')
    input(text.get('continue'), color='cyan')
    battle.showBattleMain(player, inventory, [creature1, creature2, creature3])

def encounterHunt2(player, inventory):
    creature1 = entities.getLeveledCreatureNormal(player, 'Wounded Elk', 'animal1')
    creature1.addHealth(-10)

    print(text.get('encounterHunt2', [player.name]), color='white')
    input(text.get('continue'), color='cyan')
    battle.showBattleMain(player, inventory, [creature1])

def encounterHunt3(player, inventory):
    creature1 = entities.getLeveledCreatureHard(player, 'Sabre Cat', 'animal1')

    print(text.get('encounterHunt3', [player.name]), color='white')
    input(text.get('continue'), color='cyan')
    battle.showBattleMain(player, inventory, [creature1])

def encounterHunt4(player, inventory):
    creature1 = entities.getLeveledCreatureNormal(player, 'Wild Stag', 'animal1')

    print(text.get('encounterHunt4', [player.name]), color='white')
    input(text.get('continue'), color='cyan')
    battle.showBattleMain(player, inventory, [creature1])

def encounterHunt5(player, inventory):
    creature1 = entities.getLeveledCreatureNormal(player, 'Bear', 'animal1')

    print(text.get('encounterHunt5', [player.name]), color='white')
    input(text.get('continue'), color='cyan')
    battle.showBattleMain(player, inventory, [creature1])

def encounterHunt6(player, inventory):
    print(text.get('encounterHunt6', [player.name, player.pronoun[1]]), color='white')
    while True:
        select = input().lower()
        if select == 'y' or 'yes':
            print(text.get('encounterHunt6a', [player.name, player.pronoun[1]]), color='white')

            creature1 = entities.getLeveledCreatureNormal(player, 'Bandit')
            creature2 = entities.getLeveledCreatureNormal(player, 'Bandit')
            creature3 = entities.getLeveledCreatureNormal(player, 'Bandit')

            battle.showBattleMain(player, inventory, [creature1, creature2, creature3])
            break
        elif select == 'n' or 'no':
            print(text.get('encounterHunt6a', [player.name]), color='white')
            input(text.get('continue'), color='cyan')
            break
        else:
            print(text.get('invalidSelection'), color='red')

def encounterHuntSucceed1(player, inventory):
    print(text.get('encounterHuntSuccess1', [player.name]), color='white')
    input(text.get('continue'), color='cyan')
    inventory.applyLootList(player, loot.get('trap2'))

#JAIL
def encounterJail1(player, inventory):
    creature1 = None

    if random.randint(0, 1) == 1:
        creature1 = entities.Creature('Murderer', 30, 5, 10, 8, 0, 'jail1', 'not much.')
    else:
        creature1 = entities.Creature('Gang Boss', 35, 5, 10, 8, 0, 'jail1', 'not much.')

    print(text.get('encounterJail1', [creature1.name]), color='white')
    input(text.get('continue'), color='cyan')
    battle.showBattleMain(player, inventory, [creature1])

def encounterJail2(player, inventory):
    creature1 = entities.Creature('Addict', 15, 5, 10, 10, 0, 'jail1', 'not much.')
    creature2 = entities.Creature('Addict', 20, 5, 10, 10, 0, 'jail1', 'not much.')
    creature3 = entities.Creature('Addict', 15, 5, 10, 10, 0, 'jail1', 'not much.')

    print(text.get('encounterJail2'), color='white')
    input(text.get('continue'), color='cyan')
    battle.showBattleMain(player, inventory, [creature1, creature2, creature3])

    roll = random.randint(0, 3)
    i = 8

    if roll == 1:
        i = 138
    elif roll == 2:
        i = 56
    elif roll == 3:
        i = 146

    inventory.addItem(i)
    item = items.getItem(i)

    print(text.get('stealJailItem', [item.name]), color='white')
    input(text.get('continue'), color='cyan')

def encounterJail3(player, inventory):
    creature1 = entities.Creature('Cobra', 15, 5, 10, 10, 0, 'jail1', 'not much.')

    print(text.get('encounterJail3', [player.name, player.pronoun[1]]), color='white')
    input(text.get('continue'), color='cyan')
    battle.showBattleMain(player, inventory, [creature1])

def encounterJail4(player, inventory):
    creature1 = entities.Creature('Cell Boss', 30, 5, 10, 10, 0, 'jail1', 'not much.')
    creature2 = entities.Creature('Convict', 20, 5, 10, 10, 0, 'jail1', 'not much.')

    print(text.get('encounterJail4', [player.name]), color='white')
    input(text.get('continue'), color='cyan')
    battle.showBattleMain(player, inventory, [creature1, creature2])

    roll = random.randint(0, 3)
    i = 130

    if roll == 1:
        i = 131
    elif roll == 2:
        i = 108
    elif roll == 3:
        i = 95

    inventory.equipItem(i)
    item = items.getItem(i)

    print(text.get('stealJailItem', [item.name]), color='white')
    input(text.get('continue'), color='cyan')

def encounterJail5(player, inventory):
    creature1 = None

    roll1 = random.randint(0,3)

    if roll1 == 0:
        creature1 = entities.Creature('Convict', 15, 5, 10, 10, 0, 'jail1', 'not much.')
    elif roll1 == 1:
        creature1 = entities.Creature('Thug', 25, 5, 10, 10, 0, 'jail1', 'not much.')
    elif roll1 == 2:
        creature1 = entities.Creature('Strangler', 25, 5, 10, 10, 0, 'jail1', 'not much.')
    elif roll1 == 3:
        creature1 = entities.Creature('Addict', 15, 5, 10, 10, 0, 'jail1', 'not much.')

    print(text.get('encounterJail5', [player.name, player.pronoun[1], creature1.name]), color='white')
    input(text.get('continue'), color='cyan')
    battle.showBattleMain(player, inventory, [creature1])

    roll = random.randint(0, 3)
    i = 116

    if roll == 1:
        i = 130
    elif roll == 2:
        i = 135
    elif roll == 3:
        i = 137

    inventory.equipItem(i)
    item = items.getItem(i)

    print(text.get('stealJailItem', [item.name]), color='white')
    input(text.get('continue'), color='cyan')

def encounterJail6(player, inventory):
    roll = random.randint(0, 3)
    i = 146

    if roll == 1:
        i = 1
    elif roll == 2:
        i = 131
    elif roll == 3:
        i = 145

    inventory.equipItem(i)
    item = items.getItem(i)

    print(text.get('encounterJail6', [player.name, item.name]), color='white')
    input(text.get('continue'), color='cyan')

def encounterJail7(player, inventory):
    roll = random.randint(0, 3)
    i = 136

    if roll == 1:
        i = 128
    elif roll == 2:
        i = 78
    elif roll == 3:
        i = 96

    inventory.equipItem(i)
    item = items.getItem(i)

    print(text.get('encounterJail7', [player.name]), color='white')
    print(text.get('loot', [player.name, item.name]), color='white')
    input(text.get('continue'), color='cyan')

#CONJURE
def encounterConjure1(player, inventory):
    creature1 = None
    roll = random.randint(0, 3)

    if roll == 1:
        creature1 = entities.Creature('Demon', 50, 5, 10, 9, 0, 'conjure1', 'not much.')
    elif roll == 2:
        creature1 = entities.Creature('Spectre', 50, 5, 10, 9, 0, 'conjure1', 'not much.')
    elif roll == 3:
        creature1 = entities.Creature('Ghost', 50, 5, 10, 9, 0, 'conjure1', 'not much.')
    else:
        creature1 = entities.Creature('Apparition', 50, 5, 10, 9, 0, 'conjure1', 'not much.')

    print(text.get('encounterConjure1', [creature1.name]), color='white')
    input(text.get('continue'), color='cyan')
    battle.showBattleMain(player, inventory, [creature1])

#MERCHANT
def encounterMerchant1(player, inventory):
    npc = NPC(names.getRandom('NPCmale'), 6, 'm')

    print(text.get('encounterMerchant1'), color='white')
    input(text.get('continue'), color='cyan')

#GUARD
def encounterGuard1(player, inventory):
    print(text.get('encounterGuard1', [player.name]), color='white')
    input(text.get('continue'), color='cyan')

    guards = []

    for i in range(random.randint(1,3)):
        guards.append(entities.Creature('Guard', 75, 5, 10, 9, 0, 'villager1', 'not much.'))

    battle.showBattleMain(player, inventory, guards)

    for guard in guards:
        if guard.health[0] <= 0:
            player.addBounty(constant('bountyMurder'))

#BOUNTY
def encounterBounty1(player, inventory):
    print(text.get('encounterBounty1', [player.name]), color='white')

    npc = NPC('Guard', 8, 'm', None, 'bounty1')

    if random.randint(0,1) == 1:
        npc.takesBribe = True

    opinionMin = int(player.bounty / -20)
    opinionMax = int(player.bounty / -10)

    opinionMin = max(-100, min(-50, opinionMin))
    opinionMax = max(-51, min(-25, opinionMax))

    npc.opinion = random.randint(opinionMin, opinionMax)

    dialogue.showDialogueMain(npc.dialogue, npc, player, inventory)

    if npc.battle:

        player.addbounty(constant('bountyAssault'))

        guards = []

        for i in range(random.randint(1,2)):
            guards.append(entities.Creature('Guard', 75, 5, 10, 9, 0, 'villager1', 'not much.'))

        battle.showBattleMain(player, inventory, guards)

        for guard in guards:
            if guard.health[0] <= 0:
                player.addBounty(constant('bountyMurder'))

    input(text.get('continue'), color='blue')

#CITY
def encounterCity1(player, inventory):
    maxGold = min(constant('eventMaxGoldTheft'), int(inventory.gold / 10))
    gold = random.randint(0, maxGold)
    chase = False

    while True:
        select = input(text.get('encounterCity1', [player.name, gold]), color='cyan')
        if select == 'y' or select == 'yes':
            chase = True
            break
        elif select == 'n' or select == 'no':
            break
        else:
            print(text.get('invalidSelection'), color='red')

    if chase:
        if random.randint(0,1):
            inventory.addGold(-gold)
            print(text.get('encounterCity1b', [player.name]), color='blue')
            input(text.get('continue'), color='cyan')
            enemies = []
            for i in range(random.randint(2, 3)):
                enemies.append(entities.Creature('Thug', 75, 5, 10, 9, 0, 'villager1', 'not much.'))
            battle.showBattleMain(player, inventory, enemies)
        else:
            print(text.get('encounterCity1a', [player.name, gold]), color='blue')
            input(text.get('continue'), color='cyan')
    else:
        inventory.addGold(-gold)
        print(text.get('encounterCity1c', [player.name]), color='blue')
        input(text.get('continue'), color='cyan')


ENCOUNTER = []
JAIL_ENCOUNTER = []
CONJURE_ENCOUNTER = []
GUARD_ENCOUNTER = []
BOUNTY_ENCOUNTER = []
HUNT_ENCOUNTER = []
HUNT_SUCCESS_ENCOUNTER = []
CITY_ENCOUNTER = []

ENCOUNTER.append(encounter1)
ENCOUNTER.append(encounter2)
ENCOUNTER.append(encounter3)
ENCOUNTER.append(encounter4)
ENCOUNTER.append(encounter5)
ENCOUNTER.append(encounter6)
ENCOUNTER.append(encounter7)
ENCOUNTER.append(encounter8)
ENCOUNTER.append(encounter9)
ENCOUNTER.append(encounter10)

JAIL_ENCOUNTER.append(encounterJail1)
JAIL_ENCOUNTER.append(encounterJail2)
JAIL_ENCOUNTER.append(encounterJail3)

CONJURE_ENCOUNTER.append(encounterConjure1)

GUARD_ENCOUNTER.append(encounterGuard1)

BOUNTY_ENCOUNTER.append(encounterBounty1)

HUNT_ENCOUNTER.append(encounterHunt1)
HUNT_ENCOUNTER.append(encounterHunt2)
HUNT_ENCOUNTER.append(encounterHunt3)
HUNT_ENCOUNTER.append(encounterHunt4)
HUNT_ENCOUNTER.append(encounterHunt5)
HUNT_ENCOUNTER.append(encounterHunt6)

HUNT_SUCCESS_ENCOUNTER.append(encounterHuntSucceed1)

CITY_ENCOUNTER.append(encounterCity1)

def getRandom():
    return random.choice(ENCOUNTER)

def getRandomJail():
    return random.choice(JAIL_ENCOUNTER)

def getRandomConjure():
    return random.choice(CONJURE_ENCOUNTER)

def getRandomGuard():
    return random.choice(GUARD_ENCOUNTER)

def getRandomBounty():
    return random.choice(BOUNTY_ENCOUNTER)

def getRandomHunt():
    return random.choice(HUNT_ENCOUNTER)

def getRandomHuntSuccess():
    return random.choice(HUNT_SUCCESS_ENCOUNTER)
