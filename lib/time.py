from lib.constants import get as Constant
from lib.colortext import colorprint as print
from lib.colortext import colorinput as input

MONTHS = ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')
DAYS = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
DAYTIME = ('morning', 'day', 'afternoon', 'evening', 'night')

class Clock:
    def __init__(self, time = 0):
        self.time = time
        self.timeAcc = 0
        self.lastTournament = 0
        
    def getDays(self):
        return self.time // 24
    
    def getMinutes(self):
        return int(((self.time*10 % 10) / 10) * 60)
    
    def getHours(self):
        return int(self.time % 24)
    
    def add(self, v):
        self.timeAcc += v
        self.time += v
    
    def getWeekday(self):
        i = int( (self.time / 24) % 7 )
        return DAYS[i]
    
    def getDay(self):
        i = int( (self.time / 24) % 30 ) + 1
        return i
    
    def getMonth(self):
        i = int( ( (self.time / 24) / 30) % 12 )
        return MONTHS[i]
    
    def getYear(self):
        return int(self.time // (24 * 360))

    def getTournament(self):
        return (self.time - self.lastTournament) / 24 > Constant('timeTournament')

    def setTournament(self):
        self.lastTournament = self.time
    
    def getTimeOfDay(self):
        hour = self.getHours()

        if hour > 22:
            return 'night'
        elif hour > 17:
            return 'evening'
        elif hour > 14:
            return 'afternoon'
        elif hour > 10:
            return 'midday'
        elif hour > 5:
            return 'morning'
        else:
            return 'night'

    def checkTimeAcc(self):
        if self.timeAcc >= 24 * 7:
            self.timeAcc -= 24 * 7
            return True
        else:
            return False
    
    def printDescription(self):
        print('Current Time:', self.getTimeOfDay().capitalize(), color='yellow' )
        print('{hour:02d}:{minutes:02d}'.format(hour=self.getHours(), minutes=self.getMinutes()), self.getWeekday() + ',', self.getMonth(), self.getDay(), self.getYear(), color='yellow')

    def getExternalDescription(self, time):
        hour = int(time % 24)
        min = int(((time*10 % 10) / 10) * 60)
        i = int( ( (time / 24) / 30) % 12 )
        month = MONTHS[i]
        day = int( (time / 24) % 30 ) + 1
        year = int(time // (24 * 360))
        i = int( (self.time / 24) % 7 )
        weekday = DAYS[i]

        return f'{hour:02d}:{min:02d} {weekday}, {month} {day} {year}'
