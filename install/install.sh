#!/bin/bash
echo "Install skript für die Dienste um Bienentemperatur, Gewicht und Feuchte zu messen. Es werden 3 Dienste erstellt, die im Hintergrund laufen. Publiziert wird via Grafana. Daher muss die Variable GRAFANAENDP gesetzt sein mit host:port und zusätzlich GRAFANADB mit DB-name"

if [ -z "$GRAFANAENDP" ] then
    echo "GRAFANAENDP nicht gesetzt. Ende."
    exit 1
fi

if [ -z "$GRAFANADB" ] then
    echo "GRAFANADB nicht gesetzt. Ende."
    exit 1
fi



# generell update
sudo apt-get update
sudo apt-get upgrade

# wir brauchen python3
sudo apt install python3
# wir brauchen pip3
#nö: sudo apt-get install python3-pip
#Nö: sudo pip3 install --upgrade setuptools

# Run the following command to install the Raspberry PI GPIO library:
#Nö pip3 install RPI.GPIO
#pip3 install adafruit-blinka

