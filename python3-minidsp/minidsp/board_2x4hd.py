import struct

from .hid_wrapper import HID_Device


class Board2x4HD:
    """ Commands for 2x4HD """

    def __init__(self):
        self._device = HID_Device()

    def _get_status(self):
        status = {}
        # send the 'get status command'
        COMMAND = [0x05, 0xFF, 0xDA, 0x02]
        with self._device as d:
            d.write(COMMAND)
            response = d.read()
            # sometimes we get back other stuff from the card, and have to get past them
            # before we can get what we want...
            tries = 1
            while response[:3] != COMMAND[:3]:
                if tries > 10:
                    raise RuntimeError(
                        "Tried >10 times to get a valid response to master status! Crashing!"
                    )
                # some known values that often come back are
                # ['0x5', '0xff', '0xd9', '0x02']
                # d9 is switching source; 02 is for example the usb input, so might as well process those
                if response and (len(response) > 2) and response[2] == "0xd9":
                    # throw it in just to be nice so we don't have to do it later
                    status["source"] = ["analog", "toslink", "usb"][response[3]]
                # try again
                d.write(COMMAND)
                tries += 1
                response = d.read()

            # if we've made it here, some valid volume/mute information is likely...
            # and resp starts with [0x05, 0xFF, 0xDA]
            if response[4] not in [0x00, 0x01]:
                raise RuntimeError(
                    "Received unexpected response: bad mute value " + str(response)
                )
            status["volume"] = response[3] * -0.5
            status["mute"] = response[4] == 0x01

        if "source" not in status:
            status["source"] = self._get_source()
        return status

    status = property(_get_status)

    def _get_volume(self):
        return self._get_status()["volume"]

    def _set_volume(self, volume):
        if (volume > 0) or (volume < -127.5):
            raise RuntimeError("Volume out of bounds. Range: -127.5 to 0 (db)")
        # Send volume command
        with self._device as d:
            d.write([0x42, round(-2 * volume)])

    volume = property(_get_volume, _set_volume)

    def volume_up(self, notches=1):
        """turn the volume up by 'notches' which are 0.5db"""
        current_volume = self._get_volume()
        assert (
            type(notches) is int
        ), "Can't send that in for volume change! only ints please"
        new_volume = current_volume + (notches * 0.5)
        assert -127.5 <= new_volume <= 0, "That would set volume out of bounds!"
        self._set_volume(new_volume)

    def volume_down(self, notches=1):
        """turn the volume down by 'notches' which are 0.5db"""
        self.volume_up(-notches)

    def _get_mute(self):
        return self._get_status()["mute"]

    def _set_mute(self, mute_status=True):
        assert mute_status in (True, False), "Can only send True or False"
        with self._device as d:
            if mute_status:
                m = 0x01
            else:
                m = 0x00
            d.write([0x17, m])

    def mute(self):
        self._set_mute(True)

    def unmute(self):
        self._set_mute(False)

    muted = property(_get_mute, _set_mute)

    def mute_toggle(self):
        if self._get_mute():
            self._set_mute(False)
        else:
            self._set_mute(True)

    def _get_source(self):
        # Send input source check command
        COMMAND = [0x05, 0xFF, 0xD9, 0x01]
        with self._device as d:
            tries = 1
            d.write(COMMAND)
            response = d.read()
            tries = 1
            while response[:3] != COMMAND[:3]:
                if tries > 10:
                    raise RuntimeError(
                        "Tried >10 times to get a valid response to inputSource! Crashing!"
                    )
                # could log what we DO get back here, but don't have a place to do that right now...
                # try again
                d.write(COMMAND)
                tries += 1
                response = d.read()

            # if we've made it here, some valid source information is likely...
            # and resp starts with [0x05, 0xFF, 0xD9]
            if response[3] not in [0x00, 0x01, 0x02]:
                raise RuntimeError(
                    "Received unexpected response: bad source value {}".format(
                        response[3]
                    )
                )
        # Return the source string
        sources = ["analog", "toslink", "usb"]
        return sources[response[3]]

    def _set_source(self, source):
        sources = {"analog": 0x00, "toslink": 0x01, "usb": 0x02}
        assert source in sources, "oops, that's not a valid source"
        with self._device as d:
            d.write([0x34, sources[source]])

    source = property(_get_source, _set_source)

    def _get_config(self):
        # Send config check command
        COMMAND = [0x05, 0xFF, 0xD8, 0x01]
        with self._device as d:
            d.write(COMMAND)
            response = d.read()
            tries = 1
            while response[:3] != COMMAND[:3]:
                if tries > 10:
                    raise RuntimeError(
                        "Tried >10 times to get a valid response to get config! Crashing!"
                    )
                # could log what we DO get back here, but don't have a place to do that right now...
                # try again
                d.write(COMMAND)
                tries += 1
                response = d.read()

        if response[3] not in [0x00, 0x01, 0x02, 0x03]:
            raise RuntimeError("Received unexpected config value: {}".format(response[3]))
        # Return the source index (1-indexed)
        return response[3] + 1

    def _set_config(self, config):
        # Integrity check
        if (config < 1) or (config > 4):
            raise RuntimeError("Config index out of range (should be 1-4)")
        with self._device as d:
            # these are all from mark's original code; not sure about it, as I don't
            # use configs now
            d.write([0x25, config - 1, 0x02])
            d.write([0x05, 0xFF, 0xE5, 0x01])
            d.write([0x05, 0xFF, 0xE0, 0x01])
            d.write([0x05, 0xFF, 0xDA, 0x02])

    config = property(_get_config, _set_config)

    def _get_levels(self):
        # get input levels on the DSP right now.
        # adapted from https://github.com/mrene/node-minidsp/
        COMMAND = [0x14, 0x00, 0x44, 0x02]
        with self._device as d:
            d.write(COMMAND)
            response = d.read()
            tries = 1
            while response[:3] != COMMAND[:3]:
                if tries > 10:
                    raise RuntimeError(
                        "Tried >10 times to get a valid response to get levels! Crashing!"
                    )
                d.write(COMMAND)
                tries += 1
                response = d.read()

        # current levels are in the response in two 32bit low-endian floats
        # at index 3-7 and 8-11 inclusive; so unpack two nums...
        # @@ probably fragile here :-(
        (l, r) = struct.unpack("<ff", bytes(response[3:11]))

        # trim those 32bit floats down...
        return (round(l, 2), round(r, 2))

    levels = property(_get_levels)

    def _set_input_gain(self, input=0, gain=0):
        # nb! input is not the source; it's left or right, essentially
        # input either 0 or 1; gain from -127.5 to +12
        assert -127.5 <= gain <= 12, "Gain out of bounds. Range: -127.5 to 12 (db)"
        assert input in (0, 1), "input should be either 0 or 1"
        # again, this is adapted from https://github.com/mrene/node-minidsp/
        # the node code has that last byte either at 0x1A or 0x1B, depending on input, so...
        COMMAND = [0x13, 0x80, 0x0, 0x1A + input]
        # pack the gain value into a little-endian 32bit bytes string
        # and add those 4 bytes to the command
        COMMAND += list(struct.pack("<f", gain))

        with self._device as d:
            d.write(COMMAND)
            # doesn't seem to return anything, but ...
            response = d.read()
        return response

    def set_gain(self, gain):
        # set input gain for both input channels; use the _setInputGain to set individual ones
        self._set_input_gain(0, gain)
        self._set_input_gain(1, gain)
