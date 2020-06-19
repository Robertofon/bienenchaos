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

if [ "$EUID" -ne 0 ]
  then echo "Bitte mit sudo laufen lassen!"
  exit
fi

# generell update
apt-get update
apt-get upgrade

# wir brauchen python3
apt install python3
# wir brauchen pip3
apt-get install python3-pip
#Nö: sudo pip3 install --upgrade setuptools

# Run the following command to install the Raspberry PI GPIO library:
#Nö pip3 install RPI.GPIO
#pip3 install adafruit-blinka

sudo pip3 install Adafruit_DHT


# Skripte nach usr/bin kopieren
cp src/temp+feucht-DHT22.py /usr/bin/temp+feucht-DHT22.py
cp src/weight-datageneration.py /usr/bin/weight-datageneration.py

# systemd unit files kopieren und chmod
cp src/systemd/temp+feuchte-sammler.service /etc/systemd/system/temp+feuchte-sammler.service
chmod 644 /etc/systemd/system/temp+feuchte-sammler.service
cp src/systemd/weight-sammler.service /etc/systemd/system/weight-sammler.service
chmod 644 /etc/systemd/system/weight-sammler.service

# services enablen - starten so automatisch
systemctl enable temp+feuchte-sammler
systemctl enable weight-sammler

# und starten
systemctl start temp+feuchte-sammler
systemctl start weight-sammler
