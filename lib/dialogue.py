import random

from lib import text
from lib import loot
from lib import items
from lib import quest
from lib import constants
from lib import mapper
from lib import npc as NPC
from lib import location
from lib import tournament

from lib.colortext import colorprint as print
from lib.colortext import colorinput as input
from lib.colortext import colorstr

DIALOGUE = {}

def blankFunc(npc, player, inventory, loc):
    return True

class DialogueResponse():
    def __init__(self, text, func=blankFunc):
        self.text = text
        self.func = func
        self.options = []
        self.lootList = None
        self.trade = None
        self.exit = None
        self.questTrigger = None
        self.quest = None

    def clone(self, deep=False):
        response = DialogueResponse(self.text, self.func)
        response.lootList = self.lootList
        response.trade = self.trade
        response.exit = self.exit
        response.questTrigger = self.questTrigger
        response.quest = self.quest

        if deep:
            for option in self.options:
                response.options.append(option.clone(True))
        else:
            response.options = self.options

        return response

    def addOption(self, option):
        self.options.append(option)
        return option

    def insertOption(self, pos, option):
        self.options.insert(pos, option)
        return option

    def pullOptions(self, response):
        for option in response.options:
            self.options.append(option)

    def checkResponse(self, npc, player, inventory, loc):
        return self.func(npc, player, inventory, loc)

    def setLootList(self, lootList=None):
        self.lootList = lootList

    def setTrade(self, v=None):
        self.trade = v

    def setExit(self, v=None):
        self.exit = v

    def setQuestTrigger(self, v=None):
        self.questTrigger = v

    def setQuest(self, quest=None):
        self.quest = quest

    def printText(self, npc, player, inventory):
        print(f'{npc.name}: {self.text.format(npc=npc, player=player, inventory=inventory)}', color='blue')

    def getAvailableOptions(self, npc, player, inventory, loc):
        available = []
        for option in self.options:
            if option.func(npc, player, inventory, loc):
                available.append(option)
        return available

    def processLootList(self, player, inventory):
        if self.lootList:
            inventory.applyLootList(player, loot.get(self.lootlist))

class DialogueOption():
    def __init__(self, text=None, func=blankFunc):
        self.text = text
        self.func = func
        self.responses = []

    def clone(self, deep=False):
        dialogue = DialogueOption(self.text, self.func)
        if deep:
            for response in self.responses:
                dialogue.responses.append(response.clone(True))
        else:
            dialogue.responses = self.responses

        return dialogue

    def pullResponses(self, option):
        for response in option.responses:
            self.responses.append(response)

    def addResponse(self, text, func=blankFunc):
        response = DialogueResponse(text, func)
        self.responses.append(response)
        return response

    def insertResponse(self, pos, text, func=blankFunc):
        response = DialogueResponse(text, func)
        self.responses.insert(pos, response)
        return response

    def getResponse(self, npc, player, inventory):
        for response in self.responses:
            if response.func(npc, player, inventory):
                return response

    def getQuestTriggerResponses(self):
        responses = []

        def recurse(option):
            for response in option.responses:
                if response.questTrigger:
                    responses.append(response)
                    for sub in response.options:
                        recurse(sub)
        recurse(self)

        return responses

def newDialogue(id):
    DIALOGUE[id] = DialogueOption()
    return DIALOGUE[id]

def getDialogue(id, clone=False):
    if clone:
        return DIALOGUE[id].clone()
    else:
        return DIALOGUE[id]

def cloneDialogue(prevId, id):
    DIALOGUE[id] = getDialogue(prevId, True)
    return DIALOGUE[id]

def showDialogueMain(dialogue, npc, player, inventory, loc):

    startDialogue = dialogue

    while dialogue:
        if dialogue.text:
            print(f'\n{player.name}: {dialogue.text.format(npc=npc, player=player, inventory=inventory)}', color='white')

        if len(dialogue.responses) > 0:
            for response in dialogue.responses:
                if response.func(npc, player, inventory, loc):
                    response.printText(npc, player, inventory)
                    response.processLootList(player, inventory)

                    if response.trade:
                        return 'trade'
                    elif response.exit:
                        return False

                    options = response.getAvailableOptions(npc, player, inventory, loc)
                    if len(options) > 0:
                        for i, option in enumerate(options):
                            print(f'  {i}: {option.text.format(npc=npc, player=player, inventory=inventory)}', color='white')
                        continueDialogueOption = True
                        while continueDialogueOption:
                            select = input(text.get('selection'), color='cyan')
                            try:
                                dialogue = options[int(select)]
                                continueDialogueOption = False
                            except:
                                print(text.get('invalidSelection'), color='red')
                    else:
                        dialogue = startDialogue
                    break
        else:
            dialogue = startDialogue
    input(text.get('continue'), color='cyan')
def checkHasMet(npc, player, inventory, loc):
    return npc.hasMet

def checkHasNotMet(npc, player, inventory, loc):
    return not npc.hasMet

def checkMoodVeryLow(npc, player, inventory, loc):
    return npc.mood < 25

def checkMoodLow(npc, player, inventory, loc):
    return 25 <= npc.mood <= 50

def checkMoodAverage(npc, player, inventory, loc):
    return 50 < npc.mood <= 75

def checkMoodHigh(npc, player, inventory, loc):
    return npc.mood > 75

def checkPositiveOpinion(npc, player, inventory, loc):
    return npc.opinion >= 0

def checkNegativeOpinion(npc, player, inventory, loc):
    return npc.opinion < 0

def checkOpinionVeryLow(npc, player, inventory, loc):
    return npc.opinion <= -50

def checkOpinionLow(npc, player, inventory, loc):
    return -50 < npc.opinion < 0

def checkOpinionNeutral(npc, player, inventory, loc):
    return 0 <= npc.opinion < 10

def checkOpinionHigh(npc, player, inventory, loc):
    return 10 <= npc.opinion < 50

def checkOpinionVeryHigh(npc, player, inventory, loc):
    return npc.opinion >= 50

def checkApologizeSpeech(npc, player, inventory, loc):
    return player.skills[9] >= -npc.opinion

def checkApologizeGold(npc, player, inventory, loc):
    return inventory.gold >= npc.opinion * -75

def checkBounty(npc, player, inventory, loc):
    return player.bounty > 0

def checkBountyHigh(npc, player, inventory, loc):
    return player.bounty > 1000

def checkBountyVeryHigh(npc, player, inventory, loc):
    return player.bounty > 5000

def checkBountyJail(npc, player, inventory, loc):
    if checkBountyHigh(npc, player, inventory, loc):
        player.status = 'jail'
        return True

def checkBountyFine(npc, player, inventory, loc):
    return inventory.gold >= int(player.bounty * 1.2)

def checkArenaChampion(npc, player, inventory, loc):
    return player.arenaChampion

def checkSpeechGuard(npc, player, inventory, loc):
    roll = random.randint(-10, 10)
    return player.skills[9] + roll >= 50

def finalizeHasMet(npc, player, inventory, loc):
    npc.hasMet = True
    return True

def finalizeApologizeGold(npc, player, inventory, loc):
    gold = (npc.opinion+100) * -75
    npc.gold += gold
    inventory.gold -= gold
    npc.opinion = random.randint(1,10)
    print(text.get('stealBribeComplete', [npc.name, gold]), color='blue')
    return True

def finalizeApologizeSpeech(npc, player, inventory, loc):
    npc.opinion = random.randint(1,10)
    print(text.get('stealApology', [npc.name]), color='blue')
    return True

def finalizeBattle(npc, player, inventory, loc):
    npc.battle = True
    return True

def finalizeBountyFine(npc, player, inventory, loc):
    total = int(player.bounty*1.2)
    print(text.get('stealBribeComplete', [npc.name, total]))
    inventory.addGold(-total)
    player.bounty = 0
    return True

def finalizeJail(npc, player, inventory, loc):
    player.status = 'jail'
    return True

def checkTakesBribe(npc, player, inventory, loc):
    return npc.takesBribe

def checkHasQuestForNPC(npc, player, inventory, loc):
    for entry in quest.getJournal():
        if entry.type == 0 or entry.type == 2 or entry.type == 3:
            if entry.npc == npc:
                return True
        elif entry.type == 1:
            if entry.targetNPC == npc:
                return True

def checkFetchQuestStart(npc, player, inventory, loc):
    if not npc.quest and npc.givesQuest:
        return npc.questType == 0

def checkHasFetchQuest(npc, player, inventory, loc):
    for entry in quest.getJournal():
        if entry.npc == npc and entry.type == 0:
            return True

def checkFetchQuestComplete(npc, player, inventory, loc):
    for entry in quest.getJournal():
        if entry.type == 0 and entry.npc == npc:
            for v in inventory.bag:
                if v == entry.targetItem:
                    return True

def checkDeliverQuestStart(npc, player, inventory, loc):
    if not npc.quest and npc.givesQuest:
        return npc.questType == 1

def checkHasDeliverQuest(npc, player, inventory, loc):
    for entry in quest.getJournal():
        if entry.npc == npc and entry.type == 1:
            return True

def checkDeliverQuestComplete(npc, player, inventory, loc):
    for entry in quest.getJournal():
        if entry.type == 1 and entry.targetNPC == npc:
            for v in inventory.bag:
                if v == entry.targetItem:
                    return True

def checkKillQuestStart(npc, player, inventory, loc):
    if not npc.quest and npc.givesQuest:
        return npc.questType == 2

def checkHasKillQuest(npc, player, inventory, loc):
    for entry in quest.getJournal():
        if entry.npc == npc and entry.type == 2:
            return True

def checkKillQuestComplete(npc, player, inventory, loc):
    for entry in quest.getJournal():
        if entry.type == 2 and entry.npc == npc:
            complete = mapper.getPersonByRef(entry.targetNPC)
            if not complete:
                return True

def checkHuntQuestStart(npc, player, inventory, loc):
    if not npc.quest and npc.givesQuest:
        return npc.questType == 3

def checkHasHuntQuest(npc, player, inventory, loc):
    for entry in quest.getJournal():
        if entry.npc == npc and entry.type == 3:
            return True

def checkHuntQuestComplete(npc, player, inventory, loc):
    for entry in quest.getJournal():
        if entry.type == 3 and entry.npc == npc:
            count = 0
            for v in inventory.bag:
                if v == entry.targetItem:
                    count += 1
            return count >= entry.itemQuantity

def talkAboutEarl(npc, player, inventory, loc):
    earl = mapper.getUniqueNPC('Earl')
    print(f'{npc.name}: Our Earl is Lord {earl.name} who stays at {earl.home.name}. {earl.pronoun[0].capitalize()} is a vassal\n\tserving King Ostego and the valley is {earl.pronoun[1]} realm.', color='blue')
    print(f'{npc.name}: {earl.pronoun[0].capitalize()} is known to be', end=' ', sep='', color='blue')
    if len(earl.traits) > 1:
        for i, trait in enumerate(earl.traits):
            if i == len(earl.traits)-1:
                print(f'and {trait}.', color='blue')
            else:
                print(f'{trait}', sep='', end=', ', color='blue')
    elif len(earl.traits) == 1:
        print(f'{earl.traits[1]}.', color='blue')
    else:
        print(f'a very ordinary Lord.', color='blue')
    return True

def talkToEarl(npc, player, inventory, loc):
    earl = mapper.getUniqueNPC('Earl')
    if earl.canApproach:
        print(f'{player.name} approaches the Earl, and the men allow it, removing {player.pronoun[1]} weapons.', color='white')
        input(text.get('continue'), color='cyan')
        return True
    else:
        print(f'{player.name} attempts to approach the Earl but the Lord\'s men stop {player.pronoun[2]}.', color='white')
        input(text.get('continue'), color='cyan')


def searchForNPC(npc, player, inventory, loc):
    continueSearch = True

    while continueSearch:
        print(f'{npc.name}: Who are you looking for?', color='blue')

        select = input(text.get('selection2'), color='cyan').lower()

        if select == 'b':
            continueSearch = False
        else:
            loc, travelling = mapper.getAllByNPC(player, select)

            if len(loc) > 0 or len(travelling) > 0:
                print(f'\n{npc.name}: Here is who I know about.', color='blue')
                for entry in loc:
                    print(f'{npc.name}: {entry[2]} is currently at {entry[0].name} {int(entry[1]) * 2} kilometers away.', color='blue')
                for entry in travelling:
                    print(f'{npc.name}: {entry[0].name} is currently travelling to {entry[1].name}.', color='blue')
                print()
            else:
                print(f'\n{npc.name}: I don\'t know anyone named {select.capitalize()} in the valley.', color='blue')

            continueSearch = False
    return True

def searchForLocationType(npc, player, inventory, loc):
    continueSearch = True

    while continueSearch:
        print(f'{npc.name}: What kind of location are you looking for?', color='blue')
        for i, type in enumerate(location.LOCATION_TYPES):
            print(f'  {i}: {type}', color='white')

        select = input(text.get('selection2')).lower()

        if select == 'b':
            continueSearch = False
        else:
            lType = None
            try:
                select = int(select)
                lType = location.LOCATION_TYPES[select]

            except:
                print(text.get('invalidSelection'), color='red')
                lType = None

            if lType:

                entry = mapper.getNearestByLocationType(player, lType)

                if entry:
                    print(f'\n{npc.name}: The nearest {lType} is {entry[0].name} {int(entry[1]) * 2} kilometers away.', color='blue')
                else:
                    print(f'\n{npc.name}: Unfortunately, we don\'t have a {lType} in the valley.', color='blue')
                continueSearch = False
    return True

def searchForProfessionType(npc, player, inventory, loc):
    continueSearch = True

    while continueSearch:
        print(f'{npc.name}: What kind of profession are you looking for?', color='blue')
        for i, type in enumerate(NPC.NPC_TYPES):
            print(f'  {i}: {type}', color='white')

        select = input(text.get('selection2'), color='cyan').lower()

        if select == 'b':
            continueSearch = False
        else:
            pType = None
            try:
                select = int(select)
                pType = NPC.NPC_TYPES[select]

            except:
                print(text.get('invalidSelection'), color='red')
                pType = None

            if pType:

                entry = mapper.getNearestByProfessionType(player, pType)

                if entry:
                    print(f'\n{npc.name}: The nearest {pType} is at {entry[0].name} {int(entry[1]) * 2} kilometers away.', color='blue')
                else:
                    print(f'\n{npc.name}: Unfortunately, we don\'t have a {pType} in the valley.', color='blue')

                continueSearch = False
    return True

def searchForLandmarkType(npc, player, inventory, loc):
    continueSearch = True

    while continueSearch:
        keys = []
        print(f'{npc.name}: What kind of landmark are you looking for?', color='blue')
        for i, type in enumerate(location.LANDMARK):
            keys.append(type)
            print(f'  {i}: {type}', color='white')

        select = input(text.get('selection2'), color='cyan').lower()

        if select == 'b':
            continueSearch = False
        else:
            lType = None
            try:
                select = int(select)
                lType = keys[select]

            except:
                print(text.get('invalidSelection'), color='red')
                lType = None

            if lType:

                entry = mapper.getNearestByLandmarkType(player, lType)

                if entry:
                    print(f'\n{npc.name}: The nearest {lType} is at {entry[0].name} {int(entry[1])} kilometers away.', color='white')
                else:
                    print(f'\n{npc.name}: Unfortunately, we don\'t have a {lType} in the valley.', color='white')
                continueSearch = False
    return True

def finalizeFetchQuestComplete(npc, player, inventory, loc):
    journal = quest.getJournal()
    for entry in reversed(journal):
        if entry.npc == npc:
            for i, v in enumerate(inventory.bag):
                if v == entry.targetItem:
                    npc.items.append( inventory.bag.pop(i) )
                    lootList = loot.get(entry.lootList)
                    gold = lootList.getGold()
                    exp = lootList.getExp()
                    stuff = lootList.getItems()
                    print(text.get('journalQuestLoot', [player.name]), color='white')
                    print('  Exp:', exp, ' Gold:', gold, color='yellow')
                    inventory.gold += gold
                    player.exp += exp
                    for i in stuff:
                        item = items.getItem(i)
                        inventory.bag.append(i)
                        print(' ', item.getColorString(), color='white')
                    journal.remove(entry)
                    entry.npc.addOpinion(random.randint(5, 15))
                    entry.targetNPC.addOpinion(random.randint(5, 15))
                    npc.quest = None
                    input(text.get('continue'))
                    return True

def finalizeDeliverQuestComplete(npc, player, inventory, loc):
    journal = quest.getJournal()
    for entry in reversed(journal):
        if entry.targetNPC == npc:
            for i, v in enumerate(inventory.bag):
                if v == entry.targetItem:
                    entry.targetNPC.items.append( inventory.bag.pop(i) )
                    lootList = loot.get(entry.lootList)
                    gold = lootList.getGold()
                    exp = lootList.getExp()
                    stuff = lootList.getItems()
                    print(text.get('journalQuestLoot', [player.name]), color='white')
                    print('  Exp:', exp, ' Gold:', gold, color='yellow')
                    inventory.gold += gold
                    player.exp += exp
                    for i in stuff:
                        item = items.getItem(i)
                        inventory.bag.append(i)
                        print(' ', item.getColorString(), color='white')
                    journal.remove(entry)
                    entry.npc.opinion += random.randint(5, 15)
                    entry.targetNPC.opinion += random.randint(5, 15)
                    npc.quest = None
                    input(text.get('continue'))
    return True

def finalizeDefaultQuestComplete(npc, player, inventory, loc):
    journal = quest.getJournal()
    for entry in reversed(journal):
        if entry.npc == npc:
            lootList = loot.get(entry.lootList)
            gold = lootList.getGold()
            exp = lootList.getExp()
            stuff = lootList.getItems()
            print(text.get('journalQuestLoot', [player.name]), color='white')
            print('  Exp:', exp, ' Gold:', gold, color='yellow')
            inventory.gold += gold
            player.exp += exp
            for i in stuff:
                item = items.getItem(i)
                inventory.bag.append(i)
                print(' ', item.getColorString(), color='white')
            journal.remove(entry)
            entry.npc.opinion += random.randint(5, 15)
            entry.targetNPC.opinion += random.randint(5, 15)
            npc.quest = None
            input(text.get('continue'))

    return True

def finalizeHuntQuestComplete(npc, player, inventory, loc):
    journal = quest.getJournal()
    for entry in reversed(journal):
        if entry.type == 3 and entry.npc == npc:
            count = 0
            while count < entry.itemQuantity:
                inventory.bag.remove(129)
                npc.items.append(129)
                count += 1
            lootList = loot.get(entry.lootList)
            gold = lootList.getGold()
            exp = lootList.getExp()
            stuff = lootList.getItems()
            print(text.get('journalQuestLoot', [player.name]), color='white')
            print('  Exp:', exp, ' Gold:', gold, color='yellow')
            inventory.gold += gold
            player.exp += exp
            for i in stuff:
                item = items.getItem(i)
                inventory.bag.append(i)
                print(' ', item.getColorString(), color='white')
            journal.remove(entry)
            entry.npc.opinion += random.randint(5, 15)
            npc.quest = None
            input(text.get('continue'))

    return True

def addNewFetchQuest(npc, player, inventory, loc):
    fetch = quest.addRandomQuest(0, npc, player, inventory)
    item = items.getItem(fetch.targetItem)
    inventory.gold += item.value
    print(text.get('journalFetchMoney', [player.name, item.name, item.value]), color='white')
    npc.givesQuest = False

    return True

def addNewDeliverQuest(npc, player, inventory, loc):
    deliver = quest.addRandomQuest(1, npc, player, inventory)
    item = items.getItem(deliver.targetItem)
    print(text.get('journalDeliver', [player.name, item.name, deliver.targetNPC.name]), color='white')
    npc.givesQuest = False

    return True

def addNewKillQuest(npc, player, inventory, loc):
    kill = quest.addRandomQuest(2, npc, player, inventory)
    print(text.get('journalKill', [player.name, player.pronoun[1], kill.targetNPC.name]), color='white')
    npc.givesQuest = False

    return True

def addNewHuntQuest(npc, player, inventory, loc):
    hunt = quest.addRandomQuest(3, npc, player, inventory)
    item = items.getItem(hunt.targetItem)
    print(text.get('journalHunt', [player.name, item.name]), color='white')
    npc.givesQuest = False

    return True

def checkTournamentNotReady(npc, player, inventory, loc):
    return not player.clock.getTournament()

def startTournament(npc, player, inventory, loc):
    tournament.showTournamentMain(player, inventory, loc)
    return True

def startTournamentDefense(npc, player, inventory, loc):
    tournament.showTournamentDefense(player, inventory, loc)
    return True



