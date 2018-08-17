import time
from AD7175 import AD7175

adc = AD7175()
adc.init()
adc.reset()
for i in range(16):
    adc.set_channel_config(0x10 + i, True, AD7175.SETUP_SEL["SETUP0"], i, 22)
#adc.set_channel_config(AD7175.REG["CH0"], True, AD7175.SETUP_SEL["SETUP0"], AD7175.INPUT["AIN5"], AD7175.INPUT["AIN0"])
adc.set_setup_config(AD7175.REG["SETUPCON0"], AD7175.CODING_MODE["UNIPOLAR"])

#adc.set_setup_config(AD7175.REG["SEL_REF0"], AD7175.CODING_MODE["EXTREF"])

adc.set_offset_config(AD7175.REG["OFFSET0"], 0)
adc.set_filter_config(AD7175.REG["FILTCON0"], AD7175.SPEED["1000"])
adc.set_adc_mode_config(AD7175.DATA_MODE["CONTINUOUS_CONVERSION"], AD7175.CLOCK_MODE["INTERNAL"])
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
