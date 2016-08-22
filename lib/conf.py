#!/usr/bin/python
# -*- coding: utf-8 -*-

# LED1 : GPIO
LED_1_PIN = 17
# LED2 : GPIO
LED_2_PIN = 3
# LED3 : GPIO
LED_3_PIN = 4
# LED4 : GPIO
LED_4_PIN = 2

LED_LIST = [LED_1_PIN, LED_2_PIN, LED_3_PIN, LED_4_PIN]

# SWITCH1 : GPIO
SWITCH_1_PIN = 9
# SWITCH2 : GPIO
SWITCH_2_PIN = 10
# SWITCH3 : GPIO
SWITCH_3_PIN = 22
# SWITCH4 : GPIO
SWITCH_4_PIN = 7
# SWITCH START : GPIO
SWITCH_START_PIN = 11

# GPIOのIN/OUTモード
MODE_IN = 0
MODE_OUT = 1

# LEDのON/OFF
LED_OFF = 0
LED_ON = 1

# LCD GPIO NO
RS = 25
E  = 24
D4 = 14
D5 = 23
D6 = 15
D7 = 18

# ゲーム用スレッド
game = None
# LED用スレッド
led = None
# スイッチ押下判定スレッド
switch = None
# LCD
lcd = None

# スコア
score = 0
# 残り時間(設定値)
remaining_time = 30
# 残り時間
countdown_time = 0
# LED点灯時間[s]
lighting_time_sec = 1.0
