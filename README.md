# minidsp-setup

## Raspberry Pi General:
1. Add ssh and wpa_supplicant.conf to SD Card
2. Change password
3. Expose GPIO throughout network (raspi-config)
4. Enable I2C (raspi-config)
`sudo apt-get update`
6. sudo apt-get upgrade

## MiniDSP Control:
1. sudo apt-get install python3-pip
2. sudo pip3 install Cython
3. sudo apt-get install git
4. sudo pip3 install adafruit-circuitpython-ht16k33
5. sudo apt-get install python3-pil
6. sudo pip3 install RPi.GPIO
7. sudo apt-get install python3-dev libusb-1.0-0-dev libudev-dev
8. sudo pip3 install --upgrade setuptools
9. sudo pip3 install hidapi
10. sudo pip3 install evdev
