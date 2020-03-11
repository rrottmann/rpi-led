#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2020 Reiner Rottmann. All rights reserved.
# Released under BSD License. See LICENSE.txt

import sys
import time

import importlib.util

from enum import Enum

try:
    importlib.util.find_spec('RPi.GPIO')
    import RPi.GPIO as GPIO
except ImportError:
    """
    import FakeRPi.GPIO as GPIO
    OR
    import FakeRPi.RPiO as RPiO
    """
    import FakeRPi.GPIO as GPIO

GPIO.setwarnings(False)

PIN_RED, PIN_GREEN, PIN_BLUE, PIN_GND = 40, 38, 36, 34


class Colors(Enum):
    BLACK = (False, False, False)
    RED = (True, False, False)
    GREEN = (False, True, False)
    BLUE = (False, False, True)
    YELLOW = (True, True, False)
    CYAN = (False, True, True)
    MAGENTA = (True, False, True)
    WHITE = (True, True, True)


def usage():
    print(f'{sys.argv[0]} [ COMMAND ] ( PATTERN )')
    print('''

Copyright (c) 2020 Reiner Rottmann. All rights reserved.
Released under BSD License. See LICENSE.txt

# LED

The multi-color RGB LED status indicator.  It accepts either a combination of color and pattern.

## HEADER

> ................xxxx
> 0...................

## LED Colors

| COMMAND | Description                    |
| :------ | :----------------------------- |
| R       | Red                            |
| G       | Green                          |
| B       | Blue                           |
| Y       | Yellow (AKA as Amber)          |
| C       | Cyan (AKA Light Blue)          |
| M       | Magenta (AKA Violet or Purple) |
| W       | White                          |
| O       | Off                            |

## LED Patterns

| PATTERN  | Description                                              |
| :------- | :------------------------------------------------------- |
| SOLID    | *Default* No blink. Used if pattern argument is ommitted |
| SLOW     | Symmetric 1000ms ON, 1000ms OFF, repeating               |
| FAST     | Symmetric 100ms ON, 100ms OFF, repeating                 |
| VERYFAST | Symmetric 10ms ON, 10ms OFF, repeating                   |
| SINGLE   | 1 100ms blink(s) ON followed by 1 second OFF, repeating  |
| DOUBLE   | 2 100ms blink(s) ON followed by 1 second OFF, repeating  |
| TRIPLE   | 3 100ms blink(s) ON followed by 1 second OFF, repeating  |
| QUAD     | 4 100ms blink(s) ON followed by 1 second OFF, repeating  |
| QUIN     | 5 100ms blink(s) ON followed by 1 second OFF, repeating  |
| ISINGLE  | 1 100ms blink(s) OFF followed by 1 second ON, repeating  |
| IDOUBLE  | 2 100ms blink(s) OFF followed by 1 second ON, repeating  |
| ITRIPLE  | 3 100ms blink(s) OFF followed by 1 second ON, repeating  |
    ''')


def setup():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    for pin in [PIN_RED, PIN_GREEN, PIN_BLUE]:
        GPIO.setup(pin, GPIO.OUT)


def on(color=Colors.RED):
    if color.value[0]:
        GPIO.output(PIN_RED, True)
    else:
        GPIO.output(PIN_RED, False)
    if color.value[1]:
        GPIO.output(PIN_GREEN, True)
    else:
        GPIO.output(PIN_GREEN, False)
    if color.value[2]:
        GPIO.output(PIN_BLUE, True)
    else:
        GPIO.output(PIN_BLUE, False)


def off():
    on(color=Colors.BLACK)


def blink(color=Colors.RED, t=0.1):
    on(color)
    time.sleep(t)
    off()
    time.sleep(t)


def iblink(color=Colors.RED, t=0.1):
    off()
    time.sleep(t)
    on(color)
    time.sleep(t)


# # loop through 50 times, on/off for 1 second
# for i in range(50):
#     GPIO.output(40, True)
#     time.sleep(1)
#     GPIO.output(40, False)
#     time.sleep(1)
# GPIO.cleanup()

if __name__ == '__main__':
    if not len(sys.argv) in [2, 3]:
        usage()
        sys.exit(1)
    setup()

    COMMAND = sys.argv[1].upper()

    if len(sys.argv) == 3:
        PATTERN = sys.argv[2].upper()
    else:
        PATTERN = 'SOLID'

    if COMMAND in ['R', 'RED', 'ROT']:
        COLOR = Colors.RED
    elif COMMAND in ['G', 'GREEN', 'GRUEN', 'GRÜN']:
        COLOR = Colors.GREEN
    elif COMMAND in ['B', 'BLUE', 'BLAU']:
        COLOR = Colors.BLUE
    elif COMMAND in ['Y', 'A', 'YELLOW', 'AMBER', 'GELB', 'BERNSTEIN']:
        COLOR = Colors.YELLOW
    elif COMMAND in ['C', 'CYAN']:
        COLOR = Colors.CYAN
    elif COMMAND in ['M', 'MAGENTA', 'V', 'P', 'VIOLET', 'PURPLE', 'PURPUR', 'VIOLETT']:
        COLOR = Colors.MAGENTA
    elif COMMAND in ['W', 'WHITE', 'WEISS']:
        COLOR = Colors.WHITE
    else:
        COLOR = Colors.BLACK

    try:
        if PATTERN == 'SOLID':
            on(COLOR)
        elif PATTERN == 'SLOW':
            while True:
                on(COLOR)
                time.sleep(1)
                off()
                time.sleep(1)
        elif PATTERN == 'FAST':
            while True:
                on(COLOR)
                time.sleep(0.1)
                off()
                time.sleep(0.1)
        elif PATTERN == 'VERYFAST':
            while True:
                on(COLOR)
                time.sleep(0.01)
                off()
                time.sleep(0.01)
        elif PATTERN == 'SINGLE':
            while True:
                blink(COLOR)
                off()
                time.sleep(1)
        elif PATTERN == 'DOUBLE':
            while True:
                for _ in range(2):
                    blink(COLOR)
                off()
                time.sleep(1)
        elif PATTERN == 'TRIPLE':
            while True:
                for _ in range(3):
                    blink(COLOR)
                off()
                time.sleep(1)
        elif PATTERN == 'QUAD':
            while True:
                for _ in range(4):
                    blink(COLOR)
                off()
                time.sleep(1)
        elif PATTERN == 'QUIN':
            while True:
                for _ in range(5):
                    blink(COLOR)
                off()
                time.sleep(1)
        elif PATTERN == 'ISINGLE':
            while True:
                iblink(COLOR)
                off()
                time.sleep(1)
        elif PATTERN == 'IDOUBLE':
            while True:
                for _ in range(2):
                    iblink(COLOR)
                off()
                time.sleep(1)
        elif PATTERN == 'ITRIPLE':
            while True:
                for _ in range(3):
                    iblink(COLOR)
                off()
                time.sleep(1)
        elif PATTERN == 'IQUAD':
            while True:
                for _ in range(4):
                    iblink(COLOR)
                off()
                time.sleep(1)
        elif PATTERN == 'IQUIN':
            while True:
                for _ in range(5):
                    iblink(COLOR)
                off()
                time.sleep(1)
        elif PATTERN == 'SUCCESS':
            for _ in range(10):
                on(COLOR)
                time.sleep(0.5)
                off()
                time.sleep(0.5)
            on(COLOR)
        elif PATTERN.isdigit():
            while True:
                blink(COLOR, t=PATTERN)
                off()
                time.sleep(PATTERN)
    except KeyboardInterrupt:
        off()
        GPIO.cleanup()
        sys.exit(0)
