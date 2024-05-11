from lib import dialogue
from lib.dialogue import DialogueOption

dialogue1 = dialogue.newDialogue('bounty1')
response1 = dialogue1.addResponse('Stop right there {player.name}! You\'re under arrest!')

option1 = response1.addOption( DialogueOption('Would some gold make you forget about me?', dialogue.checkApologizeGold) )
response1a = option1.addResponse('Perhaps. My pocket is a bit light...', dialogue.checkTakesBribe)
option1a1 = response1a.addOption( DialogueOption('Here you go.'))
response1a1a = option1a1.addResponse('Good. Now be on your way before someone sees.', dialogue.finalizeApologizeGold)
response1a1a.setExit(True)
response1b = option1.addResponse('What do you take me for! Forget it!', dialogue.finalizeJail)
response1b.setExit(True)

option2 = response1.addOption( DialogueOption('You\'ll never take me alive! (ATTACK)') )
response2a = option2.addResponse('Come peace fully now {player.name}.')
option2a1 = response2a.addOption( DialogueOption('No. I\'m not going with you. (ATTACK)') )
response2a1a = option2a1.addResponse('Very well. I won\'t hold back', dialogue.finalizeBattle)
option2a2 = response2a.addOption( DialogueOption('Very well. I submit.') )
response2a2a = option2a2.addResponse('I\'m glad you made the right choice.', dialogue.finalizeJail)
response2a2a.setExit(True)

option3 = response1.addOption( DialogueOption('Who? I\'m not this person you\'re looking for.') )
response3a = option3.addResponse('My mistake. Move Along.', dialogue.checkSpeechGuard)
response3a.setExit(True)
response3b = option3.addResponse('Nice try. Off to jail with you.', dialogue.finalizeJail)
response3b.setExit(True)

option4 = response1.addOption( DialogueOption('Very well. I submit.') )
response4a = option4.addResponse('Very good. I hoped you would come peacefully.', dialogue.finalizeJail)
response4a.setExit(True)
