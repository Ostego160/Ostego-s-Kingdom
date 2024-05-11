from lib import dialogue
from lib.dialogue import DialogueOption
from lib import mapper
from lib import location
from lib import npc

dialogue1 = dialogue.cloneDialogue('noble1', 'court1')

response1 = dialogue1.responses[0]

option1 = response1.insertOption(1, DialogueOption('I would like to know more about our Lord, King Ostego.'))
