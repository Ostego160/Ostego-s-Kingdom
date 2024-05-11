import random
from lib import text
from lib import items
from lib.constants import get as constant

from lib.colortext import colorprint as print
from lib.colortext import colorinput as input
from lib.colortext import colorstr

                #0              #1              #2              #3          #4      #5      #6          #7          #8          #9          #10        #11
SPELL_TYPES = ('instantDamage', 'timeDamage', 'instantHeal', 'timeHeal', 'vampire', 'kill', 'banish', 'duplicate', 'teleport', 'conjure', 'sacrifice', 'armor')
                #0        #1        #2        #3        #4        #5        #6       #7      #8      #9           #10      #11
SPELL_USAGE = ('combat', 'combat', 'dual', 'combat', 'combat', 'combat', 'combat', 'dual', 'dual', 'noncombat', 'combat', 'combat')

SPELLS = []
SPELL_COUNTERS = []

class Spell:
    def __init__(self, name, skill, type, mana, minEffect=0, maxEffect=0, desc='Unknown'):
        self.name = name
        self.skill = skill
        self.type = type
        self.mana = mana
        self.effect = [minEffect, maxEffect]
        self.timeSpell = None
        self.desc = desc
        self.usage = SPELL_USAGE[type]

        if type == 1:
            self.timeSpell = Spell(name + ' Recurring', skill, 0, 0, minEffect, maxEffect)
        elif type == 3:
            self.timeSpell = Spell(name + ' Recurring', skill, 2, 0, minEffect, maxEffect)

    def getDescription(self):
        print('Spell:', self.name, color='white')
        if self.skill == 0:
            print('Skill: Fire Magic', color='red')
        elif self.skill == 1:
            print('Skill: Nature Magic', color='green')
        print(colorstr('Usage', 'white'), self.usage.capitalize())
        print(colorstr('Effect', 'white'), self.effect)
        print(colorstr('Mana', 'blue'), self.mana)
        print('Description:', color='white')
        print(self.desc)

    def cast(self, caster, target=None, isFree=False):
        effect = random.randint(self.effect[0], self.effect[1])
        
        if self.skill == 0:
            effect += random.randint(0, int(caster.skills[4]/3) )
        elif self.skill == 1:
            effect += random.randint(0, int(caster.skills[5]/3) )
        
        if not isFree:
            caster.mana[0] -= self.mana
        
        if self.type == 0:
            target.health[0] -= effect
            print(text.get('battleMagicAttack', [caster.name, self.name, effect]), color='blue')
        elif self.type == 1:
            SPELL_COUNTERS.append( SpellCounter(self.timeSpell, caster, target, 3) )
            print(text.get('battleMagicAttack2', [caster.name, self.name]), color='blue')
        elif self.type == 2:
            caster.addHealth(effect)
            print(text.get('battleMagicAttack', [caster.name, self.name, effect]))
        elif self.type == 3:
            SPELL_COUNTERS.append( SpellCounter(self.timeSpell, caster, caster, 3) )
            print(text.get('battleMagicAttack2', [caster.name, self.name]), color='blue')
        elif self.type == 4:
            total = min(target.health[0], effect)
            target.health[0] -= total
            caster.addHealth(total)
            print(text.get('battleMagicAttack', [caster.name, self.name, total]), color='blue')
        elif self.type == 5:
            target.health[0] = 0
            print(text.get('battleMagicAttack2', [caster.name, self.name]), color='blue')
        elif self.type == 6:
            target.status = 'banish'
            print(text.get('battleMagicAttack2', [caster.name, self.name]), color='blue')
        elif self.type == 7:
            target.status = 'duplicate'
            print(text.get('battleMagicAttack2', [caster.name, self.name]), color='blue')
        elif self.type == 8:
            caster.status = 'teleport'
            print(text.get('battleMagicAttack2', [caster.name, self.name]), color='blue')
        elif self.type == 9:
            target.status = 'conjure'
            print(text.get('battleMagicAttack2', [caster.name, self.name]), color='blue')
        elif self.type == 10:
            target.health[0] -= effect
            caster.health[0] -= round(effect/4, 1)
            print(text.get('battleMagicAttack', [caster.name, self.name, effect]), color='blue')
        elif self.type == 11:
            caster.status = 'armor'
            print(text.get('battleMagicAttack2', [caster.name, self.name]), color='blue')

class SpellCounter:
    def __init__(self, spell, caster, target, timer):
        self.spell = spell
        self.caster = caster
        self.target = target
        self.timer = timer
        self.count = 0

def addSpell(name, skill, type, mana, minEffect, maxEffect, desc='Unknown'):
    SPELLS.append( Spell(name, skill, type, mana, minEffect, maxEffect, desc) )

def getSpell(i):
    return SPELLS[i]

def getSpellByName(name):
    for spell in SPELLS:
        if spell.name == name:
            return spell

def getSpellUsage(i):
    return SPELL_USAGE[i]

def addCounter(spell, caster, target, timer=3):
    SPELL_COUNTERS.append( SpellCounter(spell, caster, target, timer) )

def updateCounters():
    for counter in reversed(SPELL_COUNTERS):
        counter.count += 1
        if counter.count > counter.timer or counter.target.health[0] <= 0:
            SPELL_COUNTERS.remove(counter)
        else:
            counter.spell.cast(counter.caster, counter.target)

def clearCounters():
    SPELL_COUNTERS.clear()

def showMagicDuplicate(player, inventory):
    continueDuplicate = True

    while continueDuplicate:
        print(text.get('titleDuplicate'), color='blue')
        print(f'{player.name}\'s Items:', color='white')
        for i, v in enumerate(inventory.bag):
            item = items.getItem(v)
            print(f'  {i}: {item.getColorString()}', color='white')

        select = input(text.get('magicDuplicate'), color='cyan')
        item = None

        if select == 'b':
            return

        try:
            select = int(select)
            item = items.getItem(inventory.bag[select])
        except:
            item = None
            print(text.get('invalidSelection'), color='red')

        if item:
            cost = max(constant('magicDuplicateMinCost'), int(item.value/2))

            if player.mana[0] >= cost:
                confirmDuplicate = True
                while confirmDuplicate:
                    confirm = input(text.get('magicDuplicateCost', [cost, item.name])).lower()

                    if confirm == 'y' or confirm == 'yes':
                        inventory.bag.append( inventory.bag[select] )
                        print(text.get('magicDuplicateSuccess', [item.name]), color='blue')
                        player.addMana(-cost)
                        confirmDuplicate = False
                    elif confirm == 'n' or confirm == 'no':
                        confirmDuplicate = False
                    else:
                        print(text.get('invalidSelection'), color='red')
            else:
                print(text.get('magicDuplicateFail', [player.name, item.name]), color='red')
                input(text.get('continue'), color='cyan')



def showMagicConjure(player, inventory):
    cost = 30
    continueConjure = True
    while continueConjure:
        print(text.get('titleConjure'), color='blue')
        print('Item Types:', color='white')
        print(f'  0: Consumable', color='white')
        print(f'  1: Weapon', color='white')
        print(f'  2: Offhand', color='white')
        print(f'  3: Armor', color='white')
        print(f'  4: Hostile Spectre', color='white')
        select = input(text.get('magicConjure'), color='cyan').lower()

        if select == 'b':
            return
        elif select == '0':
            i = items.getRandomItem('consumable')
            item = items.getItem(i)
            print(text.get('magicConjureComplete', [player.name, item.name]), color='blue')
            inventory.addItem(i)
            input(text.get('continue'))
            return
        elif select == '1':
            i = items.getRandomItem('weapon')
            item = items.getItem(i)
            print(text.get('magicConjureComplete', [player.name, item.name]), color='blue')
            inventory.addItem(i)
            input(text.get('continue'))
            return
        elif select == '2':
            i = items.getRandomItem('offhand')
            item = items.getItem(i)
            print(text.get('magicConjureComplete', [player.name, item.name]), color='blue')
            inventory.addItem(i)
            input(text.get('continue'))
            return
        elif select == '3':
            i = items.getRandomItem('shield')
            item = items.getItem(i)
            print(text.get('magicConjureComplete', [player.name, item.name]), color='blue')
            inventory.addItem(i)
            input(text.get('continue'))
            return
        elif select == '4':
            print(text.get('magicConjureSpectre', [player.name]), color='blue')
            input(text.get('continue'))
            return True
        else:
            print(text.get('invalidSelection'), color='red')

def showMagicMain(player, inventory):
    spells = []

    for i in inventory.spells:
        spell = getSpell(i)
        if spell.usage == 'noncombat' or spell.usage == 'dual':
            spells.append(spell)

    continueMagic = True

    if len(spells) == 0:
        print(text.get('battleMagicNone', [player.name]), color='blue')
        input(text.get('continue'), color='cyan')
        return

    while continueMagic:
        print(text.get('titleMagic'), color='blue')
        print(text.get('magicMenu2', [player.name]), color='white')
        for i, spell in enumerate(spells):
            print(f'  {i}: {spell.name} - {spell.mana} mana', color='white')

        print(text.get('magicMenu'), color='white')

        continueSelect = True

        while continueSelect:
            select = input(text.get('selection2'), color='cyan').lower()
            spell = None

            if select == 'b':
                continueSelect = False
                continueMagic = False
            elif select == 'c':
                continueGetSpell = True

                while continueGetSpell:
                    spell = input(text.get('magicSpell'), color='cyan')
                    if spell == 'b':
                        continueGetSpell = False
                    else:
                        try:
                            spell = spells[ int(spell) ]
                        except:
                            print(text.get('invalidSelection'), color='red')
                            spell = None
                        if spell:
                            if player.mana[0] >= spell.mana:
                                spell.cast(player, player)
                                input(text.get('continue'), color='cyan')
                                continueGetSpell = False
                                continueSelect = False
                                if 7 <= spell.type <= 9:
                                    return
                            else:
                                print(text.get('magicSpellFail',[player.name, spell.name]), color='red')
                                input(text.get('continue'), color='cyan')

            elif select == 'i':
                continueGetSpell = True

                while continueGetSpell:
                    spell = input(text.get('magicSpell'), color='cyan')
                    if spell == 'b':
                        continueGetSpell = False
                    else:
                        try:
                            spell = spells[ int(spell) ]
                        except:
                            print(text.get('invalidSelection'), color='red')
                            spell = None
                        if spell:
                            spell.getDescription()
                            input(text.get('continue'))
                            continueGetSpell = False
                            continueSelect = False
            else:
                print(text.get('invalidSelection'))

addSpell('Flash', 0, 0, 10, 5, 10, text.get('descSpellFlash'))
addSpell('Burn', 0, 1, 15, 1, 5, text.get('descSpellBurn'))
addSpell('Greater Burn', 0, 1, 30, 10, 20)
addSpell('Fireball', 0, 0, 20, 12, 25)
addSpell('Beam', 0, 0, 25, 5, 50)
addSpell('Meteor', 0, 0, 30, 20, 45)
addSpell('Enflame', 0, 10, 15, 15, 25)
addSpell('Greater Enflame', 0, 10, 30, 25, 50)
addSpell('Barrier', 0, 11, 20, 25, 25)
addSpell('Vaporize', 0, 6, 50, 0, 0)
addSpell('Flame Lance', 0, 5, 60, 0, 0)

addSpell('Vines', 1, 0, 10, 5, 10)
addSpell('Poison', 1, 1, 20, 5, 15)
addSpell('Restore', 1, 2, 10, 5, 15)
addSpell('Greater Restore', 1, 2, 25, 20, 35)
addSpell('Absorb', 1, 4, 25, 5, 15)
addSpell('Greater Absorb', 1, 4, 40, 25, 35)
addSpell('Regenerate', 1, 3, 20, 5, 10)
addSpell('Death Touch', 1, 5, 60, 0, 0)
addSpell('Duplicate', 1, 7, 0, 0, 0)
addSpell('Teleport', 1, 8, 0, 0, 0)
addSpell('Conjure', 1, 9, 30, 0, 0)
