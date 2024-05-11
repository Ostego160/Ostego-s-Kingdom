from lib import dialogue
from lib.dialogue import DialogueOption
from lib import mapper
from lib import location
from lib import npc

dialogue1 = dialogue.newDialogue('villager1')
response00 = dialogue1.addResponse('I really can\'t stand you {player.name}. Please don\'t talk to me.', dialogue.checkOpinionVeryLow)
response00.setExit(True)

response0 = dialogue1.addResponse('Hello. I don\'t think we\'ve met before.', dialogue.checkHasNotMet)
option0 = response0.addOption(DialogueOption('Hello. My name is {player.name}.'))
response0a = option0.addResponse('Nice to meet you {player.name}. I am known as {npc.name}.', dialogue.finalizeHasMet)

response1 = dialogue1.addResponse('Hello there {player.name}.')

option1 = response1.addOption( DialogueOption('Hi {npc.name}, how are you today?') )
response1a = option1.addResponse('I am having a terrible day! Don\'t ask me about it.', dialogue.checkMoodVeryLow)
option1a = response1a.addOption( DialogueOption('Oh that\'s really too bad. I\'m sorry and I hope it gets better.') )
response1b = option1.addResponse('It really could be better! Things are rough.', dialogue.checkMoodLow)
option1b = response1b.addOption( DialogueOption('Oh that\'s really too bad. I\'m sorry and I hope it gets better.') )
response1c = option1.addResponse('It\'s a regular day! Everything is pretty average.', dialogue.checkMoodAverage)
option1c = response1c.addOption( DialogueOption('Well it could always be worse.') )
response1d = option1.addResponse('It\'s a wonderful day today! I\'m in a great mood.', dialogue.checkMoodHigh)
option1d = response1d.addOption( DialogueOption('That\'s really great to hear.') )

option9 = response1.addOption( DialogueOption('What is your opinion of me?') )
response9a = option9.addResponse('You are a very terrible person and I think I hate you.', dialogue.checkOpinionVeryLow)
option9a = response9a.addOption( DialogueOption('I understand.') )
response9b = option9.addResponse('I don\'t think I can trust you very much.', dialogue.checkOpinionLow)
option9b = response9b.addOption( DialogueOption('Okay hopefull I can change your mind.') )
response9c = option9.addResponse('I have a neutral opinion of you.', dialogue.checkOpinionNeutral)
option9c = response9c.addOption( DialogueOption('Okay I understand.') )
response9d = option9.addResponse('You\'re alright. I think I can trust you.', dialogue.checkOpinionHigh)
option9d = response9d.addOption( DialogueOption('That\'s really great to hear.') )
response9e = option9.addResponse('You\'re a good person and I consider you a friend.', dialogue.checkOpinionVeryHigh)
option9e = response9e.addOption( DialogueOption('That\'s really great to hear.') )

option2 = response1.addOption( DialogueOption('Would you be interested in trading some goods?') )
response2a = option2.addResponse('Of course {player.name}. Let\'s see what you have to offer.', dialogue.checkPositiveOpinion)
response2b = option2.addResponse('I don\'t trust you enough to trade {player.name}.')
option2b1 = response2b.addOption( DialogueOption('Okay {npc.name}. Let\'s talk about something else.') )
response2a.setTrade(True)

option3 = response1.addOption( DialogueOption('Do you need any help with anything?') )
response3e = option3.addResponse('I don\'t trust you enough to give you a task.', dialogue.checkNegativeOpinion)
response3e1 = response3e.addOption( DialogueOption('I understand. Let\'s talk about something else.') )

#fetch
response3a = option3.addResponse('Certainly. Can you please collect an item from a settler in the valley for me?', dialogue.checkFetchQuestStart)
option3a1 = response3a.addOption( DialogueOption('Of course') )
response3a1a = option3a1.addResponse('Thank you so much. I await your return.', dialogue.addNewFetchQuest)
option3a2 = response3a.addOption( DialogueOption('No I cannot.') )
response3a2a = option3a2.addResponse('That\'s alright.')
response3b = option3.addResponse('{player.name}, you already have a quest from me.', dialogue.checkHasQuestForNPC)
option3b1 = response3b.addOption( DialogueOption('Oh my mistake. Let\'s change the topic.') )

#deliver
response3d = option3.addResponse('I\'ve been looking for some help. Could you please deliver something to a settler for me?', dialogue.checkDeliverQuestStart)
option3d1 = response3d.addOption( DialogueOption('That\'s something I could do.') )
response3d1a = option3d1.addResponse('Very good. The settler will be waiting for the goods.', dialogue.addNewDeliverQuest)
option3d2 = response3d.addOption( DialogueOption('I\'m sorry, I don\'t have the time at the moment.') )
response3d2a = option3d2.addResponse('That\'s alright.')

#kill
response3e = option3.addResponse('There is a local bandit causing problems. I will pay a handsome reward if they are killed.', dialogue.checkKillQuestStart)
option3e1 = response3e.addOption( DialogueOption('That\'s something I could do.') )
response3e1a = option3e1.addResponse('Very good. I await your return.', dialogue.addNewKillQuest)
option3e2 = response3e.addOption( DialogueOption('I\'m sorry, I don\'t have the time at the moment.') )
response3e2a = option3e2.addResponse('That\'s alright.')

#hunt
response3f = option3.addResponse('We are having a big feast soon and we need some supplies for the festival. Could you do some hunting for me?', dialogue.checkHuntQuestStart)
option3f1 = response3f.addOption( DialogueOption('That\'s something I could do.') )
response3f1a = option3f1.addResponse('Very good. I await your return.', dialogue.addNewHuntQuest)
option3f2 = response3f.addOption( DialogueOption('I\'m sorry, I don\'t have the time at the moment.') )
response3f2a = option3f2.addResponse('That\'s alright.')

#no quest
response3c = option3.addResponse('I\'m sorry, I don\'t need any help with anything at the moment.')
option3c1 = response3c.addOption( DialogueOption('Alright I shall return later.') )

option4 = response1.addOption( DialogueOption('I\'m here about some business.', dialogue.checkHasQuestForNPC) )
response4a = option4.addResponse('Most excellent. Is the task complete?')
option4a1 = response4a.addOption( DialogueOption('Yes. Here is your requested item.', dialogue.checkFetchQuestComplete) )
response4a1a = option4a1.addResponse('Thank you so much for your help in this matter.', dialogue.finalizeFetchQuestComplete)

option4a2 = response4a.addOption( DialogueOption('Yes. Here is your requested item.', dialogue.checkDeliverQuestComplete) )
response4a2a = option4a2.addResponse('Thank you so much for your help in this matter.', dialogue.finalizeDeliverQuestComplete)

option4a3 = response4a.addOption( DialogueOption('Yes. I have killed your target.', dialogue.checkKillQuestComplete) )
response4a3a = option4a3.addResponse('Thank you. They won\'t be a problem anymore.', dialogue.finalizeDefaultQuestComplete)

option4a4 = response4a.addOption( DialogueOption('Yes. Here are your supplies.', dialogue.checkHuntQuestComplete) )
response4a4a = option4a4.addResponse('Thank you. This will be perfect.', dialogue.finalizeHuntQuestComplete)

option4a5 = response4a.addOption( DialogueOption('No it\'s not done yet.') )
response4a5a = option4a5.addResponse('That\'s alright. There is still time.')

option5 = response1.addOption( DialogueOption('What can I do to earn your trust back?', dialogue.checkNegativeOpinion) )
response5a = option5.addResponse('What did you have in mind {player.name}?')
option5a1 = response5a.addOption( DialogueOption('I\'m very sorry and would like to make amends. (Speech {player.skills[9]})', dialogue.checkApologizeSpeech) )
response5a1a = option5a1.addResponse('I appreciate your kind words. It means a lot.', dialogue.finalizeApologizeSpeech)
option5a2 = response5a.addOption( DialogueOption('Can pay you a small tribute? (Gold {npc.opinion * -75})', dialogue.checkApologizeGold) )
response5a2a = option5a2.addResponse('Thank you very much. This will smooth things over for now.', dialogue.finalizeApologizeGold)
option5a3 = response5a.addOption( DialogueOption('Nothing at the moment.') )
response5a3a = option5a3.addResponse('Maybe another time then.')

option6 = response1.addOption( DialogueOption('Can you help me find something?') )
response6a = option6.addResponse('Of course. What are you looking for?', dialogue.checkPositiveOpinion)

option6a1 = response6a.addOption( DialogueOption('Location.') )
response6a1a = option6a1.addResponse('Hopefully that helps you.', dialogue.searchForLocationType)
option6a1a1 = response6a1a.addOption( DialogueOption('Thank you {npc.name}.') )

option6a2 = response6a.addOption( DialogueOption('Profession.') )
response6a2a = option6a2.addResponse('Does that help at all?', dialogue.searchForProfessionType)
option6a2a1 = response6a2a.addOption( DialogueOption('Thank you {npc.name}.') )

option6a3 = response6a.addOption( DialogueOption('Landmark.') )
response6a3a = option6a3.addResponse('Does that help at all?', dialogue.searchForLandmarkType)
option6a3a1 = response6a3a.addOption( DialogueOption('Thank you {npc.name}.') )

option6a4 = response6a.addOption( DialogueOption('Person.') )
response6a4a = option6a4.addResponse('I hope you find who you\'re looking for.', dialogue.searchForNPC)
option6a4a1 = response6a4a.addOption( DialogueOption('Thank you {npc.name}.') )

response6b = option6.addResponse('No. I don\'t trust you anymore {player.name}.')

option7 = response1.addOption( DialogueOption('I\'ve come to kill you once and for all! (ATTACK)') )
response7a = option7.addResponse('{player.name}, surely you\'re joking...')
option7a1 = response7a.addOption( DialogueOption('Prepare to die! (ATTACK)') )
response7a1a = option7a1.addResponse('You\'ll regret this day {player.name}!', dialogue.finalizeBattle)
response7a1a.setExit(True)
option7a2 = response7a.addOption( DialogueOption('I\'m sorry. I don\'t know what came over me...') )
response7a2a = option7a2.addResponse('That\'s alright. We all have our moments.')

option8 = response1.addOption( DialogueOption('Goodbye.') )
response8a = option8.addResponse('Bye {player.name}.')
response8a.setExit(True)

#binding
response0a.options = response1.options
