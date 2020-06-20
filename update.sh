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

# Skripte nach usr/bin kopieren
# dabei über SED drüberjagen, variablen ersetzen
#cp src/temp+feucht-DHT22.py /usr/bin/temp+feucht-DHT22.py
#cp src/weight-datageneration.py /usr/bin/weight-datageneration.py
for f in temp+feucht-DHT22.py weight-datageneration.py
do
    # / ersetzen durch \/
    Var=${GRAFANA_URL//\//\\/}
    # & ersetzen durch \&
    Var=${Var//[&]/\\&}
    cat src/$f | sed 's/%GRAFANA_URL%/'$Var'/' > /usr/bin/$f
done

# systemd unit files kopieren und chmod
cp src/systemd/temp-feuchte-sammler.service /etc/systemd/system/temp-feuchte-sammler.service
cp src/systemd/weight-sammler.service /etc/systemd/system/weight-sammler.service
chmod 644 /etc/systemd/system/weight-sammler.service

# services enablen - starten so automatisch
systemctl enable temp-feuchte-sammler
systemctl enable weight-sammler

# und starten
systemctl start temp-feuchte-sammler
systemctl start weight-sammler
