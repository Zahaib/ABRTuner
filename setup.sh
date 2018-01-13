#!/bin/bash

pass=$1
echo $mypassword | sudo -S sudo apt-get update && sudo apt-get upgrade
echo $mypassword | sudo -S sudo apt-get install ubuntu-desktop gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal
echo $mypassword | sudo -S sudo apt-get install xfce4
echo $mypassword | sudo -S sudo apt-get install vnc4server

echo $mypassword | sudo -S sudo apt-get install apache2

echo $mypassword | sudo -S  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
echo $mypassword | sudo -S  sudo dpkg -i --force-depends google-chrome-stable_current_amd64.deb


echo $mypassword | sudo -S  sudo apt-get install build-essential libssl-dev
curl -sL https://raw.githubusercontent.com/creationix/nvm/v0.31.0/install.sh -o install_nvm.sh
bash install_nvm.sh
source ~/.profile
echo $mypassword | sudo -S nvm install 6.11.3
nvm use 6.11.3  

echo $mypassword | sudo -S  sudo apt-get install nodejs
echo $mypassword | sudo -S sudo apt-get install npm

echo $mypassword | sudo -S sudo apt-get install python-pip python-numpy python-scipy
echo $mypassword | sudo -S sudo pip install statistics


# sudo python setup.py install