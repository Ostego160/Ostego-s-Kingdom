from lib import dialogue
from lib.dialogue import DialogueOption
from lib import mapper
from lib import location
from lib import npc

dialogue1 = dialogue.cloneDialogue('villager1', 'noble1')

response1 = dialogue1.responses[2]

option1 = response1.insertOption(1, DialogueOption('I would like to know more about our Lord, King Ostego.'))

response1a = option1.addResponse('King Ostego has ruled these lands for many years since he retook these lands from\n\tthe Bandit King Gregor Bjornson with the aid of the Northern Army.')

option1a1 = response1a.addOption(DialogueOption('What kind of ruler is he?'))

response1a1a = option1a1.addResponse('It is said that Ostego is fair and just to his friends and cruel and merciless\n\tto his enemies. In the war against Gregor Bjornson, Ostego commanded\n\tthe army himself and when Bjornson was captured, Ostego personally killed him.')

option1a2 = response1a.addOption(DialogueOption('What is Ostego\'s connection to the Northern realm?'))

response1a2a = option1a2.addResponse('After Gregor siezed the valley over twenty years ago, Ostego sailed to the North\n\tseeking assistance from the Viking Warlord Vidar Ragnvald who obliged\n\tafter being promised a large sum in spoils. Some of the vikings remain\n\tin the valley.')

option1a3 = response1a.addOption(DialogueOption('Thank you. That is all for now.'))

response1a3a = option1a3.addResponse('Of course good sir.')

response1a1a.addOption(option1a3)
response1a2a.addOption(option1a3)


option2 = response1.insertOption(2, DialogueOption('Can you tell me more about the Earl of the Valley?'))

response2a = option2.addResponse('Hopefully that answers your question.', dialogue.talkAboutEarl)

option2a1 = response2a.addOption(DialogueOption('Thank you for the information.'))
