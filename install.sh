#!/bin/sh
#Script to download and install all dependencies to control the MiniDSP

echo "Starting the Installation..."

cd /home/pi

# Download requirements.txt
wget https://joeranriess.github.io/minidsp-setup/requirements.txt

# Packages
PACKAGES="python3-pip python3-dev libusb-1.0-0-dev libudev-dev git python3-pil"

apt-get update
apt-get upgrade -y
apt-get install $PACKAGES -y
pip3 install install --upgrade setuptools
pip3 install -r requirements.txt

rm requirements.txt

# Get project files
git clone https://github.com/joeranriess/minidsp-setup.git

# Make start script executable and create cron job
mkdir /home/pi/logs
cd /minidsp-setup/minidsp
chmod +x launcher.sh
#write out current crontab
crontab -l > tmpcron
#echo new cron into cron file
echo "@reboot sh /home/pi/minidsp-setup/minidsp/launcher.sh >/home/pi/logs/cronlog 2>&1" >> tmpcron
#install new cron file
crontab tmpcron
rm tmpcron

# Install Raspotify
curl -sL https://dtcooper.github.io/raspotify/install.sh | sh

# Change some config file entries
BOOT_CONFIG = "/boot/config.txt"
ALSA_CONFIG = "/usr/share/alsa/alsa.conf"
RASPOTIFY_CONFIG = "/etc/default/raspotify"

# CHanging /boot/config.txt
if grep -Fq "dtparam=i2c_arm" $BOOT_CONFIG
then
	# Replace the line
	echo "Modifying boot/config.txt"
	sed -i "/dtparam=i2c_arm/c\dtparam=i2c_arm=on" $BOOT_CONFIG
else
	# Create the definition
	echo "Adding to boot/config.txt"
	echo "dtparam=i2c_arm=on" >> $BOOT_CONFIG
fi

# Changing /usr/share/alsa/alsa.conf
if grep -Fq "defaults.ctl.card" $ALSA_CONFIG
then
	# Replace the line
	echo "Modifying alsa.conf"
	sed -i "s/defaults.ctl.card 0/defaults.ctl.card 1/g" $ALSA_CONFIG
else
	# Create the definition
	echo "Adding to alsa.conf"
	echo "defaults.ctl.card 1" >> $ALSA_CONFIG
fi

if grep -Fq "defaults.pcm.card" $ALSA_CONFIG
then
	# Replace the line
	echo "Modifying alsa.conf"
	sed -i "s/defaults.pcm.card 0/defaults.pcm.card 1/g" $ALSA_CONFIG
else
	# Create the definition
	echo "Adding to alsa.conf"
	echo "defaults.pcm.card 1" >> $ALSA_CONFIG
fi

# Changing /etc/default/raspotify
if grep -Fq "#DEVICE_NAME=" $RASPOTIFY_CONFIG
then
	# Replace the line
	echo "Modifying raspotify"
	sed -i 's/#DEVICE_NAME='raspotify'/DEVICE_NAME='MiniDSP'/g' $RASPOTIFY_CONFIG
else
	# Create the definition
	echo "Adding to raspotify"
	echo 'DEVICE_NAME="MiniDSP"' >> $RASPOTIFY_CONFIG
fi

if grep -Fq "#BITRATE=" $RASPOTIFY_CONFIG
then
	# Replace the line
	echo "Modifying raspotify"
	sed -i 's/#BITRATE="160"/BITRATE="320"/g' $RASPOTIFY_CONFIG
else
	# Create the definition
	echo "Adding to raspotify"
	echo 'BITRATE="320"' >> $RASPOTIFY_CONFIG
fi

if grep -Fq "#CACHE_ARGS=" $RASPOTIFY_CONFIG
then
	# Replace the line
	echo "Modifying raspotify"
	sed -i 's/#CACHE_ARGS="--cache /var/cache/raspotify"/CACHE_ARGS="--cache /var/cache/raspotify"' $RASPOTIFY_CONFIG
else
	# Create the definition
	echo "Adding to raspotify"
	echo 'CACHE_ARGS="--cache /var/cache/raspotify"' >> $RASPOTIFY_CONFIG
fi

echo "Installation complete, rebooting."
reboot
