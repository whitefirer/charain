
# coding=utf-8
# author=whitefirer

import sys
import os
import random
import time
from ctypes import *
import winsound

if os.name != 'nt':
    print("This module only can be used under windows")
    sys.exit()

# command colors
cc_map = {
    'default': 0,
    'black': 1,
    'blue': 2,
    'green': 3,
    'cyan': 4,
    'red': 5,
    'magenta': 6,
    'brown': 7,
    'lightgray': 8,
    'darkgray': 9,
    'lightblue': 10,
    'lightgreen': 11,
    'lightcyan': 12,
    'lightred': 13,
    'lightmagenta': 14,
    'yellow': 15,
    'white': 16,
}

GetStdHandle = windll.kernel32.GetStdHandle
CloseHandle = windll.kernel32.CloseHandle
GetConsoleCursorInfo = windll.kernel32.GetConsoleCursorInfo
SetConsoleCursorInfo = windll.kernel32.SetConsoleCursorInfo
GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo
SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
WriteConsoleOutput = windll.kernel32.WriteConsoleOutputW
FillConsoleOutputCharacter = windll.kernel32.FillConsoleOutputCharacterW
PeekConsoleInput = windll.kernel32.PeekConsoleInputW
ReadConsoleInput = windll.kernel32.ReadConsoleInputW

BOOL = c_bool
WORD = c_ushort
DWORD = c_ulong
LPBYTE = POINTER(c_ubyte)
LPTSTR = POINTER(c_char)
CHAR = c_char
WCHAR = c_wchar
HANDLE = c_void_p

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11


class UCHAR(Union):
    _fields_ = [('UnicodeChar', c_wchar),
                ('AsciiChar', c_char),
                ]

class CHAR_INFO(Structure):
    _fields_ = [('Char', UCHAR),
                ('Attributes', WORD),
                ]


class COORD(Structure):
    _fields_ = [('X', c_short),
                ('Y', c_short),
                ]


class SMALL_RECT(Structure):
    _fields_ = [('Left', c_short),
                ('Top', c_short),
                ('Right', c_short),
                ('Bottom', c_short),
                ]

'''
ref_url: https://docs.microsoft.com/en-us/windows/console/console-screen-buffer-info-str
'''
class CONSOLE_SCREEN_BUFFER_INFO(Structure):
    _fields_ = [('dwSize', COORD),
                ('dwCursorPosition', COORD),
                ('wAttributes', c_uint),
                ('srWindow', SMALL_RECT),
                ('dwMaximumWindowSize', COORD),
                ]


class CONSOLE_CURSOR_INFO(Structure):
    _fields_ = [('dwSize', DWORD),
                ('bVisible', BOOL),
                ]

'''
ref_url: https://docs.microsoft.com/en-us/windows/console/key-event-record-str
'''
class KEY_EVENT_RECORD(Structure):
    _fields_ = [('bKeyDown', BOOL),
                ('wRepeatCount', WORD),
                ('wVirtualScanCode', WORD),               
                ('wVirtualKeyCode', WORD),
                ('uChar', UCHAR),
                ('dwControlKeyState', DWORD),
                ]


'''
value: wVirtualKeyCode
ref_url: https://docs.microsoft.com/zh-cn/windows/desktop/inputdev/virtual-key-codes
description: Virtual-Key Codes 太多了，只取了自己要用的上下左右
'''
VK_ESCAPE = 0x1B  # ESC key
VK_LEFT   = 0x25  # LEFT ARROW key
VK_UP     = 0x26  # UP ARROW key
VK_RIGHT  = 0x27  # RIGHT ARROW key
VK_DOWN   = 0x28  # DOWN ARROW key
VK_RETURN = 0x0D  # ENTER key
VK_SPACE  = 0x20  # SPACEBAR

'''dwControlKeyState'''
CAPSLOCK_ON         = 0x0080  # The CAPS LOCK light is on.
ENHANCED_KEY        = 0x0100  # The key is enhanced.
LEFT_ALT_PRESSED    = 0x0002  # The left ALT key is pressed.
LEFT_CTRL_PRESSED   = 0x0008  # The left CTRL key is pressed.
NUMLOCK_ON          = 0x0020  # The NUM LOCK light is on.
RIGHT_ALT_PRESSED   = 0x0001  # The right ALT key is pressed.
RIGHT_CTRL_PRESSED  = 0x0004  # The right CTRL key is pressed.
SCROLLLOCK_ON       = 0x0040  # The SCROLL LOCK light is on.
SHIFT_PRESSED       = 0x0010  # The SHIFT key is pressed.


'''
ref_url: https://docs.microsoft.com/en-us/windows/console/mouse-event-record-str
'''
class MOUSE_EVENT_RECORD(Structure):
    _fields_ = [('dwMousePosition', COORD),
                ('dwButtonState', DWORD),
                ('dwControlKeyState', DWORD),
                ('dwEventFlags', DWORD),
                ]

'''
ref_url: https://docs.microsoft.com/en-us/windows/console/window-buffer-size-record-str
'''
class WINDOW_BUFFER_SIZE_RECORD(Structure):
    _fields_ = [('dwSize', COORD)]


'''
ref_url: https://docs.microsoft.com/en-us/windows/console/menu-event-record-str
'''
class MENU_EVENT_RECORD(Structure):
    _fields_ = [('dwCommandId', c_uint)]


'''
ref_url: https://docs.microsoft.com/en-us/windows/console/focus-event-record-str
'''
class FOCUS_EVENT_RECORD(Structure):
    _fields_ = [('bSetFocus', BOOL)]


class EVENT(Union):
    _fields_ = [
        ('KeyEvent', KEY_EVENT_RECORD),
        ('MouseEvent', MOUSE_EVENT_RECORD),
        ('WindowBufferSizeEvent', WINDOW_BUFFER_SIZE_RECORD),
        ('MenuEvent', MENU_EVENT_RECORD),
        ('FocusEvent', FOCUS_EVENT_RECORD),
        ]

'''EventType'''
FOCUS_EVENT = 0x0010  # The Event member contains a FOCUS_EVENT_RECORD structure. These events are used internally and should be ignored.
KEY_EVENT   = 0x0001  # The Event member contains a KEY_EVENT_RECORD structure with information about a keyboard event.
MENU_EVENT  = 0x0008  # The Event member contains a MENU_EVENT_RECORD structure. These events are used internally and should be ignored.
MOUSE_EVENT = 0x0002  # The Event member contains a MOUSE_EVENT_RECORD structure with information about a mouse movement or button press event.
WINDOW_BUFFER_SIZE_EVENT = 0x0004  # The Event member contains a WINDOW_BUFFER_SIZE_RECORD structure with information about the new size of the console screen buffer.

class INPUT_RECORD(Structure):
    _fields_ = [('EventType', WORD),
                ('Event', EVENT)
                ]

class Console:
    def __init__(self):
        self.hStdout = GetStdHandle(STD_OUTPUT_HANDLE)
        self.hStdin = GetStdHandle(STD_INPUT_HANDLE)
        self.col, self.row = self.GetWH()
        self.charInfoArray = [CHAR_INFO(UCHAR(' '), 0) for i in range(self.col*self.row)]
        self.input_size = 1
        self.input_record = INPUT_RECORD()#[INPUT_RECORD() for i in range(self.input_size)]
        self.cNumRead = DWORD(0)
        self.cci = CONSOLE_CURSOR_INFO()
        GetConsoleCursorInfo(self.hStdout, byref(self.cci))

    def __del__(self):
        self.ClearScreen()
        console.ShowCursor()
        os.system('cls')
        CloseHandle(self.hStdin)
        CloseHandle(self.hStdout)
        

    def Init(self):
        self.col, self.row = self.GetWH()
        self.charInfoArray = [CHAR_INFO(UCHAR(' '), 0) for i in range(self.col*self.row)]

    def GetWH(self):
        cmd_info = CONSOLE_SCREEN_BUFFER_INFO()
        GetConsoleScreenBufferInfo(self.hStdout, byref(cmd_info))
        w, h = cmd_info.dwSize.X, cmd_info.srWindow.Right + 1
        # if w > 200:
        #     w = 200
        # if h > 20:
        #     h = 20
        return w, h

    def ShowCursor(self):
        self.cci.bVisible = True
        SetConsoleCursorInfo(self.hStdout, byref(self.cci))

    def HideCursor(self):
        self.cci.bVisible = False
        SetConsoleCursorInfo(self.hStdout, byref(self.cci))

    def GetCurColor(self):
        cmd_info = CONSOLE_SCREEN_BUFFER_INFO()
        GetConsoleScreenBufferInfo(self.hStdout, byref(cmd_info))
        return cmd_info.wAttributes

    def ClearScreen(self):
        cmd_info = CONSOLE_SCREEN_BUFFER_INFO()
        GetConsoleScreenBufferInfo(self.hStdout, byref(cmd_info))
        cCharsWritten = DWORD()
        FillConsoleOutputCharacter(self.hStdout, CHAR_INFO(UCHAR(' '), 0), cmd_info.dwSize.X*cmd_info.dwSize.Y, COORD(0, 0), byref(cCharsWritten))

    def SetText(self, x, y, text, fore_color='default', back_color='black'):
        fore = cc_map.get(fore_color, 0xF0)
        old_color = self.GetCurColor()
        if fore:
            fore = fore - 1
        else:
            fore = old_color & 0x0F
        back = cc_map.get(back_color, 0x0F)
        if back:
            back = (back - 1) << 4
        else:
            back = old_color & 0xF0

        for i in range(len(text)):
            self.charInfoArray[self.col*y+x+i].Char.UnicodeChar = text[i]
            #self.charInfoArray[self.col*y+x+i].Char.AsciiChar = ord(text[i])
            self.charInfoArray[self.col*y+x+i].Attributes = fore + back


    def GetCharByPos(self, x, y):
        return self.charInfoArray[self.col*y+x]

    def SetCharByPos(self, x, y, char):
        self.charInfoArray[self.col*y+x] = char

    def DrawToConsole(self):
        dwBufferSize = COORD(self.col, self.row)
        dwBufferCoord = COORD(0, 0)
        lpWriteRegion = SMALL_RECT(0, 0, self.col, self.row)
        seq = CHAR_INFO * len(self.charInfoArray)
        WriteConsoleOutput(self.hStdout, seq(*self.charInfoArray), dwBufferSize, dwBufferCoord, byref(lpWriteRegion))

    def DrawText(self, x, y, text, fore_color='default', back_color='black'):
        self.SetText(x, y, text, fore_color, back_color)
        self.DrawToConsole()

    def ShowText(self, x, y, text, fore_color='default', back_color='black'):
        fore = cc_map.get(fore_color, 0)
        old_color = self.GetCurColor()
        if fore:
            fore = fore - 1
        else:
            fore = old_color & 0x0F
        back = cc_map.get(back_color, 0)
        if back:
            back = (back - 1) << 4
        else:
            back = old_color & 0xF0

        col, row = self.GetWH()
        charInfoArray = [CHAR_INFO(UCHAR(' '), 0) for i in range(col*row)]
        seq = CHAR_INFO * len(charInfoArray)

        for i in range(len(text)):
            charInfoArray[col*y+x+i].Char.UnicodeChar = text[i]
            #charInfoArray[col*y+x+i].Char.AsciiChar = ord(text[i])
            charInfoArray[col*y+x+i].Attributes = fore + back

        dwBufferSize = COORD(col, row)
        dwBufferCoord = COORD(x, y)
        lpWriteRegion = SMALL_RECT(x, y, x+len(text)-1, y)
        WriteConsoleOutput(self.hStdout, seq(*charInfoArray), dwBufferSize, dwBufferCoord, byref(lpWriteRegion))

    def GetInput(self):
        PeekConsoleInput(self.hStdin, byref(self.input_record), self.input_size, byref(self.cNumRead))
        if self.cNumRead:
            return 1
        return 0

    def ClearInput(self):
        if self.cNumRead:
            ReadConsoleInput(self.hStdin, byref(self.input_record), self.input_size, byref(self.cNumRead))


    def ReadKeyDown(self):
        if not self.GetInput():
            return 0

        if self.input_record.EventType != KEY_EVENT:
            return 0

        if self.input_record.Event.KeyEvent.bKeyDown > 0:
            return 0

        vk_key = self.input_record.Event.KeyEvent.wVirtualKeyCode

        return vk_key

    def ReadKeyPush(self):
        if not self.GetInput():
            return 0

        if self.input_record.EventType != KEY_EVENT:
            return 0

        if self.input_record.Event.KeyEvent.bKeyDown == 0:
            return 0

        vk_key = self.input_record.Event.KeyEvent.wVirtualKeyCode

        return vk_key


def Start(console):
    console.Init()
    console.HideCursor()
    console.ClearScreen()
    console.SetText(34, 2, 'charain', 'lightcyan')
    console.SetText(20, 3, 'Hello world!', 'yellow')
    console.SetText(20, 4, 'You can use ← ↑ ↓ → to contrl the chars')
    console.SetText(32, 4, '← ↑ ↓ →', 'lightred')
    console.SetText(20, 5, 'ESC to exit, SPACE to restart', 'green')
    console.SetText(20, 5, 'ESC', 'lightred')
    console.SetText(33, 5, 'SPACE', 'lightred')
    console.SetText(20, 6, 'Any other keys to let them fall down', 'lightgreen')

    console.SetText(20, 8, 'I love Coding forever! Have fun! --By whitefirer', 'cyan')
    console.SetText(58, 8, 'whitefirer', 'lightblue')
    
    console.SetText(27, 8, 'Coding', 'lightmagenta')
    
    console.DrawToConsole()


if __name__ == "__main__":
    os.system('cls')

    console = Console()

    if console.row < 8:
        input('console`s row should be >= 8.press anykey to end the program.')
        del console
        exit(0)

    Start(console)
    w, h = console.GetWH()
    key = 0
    t = time.time()
    while(True):
        vk_key = console.ReadKeyDown()
        #console.DrawText(0, 0, str(time.time()), 'blue')
        if vk_key:
            if vk_key == VK_ESCAPE:
                break
            elif vk_key == VK_SPACE:
                Start(console)
                key = 0
            elif vk_key == VK_RETURN:
                key = 0
            else:
                key = vk_key
        console.ClearInput()

        changed = False
        for k in range(h):
            j = h - 1 - k
            for i in range(w):
                cur_char = console.GetCharByPos(i, j)

                if cur_char.Char.UnicodeChar == ' ':
                    continue
                    
                ax = i
                ay = j
                if key == VK_RETURN:
                    continue

                if key not in (VK_LEFT, VK_RIGHT, VK_UP, 0):
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
                    and (i >= 0):
                    console.SetCharByPos(i, j, CHAR_INFO(UCHAR(' '), 0))
                    console.SetCharByPos(ax, ay, cur_char)
                    
                    # if key in (VK_LEFT, VK_RIGHT):
                    #     if not ( ax % int(w/h) ):
                    #         changed = True
                    # else:
                    #     changed = True
                else:
                    pass

        if changed or time.time() - t > 0.02:
            t = time.time()
            console.DrawToConsole()