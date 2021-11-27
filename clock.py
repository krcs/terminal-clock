#!/usr/bin/python3

import os
import curses
import argparse
from datetime import datetime
from asciifont import AsciiFont

def putchar(char, x, y, screen, asciifont):
    py = y
    for line in asciifont[char]:
        screen.addstr(py, x, line)
        py = py + 1

def splittime_numbers():
    now = datetime.now().time()
    return [
        now.hour // 10,
        now.hour % 10,
        now.minute // 10,
        now.minute % 10,
        now.second // 10,
        now.second % 10
    ]

def out_of_screen(win_width, win_height, screen):
    height, width = screen.getmaxyx()
    return width < win_width or height < win_height

def main():
    parser = argparse.ArgumentParser(description='Terminal clock.')
    parser.add_argument("font")
    parser.add_argument("-margin", type=int)

    arg = parser.parse_args()

    margin = 0

    if (arg.margin):
        if arg.margin >= 0:
            margin = arg.margin

    asciifont = AsciiFont(arg.font)

    screen = curses.initscr()
    curses.curs_set(0)
    curses.noecho()

    win_width = (7 * (asciifont.size[0] + margin)) + asciifont.size[0]
    win_height = asciifont.size[1]

    height, width = screen.getmaxyx()
    wx = (width - win_width) // 2
    wy = (height - win_height) // 2

    if out_of_screen(win_width, win_height, screen):
        return

    win = curses.newwin(win_height, win_width+1, wy, wx)
    win.keypad(1)
    win.nodelay(1)

    while True:
        win.erase()

        t = splittime_numbers()

        x = 0
        putchar(t[0], x, 0, win, asciifont)

        x += asciifont.size[0] + margin
        putchar(t[1], x, 0, win, asciifont)

        x += asciifont.size[0] + margin
        putchar(":",  x, 0, win, asciifont)

        x += asciifont.size[0] + margin
        putchar(t[2], x, 0, win, asciifont)

        x += asciifont.size[0] + margin
        putchar(t[3], x, 0, win, asciifont)

        x += asciifont.size[0] + margin
        putchar(":",  x, 0, win, asciifont)

        x += asciifont.size[0] + margin
        putchar(t[4], x, 0, win, asciifont)

        x += asciifont.size[0] + margin
        putchar(t[5], x, 0, win, asciifont)

        c = win.getch()

        if c == 27 or c == ord('q'):
            break

        win.timeout(1000)

    curses.endwin()

if __name__ == '__main__':
    main()
