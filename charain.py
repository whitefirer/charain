
# coding=utf-8
# author=whitefirer

import sys
import os
import random
import time
from console import *

def Start(console):
    console.Init()

    console.SetText(34, 2, 'charain', 'brown')
    console.SetText(20, 3, 'Hello world!', 'yellow')
    console.SetText(20, 4, 'You can use ← ↑ ↓ → to contrl the chars')
    console.SetText(32, 4, '← ↑ ↓ →', 'red')
    console.SetText(20, 5, 'ESC to exit, SPACE to restart, ENTER to autoplay', 'green')
    console.SetText(20, 5, 'ESC', 'red')
    console.SetText(33, 5, 'SPACE', 'red')
    console.SetText(51, 5, 'ENTER', 'red')
    console.SetText(20, 6, 'Press any other keys to let them fall down', 'green')

    console.SetText(20, 8, 'I love Coding forever! Have fun! --By whitefirer', 'brown')
    console.SetText(58, 8, 'whitefirer', 'blue')
    console.SetText(27, 8, 'Coding', 'magenta')

    console.DrawToConsole()


if __name__ == "__main__":
    console = Console()

    if console.h < 8:
        input('console`s row should be >= 8.press anykey to end the program.')
        del console
        exit(0)

    Start(console)
    w, h = console.GetWH()
    key = VK_NONE
    console.ReadKeyDown()
    console.ClearInput()
    t = time.time()
    changed = False
    auto_flag = False

    while(True):
        if not changed:
            time.sleep(0.02)

        if auto_flag and not changed:
            vk_key = random.choice([VK_LEFT, VK_RIGHT, VK_DOWN, VK_UP])
        else:
            vk_key = console.ReadKeyDown()
            console.ClearInput()

        if vk_key > 0:
            if vk_key == VK_ESCAPE:
                break
            elif vk_key == VK_SPACE:
                Start(console)
                key = VK_NONE
                auto_flag = False
            elif vk_key == VK_RETURN:
                key = VK_NONE
                auto_flag = not auto_flag
            else:
                key = vk_key

        changed = False
        for k in range(h):
            j = h - 1 - k
            for i in range(w):
                cur_char = console.GetCharByPos(i, j)

                if cur_char.Char.UnicodeChar == ' ':
                    continue

                ax, ay = i, j
                if key == VK_RETURN:
                    continue

                if key not in (VK_LEFT, VK_RIGHT, VK_UP, VK_NONE):
                    ay = j + random.randint(0, 1)
                elif key == VK_UP:
                    ay = j - random.randint(0, 1)
                elif key == VK_LEFT:
                    ax = i - random.randint(0, 1)
                elif key == VK_RIGHT:
                    ax = i + random.randint(0, 1)

                next_char = None
                if ax >= 0 and ax < w and ay < h and ay >= 0:
                    next_char = console.GetCharByPos(ax, ay)

                if (next_char and next_char.Char.UnicodeChar == ' ') \
                    and ( j < h ) \
                    and ( i < w ) \
                    and ( i >= 0 ):
                    console.SetCharByPos(ax, ay, cur_char)
                    console.SetCharByPos(i, j, CHAR_INFO(UCHAR(' '), 0))

                    changed = True
                else:
                    pass

        if time.time() - t > 0.02:
            t = time.time()
            console.DrawToConsole()