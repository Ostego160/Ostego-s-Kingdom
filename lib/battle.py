import random
from lib import character
from lib import loot
from lib import items
from lib import text
from lib import magic
from lib.constants import get as constant

from lib.colortext import colorprint as print
from lib.colortext import colorinput as input
from lib.colortext import colorstr

CURRENT = None
BATTLE_ORDER = None
CREATURES = None

def verifyCreatures(creatures):
    '''

    :param creatures:
    :return:
    '''
    for creature in creatures:
        if creature.health[0] > 0:
            return True
    return False

def verifyMagic(player, inventory):
    for i in inventory.spells:
        spell = magic.getSpell(i)
        if player.mana[0] > spell.mana:
            return True
    return False

def getBonusDamage(player, inventory):
    total = 0

    if inventory.primary:
        item = inventory.getItem(inventory.primary)
        if item.skill == 'One Handed':
            total += random.randint( 1, int(player.skills[0]/3) )
        elif item.skill == 'Two Handed':
            total += random.randint( 1, int(player.skills[1]/3) )
    else:
        total += random.randint( 1, int(player.skills[0]/5 + player.skills[1]/5) )

    return total

def calculateHit(attacker, defender, damage, isStrong=False):
    aSpeedBonus = random.randint(0, int(attacker.speed[0]))
    dSpeedBonus = random.randint(0, int(defender.speed[0]))

    if attacker.speed[1] + aSpeedBonus + constant('battleMissThreshold') > defender.speed[1] + dSpeedBonus:
        defender.health[0] -= damage
        if isStrong:
            print(text.get('battleAttack2', [attacker.name, damage]), color='white')
        else:
            print(text.get('battleAttack', [attacker.name, damage]), color='white')
    else:
        print(text.get('battleMiss', [attacker.name]))

def showGetTarget(creatures):
    while True:
        select = input(text.get('battleTarget'), color='cyan').lower()

        if select == 'b':
            return False
        try:
            creature = creatures[ int(select) ]
            if creature.health[0] <= 0:
                print(creature.name, 'is already defeated...', color='blue')
            else:
                return creature
        except:
            print(text.get('invalidSelection'), color='red')

def showGetItem(inventory):
    consumables = inventory.getConsumables()

    for i,v in enumerate(consumables):
        item = items.getItem(v)
        print(f'{i}: {item.name}')

    while True:
        select = input(text.get('selection2')).lower()
        if select == 'b':
            return False

        try:
            item = consumables[ int(select) ]
            return item
        except:
            print(text.get('invalidSelection'))

def showBattleMagic(player, inventory, creatures):
    spells = []
    for i in inventory.spells:
        spell = magic.getSpell(i)
        if spell.mana < player.mana[0] and (spell.usage == 'combat' or spell.usage == 'dual'):
            spells.append(spell)

    if len(spells) > 0:
        for i, spell in enumerate(spells):
            print(f'{i}: {spell.name} - {spell.mana} mana')

        while True:
            select = input(text.get('selection2'))
            spell = None
            if select == 'b':
                return False
            else:
                try:
                    spell = spells[int(select)]
                except:
                    print('invalidSelection')
                if spell:
                    if spell.type != 2 and spell.type != 3 and spell.type != 8 and spell.type != 7 and spell.type != 11:
                        creature = showGetTarget(creatures)
                        if creature:
                            spell.cast(player, creature)
                            return True
                    else:
                        spell.cast(player)
                        return True
    else:
        print(text.get('battleMagicNone', [player.name]))

def creatureDeath(player, inventory, creature):
    if creature.health[0] <= 0:
        lootList = loot.get( creature.lootList )
        exp   = lootList.getExp()
        gold  = lootList.getGold()
        stuff = lootList.getItems()
        print(text.get('battleEnemyDeath', [creature.name]), color='blue')
        print(text.get('battleLoot', [creature.name]), color='white')
        print('  Exp:', exp, ' Gold:', gold, color='yellow')
        inventory.gold += gold
        player.exp += exp
        for i in stuff:
            item = items.getItem(i)
            inventory.bag.append(i)
            print(' ', item.getColorString())
        if creature.bounty:
            player.addBounty(constant('bountyMurder'))
        return True
    else:
        return False

def creatureDeathAll(player, inventory, creatures, battleOrder):
    for v in reversed(battleOrder):
        if v >= 0:
            creature = creatures[v]
            if creatureDeath(player, inventory, creature):
                battleOrder.remove(v)
            elif creature.status == 'banish':
                battleOrder.remove(v)
                creature.health[0] = 0
                creature.status = None
                print(text.get('battleMagicBanish', [creature.name]))
            elif creature.status == 'duplicate':
                creature.status = None
                creatures.append(creature)
                battleOrder.append( len(creatures) - 1 )
                print(text.get('battleMagicDuplicate', [creature.name]), color='blue')

def playerDeath(player):
    if player.health[0] <= 0:
        print(text.get('battleHumanDeath', [player.name]), color='red')
        input(text.get('continue'), color='cyan')
        return True
    else:
        return False

def creatureTurn(player, inventory, creature):
    roll = random.randint(0, 2)
    miss = False

    playerSpeed = player.speed[1] + random.randint(0, int(player.speed[0]))

    armor = 1

    if player.status == 'armor':
        armor = (constant('playerArmorMax') - player.armor + constant('magicBarrierBonus')) / constant('playerArmorMax')
    else:
        armor = (128 - player.armor) / 128
    
    creatureDamage = random.randint(creature.damage[0], creature.damage[1])
    creatureDamage = creatureDamage * armor
    creatureDamage = round(creatureDamage, 1)

    creature.speed[1] = creature.speed[0]

    creatureSpeed = creature.speed[1] + random.randint(0, int(creature.speed[0]))

    if roll == 1:
        creatureSpeed *= 0.6
        creatureDamage = round(creatureDamage * 1.5, 1)
    
    if playerSpeed > creatureSpeed + constant('battleMissThreshold'):
        miss = True
    
    if roll < 2 and miss:
        print(text.get('battleMiss', [creature.name]), color='yellow')
    else:
        if roll == 0:
            print(text.get('battleAttack', [creature.name, creatureDamage]), color='yellow')
            player.health[0] -= creatureDamage
            player.health[0] = round(player.health[0], 1)
        elif roll == 1:
            print(text.get('battleAttack2', [creature.name, creatureDamage]), color='yellow')
            player.health[0] -= creatureDamage
            player.health[0] = round(player.health[0], 1)
        elif roll == 2:
            print(text.get('battleEvade', [creature.name]), color='yellow')
            creature.speed[1] = creature.speed[0] * 1.5
    
def playerTurn(player, inventory, creatures):
    if player.status == 'armor':
        if random.randint(0, 3) == 1:
            player.status = None
            print(text.get('magicSpellTimeout', [player.name, 'Barrier']), color='yellow')
        else:
            print(text.get('magicSpellContinue', [player.name, 'Barrier']), color='blue')

    print('\n' + player.name, color='white')
    print(' HP:', player.health, color='red')
    print(' MP:', player.mana, color='blue')
    for i,creature in enumerate(creatures):
        creature.printBattleInfo(i)

    player.speed[1] = player.speed[0]

    while True:
        print(text.get('battleMenu'), color='white')
        option1 = input(text.get('selection'), color='cyan').lower()

        if option1 == 'a':
            creature = showGetTarget(creatures)
            if creature:
                damage = random.randint(int( player.damage[0] ), int( player.damage[1] ))
                damage += getBonusDamage(player, inventory)
                calculateHit(player, creature, round(damage, 1))
                break
        elif option1 == 's':
            creature = showGetTarget(creatures)
            if creature:
                player.speed[1] *= 0.6
                damage = random.randint(int( player.damage[0] * 1.5 ), int( player.damage[1] * 1.5 ))
                damage += getBonusDamage(player, inventory)
                calculateHit(player, creature, round(damage, 1), True)
                break
        elif option1 == 'm':
            if verifyMagic(player, inventory):
                if showBattleMagic(player, inventory, creatures):
                    break
            else:
                print(text.get('battleMagicNone', [player.name]), color='yellow')
        elif option1 == 'e':
            print(text.get('battleEvade', [player.name]), color='blue')
            player.speed[1] = player.speed[0] * 1.5
            break
        elif option1 == 'i':
            item = showGetItem(inventory)
            if item:
                item = items.getItem(item)
                item.consume(player, inventory)
                break
        elif option1 == 'r':
            return True
    return False


def showBattleMain(player, inventory, creatures ):
    continueBattle = True
    
    def battleSort(v):
        if v == -1:
            return player.speed[0]
        else:
            creature = creatures[v]
            return creature.speed[0]
    
    battleOrder = [-1]
    
    for i in range(0, len(creatures)):
        battleOrder.append(i)
        
    battleOrder.sort(key=battleSort, reverse=True)
    
    while continueBattle:
        magic.updateCounters()

        for i, v in enumerate(reversed(battleOrder)):
            if v == -1:
                if player.health[0] > 0 and verifyCreatures(creatures) and playerTurn(player, inventory, creatures):
                    creatureSpeed = 0

                    for creature in creatures:
                        creatureSpeed += creature.speed[1]

                    creatureSpeed /= len(creatures)

                    playerSpeed = player.speed[1] + random.randint(0, int(player.speed[0]))

                    if playerSpeed + constant('battleMissThreshold') * 2 > creatureSpeed:
                        print(text.get('battleRunComplete', [player.name]), color='blue')
                        continueBattle = False
                        break
                    else:
                        print(text.get('battleRunFail', [player.name]), color='yellow')
                elif playerDeath(player):
                    #player.health[0] = player.health[1]
                    continueBattle = False
                    return
                elif player.status == 'teleport':
                    continueBattle = False
                    return
            else:
                creature = creatures[v]
                if creature.health[0] > 0:
                    creatureTurn(player, inventory, creature)
                if creatureDeath(player, inventory, creature):
                    battleOrder.pop(len(battleOrder)-i-1)

        creatureDeathAll(player, inventory, creatures, battleOrder)

        if not verifyCreatures(creatures):
            print(text.get('battleComplete', [player.name]), color='blue')
            input(text.get('continue'), color='cyan')
            continueBattle = False

        if playerDeath(player):
            continueBattle = False

    player.status = None
    magic.clearCounters()
