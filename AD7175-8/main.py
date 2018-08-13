import time
from AD717X import AD717X

adc = AD717X()
adc.init()
adc.reset()
for i in range(16):
    adc.set_channel_config(0x10 + i, True, AD717X.SETUP_SEL["SETUP0"], i, 0)
#adc.set_channel_config(AD717X.REG["CH0"], True, AD717X.SETUP_SEL["SETUP0"], AD717X.INPUT["AIN5"], AD717X.INPUT["AIN0"])
adc.set_setup_config(AD717X.REG["SETUPCON0"], AD717X.CODING_MODE["UNIPOLAR"])
adc.set_offset_config(AD717X.REG["OFFSET0"], 0)
adc.set_filter_config(AD717X.REG["FILTCON0"], AD717X.SPEED["1000"])
adc.set_adc_mode_config(AD717X.DATA_MODE["CONTINUOUS_CONVERSION"], AD717X.CLOCK_MODE["INTERNAL"])
adc.set_interface_mode_config(False, True)
time.sleep(0.01)

count = 0
data = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
while count < 100:
    value, channel, ready = adc.get_data()
    if ready:
        data[channel].append(value)
        count += 1
for i in range(16):
    print("AIN%i: %s" % (i, data[i]))

#while True:
#    print(adc.get_data())
#    time.sleep(1)
