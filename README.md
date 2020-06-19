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

## Install dependencies:
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
sudo pip3 install evdev
```
## Get started
Download the repository
```
git clone https://github.com/joeranriess/minidsp-setup.git
```
Switch to correct folder:
```
cd /minidsp-setup/minidsp
```
Make the launcher executable
```
sudo chmod +x launcher.sh
```
Create a cronjob
```
sudo crontab -e
```
Insert the following line after creating new cron file
```
@reboot sh /home/pi/minidsp-setup/minidsp/launcher.sh >/home/pi/logs/cronlog 2>&1
```
Create logs folger
```
mkdir /home/pi/logs
```
Plug everything in, check GPIO pins with those in the code and other configs, then:
```
sudo reboot
```
If everything is setup properly you should see the volume on your display.


Additional notes:
- Flirc USB IR receiver must be configured to output the configured keys according to your ir remote keys.
