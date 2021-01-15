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
* GPIO24 (18)  (Extern=Außentemp)
* 3V3 (17) - Alle Datenkabel via 4,7kOhm auf VCC und alle Sensor-VCC
* GND (34,30) - Alle Sensor-GND

## Gewichtsmessung 

Zuerst mittels ADDA-Board https://www.waveshare.com/wiki/High-Precision_AD/DA_Board#Interface_Definition

Später mit dem NAU7802 Board von SparkFun (Qwiic Scale - NAU7802) dieses liefert bequem die Versorgungsspannung mit ausreichend Amper mit. 
(Zudem brutzelt man sich nicht irgendwas beim Löten unter Strom weg ...) 

Da die Messung auch das genaue Verhältnis von Eingangssignal zu Speisespannung verwendet fallen Schwankungen der Speisepannung nicht ins Gewicht und 
das Signal war somit deutlich stabiler. 

Funktionierender Treiber von https://github.com/longapalooza/nau7802py

Verlängerung der Waage (CN) Kabelfarben
Verlängert durch Netzwerk
* Rot -> Orange ->Rot  (Spannungsversorgung +)
* Gelb -> Hellorange  ->GELB (Schirm )
* Grün -> Grün ->Gelbschwarz  (Signal +)
* Schwarz -> Braun  ->schwarz  (Spannungsversorgung -)
* Weiß -> Hellbraun  ->blau (Signal -)


## Helfende Repos

Credits gehen an ul-gh für sein Repo PiPyADC
https://github.com/ul-gh/PiPyADC

DHT22 (AM2302) auslesen:  
https://github.com/adafruit/Adafruit_Python_DHT.git

Neuer:  
https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup
