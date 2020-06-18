# bienenchaos
Erfassung von Bienenparametern mit Raspi, Sensoren, Waagen und Grafana

Mehrere Raspi ZeroW

Platinen drauf.

## Temperatur und Luftfeuchte messen

Selbsgelötetes Board mit Pullupwiderständen zu 5V.  
Anbindung von aktuell 6 Sensoren des Typs AM2302

GPIOs fürn Raspi und die Sensoren.
- Frei für unseren eigenen Sensor-HAT
* GPIO8 (24)   (Bienen0) - Sensor A
* GPIO7 (26)   (Bienen0) - Sensor B
* GPIO12 (32)   (Bienen1) - Sensor A
* GPIO16 (36)   (Bienen1) - Sensor B
* GPIO20 (38)   (Bienen2) - Sensor A
* GPIO21 (40)   (Bienen2) - Sensor B
* 3V3 (17) - Alle Datenkabel via 4,7kOhm auf VCC und alle Sensor-VCC
* GND (34,30) - Alle Sensor-GND



## ADDA-Board
https://www.waveshare.com/wiki/High-Precision_AD/DA_Board#Interface_Definition
Frei bleibende Pins
3, 5, 7, 8, 10, 18, 22, 24, 26, 27, 28, 29, 32, 36, 38, 40

funktionierender, inoffizieller Treiber
https://github.com/ul-gh/PiPyADC


Verlängerung der Waage (CN) Kabelfarben
Verlängert durch Netzwerk
* Rot -> Orange  (Spannungsversorgung +)
* Gelb -> Hellorange
* Grün -> Grün   (Signal +)
* Schwarz -> Braun  (Spannungsversorgung -)
* Weiß -> Hellbraun (Signal -)


## Helfende Repos

DHT22 (AM2302) auslesen:  
https://github.com/adafruit/Adafruit_Python_DHT.git

Neuer:  
https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup
