#!/bin/bash

if [ -z "$GRAFANA_URL" ] 
then
    echo "GRAFANA_URL nicht gesetzt. Ende."
    exit 1
fi

if [ "$EUID" -ne 0 ]
  then echo "Bitte mit sudo laufen lassen!"
  exit
fi

# generell update
apt-get update
apt-get upgrade

# wir brauchen python3
apt -y install python3
# wir brauchen pip3
apt -y install python3-pip
#Nö: sudo pip3 install --upgrade setuptools

# Run the following command to install the Raspberry PI GPIO library:
#Nö pip3 install RPI.GPIO
#pip3 install adafruit-blinka
pip3 install Adafruit_DHT
pip3 install wiringpi

# numpy
apt -y install libatlas-base-dev
apt -y
pip3 install numpy

# Jetzt noch die Dateien positionieren und Services aktivieren
./update.sh
