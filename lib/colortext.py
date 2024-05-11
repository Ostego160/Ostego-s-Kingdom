
COLORS = {
    'white': 29,
    'black': 30,
    'red': 31,
    'green': 32,
    'yellow': 33,
    'blue': 34,
    'magenta': 35,
    'cyan': 36,
    'gray': 37,
}

class ANSI():
    def background(code):
        return "\33[{code}m".format(code=code)

    def style_text(code):
        return "\33[{code}m".format(code=code)

    def color_text(code):
        return "\33[{code}m".format(code=code)

def getColorStr(string, color=0, style=2):
    if isinstance(color, str):
        color = COLORS[color]

    return ANSI.background(97) + ANSI.color_text(color) + ANSI.style_text(style) + str(string)

def colorprint(*args, color=0, style = 2, sep = ' ', end = '\n'):
    if isinstance(color, str):
        color = COLORS[color]

    ansi = ANSI.background(97) + ANSI.color_text(color) + ANSI.style_text(style)

    for arg in args:
        print(ansi + str(arg), end=sep)

    print(ANSI.color_text(0), end=end)

def colorinput(prompt='', color=0, style=2):
    response = input(getColorStr(prompt, color, style))
    print(ANSI.color_text(0), end='')
    return response

def colorstr(string, color=0):
    if isinstance(color, str):
        color = COLORS[color]
    return ANSI.color_text(color) + str(string) + ANSI.color_text(0)


def getColor(color):
    if isinstance(color, str):
        color = COLORS[color]
    return ANSI.color_text(color)

def resetColor():
    return ANSI.color_text(0)

def lightMode():
    COLORS['white'] = 30
    COLORS['black'] = 29

def darkMode():
    COLORS['white'] = 29
    COLORS['black'] = 30


