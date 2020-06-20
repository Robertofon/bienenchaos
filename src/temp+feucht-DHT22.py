#!/usr/bin/python
# Author: Robert Köpferl
# Skript, um Sensoren des Typs AM2302 auszulesen und die umgerechneten
# Temperatur und Luftfeuchte-Werte zu pushen

import sys,os
import datetime
import time
import Adafruit_DHT


grafanaurl="%GRAFANA_URL%"    #172.23.92.63:8086/write?db=mydb&u=admin&p=PASSWORD


# Einfach alle Sensoren der Reihe nach auslesen
sensoren  = [
{'Name': 'Bienen0_o', 'GPIO': 7, 'Pin': 26, 'Ziel': 'B0-o'},
{'Name': 'Bienen0_u', 'GPIO': 8, 'Pin': 24, 'Ziel': 'B0-u'},
{'Name': 'Bienen1_o', 'GPIO': 16, 'Pin': 36, 'Ziel': 'B1-o'},
{'Name': 'Bienen1_u', 'GPIO': 12, 'Pin': 32, 'Ziel': 'B1-u'},
{'Name': 'Bienen2_o', 'GPIO': 21, 'Pin': 40, 'Ziel': 'B2-o'},
{'Name': 'Bienen2_u', 'GPIO': 20, 'Pin': 38, 'Ziel': 'B2-u'},
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
        print ("GPIO: ", gpio,"  pin: ",sensor["Pin"]) 
        humidity, temperature = Adafruit_DHT.read(Adafruit_DHT.DHT22, gpio)
        #humidity, temperature = None,None

        # Note that sometimes you won't get a reading and
        # the results will be null (because Linux can't
        # guarantee the timing of calls to read the sensor).
        # If this happens try again!
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}°C  Humidity={1:0.1f}%'.format(temperature, humidity))
            os.system("curl -i -XPOST '"+grafanaurl+"' --data-binary 'temperature,location="+sensor['Ziel']+" value="+str(temperature)+"'")
            os.system("curl -i -XPOST '"+grafanaurl+"' --data-binary 'humidity,location="+sensor['Ziel']+" value="+str(humidity)+"'")
        else:
            jez = datetime.datetime.now().isoformat()
            print(f"{jez} Fehler bei Sensor {sensor['Name']} Pin:{sensor['Pin']} - keine Werte erhalten.")
        time.sleep(.01)
    # eine Runde pennen
    time.sleep(intervall)

