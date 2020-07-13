import nau7802py
import time,os

myScale = nau7802py.NAU7802()

grafanaurl="%GRAFANA_URL%"

if myScale.begin():
    while True:
        currentReading = myScale.getReading()
        currentWeight = myScale.getWeight()
        print('Reading: ' + str(currentReading)+"  "+ str(round(currentWeight, 4)))
        try:
            cmd="curl -i -XPOST '"+grafanaurl+"' --data-binary 'weight,location=bees01 value="+str(currentWeight)+"'"
            print (cmd)
            os.system(cmd)
        except:
            print("no access to grafana?")
            pass
        time.sleep(1)
