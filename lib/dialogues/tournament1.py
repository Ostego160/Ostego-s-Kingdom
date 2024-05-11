from lib import dialogue
from lib.dialogue import DialogueOption
from lib import mapper
from lib import location
from lib import npc

dialogue1 = dialogue.cloneDialogue('villager1', 'tournament1')

response1 = dialogue1.responses[0]

option1 = response1.insertOption(1, DialogueOption('Hi {npc.name}, I would like to enter the tournament!'))

response0a = option1.addResponse('I\'m sorry {player.name}. We don\'t have a tournament at the moment.', dialogue.checkTournamentNotReady)

response1a = option1.addResponse('Of course {player.name}. You are our reigning champion and will be defending your title.', dialogue.checkArenaChampion)

option1a1 = response1a.addOption(DialogueOption('Sounds good. Bring on the lackeys!'))
response1a1a = option1a1.addResponse('The tournament is concluded. There will be another one soon.', dialogue.startTournamentDefense)
response1a1a.setExit(True)

option1a2 = response1a.addOption(DialogueOption('On second thought, let\'s not.'))
response1a2a = option1a2.addResponse('That\'s alright. Come back anytime.')

response2a = option1.addResponse('Of course {player.name}. But the tournament is dangerous. Are you certain?')

option2a1 = response2a.addOption(DialogueOption('Let\'s bust some heads!'))
response2a1a = option2a1.addResponse('The tournament is concluded. There will be another one soon.', dialogue.startTournament)
response2a1a.setExit(True)

option2a2 = response2a.addOption(DialogueOption('On second thought, let\'s not.'))
response2a2a = option2a2.addResponse('That\'s alright. Come back anytime.')

