#!/bin/sh
#Script to download and install all dependencies to control the MiniDSP

echo "Starting the Installation..."

cd /home/pi

# Download requirements.txt
wget https://joeranriess.github.io/minidsp-setup/requirements.txt
echo "Successfully downloaded requirements.txt"

# Packages
PACKAGES="python3-pip python3-dev libusb-1.0-0-dev libudev-dev git python3-pil"

sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install $PACKAGES -y
echo "Successfully updated system and installed packages"
sudo pip3 install install --upgrade setuptools
sudo pip3 install -r requirements.txt
echo "Successfully installed pip3 packages"

# Get project files
git clone https://github.com/joeranriess/minidsp-setup.git
echo "Successfully downloaded project files"

# Changing /boot/config.txt
echo "Changing i2c settings"
BOOT_CONFIG="/boot/config.txt"

if grep -Fq "dtparam=i2c_arm" $BOOT_CONFIG
then
	# Replace the line
	echo "Modifying boot/config.txt"
	sudo sed -i "/dtparam=i2c_arm/c\dtparam=i2c_arm=on" $BOOT_CONFIG
else
	# Create the definition
	echo "Adding to boot/config.txt"
	sudo echo "dtparam=i2c_arm=on" >> $BOOT_CONFIG
fi
echo "Done."

#Move and create minidsp service
echo "Creating minidsp service"
wget https://joeranriess.github.io/minidsp-setup/minidsp.service
sudo cp minidsp.service /etc/systemd/system/
sudo systemctl start minidsp
sudo systemctl enable minidsp
echo "Done."

# Install Raspotify
curl -sL https://dtcooper.github.io/raspotify/install.sh | sh

# Change some config file entries
echo "Changing soundcard and raspotify configs"
ALSA_CONFIG="/usr/share/alsa/alsa.conf"
RASPOTIFY_CONFIG="/etc/default/raspotify"

# Changing /usr/share/alsa/alsa.conf
if grep -Fq "defaults.ctl.card" $ALSA_CONFIG
then
	# Replace the line
	echo "Modifying alsa.conf"
	sudo sed -i "s/defaults.ctl.card 0/defaults.ctl.card 1/g" $ALSA_CONFIG
else
	# Create the definition
	echo "Adding to alsa.conf"
	sudo echo "defaults.ctl.card 1" >> $ALSA_CONFIG
fi

if grep -Fq "defaults.pcm.card" $ALSA_CONFIG
then
	# Replace the line
	echo "Modifying alsa.conf"
	sudo sed -i "s/defaults.pcm.card 0/defaults.pcm.card 1/g" $ALSA_CONFIG
else
	# Create the definition
	echo "Adding to alsa.conf"
	sudo echo "defaults.pcm.card 1" >> $ALSA_CONFIG
fi

# Changing /etc/default/raspotify
if grep -Fq "#DEVICE_NAME=" $RASPOTIFY_CONFIG
then
	# Replace the line
	echo "Modifying raspotify"
	sudo sed -i 's/#DEVICE_NAME='raspotify'/DEVICE_NAME='MiniDSP'/g' $RASPOTIFY_CONFIG
else
	# Create the definition
	echo "Adding to raspotify"
	sudo echo 'DEVICE_NAME="MiniDSP"' >> $RASPOTIFY_CONFIG
fi

if grep -Fq "#BITRATE=" $RASPOTIFY_CONFIG
then
	# Replace the line
	echo "Modifying raspotify"
	sudo sed -i 's/#BITRATE="160"/BITRATE="320"/g' $RASPOTIFY_CONFIG
else
	# Create the definition
	echo "Adding to raspotify"
	sudo echo 'BITRATE="320"' >> $RASPOTIFY_CONFIG
fi

if grep -Fq "#CACHE_ARGS=" $RASPOTIFY_CONFIG
then
	# Replace the line
	echo "Modifying raspotify"
	sudo sed -i 's/#CACHE_ARGS="--cache /var/cache/raspotify"/CACHE_ARGS="--cache /var/cache/raspotify"' $RASPOTIFY_CONFIG
else
	# Create the definition
	echo "Adding to raspotify"
	sudo echo 'CACHE_ARGS="--cache /var/cache/raspotify"' >> $RASPOTIFY_CONFIG
fi

sudo systemctl restart raspotify

echo "Installation complete, rebooting."
sudo reboot
