#!/usr/bin/python
# Author: Robert Köpferl
# Skript, um Sensoren des Typs AD2302 auszulesen und die umgerechneten
# Temperatur und Feuchte-Werte zu pushen

import sys

import Adafruit_DHT


# Einfach alle Sensoren der Reihe nach auslesen

sensor  = [
{'Name': 'Bienen0_o', 'Pin': 24, 'Ziel': 'B0-o'},
{'Name': 'Bienen0_u', 'Pin': 26, 'Ziel': 'B0-u'},
{'Name': 'Bienen1_o', 'Pin': 32, 'Ziel': 'B1-o'},
{'Name': 'Bienen1_u', 'Pin': 36, 'Ziel': 'B1-u'},
{'Name': 'Bienen2_o', 'Pin': 38, 'Ziel': 'B2-o'},
{'Name': 'Bienen2_u', 'Pin': 40, 'Ziel': 'B2-u'},
]

* GPIO8 (24)   (Bienen0) - Sensor A
* GPIO7 (26)   (Bienen0) - Sensor B
* GPIO12 (32)   (Bienen1) - Sensor A
* GPIO16 (36)   (Bienen1) - Sensor B
* GPIO20 (38)   (Bienen2) - Sensor A
* GPIO21 (40)   (Bienen2) - Sensor B

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read(sensor, pin)



# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)
