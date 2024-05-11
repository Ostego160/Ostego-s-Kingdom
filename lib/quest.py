import random

from lib import text
from lib import items
from lib import mapper

from lib.colortext import colorprint as print
from lib.colortext import colorinput as input
from lib.colortext import colorstr

JOURNAL = []

QUEST_TYPES = ('fetch', 'deliver', 'kill', 'hunt')

QUEST_TIME = (24 * 7, 24 * 10)

class Quest:
    def __init__(self, type, npc, startTime, endTime, location, lootList='questDelivery', targetItem=None, targetNPC=None):
        self.type = type
        self.location   = location
        self.npc        = npc
        self.startTime  = startTime
        self.endTime    = endTime
        self.lootList   = lootList
        self.targetItem = targetItem
        self.targetNPC  = targetNPC
        self.state = 0
        self.itemQuantity = 0

    def update(self, clock, location, player, inventory):
        pass

    def fail(self):
        self.npc.addOpinion(random.randint(-15, -10))

def addQuest(*args):
    quest = Quest(*args)
    JOURNAL.append(quest)
    return quest

def addRandomQuest(type, npc, player, inventory):
    if type == 0:
        location = mapper.getRandomLocation()
        targetNPC = random.choice(location.people)
        while targetNPC == npc:
            targetNPC = random.choice(location.people)
        targetItem = items.getRandomItem('consumable')
        targetNPC.addItem(targetItem)
        startTime = player.clock.time
        endTime = startTime + random.randint(QUEST_TIME[0], QUEST_TIME[1])
        quest = Quest(0, npc, startTime, endTime, location, 'questDelivery', targetItem, targetNPC)
        npc.quest = quest
        JOURNAL.append(quest)
        return quest
    elif type == 1:
        location = mapper.getRandomLocation()
        targetNPC = random.choice(location.people)
        while targetNPC == npc:
            targetNPC = random.choice(location.people)
        targetItem = items.getRandomItem('consumable')
        inventory.addItem(targetItem)
        startTime = player.clock.time
        endTime = startTime + random.randint(QUEST_TIME[0]-24, QUEST_TIME[1]-24)
        quest = Quest(1, npc, startTime, endTime, location, 'questDelivery', targetItem, targetNPC)
        npc.quest = quest
        JOURNAL.append(quest)
        return quest
    elif type == 2:
        location = mapper.getRandomLocation()
        targetNPC = location.addRandomPerson(5)

        startTime = player.clock.time
        endTime = startTime + random.randint(QUEST_TIME[0], QUEST_TIME[1])
        quest = Quest(2, npc, startTime, endTime, location, 'questKill', targetNPC=targetNPC)
        npc.quest = quest
        JOURNAL.append(quest)
        return quest
    elif type == 3:
        location = npc.home
        targetItem = 129
        if not random.randint(0, 3):
            targetItem = 192
        startTime = player.clock.time
        endTime = startTime + random.randint(QUEST_TIME[0], QUEST_TIME[1])
        quest = Quest(3, npc, startTime, endTime, location, 'questDelivery', targetItem)
        quest.itemQuantity = random.randint(10, 20)
        npc.quest = quest
        JOURNAL.append(quest)
        return quest

def getJournal():
    return JOURNAL

def showJournalUpdate(player):
    hit = None

    for entry in reversed(JOURNAL):
        if player.clock.time > entry.endTime:
            print(text.get('journalTimeout', [player.name, player.pronoun[1], entry.npc.name]), color='red')
            entry.fail()
            JOURNAL.remove(entry)
            entry.npc.quest = None
            entry.npc.givesQuest = None
    if hit:
        input(text.get('continue'), color='cyan')


def showJournalMain(player):
    print(text.get('titleJournal'), color='blue')
    print(f'\n{player.name}\'s Journal:', color='white')
    if len(JOURNAL) > 0:
        for entry in JOURNAL:
            if entry.type == 0:
                npc = entry.npc
                item = items.getItem(entry.targetItem)
                print(text.get('formatBullet') + f'Fetch quest for {npc.name} at {npc.location.name}.', color='white')
                print(f'  Buy {item.name} from {entry.targetNPC.name} at {entry.location.name}\n  and return it to {npc.name}.', color='blue')
                print('  Fail date:', player.clock.getExternalDescription(entry.endTime), color='yellow')
            elif entry.type == 1:
                npc = entry.npc
                item = items.getItem(entry.targetItem)
                print(text.get('formatBullet') + f'Delivery quest for {npc.name} at {npc.location.name}.', color='white')
                print(f'  Deliver {item.name} to {entry.targetNPC.name} at {entry.location.name}.', color='blue')
                print('  Fail date:', player.clock.getExternalDescription(entry.endTime), color='yellow')
            elif entry.type == 2:
                npc = entry.npc
                target = entry.targetNPC
                print(text.get('formatBullet') + f'Kill quest for {npc.name} at {npc.location.name}.', color='white')
                print(f'  Kill {target.name} at {entry.location.name}.', color='blue')
                print('  Fail date:', player.clock.getExternalDescription(entry.endTime), color='yellow')
            elif entry.type == 3:
                npc = entry.npc
                item = items.getItem(entry.targetItem)
                print(text.get('formatBullet') + f'Hunt quest for {npc.name} at {npc.location.name}.', color='white')
                print(f'  Collect {entry.itemQuantity} {item.name}(s) and return to {npc.location.name}.', color='blue')
                print('  Fail date:', player.clock.getExternalDescription(entry.endTime), color='yellow')
    else:
        print('  No journal entries.', color='yellow')
    input(text.get('continue'), color='cyan')
