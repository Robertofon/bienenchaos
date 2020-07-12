import nau7802py, time

myScale = nau7802py.NAU7802()

if myScale.begin():
    while True:
        currentReading = myScale.getReading()
        currentWeight = myScale.getWeight()
        print('Reading: ' + str(currentReading)+"  "+ str(round(currentWeight, 4)))
        time.sleep(1)
