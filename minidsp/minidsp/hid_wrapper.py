"""Wrapper to handle talking to the actual device"""

from contextlib import AbstractContextManager

# !! important!
# this is coded to use the library cython-hidapi from here:
# https://github.com/trezor/cython-hidapi
#
# and will not work with the other hidapi library from here:
# https://github.com/apmorton/pyhidapi
#
# There's no good reason that I chose this one, but the library I adapted
# from had already chosen it, and it works for the modest use here

import hid

MINIDSP_2x4HD_VID = 0x2752
MINIDSP_2x4HD_PID = 0x0011


class HID_Device(AbstractContextManager):
    """ USB HID transport through cython-hidapi """

    def __init__(self, vid=MINIDSP_2x4HD_VID, pid=MINIDSP_2x4HD_PID):
        self._vid = vid
        self._pid = pid
        self._device = hid.device()
        self._opened = False

    def __enter__(self):
        """open up the device for writing/reading"""
        self._device.open(self._vid, self._pid)
        self._opened = True
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """close up the device"""
        self._device.close()
        self._opened = False
        # letting any exc stuff bubble up for now.
        # https://docs.python.org/3/library/stdtypes.html#typecontextmanager

    def write(self, command):
        if not self._opened:
            raise RuntimeError("Device not open; use 'with' syntax to read/write")
        # Add header specifying command length (+1 for CRC8 byte)
        command = [len(command) + 1] + command
        # Add a CRC8 byte at the end
        command = command + [sum(command) % 0x100]
        self._device.write([0x00] + command)

    def read(self):
        if not self._opened:
            raise RuntimeError("Device not opened; use 'with' syntax to read/write")
        length = 64  # not sure why this; it seems to be in the examples, though
        timeout_ms = 2000
        response = self._device.read(length, timeout_ms)
        # First byte is the response length
        return response[1 : response[0]]
