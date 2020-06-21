# minidsp-setup

## Raspberry Pi General:
1. Add ssh and wpa_supplicant.conf to SD Card
2. Change password
3. Enable I2C (raspi-config) <-- This is very important!

## The easy way
Simply copy this into the terminal and hit enter:
```
sudo curl -sL https://joeranriess.github.io/minidsp-setup/install.sh | sh
```

## The hard way
Update und upgrade Raspberry Pi OS
```
sudo apt-get update
sudo apt-get upgrade
```

## Install dependencies:
```
sudo apt-get install python3-pip python3-dev libusb-1.0-0-dev libudev-dev git python3-pil
```
Install pip3 packages
```
sudo pip3 install Cython
sudo pip3 install hidapi
sudo pip3 install adafruit-circuitpython-ht16k33
sudo pip3 install RPi.GPIO
sudo pip3 install evdev
```

## Get started
Download the repository
```
git clone https://github.com/joeranriess/minidsp-setup.git
```
Create minidsp.service file and move to /etc/systemd/system with:
```
[Unit]
Description=MiniDSP service

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/pi/minidsp-setup/minidsp/minidsp.py

[Install]
WantedBy=multi-user.target
```

Plug everything in, check GPIO pins with those in the code and other configs, then:
```
sudo systemctl start minidsp
sudo systemctl enable minidsp
```
If everything is setup properly you should see the volume on your display.

Install Raspotify according to: https://github.com/dtcooper/raspotify
Edit config file of Raspotify to your needs.
Change ALSA config to use MiniDSP as default soundcard
```
sudo nano /usr/share/alsa/alsa.conf
defaults.ctl.card 1
defaults.pcm.card 1
```
Finally:
```
sudo reboot
```

Additional notes:
- Flirc USB IR receiver must be configured to output the configured keys according to your ir remote keys.
- I highly recommend using a Raspberry Pi 4 or 3, the performance is much better on these (tested bootup times between Raspberry Pi Zero W and Raspberry Pi 4: 41 Seconds vs. 14 Seconds until Volume is shown!
