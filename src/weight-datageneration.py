import csv
import random
import time, os
import sys
import time
import numpy as np
import itertools
from ADS1256_definitions import *
from pipyadc import ADS1256
# In this example, we pretend myconfig_2 was a different configuration file
# named "myconfig_2.py" for a second ADS1256 chip connected to the SPI bus.
import ADS1256_tim01_config as myconfig_2

from tkinter import *

print ("TEST")
def fetch(e):
    print("NAME: ",e)
    global name_input
    global e1
    name_input=e1.get()
    
name_input="Nobody"

master = Tk()
Label(master, text="Name").grid(row=0)
e1 = Entry(master,font=("Arial", 26))
e1.bind("<Return>",fetch)
b1 = Button(master, text='Change', command=(lambda e=e1.get(): fetch(e)))
e1.grid(row=0, column=0)
b1.grid(row=0, column=1)

x_value = 0
total_1 = 1000
total_2 = 1000

fieldnames = ["x_value", "total_1", "name_input"]


#with open('data.csv', 'w') as csv_file:
#    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#    csv_writer.writeheader()

first=True
# Input pin for the potentiometer on the Waveshare Precision ADC board:
POTI = POS_AIN0|NEG_AINCOM
# Light dependant resistor of the same board:
LDR  = POS_AIN1|NEG_AINCOM
# The other external input screw terminals of the Waveshare board:
EXT2, EXT3, EXT4 = POS_AIN2|NEG_AINCOM, POS_AIN3|NEG_AIN4, POS_AIN4|NEG_AIN3
EXT5, EXT6, EXT7 = POS_AIN5|NEG_AINCOM, POS_AIN6|NEG_AINCOM, POS_AIN7|NEG_AINCOM

# You can connect any pin as well to the positive as to the negative ADC input.
# The following reads the voltage of the potentiometer with negative polarity.
# The ADC reading should be identical to that of the POTI channel, but negative.
POTI_INVERTED = POS_AINCOM|NEG_AIN0

# For fun, connect both ADC inputs to the same physical input pin.
# The ADC should always read a value close to zero for this.
SHORT_CIRCUIT = POS_AIN0|NEG_AIN0

# Specify here an arbitrary length list (tuple) of arbitrary input channel pair
# eight-bit code values to scan sequentially from index 0 to last.
# Eight channels fit on the screen nicely for this example..
#CH_SEQUENCE = (POTI, LDR, EXT2, EXT3, EXT4, EXT7, POTI_INVERTED, SHORT_CIRCUIT)
CH_SEQUENCE = (EXT3,)
################################################################################
##########################  CALIBRATION  CONSTANTS  ############################
# This shows how to use individual channel calibration values.
#
# The ADS1256 has internal gain and offset calibration registers, but these are
# applied to all channels without making any difference.
# I we want to use individual calibration values, e.g. to compensate external
# circuitry parasitics, we can do this very easily in software.
# The following values are only for demonstration and have no meaning.
CH_OFFSET = np.array((-10,   0, 0,   0, 750,   0,   0,   0), dtype=np.int)
GAIN_CAL  = np.array((1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0), dtype=np.float)
################################################################################

# Using the Numpy library, digital signal processing is easy as (Raspberry) Pi..
# However, this constant only specifies the length of a moving average.
FILTER_SIZE = 1
################################################################################


def do_measurement():
    ### STEP 1: Initialise ADC objects for two chips connected to the SPI bus.
    # In this example, we pretend myconfig_2 was a different configuration file
    # named "myconfig_2.py" for a second ADS1256 chip connected to the SPI bus.
    # This file must be imported, see top of the this file.
    # Omitting the first chip here, as this is only an example.

    #ads1 = ADS1256(myconfig_1)
    # (Note1: See ADS1256_default_config.py, see ADS1256 datasheet)
    # (Note2: Input buffer on means limited voltage range 0V...3V for 5V supply)
    ads2 = ADS1256(myconfig_2)
    
    # Just as an example: Change the default sample rate of the ADS1256:
    # This shows how to acces ADS1256 registers via instance property
    ads2.drate = DRATE_2_5
    ads2.pga_gain = 64
    #ads2.mux = POS_AIN4 | NEG_AIN3
    ### STEP 2: Gain and offset self-calibration:
    ads2.cal_self()

    ### Get ADC chip ID and check if chip is connected correctly.
    chip_ID = ads2.chip_ID
    print("\nADC No. 2 reported a numeric ID value of: {}.".format(chip_ID))
    # When the value is not correct, user code should exit here.
    if chip_ID != 3:
        print("\nRead incorrect chip ID for ADS1256. Is the hardware connected?")
    # Passing that step because this is an example:
    #    sys.exit(1)

    # Channel gain must be multiplied by LSB weight in volts per digit to
    # display each channels input voltage. The result is a np.array again here:
    CH_GAIN = ads2.v_per_digit * GAIN_CAL

    # Numpy 2D array as buffer for raw input samples. Each row is one complete
    # sequence of samples for eight input channel pin pairs. Each column stores
    # the number of FILTER_SIZE samples for each channel.
    rows, columns = FILTER_SIZE, len(CH_SEQUENCE)
    filter_buffer = np.zeros((rows, columns), dtype=np.int)
    
    # Fill the buffer first once before displaying continuously updated results
    print("Channels configured: {}\n"
          "Initializing filter (this can take a minute)...".format(
              len(CH_SEQUENCE)))
    for row_number, data_row in enumerate(filter_buffer):
        # Do the data acquisition of eight multiplexed input channels.
        # The ADS1256 read_sequence() method automatically fills into
        # the buffer specified as the second argument:
        ads2.read_sequence(CH_SEQUENCE, data_row)
        # Depending on aquisition speed and filter lenth, this can take long...
        sys.stdout.write(
            "\rProgress: {:3d}%".format(int(100*(row_number+1)/FILTER_SIZE)))
        sys.stdout.flush()


    # From now, update filter_buffer cyclically with new ADC samples and
    # calculate results with averaged results.
    print("\n\nOutput values averaged over {} ADC samples:".format(FILTER_SIZE))
    # The following is an endless loop!
    timestamp = time.time() # Limit output data rate to fixed time interval
    for data_row in itertools.cycle(filter_buffer):
        #
        # Do the data acquisition of eight multiplexed input channels
        #
        # The result channel values are directy read into the array specified
        # as the second argument, which must be a mutable type.
        ads2.read_sequence(CH_SEQUENCE, data_row)
    
        elapsed = time.time() - timestamp
        if elapsed > .1:
            timestamp += .1

            # Calculate moving average of input samples, subtract offset
            ch_unscaled = np.average(filter_buffer, axis=0) - CH_OFFSET
            ch_volts = ch_unscaled * CH_GAIN

        tim_nice_output([int(i) for i in ch_unscaled], ch_volts)
### END EXAMPLE ###


#############################################################################
# Format nice looking text output:
def nice_output(digits, volts):
    sys.stdout.write(
          "\0337" # Store cursor position
        +
"""These are the raw sample values for the channels:
Poti_CH0,  LDR_CH1,     AIN2,     AIN3,     AIN4,     AIN7, Poti NEG, Short 0V
"""
        + ", ".join(["{: 8d}".format(i) for i in digits])
        +
"""

These are the sample values converted to voltage in V for the channels:
Poti_CH0,  LDR_CH1,     AIN2,     AIN3,     AIN4,     AIN7, Poti NEG, Short 0V
"""
        + ", ".join(["{: 8.3f}".format(i) for i in volts])
        + "\n\033[J\0338" # Restore cursor position etc.
    )
    
def tim_nice_output(digits, volts):
    global first
    global res0
    global total_1
    res=float(64000*volts[0:1])
    if first:
        res0=res
    res=res-res0
    first=False
    sys.stdout.write(
          "\0337" # Store cursor position
        + "{: 8.4f}".format(res)
        + "\n\033[J\0338" # Restore cursor position etc.
    )
    total_1=res
    #write_csv(res)
    to_grafana(csv)
    
def write_csv(res):
    with open('data.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        #res=do_measurement()
        #print("res: ",res)
        global x_value
        info = {
            "x_value": x_value,
            "total_1": "{: 8.4f}".format(res),
            "name_input": name_input
        }

        csv_writer.writerow(info)
        print(x_value, "{: 8.4f}".format(total_1), name_input)
        #if x_value>100:
        #os.system('tail -100 data.csv > temp.csv')
        #    os.system('head -1 data.csv | cat - temp.csv > newfile.csv && rm -f temp.csv')
        #else:
        os.system('tail -100 data.csv > /dev/shm/shortfile.csv')
        x_value += 1
        #total_1 = total_1 + random.randint(-8, 8)
        #total_2 = total_2 + random.randint(-6, 6)

    time.sleep(.001) 
    master.update()

def to_grafana(res):
    try:
        os.system("curl -i -XPOST '172.23.92.63:8086/write?db=mydb&u=admin&p=PASSWORD' --data-binary 'weight,location=bees01 value="str(res))+"'")
    except:
        print("no access to grafana?")
        pass
    
x_value=0    
do_measurement()
