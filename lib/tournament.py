import random
from lib.entities import Creature
from lib import names
from lib import mapper
from lib import text
from lib import battle

from lib.colortext import colorprint as print
from lib.colortext import colorinput as input
from lib.colortext import colorstr

def newRandomEnemy(npc=None):
    name = names.getRandom('NPCmale')

    if npc:
        name = npc.name
    elif random.randint(0,1) == 1:
        name = names.getRandom('NPCfemale')

    maxHealth = random.randint(80, 120)
    minDamage = random.randint(5, 10)
    maxDamage = random.randint(12, 22)
    speed = random.randint(7, 10)

    return Creature(name, maxHealth, minDamage, maxDamage, speed, 0, 'villager1', 'not much.')

def showTournamentMain(player, inventory, location):
    player.clock.setTournament()

    combatants = []

    champion = newRandomEnemy()
    champion.addHealthMax(50)

    for npc in location.people:
        combatants.append(newRandomEnemy(npc))

    for i in range(random.randint(2,4)):
        combatants.append(newRandomEnemy())

    print()
    print(text.get('tournamentIntro'), color='blue')
    print(text.get('tournamentEntries'), color='white')

    for enemy in combatants:
        print(f'  {enemy.name}', color='white')

    input(text.get('continue'), color='cyan')

    while len(combatants) > 0:
        print(text.get('titleTournament'), color='blue')
        enemy = combatants.pop()
        print(text.get('tournamentBattle', [player.name, enemy.name]), color='red')
        input(text.get('continue'), color='cyan')
        battle.showBattleMain(player, inventory, [enemy] )

        if player.health[0] > 0:
            print(text.get('tournamentRoundWin', [player.name]), color='blue')
            player.addHealth(random.randint(10, 20))
            input(text.get('continue'), color='cyan')
        else:
            print(text.get('tournamentRoundLoss', [player.name]), color='yellow')
            input(text.get('continue'), color='cyan')
            break

        for i in range(len(combatants) // 2):
            randomEnemy = random.choice(combatants)
            combatants.remove(randomEnemy)
            print(text.get('tournamentEnemyRound', [randomEnemy.name]), color='white')
        print()

    if player.health[0] > 0:
        print(text.get('tournamentMaster', [player.name, champion.name]), color='blue')
        battle.showBattleMain(player, inventory, [champion] )

    if player.health[0] > 0:
        player.arenaChampion = True
        print(text.get('tournamentWin', [player.name, champion.name]), color='blue')
        input(text.get('continue'), color='cyan')
    else:
        player.setHealth(5)
        print(text.get('tournamentHeal', [player.name, player.pronoun[0]]), color='blue')
        input(text.get('continue'), color='cyan')

def showTournamentDefense(player, inventory, location):
    player.clock.setTournament()

    combatants = []

    for npc in location.people:
        combatants.append(newRandomEnemy(npc))

    for i in range(random.randint(2, 4)):
        combatants.append(newRandomEnemy())

    finalist = random.choice(combatants)

    finalist.addHealthMax(100)
    finalist.addDamageMax(10)

    print()
    print(text.get('tournamentIntro'), color='blue')
    print(text.get('tournamentEntries'), color='white')
    for enemy in combatants:
        print(f'  {enemy.name}')
    input(text.get('continue'), color='cyan')
    print(text.get('tournamentDefense'), color='blue')
    print(text.get('tournamentFinalist', [player.name, finalist.name]), color='red')
    input(text.get('continue'), color='cyan')

    battle.showBattleMain(player, inventory, [finalist] )

    if player.health[0] > 0:
        print(text.get('tournamentRoundWin', [player.name]), color='blue')
        print(text.get('tournamentDefenseWin', [player.name]), color='blue')
        input(text.get('continue'), color='cyan')
    else:
        player.setHealth(5)
        player.arenaChampion = False
        print(text.get('tournamentDefenseLoss', [player.name]), color='yellow')
        print(text.get('tournamentHeal', [player.name, player.pronoun[0]]), color='blue')
        input(text.get('continue'), color='cyan')

