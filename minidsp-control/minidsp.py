import serial
import io
import os
import time
import socket
import logging
import logging.handlers

import minidsp

logger = logging.getLogger('minidsp-pre_logger')
logger.setLevel(logging.INFO)

# prevent multiple entries in syslog
if not logger.handlers:
    handler = logging.handlers.SysLogHandler(address = '/dev/log')
    formatter = logging.Formatter('(%(levelname)s) %(module)s.%(funcName)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

port = '/dev/ttyACM0'
baud = 115200

state_input = ''
state_profile = 0
state_dsp = True
state_mute = False
state_volume = 0
ip_address = ''

while not os.path.exists(port):
  logger.critical(port + ' not present. Wait 10s')
  time.sleep(10)

serial_port = serial.Serial(port, baud, timeout=0.5)

def get_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  try:
    s.connect(('10.255.255.255', 1))
    ip = s.getsockname()[0]
  except:
    ip = '127.0.0.1'
  finally:
    s.close()
  return ip

def handle_data(data):
  board = minidsp.board_ddrc24.BoardDDRC24('usbhid')
  if(data == 'I1'):
    board.setInputSource('toslink')
    logger.debug('input: toslink')
  elif(data == 'I2'):
    board.setInputSource('analog')
    logger.debug('input: analog')
  elif(data == 'I3'):
    board.setInputSource('usb')
    logger.debug('input: usb')
  elif(data == 'P1'):
    board.setConfig(1)
    logger.debug('set config: 1')
  elif(data == 'P2'):
    board.setConfig(2)
    logger.debug('set config: 2')
  elif(data == 'P3'):
    board.setConfig(3)
    logger.debug('set config: 3')
  elif(data == 'P4'):
    board.setConfig(4)
    logger.debug('set config: 4')
  elif(data == 'D0'):
    board.setDiracStatus(False)
    logger.debug('set dirac off')
  elif(data == 'D1'):
    board.setDiracStatus(True)
    logger.debug('set dirac on')
  elif(data == 'M0'):
    board.setMute(False)
    logger.debug('set mute off')
  elif(data == 'M1'):
    board.setMute(True)
    logger.debug('set mute on')
  elif(data == 'S'):
    logger.info('shutdown')
    os.system('sudo shutdown -h now')
  elif(data.startswith('V+')):
    volume = board.getVolume()
    volume_step = float(data[2:len(data)])
    volume = volume + volume_step
    if(volume > 0):
      volume = 0
    board.setVolume(volume)
    str_vol = 'V' + str(volume) + '\n'
    serial_port.write(str.encode(str_vol))
    logger.debug('set volume: ' + str(volume))
  elif(data.startswith('V-')):
    volume = board.getVolume()
    volume_step = float(data[2:len(data)])
    volume = volume - volume_step
    if(volume < -127.5):
      volume = -127.5
    board.setVolume(volume)
    str_vol = 'V' + str(volume) + '\n'
    serial_port.write(str.encode(str_vol))
    logger.debug('set volume: ' + str(volume))
  elif(data == 'IP'):
    str_ip = 'IP' + get_ip() + '\n'
    serial_port.write(str.encode(str_ip))
  elif(data == 'H'):
    str_hostname = 'H' + socket.gethostname().partition('.')[0] + '\n'
    serial_port.write(str.encode(str_hostname))
  elif(data == 'C'):
    # close the board
    # start the VirtualHere server
    board.close();
    os.system('sudo systemctl start virtualhere')

  time.sleep(0.01)
  board.close()

def main():
  input_string = ''
  string_complete = False

  board = None

  board = minidsp.board_ddrc24.BoardDDRC24('usbhid')

  state_input = board.getInputSource()
  state_profile = board.getConfig()
  state_dsp = board.getDiracStatus()
  state_mute = board.getMute()
  state_volume = board.getVolume()
  ip_address = get_ip()

  board.close()
  
  logger.info('minidsp.py started')
  logger.debug('program start')
  logger.debug('input state: %s', state_input)
  logger.debug('profile state: %s', state_profile)
  logger.debug('dirac state: %s', state_dsp)
  logger.debug('mute state: %s', state_mute)
  logger.debug('volume state: %s', state_volume)
  logger.debug('ip address: %s', ip_address)
  logger.debug('hostname: %s', socket.gethostname().partition('.')[0])
  # Send 'R\n' twice. For some reason the first port.write doesn't make it to the Arduino
  serial_port.write(b'R\n')
  serial_port.write(b'R\n')
  serial_port.write(str.encode('IN' + state_input + '\n'))
  serial_port.write(str.encode('P' + str(state_profile) + '\n'))
  serial_port.write(str.encode('D' + str(state_dsp) + '\n'))
  serial_port.write(str.encode('M' + str(state_mute) + '\n'))
  serial_port.write(str.encode('V' + str(state_volume) + '\n'))
  serial_port.write(str.encode('IP' + ip_address + '\n'))
  serial_port.write(str.encode('H' + socket.gethostname().partition('.')[0] + '\n'))

  while True:
    r = serial_port.read().decode()

    input_string += r

    if(r == '\n'):
      string_complete = True
    else:
      string_complete = False
    
    if(string_complete):
      command = input_string.strip()
      input_string = ''
      string_complete = False
      handle_data(command)

    #serial_port.reset_input_buffer()
    #serial_port.reset_output_buffer()

if (__name__ == '__main__'):
  main()
