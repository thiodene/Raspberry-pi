import time
# http://tightdev.net/SpiDev_Doc.pdf
import spidev

class AD717X:
    # Enables/disables debug prints
    DEBUG_ENABLED = 0 
    # TODO: Find out correct delay
    TRANSFER_DELAY = 0.001

    REG = {
        # Other registers
        "ID": 0x07,
        "DATA": 0x04,
        "COMMS": 0x00,
        "IFMODE": 0x02,
        "STATUS": 0x00,
        "ADCMODE": 0x01,
        "GPIOCON": 0x06,
        "REGCHECK": 0x03,

        # Channel registers
        "CH0": 0x10,
        "CH1": 0x11,
        "CH2": 0x12,
        "CH3": 0x13,
        "CH4": 0x14,
        "CH5": 0x15,
        "CH6": 0x16,
        "CH7": 0x17,
        "CH8": 0x18,
        "CH9": 0x19,
        "CH10": 0x1A,
        "CH11": 0x1B,
        "CH12": 0x1C,
        "CH13": 0x1D,
        "CH14": 0x1E,
        "CH15": 0x1F,

        # Setup config register
        "SETUPCON0": 0x20,
        "SETUPCON1": 0x21,
        "SETUPCON2": 0x22,
        "SETUPCON3": 0x23,
        "SETUPCON4": 0x24,
        "SETUPCON5": 0x25,
        "SETUPCON6": 0x26,
        "SETUPCON7": 0x27,

        # Filter config registers
        "FILTCON0": 0x28,
        "FILTCON1": 0x29,
        "FILTCON2": 0x2A,
        "FILTCON3": 0x2B,
        "FILTCON4": 0x2C,
        "FILTCON5": 0x2D,
        "FILTCON6": 0x2E,
        "FILTCON7": 0x2F,

        # Offset registers
        "OFFSET0": 0x30,
        "OFFSET1": 0x31,
        "OFFSET2": 0x32,
        "OFFSET3": 0x33,
        "OFFSET4": 0x34,
        "OFFSET5": 0x35,
        "OFFSET6": 0x36,
        "OFFSET7": 0x37,

        # Gain registers
        "GAIN0": 0x38,
        "GAIN1": 0x39,
        "GAIN2": 0x3A,
        "GAIN3": 0x3B,
        "GAIN4": 0x3C,
        "GAIN5": 0x3D,
        "GAIN6": 0x3E,
        "GAIN7": 0x3F
    }

    INPUT = {
        # Analog inputs
        "AIN0": 0x00,
        "AIN1": 0x01,
        "AIN2": 0x02,
        "AIN3": 0x03,
        "AIN4": 0x04,
        "AIN5": 0x05,
        "AIN6": 0x06,
        "AIN7": 0x07,
        "AIN8": 0x08,
        "AIN9": 0x09,
        "AIN10": 0x0A,
        "AIN11": 0x0B,
        "AIN12": 0x0C,
        "AIN13": 0x0D,
        "AIN14": 0x0E,
        "AIN15": 0x0F,
        "AIN16": 0x10,

        # Other channel input registers
        "REF_POS": 0x15,
        "REF_NEG": 0x16,
        "TEMP_SENSOR_POS": 0x11,
        "TEMP_SENSOR_NEG": 0x12
    }

    SETUP_SEL = {
        "SETUP0": 0x00,
        "SETUP1": 0x01,
        "SETUP2": 0x02,
        "SETUP3": 0x03,
        "SETUP4": 0x04,
        "SETUP5": 0x05,
        "SETUP6": 0x06,
        "SETUP7": 0x07
    }

    # Filter speed values (samples per second)
    SPEED = {
        "5": 0x14,
        "10": 0x13,
        "16": 0x12,
        "20": 0x11,
        "50": 0x10,
        "60": 0x0F,
        "100": 0x0E,
        "200": 0x0D,
        "397": 0x0C,
        "500": 0x0B,
        "1000": 0x0A,
        "2500": 0x09,
        "5000": 0x08,
        "10000": 0x07,
        "15625": 0x06,
        "25000": 0x05,
        "31250": 0x04,
        "50000": 0x03,
        "62500": 0x02,
        "125000": 0x01,
        "250000": 0x00
    }

    # Setup coding modes
    CODING_MODE = {
        "BIPOLAR": 0x01,
        "UNIPOLAR": 0x00
    }

    # Clock mode
    CLOCK_MODE = {
        "INTERNAL": 0x00,
        "INTERNAL_OUTPUT": 0x01,
        "EXTERNAL_INPUT": 0x02,
        "EXTERNAL_CRYSTAL": 0x03
    }

    # Data conversion modes
    DATA_MODE = {
        "CONTINUOUS_READ": 0x02,
        "SINGLE_CONVERSION": 0x01,
        "CONTINUOUS_CONVERSION": 0x00
    }

    def init(self):
        self.spi = spidev.SpiDev() # create SPI object
        self.spi.open(0, 0) # open SPI port 0, device (CS) 0
        self.spi.mode = 3 # use SPI mode 3, sets Clock Polarity and Phase [CPOL|CPHA] configuration

        # TODO: Setup coding is different 4 each setup
        self.contread = False
        self.data_stat = False

        # resync the ADC
        self.resync()
        # read the ADC device ID */
        value = self.get_register(self.REG["ID"], 2);
        # check if the id matches 0x30DX or 0x3CDX, where X is don't care
        value[1] &= 0xF0

        device = None
        # AD7173
        if value[0] == 0x30 and value[1] == 0xD0:
            device = "AD7173"
        # AD7175
        elif value[0] == 0x3C and value[1] == 0xD0:
            device = "AD7175"

        # when ID is valid
        if device:
            self.debug("init: device ID %s :)" % device)
        else:
            self.debug("init: device ID unrecognized :( %s" % value)

        # return the detected device name
        return device

    def debug(self, message):
        if self.DEBUG_ENABLED:
            print(message)

    # returns ADC to default state
    def reset(self):
        # sending at least 64 high bits
        self.spi.xfer2([0xFF] * 8)

    # resyncs the ADC communication
    def resync(self):
        # toggle the chip select
        self.spi.cshigh = True
        time.sleep(self.TRANSFER_DELAY)
        self.spi.cshigh = False

    # reads a register from the ADC
    def set_register(self, reg, value):
        # check if valid register
        assert reg >= 0x00 and reg <= 0x3F, "set_register: reg out of range %x" % reg

        # send communication register id 0x00
        # send desired register 0x00 - 0xFF
        # write the desired value
        self.spi.xfer2([0x00, (0x00 | reg)] + value)

        self.debug("write_register: wrote %s to reg %s" % (list(map(hex, value)) , hex(reg)))
        time.sleep(self.TRANSFER_DELAY)

    def get_register(self, reg, read_len):
        # check if valid register
        assert reg >= 0x00 and reg <= 0x3F, "get_register: reg out of range %x" % reg

        # register value
        value = []
        # send communication register id 0x00
        # send desired register 0x00 - 0xFF
        # read the desired value
        value = self.spi.xfer2([0x00, (0x40 | reg)] + ([0x00] * read_len))
        # ignore first 2 bytes
        value = value[2:]

        self.debug("read_register: read %s from reg %s" % (list(map(hex, value)), hex(reg)))
        time.sleep(self.TRANSFER_DELAY)
        # return the register value
        return value

    def set_adc_mode_config(self, mode, clocksel):
        # Address: 0x01, Reset: 0x2000, Name: ADCMODE

        # prepare the configuration value
        # AD7175: HIDE_DELAY [14]
        # REF_EN [15], RESERVED [14], SING_CYC [13], RESERVED [12:11],
        # DELAY [10:8], RESERVED [7], MODE [6:4], CLOCKSEL [3:2], RESERED [1:0]
        value = [0x00, 0x00]
        value[0] = 0x80
        value[1] = (mode << 4) | (clocksel << 2)

        # update the configuration value
        self.set_register(self.REG["ADCMODE"], value)

        # verify the updated configuration value
        new_value = self.get_register(self.REG["ADCMODE"], 2)
        assert new_value == value, "set_adc_mode_config: value mismatch %s != %s" % (value, new_value)

    def set_interface_mode_config(self, contread, data_stat):
        # Address: 0x02, Reset: 0x0000, Name: IFMODE

        # prepare the configuration value
        # AD7175: RESERVED [10]
        # RESERVED [15:13], ALT_SYNC [12], IOSTRENGTH [11], HIDE_DELAY [10],
        # RESERVED [9], DOUT_RESET [8], CONTREAD [7], DATA_STAT [6],
        # REG_CHECK [5], RESERVED [4], CRC_EN [3:2], RESERVED [1], WL16 [0]
        value = [0x00, 0x00]
        value[1] = (contread << 7) | (data_stat << 6)

        # update the configuration value
        self.set_register(self.REG["IFMODE"], value)

        # verify the updated configuration value
        new_value = self.get_register(self.REG["IFMODE"], 2)
        assert new_value == value, "set_interface_mode_config: value mismatch %s != %s" % (value, new_value)

        # With continuous read mode we can only read the data register
        self.contread = contread
        # If the status register should be appended to the data register
        self.data_stat = data_stat

    def set_channel_config(self, ch_reg, ch_en, setup_sel, ainpos, ainneg):
        # Address: 0x10, Reset: 0x8001, Name: CH0
        # Address Range: 0x11 to 0x1F, Reset: 0x0001, Name: CH1 to CH15

        # prepare the configuration value
        # CH_EN0 [15], SETUP_SEL0 [14:12], RESERVED [11:10], AINPOS0 [9:5], AINNEG0 [4:0]
        value = [0x00, 0x00]
        value[0] = (ch_en << 7) | (setup_sel << 4) | (ainpos >> 3)
        value[1] = ((ainpos << 5) & 0xFF) | ainneg

        #print "setup channel"
        #print value
        # update the configuration value
        self.set_register(ch_reg, value)

        # verify the updated configuration value
        new_value = self.get_register(ch_reg, 2)
        assert new_value == value, "set_channel_config: value mismatch %s != %s" % (value, new_value)

    def set_setup_config(self, setupcon_reg, bi_unipolar):
        # Address Range: 0x20 to 0x27, Reset: 0x1000, Name: SETUPCON0 to SETUPCON7

        # prepare the configuration value
        # AD7175: REFBUF0+ [11], REFBUF0- [10], AINBUF0+ [9], AINBUF0- [8], RESERVED [6]
        # RESERVED [15:13], BI_UNIPOLAR0 [12], REF_BUF_0[1:0] [11:10], AIN_BUF_0[1:0] [9:8]
        # BURNOUT_EN0 [7], BUFCHOPMAX0 [6], REF_SEL0 [5:4], RESERVED [3:0]
        value = [0x00, 0x00]
        value[0] = (bi_unipolar << 4)
        value[1] = 0x00

        #print "setup register" 
        #print value 
        # update the configuration value
        self.set_register(setupcon_reg, value)

        # verify the updated configuration value
        new_value = self.get_register(setupcon_reg, 2)
        assert new_value == value, "set_setup_config: value mismatch %s != %s" % (value, new_value)

    def set_filter_config(self, filter_reg, ord):
        # Address Range: 0x28 to 0x2F, Reset: 0x0000, Name: FILTCON0 to FILTCON7

        # prepare the configuration value
        # SINC3_MAP0 [15], RESERVED [14:12], ENHFILTEN0 [11],
        # ENHFILT0 [10:8], RESERVED [7], ORDER0 [6:5], ORD0 [4:0]
        value = [0x00, 0x00]
        value[1] = ord

        # update the configuration value
        self.set_register(filter_reg, value)

        # verify the updated configuration value
        new_value = self.get_register(filter_reg, 2)
        assert new_value == value, "set_filter_config: value mismatch %s != %s" % (value, new_value)

    def set_offset_config(self, offset_reg, offset):
        # Address Range: 0x30 to 0x37, Reset: 0x800000, Name: OFFSET0 to OFFSET7

        # add the default offset value
        offset += 8388608

        # prepare the configuration value
        # OFFSET [23:0]
        value = [0x00, 0x00, 0x00]
        value[0] = (offset >> 16) & 0xFF
        value[1] = (offset >> 8) & 0xFF
        value[2] = (offset) & 0xFF

        # update the configuration value
        self.set_register(offset_reg, value)

        # verify the updated configuration value
        new_value = self.get_register(offset_reg, 3)
        assert new_value == value, "set_offset_config: value mismatch %s != %s" % (value, new_value)

    def get_data(self):
        # when not in continuous read mode, send the read command
        if self.contread:
            # get the ADC conversion result (24 bits)
            value = self.spi.xfer2([0x00] * 3)
        else:
            # send communication register id 0x00
            # send read command 0x40 to the data register 0x04
            # get the ADC conversion result (24 bits)
            value = self.spi.xfer2([0x00, (0x40 | self.REG["DATA"]), 0x00, 0x00, 0x00, 0x00])
            # ignore first 2 bytes
            value = value[2:]

        # Add together as an integer
        data = (value[0] << 16 | value[1] << 8 | value[2])

        ready = None
        channel = None
        if self.data_stat:
            ready = not (value[3] & 0x80)
            channel = value[3] & 0x0F

        self.debug("get_data: read %s from reg 0x04" % list(map(hex, value)))
        # return the conversion result
        return data, channel, ready

    def get_status(self):
        # read ADC status register
        value = self.get_register(self.REG["STATUS"], 1)
        # return channel register value
        return (value[0] & 0x0F, not (value[0] & 0x80))
