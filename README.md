# minidsp-setup

## Raspberry Pi General:
1. Add ssh and wpa_supplicant.conf to SD Card
2. Change password
3. Expose GPIO throughout network (raspi-config)
4. Enable I2C (raspi-config)
5. sudo apt-get update
6. sudo apt-get upgrade
7. sudo apt-get install python3-pip
8. sudo pip3 install Cython
9. sudo apt-get install git


## Display:
1. sudo pip3 install adafruit-circuitpython-ht16k33
2. sudo apt-get install python3-pil


## IR Receiver:
1. sudo apt-get install lirc
2. sudo mv /etc/lirc/lirc_options.conf.dist /etc/lirc/lirc_options.conf
3. sudo apt-get install lirc
4. Edit /etc/lirc/lirc_options.conf as follows by changing these two lines:

:

:

driver = default

device = /dev/lirc0

:

:

5. sudo mv /etc/lirc/lircd.conf.dist /etc/lirc/lircd.conf
6. Edit /boot/config.txt by adding one line in the lirc-rpi module section as follows. This example assumes the RPi is 'listening' on BCM Pin 17 for the IR receiver but any RPi IO pin can be used. I have not tried it yet but if you want to send commands from the RPi then add and uncomment the 4th line shown below to send IR commands on BCM pin 18

:

:

:

\# Uncomment this to enable the lirc-rpi module

\#dtoverlay=lirc-rpi

dtoverlay=gpio-ir,gpio_pin=24

\#dtoverlay=gpio-ir-tx, gpio_pin=18

:

:

:

7. sudo systemctl stop lircd.service
8. sudo systemctl start lircd.service
9. sudo systemctl status lircd.service
10. sudo reboot
11. sudo systemctl stop lircd.service (optional)
12. sudo mode2 -d /dev/lirc0 --> test remote (optional)
13. sudo mv /etc/lirc/lircd.conf.d/devinput.lircd.conf /etc/lirc/lircd.conf.d/devinput.lircd.conf.copy
14. Place remote files into /etc/lirc/lircd.conf.d from http://lirc.sourceforge.net/remotes/
15. sudo reboot


## Relay:
1. sudo pip3 install RPi.GPIO


## MiniDSP Control:
1. sudo apt-get install python3-dev libusb-1.0-0-dev libudev-dev
2. sudo pip3 install --upgrade setuptools
3. sudo pip3 install hidapi
