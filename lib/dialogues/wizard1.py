from lib import dialogue
from lib.dialogue import DialogueOption
from lib import mapper
from lib import location
from lib import npc

dialogue1 = dialogue.cloneDialogue('villager1', 'wizard1')

response1 = dialogue1.responses[0]

option1 = response1.insertOption(1, DialogueOption('I would like to know more about the Mages Guild.'))

response1a = option1.addResponse('The Mages Guild is where young men and women train as a mage apprentices.\n\tIt\'s the only institution authorized by King Ostego to practice magic.')

option1a1 = response1a.addOption(DialogueOption('I understand. Thank you for the information.'))

option2 = response1.insertOption(2, DialogueOption('Could I enroll in a class to gain new arcane knowledge?'))

response2a = option2.addResponse('Certainly. Being enrolled in the college requires you to remain at the\n\tMages Guild until the classes are complete although you can drop at anytime.\n\tWould you like to proceed with enrollment?')

option2a1 = response2a.addOption(DialogueOption('That sounds good. Let\'s move forward with enrollment.'))

response2a1a = option2a1.addResponse('For which school of magic will you study?')

option2a1a1 = response2a1a.addOption(DialogueOption('Fire Magic.'))

response2a1a1a = option2a1a1.addResponse('What level of class will you take?')

option2a1a1a1a1 = response2a1a1a.addOption(DialogueOption('Novice Level - 7 Days.'))
response2a1a1a1a = option2a1a1.addResponse('Very good. Right this way and I shall have someone find you quarters.')
response2a1a1a1a.setExit(True)

option2a1a1a1a2 = response2a1a1a.addOption(DialogueOption('Apprentice Level - 30 Days.'))
option2a1a1a1a2.responses.append(response2a1a1a1a)
option2a1a1a1a3 = response2a1a1a.addOption(DialogueOption('Journeyman Level - 60 Days.'))
option2a1a1a1a3.responses.append(response2a1a1a1a)
option2a1a1a1a4 = response2a1a1a.addOption(DialogueOption('Master Level - 90 Days.'))
option2a1a1a1a4.responses.append(response2a1a1a1a)

option2a1a2 = response2a1a.addOption(DialogueOption('Nature Magic.'))
option2a1a2.responses.append(response2a1a1a)

option2a2 = response2a.addOption(DialogueOption('On second thought, I\'ve changed my mind.'))
