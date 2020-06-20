#!/bin/sh

# Download requirements.txt
wget https://raw.githubusercontent.com/joeranriess/minidsp-setup/master/minidsp-setup/requirements.txt

# Packages
PACKAGES="python3-pip python3-dev libusb-1.0-0-dev libudev-dev git python3-pil"

apt-get update
apt-get upgrade -y
apt-get install $PACKAGES -y
pip3 install install --upgrade setuptools
pip3 install -r requirements.txt
###requirements.txt###
Cython
hidapi
adafruit-circuitpython-ht16k33
RPi.GPIO
evdev

# Do other stuff
CONFIG = "/path/to/file.sh"





dtparam=i2c_arm=on
sudo nano /usr/share/alsa/alsa.conf
defaults.ctl.card 1
defaults.pcm.card 1
