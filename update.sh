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

# Skripte nach /opt/bienen kopieren
mkdir -p /opt/bienen
# dabei über SED drüberjagen, variablen ersetzen
#cp src/temp+feucht-DHT22.py /opt/bienen/temp+feucht-DHT22.py
#cp src/weight-datageneration.py /opt/bienen/weight-datageneration.py
for f in temp+feucht-DHT22.py weight-datageneration.py
do
    # / ersetzen durch \/
    Var=${GRAFANA_URL//\//\\/}
    # & ersetzen durch \&
    Var=${Var//[&]/\\&}
    cat src/$f | sed 's/%GRAFANA_URL%/'$Var'/' > /usr/bin/$f
done

# Repo von ul-gh/PiPyADC in /opt/bienen clonen
git submodule update PiPyADC
cp -av PiPyADC /opt/bienen/PiPyADC 

# systemd unit files kopieren und chmod
cp src/systemd/temp-feuchte-sammler.service /etc/systemd/system/temp-feuchte-sammler.service
cp src/systemd/weight-sammler.service /etc/systemd/system/weight-sammler.service
chmod 644 /etc/systemd/system/weight-sammler.service
chmod 644 /etc/systemd/system/temp-feuchte-sammler.service

# services enablen - starten so automatisch
systemctl enable temp-feuchte-sammler
systemctl enable weight-sammler

# und starten
systemctl start temp-feuchte-sammler
systemctl start weight-sammler
