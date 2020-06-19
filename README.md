# minidsp-setup

## Raspberry Pi General:
1. Add ssh and wpa_supplicant.conf to SD Card
2. Change password
3. Expose GPIO throughout network (raspi-config)
4. Enable I2C (raspi-config)

Update und upgrade Raspberry Pi OS
```
sudo apt-get update
sudo apt-get upgrade
```

## MiniDSP Control:
Install PIP for Python3
```
sudo apt-get install python3-pip
```
Cython is needed to use usb hid API
```
sudo pip3 install Cython
```
Install further libraries to support USB access
```
sudo apt-get install python3-dev libusb-1.0-0-dev libudev-dev
sudo pip3 install --upgrade setuptools
sudo pip3 install hidapi
```
Install git to clone the repository
```
sudo apt-get install git
```
Install Python library for display and image library
```
sudo pip3 install adafruit-circuitpython-ht16k33
sudo apt-get install python3-pil
```
Install GPIO Python library
```
sudo pip3 install RPi.GPIO
```
Install evdev library to read keyboard input in background
```
10. sudo pip3 install evdev
```
