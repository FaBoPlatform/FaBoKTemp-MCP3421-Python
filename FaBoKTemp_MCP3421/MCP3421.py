# coding: utf-8
## @package FaBoKTemp_MCP3421
#  This is a library for the FaBo KTemp I2C Brick.
#
#  http://fabo.io/209.html
#
#  Released under APACHE LICENSE, VERSION 2.0
#
#  http://www.apache.org/licenses/
#
#  FaBo <info@fabo.io>

import smbus
import time

## MCP3421 Slave Address
SLAVE_ADDRESS = [0x68, 0x69, 0x6a, 0x6b, 0x6c, 0x6d, 0x6e, 0x6f]

# Config Parameter
CONFIG_RDY_ON          = 0b10000000
CONFIG_RDY_OFF         = 0b00000000

CONFIG_CONV_ONE_SHOT   = 0b00000000
CONFIG_CONV_CONTINUOUS = 0b00010000

CONFIG_RATE_240SPS     = 0b00000000
CONFIG_RATE_60SPS      = 0b00000100
CONFIG_RATE_15SPS      = 0b00001000
CONFIG_RATE_3_75SPS    = 0b00001100

CONFIG_GAIN_X1         = 0b00000000
CONFIG_GAIN_X2         = 0b00000001
CONFIG_GAIN_X4         = 0b00000010
CONFIG_GAIN_X8         = 0b00000011

## smbus
bus = smbus.SMBus(1)

## FaBo KTemp I2C Controll class
class MCP3421:

    config = 0x00

    ## Constructor
    #  @param [in] address MCP3421 I2C slave address default:0x68
    def __init__(self, address=SLAVE_ADDRESS[0]):
#        self.address = self.deviceSerch()
        self.address = address
        self.configuration()

    ## Device serch
    #  Looking for the MCP3421 device
    #  if it is not found and the process ends
    #  @return Slave Address
    def deviceSerch(self):
        for addr in SLAVE_ADDRESS:
            try:
                test = bus.read_byte_data(addr, 0x00)
                print "Device Addres:",  hex(addr)
                print
                return addr

            except:
                pass

        print "MCP3421 Not Found!!"
        exit()

    ## Configure Device
    def configuration(self):
        self.config = CONFIG_RDY_ON | CONFIG_CONV_CONTINUOUS | CONFIG_RATE_3_75SPS | CONFIG_GAIN_X8
        bus.write_byte_data(self.address, 0x00, self.config)

    ## Read Temperature Data
    #  @param [out] value Temperature Data
    def read(self, cp=500):
        mvuv = 1 << (3+2*3)

        data = bus.read_i2c_block_data(self.address, self.config, 4)

        temp = (data[0] << 16) + (data[1] << 8) + data[2]

        if data[0] & (0x80):
            temp -= (1<<24)

        temp = (temp *(1000/mvuv) + cp) / 40.7

        return temp

if __name__ == "__main__":
    mcp3421 = MCP3421()

    while True:
        temp = mcp3421.read()
        print "KTemp = ", temp
        print
        time.sleep(1)
