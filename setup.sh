#!/bin/bash

pass=$1
echo $pass | sudo -S apt-get update && sudo apt-get upgrade
echo $pass | sudo -S apt-get install ubuntu-desktop gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal
echo $pass | sudo -S apt-get install xfce4
echo $pass | sudo -S apt-get install vnc4server
echo "VNCserver installed..."

echo $pass | sudo -S apt-get install apache2
echo "Apache2 installed..."

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
echo $pass | sudo -S dpkg -i --force-depends google-chrome-stable_current_amd64.deb
echo "Google Chrome installed..."

echo $pass | sudo -S apt-get install build-essential libssl-dev
curl -sL https://raw.githubusercontent.com/creationix/nvm/v0.31.0/install.sh -o install_nvm.sh
bash install_nvm.sh
source ~/.profile
echo $pass | sudo -S nvm install 6.11.3
nvm use 6.11.3  
echo "node installed..."
node -v

echo $pass | sudo -S apt-get install nodejs
echo "nodejs installed..."
nodejs -v

echo $pass | sudo -S apt-get install npm
echo "npm installed..."

echo $pass | sudo -S apt-get install python-pip python-numpy python-scipy
echo $pass | sudo -S pip install statistics
echo "python packages installed..."


# sudo python setup.py install