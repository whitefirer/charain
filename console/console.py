# coding=utf-8
# author=whitefirer

import curses
import random
import sys
import os
import time

cc_map = {
    'none': -1,
    'default': 0,
    'white': 0,
    'black': 1,
    'red': 2,
    'green': 3,
    'yellow': 4,
    'blue': 5,
    'magenta': 6,
    'brown': 7,
    'lightgray': 8,
    'darkgray': 9,
    'lightred': 10,
    'lightgreen': 11,
    'ligtyellow': 12,
    'lightblue': 13,
    'lightmagenta': 14,
    'cyan': 15,
    'lightwhite': 16,
    'lightbrown': 46,
}

VK_NONE   = 0x00  # NO key
VK_ESCAPE = 0x1B  # ESC key
VK_LEFT   = curses.KEY_LEFT #0x25  # LEFT ARROW key
VK_UP     = curses.KEY_UP #0x26  # UP ARROW key
VK_RIGHT  = curses.KEY_RIGHT #0x27  # RIGHT ARROW key
VK_DOWN   = curses.KEY_DOWN #0x28  # DOWN ARROW key
VK_RETURN = 0x0D  # ENTER key
VK_SPACE  = 0x20  # SPACEBAR

class UCHAR:
    def __init__(self, wchar, char=''):
        self.UnicodeChar = wchar
        self.AsciiChar = char

class CHAR_INFO:
    def __init__(self, wchar, attr, char=''):
        self.Char = wchar
        self.Attributes = attr

class Console:
    def __init__(self):
        self.screen = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i+1, i, -1)
        curses.curs_set(0)
        curses.noecho()

        self.w, self.h = self.GetWH()
        self.charInfoArray = [CHAR_INFO(UCHAR(' '), 0) for i in range(self.h*self.w)]
        self.window = curses.newwin(self.h, self.w+1, 0, 0)
        self.window.keypad(1)
        self.window.timeout(1)

    def Init(self):
        self.ClearScreen()
        self.w, self.h = self.GetWH()

    def GetWH(self):
        h, w = self.screen.getmaxyx()
        return w, h

    def HideCursor(self):
        curses.curs_set(0)

    def ShowCursor(self):
        curses.curs_set(1)

    def ClearScreen(self):
        self.charInfoArray = [CHAR_INFO(UCHAR(' '), 0) for i in range(self.w*self.h)]
        self.window.clear()

    def SetText(self, x, y, text, fore_color='default'):
        if type(fore_color) == str:
            color = cc_map.get(fore_color, 0)
        else:
            color = fore_color
        self.window.addstr(y, x, text, curses.color_pair(color))

        for i in range(len(text)):
            self.charInfoArray[self.w*y+x+i].Char.UnicodeChar = text[i]
            self.charInfoArray[self.w*y+x+i].Attributes = color

    def GetCharByPos(self, x, y):
        return self.charInfoArray[self.w*y+x]

    def SetCharByPos(self, x, y, char):
        self.SetText(x, y, char.Char.UnicodeChar, char.Attributes)

    def DrawToConsole(self):
        self.window.refresh()

    def GetInput(self):
        return self.window.getch()

    def ReadKeyDown(self):
        return self.window.getch()

    def ClearInput(self):
        pass

    def Close(self):
        curses.endwin()

    def __del__(self):
        curses.endwin()

if __name__ == "__main__":
    console = Console()
    console.Init()
    w, h = console.GetWH()
    if h < 20:
        del console
        input('console`s row should be >= 20')
        exit(0)
    i = 0
    for color in cc_map:
        console.SetText(1, i, color, color)
        i = i + 1

    console.DrawToConsole()
    time.sleep(3)