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
cp src/nau7802py.py /opt/bienen/nau7802py.py
cp src/ADS1256_tim01_config.py /opt/bienen/ADS1256_tim01_config.py
# dabei über SED drüberjagen, variablen ersetzen
for f in temp+feucht-DHT22.py weight-datageneration.py
do
    # / ersetzen durch \/
    Var=${GRAFANA_URL//\//\\/}
    # & ersetzen durch \&
    Var=${Var//[&]/\\&}
    cat src/$f | sed 's/%GRAFANA_URL%/'$Var'/' > /opt/bienen/$f
done

# Repo von ul-gh/PiPyADC in /opt/bienen clonen
git submodule update --init
cp -av PiPyADC/* /opt/bienen/PiPyADC/ 

# systemd unit files kopieren und chmod
cp src/systemd/temp-feuchte-sammler.service /etc/systemd/system/temp-feuchte-sammler.service
cp src/systemd/weight-sammler.service /etc/systemd/system/weight-sammler.service
chmod 644 /etc/systemd/system/weight-sammler.service
chmod 644 /etc/systemd/system/temp-feuchte-sammler.service

# services enablen - starten so automatisch
systemctl enable temp-feuchte-sammler
systemctl enable weight-sammler

# und starten
systemctl restart temp-feuchte-sammler
systemctl restart weight-sammler
