from lib import dialogue
from lib.dialogue import DialogueOption
from lib import mapper
from lib import location
from lib import npc

dialogue1 = dialogue.cloneDialogue('villager1', 'sheriff1')

response1 = dialogue1.responses[0]

option1 = response1.insertOption(1, DialogueOption('I would like to deal with my bounty.', dialogue.checkBounty))

response1a = option1.addResponse('A wise decision. You can either pay the fine or serve a jail sentence.')

option1a1 = response1a.addOption(DialogueOption('I will pay you to make this matter go away. Gold - {int(player.bounty*1.2)}', dialogue.checkBountyFine))

response1a1a = option1a1.addResponse('Very good. I will see that your bounty is taken care of immediately.', dialogue.finalizeBountyFine)

option1a2 = response1a.addOption(DialogueOption('I will serve the jail sentence.'))

response1a2a = option1a2.addResponse('Very well. Men take {player.pronoun[2]} into custody and be gentle about it.', dialogue.finalizeBountyFine)

option1a3 = response1a.addOption(DialogueOption('Actually never mind.'))

response1a3a = option1a3.addResponse('Not so fast. You\'re crimes are well known. Men, seize {player.pronoun[2]}!', dialogue.checkBountyJail)

response1a3b = option1a3.addResponse('Very well. But next time I might not be so friendly.')
