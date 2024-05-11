import random
from lib.constants import get as constant
from lib import text
from lib import encounter
from lib import items
from lib import character
from lib import magic
from lib import quest
from lib import mapper
from lib import loot

import time
import os

def setSaveDir():
    filepath = os.getcwd()

    filepath = filepath.rsplit('\\', 1)[0]

    os.chdir(filepath)

    if not os.path.isdir('saves'):
        os.mkdir('saves')

    filepath += '\\saves'

    os.chdir(filepath)

def saveGame(player, inventory, map):

    filename = f'{test} {time.time()}.txt'
    file = open(filename, 'w')
    file.write('Test!')

