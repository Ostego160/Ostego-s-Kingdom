import random
from lib import text

from lib.colortext import colorprint as print
from lib.colortext import colorinput as input
from lib.colortext import colorstr

SLOTS = ['none', 'weapon', 'head', 'torso', 'hands', 'feet']

class Item:
    slot = None
    consumable = None
    skill = None
    type = 'item'

    def __init__(self, name, weight, value, desc):
        self.setBasicStats(name, weight, value, desc)
    
    def setBasicStats(self, name, weight, value, desc):
        self.name   = name
        self.weight = weight
        self.value  = value
        self.desc   = desc
    
    def getString(self):
        return self.name + ' - Weight:' + str(self.weight) + ', Value:' + str(self.value)

    def getColorString(self):
        return colorstr(self.getString(), 'yellow')
    
    def getDescription(self):
        print(self.name)
        print('  Weight:' + str(self.weight) + ', Value:' + str(self.value))
        print('  Desc:' )
        print('  ' + self.desc)

class Weapon(Item):
    slot = 'primary'
    type = 'weapon'
    
    def __init__(self, name, weight, value, min_damage, max_damage, speed, skill, desc):
        self.setBasicStats(name, weight, value, desc)
        self.setWeaponStats(min_damage, max_damage, speed, skill)
    
    def setWeaponStats(self, min_damage, max_damage, speed, skill):
        self.damage = [min_damage, max_damage]
        self.speed = speed
        self.skill = skill
        
    def getString(self):
        return self.name + ' - Skill:' + self.skill + ', Dmg:' + str(self.damage) + ', Spd:' + str(self.speed) + ', Weight:' + str(self.weight) + ', Value:' + str(self.value)

    def getColorString(self):
        return colorstr(self.getString(), 'red')

    def getDescription(self):
        print(self.name, color='white')
        print('  Skill:', self.skill, color='yellow')
        print('  Weight:' + str(self.weight) + ', Value:' + str(self.value), color='white')
        print('  Damage:' + str(self.damage[0]) + ' / ' + str(self.damage[1]) + ', Speed:' + str(self.speed), color='white')
        print('  Desc:', color='white')
        print('  ' + self.desc)

class Armor(Item):
    type = 'armor'

    def __init__(self, name, weight, value, armor, slot, desc):
        self.setBasicStats(name, weight, value, desc)
        self.setArmorStats(armor, slot)
    
    def setArmorStats(self, armor, slot):
        if slot == 'head' or slot == 'torso' or slot == 'hands' or slot == 'feet' or slot == 'secondary':
            self.slot = slot
            self.armor = armor
    
    def getString(self):
        return self.name + ' - Slot:' + self.slot + ', Armor:' + str(self.armor) + ', Weight:' + str(self.weight) + ', Value:' + str(self.value)

    def getColorString(self):
        return colorstr(self.getString(), 'blue')

    def getDescription(self):
        print(self.name, color='white')
        print('  Slot:', self.slot, color='yellow')
        print('  Weight:' + str(self.weight) + ', Value:' + str(self.value), color='white')
        print('  Armor:' + str(self.armor), color='white')
        print('  Desc:', color='white')
        print('  ' + self.desc)
    
class Shield(Item):
    slot = 'secondary'
    type = 'shield'
    
    def __init__(self, name, weight, value, min_damage, max_damage, armor, speed, desc):
        self.setBasicStats(name, weight, value, desc)
        self.setShieldStats(min_damage, max_damage, armor, speed)
    
    def setShieldStats(self, min_damage, max_damage, armor, speed):
            self.damage = [min_damage, max_damage]
            self.armor  = armor
            self.speed  = speed
    
    def getString(self):
        return self.name + ' - Slot:' + self.slot + ', Dmg:' + str(self.damage) + ', Armor:' + str(self.armor) + ', Weight:' + str(self.weight) + ', Value:' + str(self.value)

    def getColorString(self):
        return colorstr(self.getString(), 'cyan')

    def getDescription(self):
        print(self.name, color='white')
        print('  Slot:', self.slot, color='yellow')
        print('  Weight:' + str(self.weight) + ', Value:' + str(self.value), color='white')
        print('  Damage:' + str(self.damage[0]) + ' / ' + str(self.damage[1]) + ', Armor:' + str(self.armor), color='white')
        print('  Desc:', color='white')
        print('  ' + self.desc)
        
class Consumable(Item):
    consumable = True
    type = 'consumable'

    def __init__(self, name, weight, value, food, health, mana, exp, desc):
        self.setBasicStats(name, weight, value, desc)
        self.setModifierStats(food, health, mana, exp)
    
    def setModifierStats(self, food, health, mana, exp):
        self.food = food
        self.health = health
        self.mana = mana
        self.exp = exp
    
    def getString(self):
        return self.name + ' - Food+:' + str(self.food) + ', Health+:' + str(self.health) + ', Mana+:' + str(self.mana) + ', Exp+:' + str(self.exp) + ', Weight:' + str(self.weight) + ', Value:' + str(self.value)

    def getColorString(self):
        return colorstr(self.getString(), 'green')

    def getDescription(self):
        print(self.name, color='white')
        print('  Food+:', self.health, 'Health+:', self.health, ' Mana+:', self.mana, ' Exp+:', self.exp, color='white')
        print('  Weight:' + str(self.weight) + ', Value:' + str(self.value), color='white')
        print('  Desc:', color='white')
        print('  ' + self.desc)

    def consume(self, player, inventory):
        print(text.get('inventoryConsumeConfirm', [player.name, self.name]), color='blue')
        player.addHunger(-self.food)
        player.addHealth(self.health)
        player.addMana(self.mana)
        player.addExperience(self.exp)
        return True

class SpellBook(Consumable):
    type = 'spellbook'

    def __init__(self, name, weight, value, spell, desc):
        self.setBasicStats(name, weight, value, desc)
        self.spell = spell

    def consume(self, player, inventory):
        if self.spell in inventory.spells:
            print(text.get('inventorySpellKnown'))
            return False
        else:
            print(text.get('inventorySpellBookConfirm', [player.name, self.name]), color='blue')
            inventory.addSpell(self.spell)
            return True
    
    def getString(self):
        return self.name + ' - Weight:' + str(self.weight) + ', Value:' + str(self.value)

    def getColorString(self):
        return colorstr(self.getString(), 'magenta')
    
    def getDescription(self):
        print(self.name, color='white')
        print('  Weight:' + str(self.weight) + ', Value:' + str(self.value), color='white')
        print('  Desc:', color='white')
        print('  ' + self.desc)

class Mount(Item):
    slot = 'mount'
    type = 'mount'

    def __init__(self, name, weight, value, speed, desc):
        self.setBasicStats(name, weight, value, desc)
        self.speed = speed

    def getString(self):
        return self.name + ' - Speed: ' + str(self.speed) + ', Value:' + str(self.value)

    def getColorString(self):
        return colorstr(self.getString(), 'white')

    def getDescription(self):
        print(self.name, color='white')
        print('  Value: ' + str(self.value), color='white')
        print('  Speed: ' + str(self.value), color='white')
        print('  Desc:', color='white')
        print('  ' + self.desc)

ITEM_LIST = [
    Item('Nothing', 0, 0, 'Nothing.'),
    
    Weapon('Stone Knife', 1, 30, 4, 7, 13, 'One Handed', 'A small flint stone knife fixed to a wooden handle.'),
    Weapon('Iron Knife', 2, 50, 5, 10, 13, 'One Handed', 'A small iron blade usually used in skinning or cooking.'),
    Weapon('Dagger', 2, 75, 6, 11, 12, 'One Handed', 'A small concealable blade.'),
    Weapon('Punch Dagger', 2, 50, 5, 7, 11, 'One Handed', 'A grip with a blade in the middle so it fits between the fingers.'),
    Weapon('Stone Axe', 5, 40, 7, 10, 8, 'One Handed', 'A hand-made axe fashioned from the wilderness.'),
    Weapon('Axe', 4, 80, 8, 14, 9, 'One Handed', 'A basic axe with an iron head.'),
    Weapon('Battle Axe', 6, 140, 9, 15, 8, 'One Handed', 'A large steel axe with a spike on the back.'),
    Weapon('Wooden Cudgel', 2, 20, 3, 5, 9, 'One Handed', 'A simple wooden club with a hand wrap.'),
    Weapon('Wooden Sword', 2, 25, 3, 5, 10, 'One Handed', 'A wooden sword for children or training.'),
    Weapon('Sickle', 3, 40, 3, 9, 10, 'One Handed', 'A common sickle useful for harvesting wheat.'),
    Weapon('Mace', 3, 100, 5, 9, 9, 'One Handed', 'A basic mace with a flanged iron head used by thugs and infantry alike.'),
    Weapon('Flail', 5, 200, 5, 17, 8, 'One Handed', 'A spiked iron ball and chain attached to a wooden poll.'),
    Weapon('War Hammer', 6, 110, 6, 15, 8, 'One Handed', 'A heavy iron hammer with a deadly spike on back.'),
    Weapon('Viking Axe', 5, 150, 7, 14, 9, 'One Handed', 'A large but agile axe used by vikings on raids.'),
    Weapon('Broken Sword', 3, 40, 2, 5, 10, 'One Handed', 'An old sword broken from past battles.'),
    Weapon('Mining Pick', 4, 50, 2, 6, 8, 'One Handed', 'A basic mining pick that could do some damage in a pinch.'),
    Weapon('Short Sword', 3, 100, 5, 12, 11, 'One Handed', 'A common shortsword used by traders and peasants.'),
    Weapon('Saber', 3, 200, 5, 10, 11, 'One Handed', 'A sword with a curved blade for exceptional slashing.'),
    Weapon('Long Sword', 4, 150, 7, 14, 9, 'One Handed', 'A long sword used by the soldiers.'),
    Weapon('Broad Sword', 3, 100, 5, 13, 10, 'One Handed', 'A long sword used by the soldiers.'),
    Weapon('Short Spear', 3, 90, 9, 14, 10, 'One Handed', 'A short spear usually carried by line soldiers.'),
    Weapon('Katana', 4, 200, 7, 11, 11, 'One Handed', 'A blade crafted by the finest Eastern craftsmen.'),
    Weapon('Throwing Knives', 9, 250, 4, 11, 11, 'One Handed', 'A set of knives used by entertainers and thieves alike.'),
    Weapon('Throwing Axes', 9, 250, 5, 15, 10, 'One Handed', 'A set of axes designed to be thrown.'),
    Weapon('Throwing Spears', 8, 225, 4, 13, 10, 'One Handed', 'A bundle of throwing spears for ranged warfare.'),
    
    Weapon('Pitchfork', 5, 75, 4, 12, 8, 'Two Handed', 'A basic farming tool that can be deadly in the right hands.'),
    Weapon('Shovel', 5, 95, 5, 11, 8, 'Two Handed', 'A basic farming tool that can be deadly in the right hands.'),
    Weapon('Hoe', 4, 50, 1, 9, 8, 'Two Handed', 'A tool used to prepare soil for planting.'),
    Weapon('Broom', 2, 50, 1, 5, 7, 'Two Handed', 'A basic tool for sweeping. Hardly a weapon but you can swing it.'),
    Weapon('Maul', 8, 300, 10, 20, 7, 'Two Handed', 'A large two-handed war hammer that crushes most armor.'),
    Weapon('Bastard Sword', 5, 120, 8, 16, 9, 'Two Handed', 'A two handed blade built for speed and agility.'),
    Weapon('Great Sword', 7, 350, 10, 20, 8, 'Two Handed', 'A large two handed blade that slow but deadly.'),
    Weapon('Two Handed Axe', 7, 150, 10, 22, 7, 'Two Handed', 'A large battle axe great for breaking shields.'),
    Weapon('Ornate Sword', 6, 400, 6, 18, 8, 'Two Handed', 'A large and decorated two handed sword usually worn by lords.'),
    Weapon('Wooden Staff', 3, 50, 4, 9, 11, 'Two Handed', 'A wooden staff useful for walks or self defence.'),
    Weapon('Iron Staff', 5, 200, 6, 14, 9, 'Two Handed', 'An iron reinforced staff used by battlemages and nobles.'),
    Weapon('Quaterstaff', 4, 150, 5, 12, 12, 'Two Handed', 'A short staff useful for self defense.'),
    Weapon('Wooden Spear', 3, 70, 4, 13, 10, 'Two Handed', 'A sharpened wooden stick useful for hunting wild game.'),
    Weapon('Iron Pike', 6, 180, 9, 19, 8, 'Two Handed', 'A reinforced iron spear with a heavy point.'),
    Weapon('Glaive', 7, 300, 12, 20, 8, 'Two Handed', 'A powerful polearm with a large blade on the end.'),
    
    Weapon('Short Bow', 4, 250, 1, 12, 13, 'Ranged', 'A well-made but simple bow used to hunt small game.'),
    Weapon('Yew Bow', 5, 350, 2, 15, 11, 'Ranged', 'A strong bow made from yew and finely decorated.'),
    Weapon('Ranger Bow', 4, 300, 3, 14, 10, 'Ranged', 'A high-strung speciality bow used by forest rangers.'),
    Weapon('Recurve Bow', 5, 400, 3, 21, 10, 'Ranged', 'A smaller but effective bow that yields excellent power.'),
    Weapon('Long Bow', 6, 500, 2, 24, 9, 'Ranged', 'A large bow used by military archers.'),
    Weapon('War Bow', 6, 600, 8, 22, 9, 'Ranged', 'A powerful bow crafted for armor penetration.'),
    Weapon('Noble Bow', 6, 750, 7, 22, 10, 'Ranged', 'An ornate and powerful bow used to take down large game.'),
    Weapon('Small Crossbow', 4, 200, 3, 12, 11, 'Ranged', 'A small crossbow excellent for dispatching varmints.'),
    Weapon('Wooden Crossbow', 5, 300, 4, 15, 9, 'Ranged', 'A simple crossbow used mostly for hunting and village defense.'),
    Weapon('Iron Crossbow', 7, 450, 5, 20, 8, 'Ranged', 'A heavy crossbow used by line soldiers.'),
    Weapon('Heavy Crossbow', 9, 500, 6, 22, 8, 'Ranged', 'A very slow and heavy crossbow reinforced with steel.'),
    Weapon('Leather Sling', 2, 225, 1, 10, 14, 'Ranged', 'A strap of leather crafted to send pellets at your enemy.'),
    Weapon('Reinforced Sling', 3, 225, 3, 12, 14, 'Ranged', 'A better version of the sling that does more damage.'),
    
    Armor('Beggar\'s Rags', 3, 5, 1, 'torso', 'Torn rags worn by beggars and criminals.'),
    Armor('Villager Tunic', 3, 25, 2, 'torso', 'A simple cloth tunic made of flax and horsehair thread.'),
    Armor('Cloth Tunic', 3, 60, 2, 'torso', 'Commoner cloth tunic usually worn by peasants.'),
    Armor('Quilted Tunic', 5, 80, 3, 'torso', 'A basic quilted tunic offering minimal protection.'),
    Armor('Strapped Tunic', 5, 95, 4, 'torso', 'A nice tunic with some straps to hold the cloth down.'),
    Armor('Blacksmith\'s Apron', 5, 75, 4, 'torso', 'A an apron with a leather front to protect against furnaces.'),
    Armor('Gambeson', 6, 100, 4, 'torso', 'A cloth based woven armor that provides slash protection.'),
    Armor('Wool Coat', 5, 80, 3, 'torso', 'A large coat meant to keep the wearer warm during the winter.'),
    Armor('Leather Jerkin', 7, 120, 5, 'torso', 'A fine leather vest over a cloth tunic.'),
    Armor('Leather Vest', 7, 90, 4, 'torso', 'A fine leather vest over a cloth tunic.'),
    Armor('Fur Coat', 6, 300, 6, 'torso', 'A fur coat made from Elk usually worn by woodsmen.'),
    Armor('Scale Mail', 12, 250, 11, 'torso', 'A common iron breastplate worn by foot soldiers.'),
    Armor('Iron Breastplate', 15, 250, 15, 'torso', 'A common iron breastplate worn by foot soldiers.'),
    Armor('Steel Breastplate', 16, 350, 16, 'torso', 'A fine steel breast plate with good protection.'),
    Armor('Lamellar Breastplate', 11, 275, 10, 'torso', 'A fine steal breast plate with good protection.'),
    Armor('Leather Armor', 8, 150, 7, 'torso', 'Common leather armor used by rangers.'),
    Armor('Chainmail', 10, 200, 9, 'torso', 'Finely made chainmail used by squires and knights.'),
    Armor('Wizard Robes', 4, 150, 3, 'torso', 'A pair of wizard robes imbued with power and wisdom.'),
    Armor('Priest Robes', 3, 75, 2, 'torso', 'A set of robes usually worn by the priests of this land.'),
    
    Armor('Cloth Coif', 1, 25, 1, 'head', 'A lightweight cotton coif worn by peasants.'),
    Armor('Merchant Cap', 1, 100, 1, 'head', 'A fine cap made from wool.'),
    Armor('Townsman Cap', 1, 50, 1, 'head', 'A basic hat that protects from the sun and looks average.'),
    Armor('Wizard Hat', 1, 75, 1, 'head', 'A traditional and floppy wizard hat.'),
    Armor('Witch\'s Hat', 1, 60, 1, 'head', 'A black hat worn by witches. Who wore this originally?'),
    Armor('Leather Coif', 1, 60, 2, 'head', 'A leather coif that offers minimal protection.'),
    Armor('Leather Helmet', 2, 90, 3, 'head', 'A sturdy leather helmet that offer basic protection.'),
    Armor('Viking Helmet', 3, 160, 5, 'head', 'A thick iron helmet that protects against many blows.'),
    Armor('Horned Helmet', 4, 250, 5, 'head', 'A iron helmet with horns fixed meant to intimidate enemies.'),
    Armor('Fur Hat', 1, 90, 2, 'head', 'A thick fur hat to protect against the cold.'),
    Armor('Iron Skullcap', 3, 180, 3, 'head', 'A common iron cap used by village militias.'),
    Armor('Full Iron Helmet', 5, 220, 5, 'head', 'A iron helmet with better head and neck protection.'),
    Armor('Plate Helmet', 6, 350, 7, 'head', 'A full-face steal helmet for maximum protection.'),
    Armor('Great Helmet', 7, 375, 8, 'head', 'A full-face steal helmet for maximum protection.'),
    Armor('Chainmail Coif', 4, 250, 5, 'head', 'A finely made chainmail coif fit for a noble or knight.'),
    Armor('Spiked Helmet', 4, 125, 4, 'head', 'A heavy helmet worn my infantry soldiers.'),
    Armor('Minotaur Helmet', 5, 275, 6, 'head', 'A mythical helmet worn by the minotaurs of this land.'),
    Armor('Wolf Helmet', 5, 275, 5, 'head', 'An iron helmet with the pelt of a wolf fixed to it.'),
    Armor('Bear Helmet', 6, 340, 6, 'head', 'A sturdy helmet covered in the pelt of a bear.'),
    Armor('Circlet', 2, 500, 6, 'head', 'A fine silver and gold circlet with a single small gem on the front.'),
    
    Armor('Hand Wraps', 1, 20, 1, 'hands', 'A basic pair of hand wraps used for boxing and yardwork.'),
    Armor('Noble Gloves', 1, 100, 2, 'hands', 'A finely crafted pair of gloves fit for a noble.'),
    Armor('Leather Gloves', 1, 50, 2, 'hands', 'A thick pair of leather gloves.'),
    Armor('Fingerless Gloves', 1, 45, 2, 'hands', 'A pair of leather gloves without fingers for agility.'),
    Armor('Leather Bracers', 1, 40, 2, 'hands', 'A pair of leather bracers popular amongst hunters.'),
    Armor('Fur Mittens', 2, 65, 3, 'hands', 'Thick fur gloves that provide excellent protection from the cold.'),
    Armor('Fur Bracers', 1, 55, 2, 'hands', 'Thick fur bracers favored by Northmen and woodsmen.'),
    Armor('Engraved Bracers', 3, 460, 5, 'hands', 'A pair of gold and steel bracers finely decorated and engraved.'),
    Armor('Reinforced Gloves', 2, 90, 3, 'hands', 'Leather gloves with iron reinforcement for added protection.'),
    Armor('Spiked Gauntlets', 3, 95, 4, 'hands', 'A pair of intimidating gauntlets with iron spikes built in.'),
    Armor('Chainmail Mittens', 3, 100, 5, 'hands', 'Chainmail mittens you can wear to protect your hands.'),
    Armor('Iron Gauntlets', 4, 150, 6, 'hands', 'Heavy iron gauntlets worn by line soldiers.'),
    Armor('Plate Gauntlets', 5, 200, 7, 'hands', 'Steel plate gloves for excellent protection.'),
    
    Armor('Cloth Sandals', 1, 10, 1, 'feet', 'A basic foot covering that beggars wear.'),
    Armor('Jester\'s Shoes', 1, 40, 1, 'feet', 'A silly looking shoe with pointed toes and tassels.'),
    Armor('Old Leather Boots', 2, 45, 2, 'feet', 'An old and battered pair of leather boots.'),
    Armor('Leather Boots', 2, 80, 3, 'feet', 'A thick pair of leather boots.'),
    Armor('Horseman Boots', 2, 100, 4, 'feet', 'A nice pair of cavalry boots with reinforced shins.'),
    Armor('Fur Boots', 3, 100, 4, 'feet', 'A fine pair of fur boots that come from the North.'),
    Armor('Reinforced Boots', 4, 200, 5, 'feet', 'Iron reinforced boots that provide better protection.'),
    Armor('Noble Boots', 2, 240, 4, 'feet', 'Well made nobles boots.'),
    Armor('Plate Greaves', 6, 400, 7, 'feet', 'Steal greaves to protect the lower half.'),
    Armor('Chainmail Greaves', 4, 250, 5, 'feet', 'Finely made and noisy chainmail to protect your lower half.'),
    
    Shield('Torch', 1, 50, 1,8, 1, 10, 'A basic torch for your off-hand.'),
    Shield('Wooden Shield', 3, 90, 1,5, 7, 8, 'A battered and old wooden shield.'),
    Shield('Tower Shield', 10, 500, 1,8, 15, 7, 'A battered and old wooden shield.'),
    Shield('Leather Buckler', 2, 100, 1,5, 9,9,  'A lightweight shield wrapped in leather.'),
    Shield('Kiteshield', 7, 125, 2,7, 12, 8, 'A strong kiteshield used by the infantry.'),
    Shield('Round Shield', 5, 125, 2,5, 10, 8, 'A round shield used by vikings of the North.'),
    Shield('Engraved Shield', 6, 400, 2,5, 12, 8, 'A finely engraved shield with gold inlays.'),
    Shield('Northern Shield', 6, 300, 2,5, 11, 8, 'A sturdy shield used by the Northmen.'),
    Shield('Arming Knife', 1, 50, 2,6, 4, 14, 'A common blade used in the off-hand.'),
    Shield('Arming Sword', 3, 200, 2,9, 6, 11, 'A fine off-hand blade used in duels.'),
    Shield('Hooked Sword', 3, 200, 2,7, 8, 12, ' A hooked sword intended to deflect incoming blows.'),
    Shield('Hatchet', 3, 75, 4,6, 4, 9, 'A small hatchet used in the off-hand for chopping and self-defense.'),
    Shield('Iron Chain', 3, 100, 1,7, 4, 9, 'A iron chain useable for basic self defense.'),
    
    Consumable('Raw Meat', 1, 10, 1, 1, 0, 0, 'Some raw meat that provides little nutritional value on it\'s own.'),
    Consumable('Cooked Meat', 1, 15, 8, 5, 0, 0, 'A juicy piece of cooked meat.'),
    Consumable('Apple', 1, 10, 6, 4, 0, 0, 'A fresh apple ready to be eaten.'),
    Consumable('Cabbage', 1, 15, 8, 5, 0, 0, 'A fully grown cabbage with delicious green leaves.'),
    Consumable('Onion', 1, 10, 5, 4, 0, 0, 'A pungent onion perfect for a stew.'),
    Consumable('Melon', 1, 15, 7, 5, 0, 0, 'A large and ripe melon recently harvested from the fields.'),
    Consumable('Bread', 1, 50, 12, 8, 0, 0, 'A fresh loaf of bread fresh from a bakery.'),
    Consumable('Glorigon', 1, 50, 0, 10, 0, 0, 'A small bundle of sageroot with healing properties.'),
    Consumable('Mageroot', 1, 50, 0, 5, 10, 0, 'A special herb that restores mana and a little bit of health.'),
    Consumable('Mindweed', 1, 50, 0, 5, 5, 100, 'A magic herb that grants experience from the realm.'),
    Consumable('Ermandus', 1, 100, 0, 15, 15, 0, 'A potent herb that boosts both health and mana.'),
    Consumable('Cannabis', 1, 125, 0, 0, 20, 100, 'A potent herb that expands awareness.'),
    Consumable('Ale', 1, 50, 3, 8, 0, 0, 'An wheat ale sealed in a clay bottle.'),
    Consumable('Wine', 1, 100, 3, 8, 0, 0, 'An fine grape wine sealed in a glass bottle.'),
    Consumable('Pie', 2, 75, 15, 12, 0, 0, 'An apple pie cooked to perfection.'),
    Consumable('Wizard\'s Cake', 1, 150, 15, 5, 8, 0, 'A specially made cake made just for wizards.'),
    Consumable('Waterskin', 1, 25, 4, 5, 0, 0, 'A standard waterskin full of water.'),
    
    Consumable('Small Health Potion', 1, 100, 0, 25, 0, 0, 'A potion made by the apothecary sealed in a small jar.'),
    Consumable('Health Potion', 2, 175, 0, 40, 0, 0, 'A standard potion brewed for rejuvenation purposes.'),
    Consumable('Small Mana Potion', 1, 100, 0, 0, 25, 0, 'A small potion made to stimulate the mind.'),
    Consumable('Mana Potion', 2, 200, 0, 0, 40, 0, 'A standard mage\'s potion brewed for casting purposes.'),
    Consumable('Recovery Potion', 2, 500, 0, 25, 25, 0, 'A potion brewed for both health and mana regeneration.'),
    Consumable('Special Potion', 3, 750, 0, 40, 40, 250, 'A special potion meant to embue a person with power.'),
    
    Consumable('Missing Note', 1, 15, 0, 0, 0, 25, 'A single page with a few notes scribbled on it.'),
    Consumable('Tome Pages', 1, 25, 0, 0, 0, 25, 'A few torn pages from a journal or manuscript.'),
    Consumable('Small Book', 1, 100, 0, 0, 0, 100, 'A short book that will likely teach you something.'),
    Consumable('Book', 2, 250, 0, 0, 0, 250, 'A full manuscript on various topics that are useful.'),
    Consumable('Large Book', 3, 500, 0, 0, 0, 500, 'Several wrapped volumes on the world we live in.'),
    
    SpellBook('Spell Book: Flash', 1, 500, 0, 'An ancient manuscript containing magic formula for Flash.'),
    SpellBook('Spell Book: Burn', 1, 600, 1, 'Instructions for the spell Burn, a recurring damage spell.'),
    SpellBook('Spell Book: Greater Burn', 1, 2000, 2, 'Instructions for an enhanced version of the spell Burn.'),
    SpellBook('Spell Book: Fireball', 1, 1200, 3, 'A dusty tome with the spell of Fireball.'),
    SpellBook('Spell Book: Beam', 1, 2000, 4, 'A tome containing the powerful spell called Beam.'),
    SpellBook('Spell Book: Meteor', 1, 2500, 5, 'This spellbook calls forth a meteor from the heavens.'),
    SpellBook('Spell Book: Enflame', 1, 1500, 6, 'This ancient tome contains the dangerous spell Enflame.'),
    SpellBook('Spell Book: Greater Enflame', 1, 3000, 7, 'An ancient manuscript with the enhanced Enflame spell.'),
    SpellBook('Spell Book: Barrier', 1, 4000, 8, 'This iron bound book contains the spell Barrier.'),
    SpellBook('Spell Book: Vaporize', 1, 5000, 9, 'This book brims with the power of the spell Vaporize.'),
    SpellBook('Spell Book: Flame Lance', 1, 5000, 10, 'This forbidden tome contains the secret spell Flame Lance.'),

    SpellBook('Spell Book: Vines', 1, 500, 11, 'A spell tome containing the nature spell Vines.'),
    SpellBook('Spell Book: Poison', 1, 1500, 12, 'This spell book contains the mythical spell Poison.'),
    SpellBook('Spell Book: Restore', 1, 600, 13, 'This spell book contains the healing spell Restore.'),
    SpellBook('Spell Book: Greater Restore', 1, 2500, 14, 'An ancient manuscript containing the enhanced spell Greater Restore.'),
    SpellBook('Spell Book: Absorb', 1, 2500, 15, 'A spell book with the instructions for the Absorb spell.'),
    SpellBook('Spell Book: Greater Absorb', 1, 4000, 16, 'A powerful and forbidden spell book containing the enhanced Greater Absorb.'),
    SpellBook('Spell Book: Regenerate', 1, 3000, 17, 'A spell book with the heal-over-time spell Regenerate.'),
    SpellBook('Spell Book: Death Touch', 1, 6000, 18, 'A black spell book containing the forbidden spell Death Touch.'),
    SpellBook('Spell Book: Duplicate', 1, 4000, 19, 'An ancient manuscript containing the Ducplicate spell.'),
    SpellBook('Spell Book: Teleport', 1, 6000, 20, 'A white book containing the spell Teleport.'),
    SpellBook('Spell Book: Conjure', 1, 6000, 21, 'A blue book containing the spell Conjure.'),

    Mount('Donkey', 1, 700, 1.2, 'A standard donkey for carrying loads or even a person.'),
    Mount('Field Ox', 1, 800, 1.2, 'A large ox from the field that is great for pulling a plow.'),
    Mount('Work Horse', 1, 1200, 1.4, 'A fine work horse that can work the fields.'),
    Mount('Mega Boar', 1, 1500, 1.45, 'A large and hulking beast with massive tusks.'),
    Mount('Paint Horse', 1, 1800, 1.5, 'A good horse for travelling the roads and the most common.'),
    Mount('Bander Hound', 1, 2000, 1.55, 'A massive hound that is as loyal as it is large.'),
    Mount('Mustang', 1, 2500, 1.6, 'A formerly wild horse with strength and speed.'),
    Mount('Sabre Cat', 1, 3000, 1.7, 'A large and powerful cat native to the valley.'),
    Mount('Noble Horse', 1, 4000, 1.8, 'A powerful and fast horse with a long lineage.'),
    Mount('Race Horse', 1, 5000, 2, 'A powerful and fast horse with incredible speed.'),
    Mount('Pegasi', 1, 7500, 2.1, 'A magnificent and legendary winged horse whose sighting is a good omen.'),
    Mount('Wyvern', 1, 10000, 2.5, 'A large and powerful creature occasionally seen in the skies of the valley.'),

    Item('Bones', 1, 10, 'A collection of random bones from an unknown source.'),
    Item('Leather', 1, 25, 'A leather strip that has been collected from an animal of some kind.'),
    Item('Bolt of Cloth', 1, 75, 'A woven bolt of cloth ready for tailoring.'),
    Item('Bolt of Silk', 1, 200, 'A luxurious and soft bolt of silk. How fancy!'),
    Item('Rags', 1, 10, 'A bundle of torn and ruined cloth.'),
    Item('Sticks', 2, 15, 'A bundle of sticks collected with no immediate purpose.'),
    Item('Wood Carving', 1, 30, 'A small decorative carving of wood.'),
    Item('Runestones', 1, 50, 'Small stones with runes carved in them likely by a Northman.'),
    Item('Wood Cup', 1, 15, 'A used wooden cup. Still smells like mead...'),
    Item('Emerald', 1, 250, 'A small glistening green emerald worth a fair price.'),
    Item('Ruby', 1, 500, 'A small radiant ruby worth a sizeable sum at a trader.'),
    Item('Diamond', 1, 1000, 'A small diamond worth a small fortune and sought after by kings.'),
    Item('Firewood', 3, 25, 'A piece of firewood for keeping warm in the winter.'),
    Item('Clay Cup', 2, 35, 'A basic cup made from clay. Appears clean.'),
    Item('Basket', 1, 30, 'A small wicker basket useful for storing flowers and herbs.'),
    Item('Small Painting', 2, 125, 'A small and basic painting. Looks nice.'),
    Item('Statuette', 1, 150, 'A small and well carved statue of a person. Who could it be?'),
    Item('Simple Necklace', 1, 25, 'A simple necklace with a wooden pendant.'),
    Item('Gold Ring', 1, 150, 'A small gold ring that should fetch a tidy sum.'),
    Item('Silver Bracelet', 1, 100, 'A finely made silver bracelet popular amongst ladies.'),
    Item('Silver Cup', 2, 150, 'A silver cup perfect for drinking ale from.'),
    Item('Gold Goblet', 2, 250, 'A gold goblet with engravings fit for a lord.'),
    Item('Ancient Coin', 1, 300, 'A small but ancient coin from a lost forgotten empire.'),
    
    Item('Gold Nugget', 1, 250, 'A glimmering nugget of solid gold.'),
    Item('Silver Nugget', 1, 125, 'A shiny nugget of siver.'),
    Item('Gold Ingot', 10, 2500, 'A solid ingot of gold worth a small fortune.'),
    Item('Silver Ingot', 10, 1250, 'A solid ingot of silver that should fetch a hefty price.'),
    Item('Fishing Pole', 2, 350, 'A standard fishing rod with fishing line, hook, and floater.'),
]

def getItem(i):
    return ITEM_LIST[i]

def getRandomItem(type=None):
    if type:
        while True:
            i = random.randint(0, len(ITEM_LIST)-1)
            if getItem(i).type == type:
                return i
    else:
        return random.randint(0, len(ITEM_LIST)-1)

def printItems():
    i = 0
    for item in ITEM_LIST:
        print( str(i) + ': ' + item.getColorString() )
        i += 1

class Inventory:
    def __init__(self):
        self.gold = 0
        self.primary = 0
        self.secondary = 0
        self.head = 0
        self.torso = 0
        self.hands = 0
        self.feet = 0
        self.mount = 0
        self.bag = []
        self.spells = []

    def applyLootList(self, player, lootList):
        exp = lootList.getExp()
        gold = lootList.getGold()
        stuff = lootList.getItems()
        self.addGold(gold)
        player.addExperience(exp)
        print(text.get('inventoryLoot', [player.name, exp, gold]), color='yellow')
        print('Inventory:', color='white')
        for i in stuff:
            self.addItem(i)
            item = getItem(i)
            print('', item.getString())
        input(text.get('continue'), color='cyan')
    
    def printAll(self):
        print('Total Gold:', self.gold, color='yellow')
        print('Equipped Items:', color='white')
        
        if self.primary > 0:
            print('  Primary:', ITEM_LIST[ self.primary ].getString(), color='white' )
        else:
            print('  Primary: None')
            
        if self.secondary > 0:    
            print('  Secondary:', ITEM_LIST[ self.secondary  ].getString(), color='white' )
        else:
            print('  Seconday: None')
        
        if self.head > 0:
            print('  Head:', ITEM_LIST[ self.head  ].getString(), color='white' )
        else:
            print('  Head: None')
        
        if self.torso > 0:
            print('  Torso:', ITEM_LIST[ self.torso ].getString(), color='white' )
        else:
            print('  Torso: None')
        
        if self.hands > 0:
            print('  Hands:', ITEM_LIST[ self.hands ].getString(), color='white' )
        else:
            print('  Hands: None')
        
        if self.feet > 0:
            print('  Feet:', ITEM_LIST[ self.feet ].getString(), color='white' )
        else:
            print('  Feet: None')

        if self.mount > 0:
            print('  Mount:', ITEM_LIST[ self.mount ].getString(), color='white' )
        else:
            print('  Mount: None')
            
        print('Inventory Items:', color='white')
        for i in range( len(self.bag) ):
            item = ITEM_LIST[ self.bag[i] ]
            print( '  ' + str(i) + ':', item.getColorString(), color='white' )

    
    def getItem(self, i):
        return ITEM_LIST[i]
    
    def addItem(self, i):
        self.bag.append(i)

    def addSpell(self, i):
        if i not in self.spells:
            self.spells.append(i)

        self.spells.sort()

    def setGold(self, i):
        self.gold = i
    
    def addGold(self, i):
        self.gold += i
    
    def removeItem(self, i):
        return self.bag.pop(i)

    def getConsumables(self):
        consumables = []
        for i in self.bag:
            item = ITEM_LIST[i]
            if item.consumable:
                consumables.append(i)
        return consumables
        
    def equipItem(self, i):
        item = ITEM_LIST[i]
        if item.slot == 'primary':
            if item.skill == 'One Handed':
                self.unequipSlot('primary')
            else:
                self.unequipSlot('primary')
                self.unequipSlot('secondary')
            self.primary = i
            print('Primary slot equipped.', color='blue')
        elif item.slot == 'secondary':
            if self.primary > 0 and ITEM_LIST[self.primary].skill != 'One Handed':
                self.unequipSlot('primary')
            self.unequipSlot('secondary')
            self.secondary = i
            print('Secondary slot equipped.', color='blue')
        elif item.slot == 'head':
            self.unequipSlot('head')
            self.head = i
            print('Head slot equipped.', color='blue')
        elif item.slot == 'torso':
            self.unequipSlot('torso')
            self.torso = i
            print('Torso slot equipped.', color='blue')
        elif item.slot == 'hands':
            self.unequipSlot('hands')
            self.hands = i
            print('Hands slot equipped.', color='blue')
        elif item.slot == 'feet':
            self.unequipSlot('feet')
            self.feet = i
            print('Feet slot equipped.', color='blue')
        elif item.slot == 'mount':
            self.unequipSlot('mount')
            self.mount = i
            print('Mount saddled.', color='blue')
            
    def unequipSlot(self, slot):
        if slot == 'primary':
            if self.primary > 0:
                item = self.primary
                self.primary = 0
                self.bag.append(item)
                print('Primary slot unequipped.', color='blue')
        elif slot == 'secondary':
            if self.secondary > 0:
                item = self.secondary
                self.secondary = 0
                self.bag.append(item)
                print('Secondary slot unequipped.', color='blue')
        elif slot == 'head':
            if self.head > 0:
                item = self.head
                self.head = 0
                self.bag.append(item)
                print('Head slot unequipped.', color='blue')
        elif slot == 'torso':
            if self.torso > 0:
                item = self.torso
                self.torso = 0
                self.bag.append(item)
                print('Torso slot unequipped.', color='blue')
        elif slot == 'hands':
            if self.hands > 0:
                item = self.hands
                self.hands = 0
                self.bag.append(item)
                print('Hands slot unequipped.', color='blue')
        elif slot == 'feet':
            if self.feet > 0:
                item = self.feet
                self.feet = 0
                self.bag.append(item)
                print('Feet slot unequipped.', color='blue')
        elif slot == 'mount':
            if self.mount > 0:
                item = self.mount
                self.mount = 0
                self.bag.append(item)
                print('Mount unsaddled.', color='blue')
                
    def getTotalArmor(self):
        total = 0
        if self.secondary > 0:
            item = ITEM_LIST[self.secondary]
            if item.armor:
                total += item.armor
        if self.head > 0:
            item = ITEM_LIST[self.head]
            total += item.armor
        if self.torso > 0:
            item = ITEM_LIST[self.torso]
            total += item.armor
        if self.hands > 0:
            item = ITEM_LIST[self.hands]
            total += item.armor
        if self.feet > 0:
            item = ITEM_LIST[self.feet]
            total += item.armor
        return round(total, 1)
    
    def getTotalDamage(self):
        total = [0,0]
        if self.secondary > 0:
            item = ITEM_LIST[self.secondary]
            if item.damage:
                total[0] += item.damage[0]
                total[1] += item.damage[1]
        if self.primary > 0:
            item = ITEM_LIST[self.primary]
            total[0] += item.damage[0]
            total[1] += item.damage[1]

        if total[0] == 0 and total[1] == 0:
            total[0] = 1
            total[1] = 5
        else:
            total[0] = round(total[0], 1)
            total[1] = round(total[1], 1)

        return total
    
    def getTotalWeight(self):
        total = 0
        if self.primary > 0:
            item = ITEM_LIST[self.primary]
            total += item.weight
        if self.secondary > 0:
            item = ITEM_LIST[self.secondary]
            total += item.weight
        if self.head > 0:
            item = ITEM_LIST[self.head]
            total += item.weight
        if self.torso > 0:
            item = ITEM_LIST[self.torso]
            total += item.weight
        if self.hands > 0:
            item = ITEM_LIST[self.hands]
            total += item.weight
        if self.feet > 0:
            item = ITEM_LIST[self.feet]
            total += item.weight
        return round(total, 1)

    def getTotalSpeed(self, weight=0):
        total = 0
        count = 0

        if self.primary > 0:
            total += ITEM_LIST[self.primary].speed
            count += 1

        if self.secondary > 0:
            total += ITEM_LIST[self.secondary].speed
            count += 1

        if total == 0:
            total = 10 - weight / 15
        else:
            total /= count
            total = round(total - weight / 15, 1)

        return [total, total]

    def getMoveSpeed(self, weight):
        if self.mount > 0:
            mount = getItem(self.mount)
            return mount.speed
        else:
            return 1
            
def showInventoryMain(player, inventory):
    while True:
        print()
        print(text.get('titleInventory'), color='blue')
        inventory.printAll()
        print(text.get('inventoryMenu'), color='white')
        select = input(text.get('selection'), color='cyan').lower()
        if select == 'u':
            confirmUnequip = False
            while confirmUnequip != True:
                print(text.get('inventoryUnequip'), color='blue')

                unequipSelect = input()
                if unequipSelect == '0':
                    inventory.unequipSlot('primary')
                    confirmUnequip = True
                    input(text.get('continue'), color='cyan')
                elif unequipSelect == '1':
                    inventory.unequipSlot('secondary')
                    confirmUnequip = True
                    input(text.get('continue'), color='cyan')
                elif unequipSelect == '2':
                    inventory.unequipSlot('head')
                    confirmUnequip = True
                    input(text.get('continue'), color='cyan')
                elif unequipSelect == '3':
                    inventory.unequipSlot('torso')
                    confirmUnequip = True
                    input(text.get('continue'), color='cyan')
                elif unequipSelect == '4':
                    inventory.unequipSlot('hands')
                    confirmUnequip = True
                    input(text.get('continue'), color='cyan')
                elif unequipSelect == '5':
                    inventory.unequipSlot('feet')
                    confirmUnequip = True
                    input(text.get('continue'), color='cyan')
                elif unequipSelect == '6':
                    inventory.unequipSlot('mount')
                    confirmUnequip = True
                    input(text.get('continue'), color='cyan')
                elif unequipSelect == 'b':
                    confirmUnequip = True
                else:
                    print(text.get('invalidSelection'), color='red')
        elif select == 'e':
            itemSelectConfirm = False
            
            while itemSelectConfirm != True:
                itemSelect = input(text.get('selection2'), color='cyan').lower()
                if itemSelect == 'b':
                    itemSelectConfirm = True
                else:
                    try:
                        itemSelect = int(itemSelect)
                    except:
                        print(text.get('invalidSelection'), color='red')
                        itemSelect = None

                    if itemSelect is not None and itemSelect < len(inventory.bag):
                        i = inventory.bag[itemSelect]
                        item = ITEM_LIST[i]
                        if item.slot:
                            inventory.equipItem( inventory.removeItem(itemSelect) )
                            print(text.get('inventoryEquipConfirm', [player.name, item.name]), color='blue')
                            itemSelectConfirm = True
                            input(text.get('continue'), color='cyan')
                        else:
                            print(text.get('invalidSelection'), color='red')
        elif select == 'c':
            itemSelectConfirm = False

            while itemSelectConfirm != True:
                itemSelect = input(text.get('selection2'), color='cyan').lower()
                if itemSelect == 'b':
                    itemSelectConfirm = True
                else:
                    try:
                        itemSelect = int(itemSelect)
                        i = inventory.bag[itemSelect]
                        item = ITEM_LIST[i]
                        if item.consumable:
                            if item.consume(player, inventory):
                                inventory.removeItem(itemSelect)
                            itemSelectConfirm = True
                            input(text.get('continue'), color='cyan')
                        else:
                            print(text.get('invalidSelection'), color='red')
                    except:
                        print(text.get('invalidSelection'), color='red')
        elif select == 'i':
            itemSelectConfirm = False

            while itemSelectConfirm != True:
                itemSelect = input(text.get('selection2'), color='cyan').lower()
                if itemSelect == 'b':
                    itemSelectConfirm = True
                else:
                    try:
                        itemSelect = int(itemSelect)
                        i = inventory.bag[itemSelect]
                        item = ITEM_LIST[i]
                        item.getDescription()
                        itemSelectConfirm = True
                        input(text.get('continue'), color='cyan')
                    except:
                        print(text.get('invalidSelection'), color='red')

        elif select == 'b':
            break
