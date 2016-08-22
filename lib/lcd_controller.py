#!/usr/bin/python
# -*- coding: utf-8 -*-

import wiringpi as pi, os, struct
from lib.sc1602 import sc1602
import lib.conf as conf

SPACE16 = "                "

class LCDController(object):
    def __init__(self):
        self.lcd = sc1602(conf.RS, conf.E, conf.D4, conf.D5, conf.D6, conf.D7)
        self.clear()

    def print1stLine(self, message):
        self.lcd.move(0x00, 0x00)
        message = message + SPACE16
        self.lcd.write(message[0:16])

    def print2ndLine(self, message):
        self.lcd.move(0x00, 0x01)
        message = message + SPACE16
        self.lcd.write(message[0:16])

    def clear(self):
        self.lcd.move_home()
        self.lcd.set_cursol(0)
        self.lcd.set_blink(0)
        self.print1stLine("")
        self.print2ndLine("")
