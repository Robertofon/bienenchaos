#!/usr/bin/python
# Author: Robert Köpferl
# Skript, um Sensoren des Typs AD2302 auszulesen und die umgerechneten
# Temperatur und Luftfeuchte-Werte zu pushen

import sys
import datetime
import time
#import Adafruit_DHT


# Einfach alle Sensoren der Reihe nach auslesen
sensoren  = [
{'Name': 'Bienen0_o', 'GPIO': 8, 'Pin': 24, 'Ziel': 'B0-o'},
{'Name': 'Bienen0_u', 'GPIO': 7, 'Pin': 26, 'Ziel': 'B0-u'},
{'Name': 'Bienen1_o', 'GPIO': 12, 'Pin': 32, 'Ziel': 'B1-o'},
{'Name': 'Bienen1_u', 'GPIO': 16, 'Pin': 36, 'Ziel': 'B1-u'},
{'Name': 'Bienen2_o', 'GPIO': 20, 'Pin': 38, 'Ziel': 'B2-o'},
{'Name': 'Bienen2_u', 'GPIO': 21, 'Pin': 40, 'Ziel': 'B2-u'},
]
intervall = 10
jez = datetime.datetime.now().isoformat()

print(f"{jez}: Starten von AD2302-Auslese-Skript. Läuft dauerhaft, periodisches Abfragen im Intervall: {intervall}s. Folgende Sensoren konfiguriert:")

for sensor in sensoren:
    print( sensor['Name'], "@ GPIO:", sensor['GPIO'], "/ Pin: ", sensor['Pin'])

while True:
    for sensor in sensoren:
        gpio = sensor['GPIO']
        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        # using read fails immediately
        #humidity, temperature = Adafruit_DHT.read('22', gpio)
        humidity, temperature = None,None

        # Note that sometimes you won't get a reading and
        # the results will be null (because Linux can't
        # guarantee the timing of calls to read the sensor).
        # If this happens try again!
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}°C  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            jez = datetime.datetime.now().isoformat()
            print(f"{jez} Fehler bei Sensor {sensor['Name']} Pin:{sensor['Pin']} - keine Werte erhalten.")
    # eine Runde pennen
    time.sleep(intervall)
