CONSTANTS = {
    'battleMissThreshold': 4,

    'bountyAssault': 500,
    'bountyEscape': 250,
    'bountyMurder': 2500,
    'bountyThreshold': 250,

    'magicBarrierBonus': 25,
    'magicDuplicateMinCost': 25,
    'magicTeleportBaseCost': 200,

    'playerSpeedBase': 10,
    'playerArmorMax': 128,
    'playerSkillMax': 128,
    'playerHealthMax': 256,
    'playerManaMax': 256,
    'playerStarveThreshold': 48,
    'playerExhaustionThreshold': 48,

    'creatureSpeedBase': 10,
    'creatureDamageMax': 32,
    'creatureHealthMax': 256,

    'timeTournament': 7,
    'timeStart': 10000000,

    'huntChanceEncounter': 25,
    'huntChanceFailure': 25,

    'eventMaxGoldTheft': 250,
}

def set(k,v):
    CONSTANTS[k] = v

def get(k):
    return CONSTANTS[k]
