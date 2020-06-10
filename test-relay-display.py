#!/usr/bin/python3

import time
import RPi.GPIO as GPIO
import board
from adafruit_ht16k33.segments import Seg14x4

i2c = board.I2C()
display = Seg14x4(i2c)

GPIO.setmode(GPIO.BCM)

prefix = "CH0"
channel = 1
switches = [5,6,13,19,26,12]
#switches = [19]

for i in switches:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, GPIO.LOW)
        print(i)
        display.print(prefix+str(channel))
        time.sleep(1.0)
        GPIO.output(i, GPIO.HIGH)
        channel = channel + 1

GPIO.cleanup()
display.fill(0)