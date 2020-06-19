#!/usr/bin/python3

from minidsp.board_2x4hd import Board2x4HD
import time
import RPi.GPIO as GPIO
import board
import asyncio
from adafruit_ht16k33.segments import Seg14x4
from evdev import InputDevice, categorize, ecodes


#define Global
i2c = board.I2C()
display = Seg14x4(i2c)
GPIO.setmode(GPIO.BCM)

state_input = ''
state_profile = 0
#state_dsp = True
state_mute = False
state_volume = 0

def handle_data(data):
  minidsp = Board2x4HD()
  global state_input
  global state_mute
  global state_volume
  global state_profile

  if(data == 'KEY_A'):
    display.print(' OPT')
    if (state_input != 'toslink'):
      minidsp._set_source('toslink')
      state_input = 'toslink'
    time.sleep(0.5)
    if (state_mute):
      display.print('MUTE')
    else:
      if (state_volume > -10.0):
        display.print(' ' + str(state_volume))
      else:
        display.print(str(state_volume))

  elif(data == 'KEY_B'):
    display.print(' AUX')
    if (state_input != 'analog'):
      minidsp._set_source('analog')
      state_input = 'analog'
    time.sleep(0.5)
    if (state_mute):
      display.print('MUTE')
    else:
      if (state_volume > -10.0):
        display.print(' ' + str(state_volume))
      else:
        display.print(str(state_volume))

  elif(data == 'KEY_C'):
    display.print(' USB')
    if (state_input != 'usb'):
      minidsp._set_source('usb')
      state_input = 'usb'
    time.sleep(0.5)
    if (state_mute):
      display.print('MUTE')
    else:
      if (state_volume > -10.0):
        display.print(' ' + str(state_volume))
      else:
        display.print(str(state_volume))

  elif(data == 'KEY_1'):
    display.print(' Pro1')
    if (state_profile != 1):
      minidsp._set_config(1)
      switch_relay(1)
      state_profile = 1
    time.sleep(0.5)
    if (state_mute):
      display.print('MUTE')
    else:
      if (state_volume > -10.0):
        display.print(' ' + str(state_volume))
      else:
        display.print(str(state_volume))

  elif(data == 'KEY_2'):
    display.print(' Pro2')
    if (state_profile != 2):
      minidsp._set_config(2)
      switch_relay(2)
      state_profile = 2
    time.sleep(0.5)
    if (state_mute):
      display.print('MUTE')
    else:
      if (state_volume > -10.0):
        display.print(' ' + str(state_volume))
      else:
        display.print(str(state_volume))

  elif(data == 'KEY_3'):
    display.print(' Pro3')
    if (state_profile != 3):
      minidsp._set_config(3)
      switch_relay(3)
      state_profile = 3
    time.sleep(0.5)
    if (state_mute):
      display.print('MUTE')
    else:
      if (state_volume > -10.0):
        display.print(' ' + str(state_volume))
      else:
        display.print(str(state_volume))

#  elif(data == 'KEY_4'):
#    display.print(' Pro4')
#    if (state_profile != 4):
#      minidsp._set_config(4)
#      switch_relay(4)
#      state_profile = 4
#    time.sleep(0.5)
#    if (state_mute):
#      display.print('MUTE')
#    else:
#      if (state_volume > -10.0):
#        display.print(' ' + str(state_volume))
#      else:
#        display.print(str(state_volume))

#  elif(data == '9'):
#    minidsp.setDiracStatus(False)
#  elif(data == '0'):
#    minidsp.setDiracStatus(True)

  elif(data == 'KEY_M'):
    if state_mute:
      if (state_volume > -10.0):
        display.print(' ' + str(state_volume))
      else:
        display.print(str(state_volume))
      minidsp.unmute()
      state_mute = False
    else:
      display.print('MUTE')
      minidsp.mute()
      state_mute = True

#  elif(data == 's'):
#    os.system('sudo shutdown -h now')

  elif(data.startswith('KEY_H')):
    newVolume = state_volume
    volume_step = 0.5
    newVolume = newVolume + volume_step
    if(newVolume > 0):
      newVolume = 0
    if (newVolume > -10.0):
      display.print(' ' + str(newVolume))
    else:
      display.print(str(newVolume))
    minidsp._set_volume(newVolume)
    state_volume = newVolume

  elif(data.startswith('KEY_L')):
    newVolume = state_volume
    volume_step = 0.5
    newVolume = newVolume - volume_step
    if(newVolume < -127.5):
      newVolume = -127.5
    if (newVolume > -10.0):
      display.print(' ' + str(newVolume))
    else:
      display.print(str(newVolume))
    minidsp._set_volume(newVolume)
    state_volume = newVolume


#  print(state_input)
#  print(state_mute)
#  print(state_volume)
#  print(state_profile)
  time.sleep(0.01)

def switch_relay(state):
  ch1 = 5
  ch2 = 6
  ch3 = 13
  ch4 = 19
  ch5 = 26
  ch6 = 12
  mainGroup = (ch1, ch2, ch3, ch4, ch5, ch6)

  GPIO.cleanup(mainGroup)

  if (state == 1):
    group1 = (ch1, ch2, ch3, ch4)
    GPIO.setup(group1, GPIO.OUT)
    GPIO.output(group1, GPIO.LOW)
  elif (state == 2):
    group2 = (ch1, ch2)
    GPIO.setup(group2, GPIO.OUT)
    GPIO.output(group2, GPIO.LOW)
  elif (state == 3):
    group3 = (ch5, ch6)
    GPIO.setup(group3, GPIO.OUT)
    GPIO.output(group3, GPIO.LOW)
#  elif (state == 4):
#    group1 = (ch1, ch2, ch3, ch4)
#    GPIO.setup(group1, GPIO.OUT)
#    GPIO.output(group1, GPIO.LOW)

def main():
  minidsp = None

  minidsp = Board2x4HD()
  dev = InputDevice('/dev/input/event0')

  global state_input
  global state_mute
  global state_volume
  global state_profile

  state_input = minidsp.source
  state_mute = minidsp.muted
  state_volume = minidsp.volume
  state_profile = minidsp.config
#  state_dsp = minidsp.getDiracStatus()
#  ip_address = get_ip()

#  print(state_input)
#  print(state_mute)
#  print(state_volume)
#  print(state_profile)

  if (state_input == 'toslink'):
    display.print(' OPT')
  elif (state_input == 'analog'):
    display.print(' AUX')
  elif (state_input == 'usb'):
    display.print(' USB')
  switch_relay(state_profile)
  time.sleep(0.5)
  if (state_mute):
    display.print('MUTE')
  else:
    if (state_volume > -10.0):
      display.print(' ' + str(state_volume))
    else:
      display.print(str(state_volume))

#  while True:
#  for event in dev.read_loop():
#    try:
#        keypress = getkey()
#    except:
#        keypress=''
  async def helper(dev):
    prev_event_timestamp = 0
    async for event in dev.async_read_loop():
      if event.type == ecodes.EV_KEY:
        data = categorize(event)
        if data.keystate == 1:
          event_timestamp = data.event.timestamp()
          if ((event_timestamp - prev_event_timestamp) > 0.4):
            prev_event_timestamp = event_timestamp
            keypress = data.keycode
            if (keypress != "" and keypress != None and keypress !='KEY_Q'):
              handle_data(keypress)

            elif (keypress == 'KEY_Q'):
              display.fill(0)
              GPIO.cleanup()
              break

  loop = asyncio.get_event_loop()
  loop.run_until_complete(helper(dev))

if (__name__ == '__main__'):
  main()
