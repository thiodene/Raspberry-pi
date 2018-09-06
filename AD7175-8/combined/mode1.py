# This script is used to format the 20 Channels and save the Data from ADS1015 and AD7175-8 on a csv file

import time
from AD717X import AD717X
import os
import errno

# Import config variables
from configs.config import config_absolute_time, config_relative_time, config_exhale_time, config_current_id

#Import the ADS1x15 module.
import Adafruit_ADS1x15

# Create an ADS1015 ADC (12-bit) Instance.
ads = Adafruit_ADS1x15.ADS1015()
GAIN = 1

# Initialize the Analog Devices AD7175-8
adc = AD717X()
adc.init()
adc.reset()
for i in range(16):
    adc.set_channel_config(0x10 + i, True, AD717X.SETUP_SEL["SETUP0"], i, 22)
adc.set_setup_config(AD717X.REG["SETUPCON0"], AD717X.CODING_MODE["UNIPOLAR"])

adc.set_offset_config(AD717X.REG["OFFSET0"], 0)
adc.set_filter_config(AD717X.REG["FILTCON0"], AD717X.SPEED["25000"])
adc.set_adc_mode_config(AD717X.DATA_MODE["CONTINUOUS_CONVERSION"], AD717X.CLOCK_MODE["INTERNAL"])
adc.set_interface_mode_config(False, True)
time.sleep(0.01)

# Reading AD7175-8 values message
print('Reading AD7175-8 values, press Ctrl-C to quit...')

# Open the file to save the data as csv
path = '../result_documents/life/' 
mode = 1
current_time = int(time.time())
download_dir = path + str(id) + '-' + str(current_time) + '-' + str(mode) + ".csv"

try:
  os.remove(download_dir)
except OSError:
  pass

csv = open(download_dir, "w")

# Mode 1
mode = 1

# keep polling CH0 and CH1 values
start = time.time()
while (time.time() - start) <= 30.0:


    # Write data array for 20 channels in total: 16 for AD7175-8 and 4 for ADS1015
    data = [None] * 20
    ndata = 0
    row = ''
    current_milli_time = int(time.time() * 1000)
    while ndata < 16:
        value, channel, ready = adc.get_data()
        #print("channel:" + str(channel) + " value:" + str(value)) 
        #time.sleep(0.1)
        if data[channel] is None:
            data[channel] = value
            ndata+= 1

    row += '{:15}'.format(current_milli_time)
    row += ',{:2}'.format(1) 
    row += ',{:3}'.format("C01")
    row += ',{:5}'.format(data[0])
    row += ',{:3}'.format("C02")
    row += ',{:5}'.format(data[1])
    row += ',{:3}'.format("C03")
    row += ',{:5}'.format(data[2])
    row += ',{:3}'.format("C04")
    row += ',{:5}'.format(data[3])
    row += ',{:3}'.format("C05")
    row += ',{:5}'.format(data[4])
    row += ',{:3}'.format("C06")
    row += ',{:5}'.format(data[5])
    row += ',{:3}'.format("C07")
    row += ',{:5}'.format(data[6])
    row += ',{:3}'.format("C08")
    row += ',{:5}'.format(data[7])
    row += ',{:3}'.format("C09")
    row += ',{:5}'.format(data[8])
    row += ',{:3}'.format("C10")
    row += ',{:5}'.format(data[9])
    row += ',{:3}'.format("C11")
    row += ',{:5}'.format(data[10])
    row += ',{:3}'.format("C12")
    row += ',{:5}'.format(data[11])
    row += ',{:3}'.format("C13")
    row += ',{:5}'.format(data[12])
    row += ',{:3}'.format("C14")
    row += ',{:5}'.format(data[13])
    row += ',{:3}'.format("C15")
    row += ',{:5}'.format(data[14])
    row += ',{:3}'.format("C16")
    row += ',{:5}'.format(data[15])

    for i in range(4):
        # Read the AD7175-8
        data.append(ads.read_adc(i, gain=GAIN, data_rate=1600))
        nchan = 17 + i
        row += ',{:3}'.format("C" + str(nchan))
        row += ',{:5}'.format(ads.read_adc(i, gain=GAIN, data_rate=1600))
        if i == 3:
            row += " \n"
            csv.write(row)

csv.close()
