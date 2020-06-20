#!/usr/bin/python3

# That was my initial approach. You can use it for testing purposes.
# Biggest issue I came across was the unability of reading keyboard
# input while running in background. So I used a different approach
# than getkey

from minidsp.board_2x4hd import Board2x4HD
import time
import RPi.GPIO as GPIO
import board
from adafruit_ht16k33.segments import Seg14x4
from getkey import getkey, keys

#define Global
i2c = board.I2C()
display = Seg14x4(i2c)
minidsp = Board2x4HD()
GPIO.setmode(GPIO.BCM)

def ProcessInput():

    minidsp = Board2x4HD()

    try:
        keypress = getkey()
    except:
        keypress=""

    if (keypress != "" and keypress != None):

        if (keypress == keys.SPACE):
            print("Space pressed")
            if (minidsp.muted):
                minidsp.unmute()
                print("Volume: {} dB".format(minidsp.volume))
                display.print(str(minidsp.volume))
            else:
                minidsp.mute()
                print("Muted")
                display.print("MUTE")

        elif (keypress == keys.UP):
            print("Up pressed")
            minidsp.volume_up(1)
            GPIO.setup(5, GPIO.OUT)
            GPIO.output(5, GPIO.LOW)
            print("New volume: {} dB".format(minidsp.volume))
            display.print(str(minidsp.volume))

        elif (keypress == keys.DOWN):
            print("Down pressed")
            minidsp.volume_down(1)
            print("New volume: {} dB".format(minidsp.volume))
            display.print(str(minidsp.volume))

        elif (keypress == "1"):
            print(keypress + " pressed")
            minidsp._set_config(1)
            print("Config: 1")
            display.print("PRE1")
            time.sleep(0.5)
            display.print(str(minidsp.volume))

        elif (keypress == "2"):
            print(keypress + " pressed")
            minidsp._set_config(2)
            print("Config: 2")
            display.print("PRE2")
            time.sleep(0.5)
            display.print(str(minidsp.volume))

        elif (keypress == "3"):
            print(keypress + " pressed")
            minidsp:_set_config(3)
            print("Config: 3")
            display.print("PRE3")
            time.sleep(0.5)
            display.print(str(minidsp.volume))

        elif (keypress == "a"):
            print(keypress + " pressed")
            minidsp._set_source("toslink")
            print("Source: Toslink")
            display.print(" OPT")
            time.sleep(0.5)
            display.print(str(minidsp.volume))

        elif (keypress == "b"):
            print(keypress + " pressed")
            minidsp._set_source("analog")
            print("Source: Analog")
            display.print(" AUX")
            time.sleep(0.5)
            display.print(str(minidsp.volume))

        elif (keypress == "c"):
            print(keypress + " pressed")
            minidsp._set_source("usb")
            print("Source: USB")
            display.print(" USB")
            time.sleep(0.5)
            display.print(str(minidsp.volume))

        else:
            return False

print("Starting Up...")
print(minidsp.status)
if (minidsp.source == "toslink"):

    display.print(" OPT")
    time.sleep(0.5)
elif (minidsp.source == "analog"):
    display.print(" AUX")
    time.sleep(0.5)
else:
    display.print(" USB")
    time.sleep(0.5)
if (minidsp.muted):
    display.print("MUTE")
else:
    display.print(str(minidsp.volume))
while True:
    ProcessInput()
    if ProcessInput() == False:
        display.fill(0)
        GPIO.cleanup()
        break
#ProcessInput()
