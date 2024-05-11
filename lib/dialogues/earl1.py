from lib import dialogue
from lib.dialogue import DialogueOption
from lib import mapper
from lib import location
from lib import npc

noble = dialogue.getDialogue('noble1')

dialogue1 = dialogue.newDialogue('earl1')

response0 = dialogue1.addResponse('Please step forward.', dialogue.talkToEarl)
option1 = response0.addOption(DialogueOption('May I request an audience, your grace?'))
option1.pullResponses(noble)

response1 = dialogue1.addResponse('Get this peasant out of my sight!')
response1.setExit(True)