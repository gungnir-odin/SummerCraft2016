#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading
import time
import random
import wiringpi as pi
from lib import conf
from lib.lcd_controller import LCDController


class GameThread(threading.Thread):
    '''
    ゲーム用スレッド

    LEDの点灯/消灯を制御する。
    stopメソッド呼出で、本スレッドは停止する。
    '''
    def __init__(self):
        threading.Thread.__init__(self)
        self.endEvent = threading.Event()

    def run(self):
        while not self.endEvent.is_set():
            # LEDスレッド
            conf.led = LEDThread()
            conf.led.start()
            conf.led.join()

    def stop(self):
        if conf.led is not None:
            conf.led.stop()

        self.endEvent.set()

class LEDThread(threading.Thread):
    '''
    LED用スレッド

    LED点灯から消灯までの時間を制御する。
    stopメソッド呼出で、本スレッドは停止する。
    '''
    def __init__(self):
        threading.Thread.__init__(self)
        self.endEvent = threading.Event()
        self.choice_number = random.randint(0, 3)

    def run(self):
        while not self.endEvent.is_set():
            time.sleep(0.2)
            #print("LED点灯：" + str(self.choice_number))
            pi.digitalWrite(conf.LED_LIST[self.choice_number], conf.LED_ON)

            if conf.score <= 5:
                conf.lighting_time_sec = 1.0
            elif 5 < conf.score :
                conf.lighting_time_sec = 0.5
            elif 15 < conf.score:
                conf.lighting_time_sec = 0.25

            time.sleep(conf.lighting_time_sec)
            self.stop()

    def stop(self):
            self.endEvent.set()
            #print("LED消灯")
            pi.digitalWrite(conf.LED_LIST[self.choice_number], conf.LED_OFF)

class SwitchThread(threading.Thread):
    '''
    スイッチ押下判定スレッド

    スイッチ押下時の動作を制御する
    '''
    def __init__(self):
        threading.Thread.__init__(self)
        self.endEvent = threading.Event()
        print("スタートボタン押下待ち")

    def run(self):
        while not self.endEvent.is_set():
            #print("ボタン押下待ち開始")
            if(pi.digitalRead(conf.SWITCH_START_PIN) == 1):
                # スタートボタン押下
                if conf.game is None:
                    # ゲームスレッド停止時なら、初期化処理してゲーム開始

                    # スコアクリア
                    conf.score = 0
                    # 制限時間設定
                    conf.countdown_time = conf.remaining_time

                    # ゲームスレッド開始
                    conf.game = GameThread()
                    conf.game.start()

            elif(pi.digitalRead(conf.SWITCH_1_PIN) == 1):
                # １番スイッチ押下
                if conf.led is not None and conf.led.choice_number == 0:
                    conf.score += 1
                    conf.led.stop()
                else:
                    conf.score -= 1

            elif(pi.digitalRead(conf.SWITCH_2_PIN) == 1):
                # ２番スイッチ押下
                if conf.led is not None and conf.led.choice_number == 1:
                    conf.score += 1
                    conf.led.stop()
                else:
                    conf.score -= 1

            elif(pi.digitalRead(conf.SWITCH_3_PIN) == 1):
                # ３番スイッチ押下
                if conf.led is not None and conf.led.choice_number == 2:
                    conf.score += 1
                    conf.led.stop()
                else:
                    conf.score -= 1

            elif(pi.digitalRead(conf.SWITCH_4_PIN) == 1):
                # ４番スイッチ押下
                if conf.led is not None and conf.led.choice_number == 3:
                    conf.score += 1
                    conf.led.stop()
                else:
                    conf.score -= 1

            time.sleep(0.1)

    def stop(self):
            self.endEvent.set()
            print("ボタン押下待ち終了")

if __name__ == "__main__":

    # ラズパイGPIO 初期化処理
    pi.wiringPiSetupGpio()

    #LED1
    pi.pinMode(conf.LED_1_PIN, conf.MODE_OUT)
    pi.digitalWrite(conf.LED_1_PIN, conf.LED_OFF)
    #LED2
    pi.pinMode(conf.LED_2_PIN, conf.MODE_OUT)
    pi.digitalWrite(conf.LED_2_PIN, conf.LED_OFF)
    #LED3
    pi.pinMode(conf.LED_3_PIN, conf.MODE_OUT)
    pi.digitalWrite(conf.LED_3_PIN, conf.LED_OFF)
    #LED4
    pi.pinMode(conf.LED_4_PIN, conf.MODE_OUT)
    pi.digitalWrite(conf.LED_4_PIN, conf.LED_OFF)

    #SW1
    pi.pinMode(conf.SWITCH_1_PIN, conf.MODE_IN)
    #SW2
    pi.pinMode(conf.SWITCH_2_PIN, conf.MODE_IN)
    #SW3
    pi.pinMode(conf.SWITCH_3_PIN, conf.MODE_IN)
    #SW4
    pi.pinMode(conf.SWITCH_4_PIN, conf.MODE_IN)
    #SW_START
    pi.pinMode(conf.SWITCH_START_PIN, conf.MODE_IN)

    # LCD の初期化
    lcd = LCDController()
    lcd.print1stLine("Press Red Button")

    # スイッチ押下判定スレッド開始
    conf.switch = SwitchThread()
    conf.switch.start()

    while True:
        while conf.countdown_time > 0:
            conf.countdown_time -= 1
            time.sleep(1)

            lcd.print1stLine("Time:" + str(conf.countdown_time))
            lcd.print2ndLine("Score:" + str(conf.score))
            print("残り時間：" + str(conf.countdown_time) + "秒  スコア　：" + str(conf.score) + "　LED：" + str(conf.led.choice_number))
        else:
            if conf.game is not None:
                # ゲーム終了時処理
                conf.game.stop()
                conf.game = None
                lcd.print1stLine("Press Red Button")
                print("スタートボタン押下待ち")
