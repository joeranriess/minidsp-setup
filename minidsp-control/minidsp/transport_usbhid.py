import hid
import time

import logging
import logging.handlers

logger = logging.getLogger('minidsp-pre_logger')
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.handlers.SysLogHandler(address = '/dev/log')
    formatter = logging.Formatter('(%(levelname)s) %(module)s.%(funcName)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class TransportUSBHID:
    """ USB HID transport through cython-hidapi """

    def __init__(self, vid, pid):
        try:
            self._hid_device = hid.device()
            self._hid_device.open(vid, pid)
            self._hid_device.set_nonblocking(1)
        except:
            # Throw error here
            logger.critical('HID device failed to open')
            raise RuntimeError("HID device failed to open")

    def write(self, command):
        # init hid command to report id (0) plus 64 0xFF
        hid_buf = [0x00] + [0xff]*64
        # Add header specifying command length (+1 for CRC8 byte)
        command = [len(command)+1] + command
        # Add a CRC8 byte at the end
        command = command + [sum(command) % 0x100]
        # Insert the fully fledged command into the data sequence
        hid_buf[1:len(command)+1] = command

        # Send it
        try:
            self._hid_device.write(hid_buf)
        except:
            logger.critical('HID send failed.')
            raise RuntimeError("HID send failed!!!")

        # Read back the response
        try:
            resp = self._hid_device.read(64, 250)
        except:
            logger.critical('HID read failed.')
            raise RuntimeError("HID read failed!!!")
        
        # First byte is the response length
        
        if resp:
          resp = resp[1:resp[0]]

        return resp
    
    def close(self):
      try:
        self._hid_device.close()
      except:
        logger.critical('Error closing device.')
        raise RunTimeError("Error closing device.")

