from lib import text
from lib import items

from lib.colortext import colorprint as print
from lib.colortext import colorinput as input
from lib.colortext import colorstr

def printGold(npc, player, inventory):
    print(player.name, 'gold:', inventory.gold, color='white')
    print(npc.name, 'gold:', npc.gold, color='yellow')

def getPrices(npc, player, container, isSale=False):
    prices = []

    for i in container:
        item = items.getItem(i)
        moodPenalty = 0.10 * item.value * ((100-npc.mood) / 100)
        tradePenalty = 0.20 * item.value * ((255 - player.skills[9]) / 255)
        if isSale:
            value = item.value - moodPenalty - tradePenalty
        else:
            value = item.value + moodPenalty + tradePenalty
        prices.append( int(value) )

    return prices

def showSellMenu(npc, player, inventory):
    prices = getPrices(npc, player, inventory.bag, True)
    printGold(npc, player, inventory)
    print(player.name, 'items:', color='white')
    if len(inventory.bag) == 0:
        print(text.get('tradeNone', [player.name]), color='yellow')
        input(text.get('continue'), color='cyan')
    else:
        for i,j in enumerate(inventory.bag):
            item = items.getItem(j)
            print(' ', str(i) + ':', item.getColorString() + ' Price:', prices[i], color='white')

        select = None
        item = None

        while not select:
            continueSell = True
            select = input(text.get('tradeSell'), color='cyan')
            if select == 'b':
                break
            else:
                try:
                    select = int(select)
                    item = inventory.bag[select]
                except:
                    print(text.get('invalidSelection'), color='red')
                    select = None

                if continueSell:
                    item = items.getItem(item)

                    value = prices[int(select)]

                    if npc.gold >= value:
                        confirm = None

                        while not confirm:
                            confirm = input(text.get('tradeSellConfirm', [item.name, value]), color='cyan').lower()

                            if confirm == 'y' or confirm == 'yes':
                                npc.items.append( inventory.bag.pop( select ) )
                                prices.pop(select)
                                inventory.gold += value
                                npc.gold -= value

                                print(text.get('tradeSellComplete', [item.name]), color='blue')

                                input(text.get('continue'), color='cyan')

                                return
                            elif confirm == 'n' or confirm == 'no':
                                continueSell = False
                                select = None
                                break

                    else:
                        confirm = None

                        while not confirm:
                            confirm = input(text.get('tradeSellFail', [item.name, npc.name, npc.gold]), color='cyan').lower()

                            if confirm == 'y' or confirm == 'yes':
                                npc.items.append( inventory.bag.pop( select ) )
                                prices.pop(select)
                                inventory.gold += npc.gold
                                npc.gold = 0

                                print(text.get('tradeSellComplete', [item.name]), color='blue')

                                input(text.get('continue'), color='cyan')
                                continueSell = False
                            elif confirm == 'n' or confirm == 'no':
                                select = None
                                break
    
def showBuyMenu(npc, player, inventory):
    prices = getPrices(npc, player, npc.items)

    printGold(npc, player, inventory)
    print(npc.name, 'items:', color='white')
    if len(npc.items) == 0:
        print(text.get('tradeNone', [npc.name]), color='yellow')
        input(text.get('continue'), color='cyan')
    else:
        for i,j in enumerate(npc.items):
            item = items.getItem(j)
            print(' ' + str(i) + ':', item.getColorString() + ' Price:', prices[i], color='white')
            
        select = None
        item = None
        
        while not select:
            select = input(text.get('tradeBuy'), color='cyan')

            if select == 'b':
                break
            else:
                try:
                    select = int(select)
                    item = npc.items[select]
                except:
                    print(text.get('invalidSelection'), color='red')
                    select = None

                continueSell = True

                if continueSell:
                    item = items.getItem(item)
                    value = prices[select]

                    if inventory.gold >= value:
                        confirm = None

                        while not confirm:
                            confirm = input(text.get('tradeBuyConfirm', [item.name, value]), color='cyan').lower()

                            if confirm == 'y' or confirm == 'yes':
                                inventory.bag.append( npc.items.pop( select ) )
                                inventory.gold -= value
                                npc.gold += value

                                print(text.get('tradeBuyComplete', [item.name]), color='blue')

                                input(text.get('continue'), color='cyan')

                                return
                            elif confirm == 'n' or confirm == 'no':
                                continueSell = False
                                select = None
                                break

                    else:
                        print(text.get('tradeBuyFail', [item.name]), color='yellow')
                        input(text.get('continue'), color='cyan')
                        continueSell = False
                        select = None
                        break
        
def showTradeMain(npc, player, inventory):
    continueTrade = True
    
    while continueTrade:
        print()
        print(text.get('titleTrade'), color='blue')
        print(text.get('tradeMenu'), color='white')
        select = input(text.get('selection2'), color='cyan').lower()
        
        if select == '0':
            showBuyMenu(npc, player, inventory)
        elif select == '1':
            showSellMenu(npc, player, inventory)
        elif select == 'b':
            continueTrade = False
        else:
            print(text.get('invalidSelection'), color='red')
