import time
from AD717X import AD717X

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
adc.set_filter_config(AD717X.REG["FILTCON0"], AD717X.SPEED["1000"])
adc.set_adc_mode_config(AD717X.DATA_MODE["CONTINUOUS_CONVERSION"], AD717X.CLOCK_MODE["INTERNAL"])
adc.set_interface_mode_config(False, True)
time.sleep(0.01)

# Write data array for 20 channels in total: 16 for AD7175-8 and 4 for ADS1015
data = [None]*20
ndata = 0
while ndata < 16:
    value, channel, ready = adc.get_data()
    #print("channel:" + str(channel) + " value:" + str(value))
    #time.sleep(0.1)
    if data[channel] is None:
        data[channel] = value
        # data.append(value)
        ndata+= 1

for i in range(4):
    # Read the AD7175-8
    data.append(ads.read_adc(i, gain=GAIN, data_rate=1600))


for i in range(20):
    print("AIN%i: %s" % (i, data[i]))

