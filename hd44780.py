#! /usr/bin/python

# A Python library to interact with a HD44780 display via a MCP23017 I2C IO Expander.
# Thanks goes to Nathan Chantrell http://nathan.chantrell.net.
# GNU GPL v3

import smbus
import sys
import getopt
from time import sleep
import os

a = [(0x12, 0), (0x12, 1), (0x12, 2), (0x12, 3), (0x12, 4), (0x12, 5), (0x12, 6), (0x12, 7)]
b = [(0x13, 0), (0x13, 1), (0x13, 2), (0x13, 3), (0x13, 4), (0x13, 5), (0x13, 6), (0x13, 7)]

class LCD:
    def __init__(self,bus_id=1,address=0x20,data_pins=[b[4], b[5], b[6], b[7]],en=b[1],backlight=b[3],rs=b[0]):
        self.bus = smbus.SMBus(bus_id)

        self.address = address
        #self.bus.write_byte_data(self.address,0x00,0x00) # Set all of bank A to outputs
        self.bus.write_byte_data(self.address,0x01,0x00) # Set all of bank B to outputs

        self.data_pins = data_pins

        #self.bus.write_byte_data(self.address, 0x12, 0)
        self.bus.write_byte_data(self.address, 0x13, 0)
        sleep(0.020)


        #self.vcc = vcc
        self.en = en
        self.backlight = backlight
        self.rs = rs
        #self.high(self.vcc)
        self.high(self.backlight)
        sleep(0.020)

        self.write8bits(0x30, high_only=True)
        sleep(0.020)
        self.write8bits(0x30, high_only=True)
        sleep(0.020)
        self.write8bits(0x30, high_only=True)
        sleep(0.020)
        self.write8bits(0x20, high_only=True)
        self.write8bits(0x2b)
        self.write8bits(0x08)
        self.write8bits(0x01)
        self.write8bits(0x0c)
        self.write8bits(0x06)

    def newline(self):
        self.write8bits(0xC0)

    def high(self, (register, pin)):
        value = self.bus.read_byte_data(self.address, register)
        value |= (1 << pin)
        self.bus.write_byte_data(self.address, register, value)

    def low(self, (register, pin)):
        value = self.bus.read_byte_data(self.address, register)
        value &= ~(1 << pin)
        self.bus.write_byte_data(self.address, register, value)

    def pulse(self):
        self.low(self.en)
        sleep(0.000001)
        self.high(self.en)
        sleep(0.000001)
        self.low(self.en)
        sleep(0.000001)

    def pulseled(self):
        for i in range(0,2):
            self.low(self.backlight)
            sleep(0.3)
            self.high(self.backlight)
            sleep(0.3)

    def write8bits(self, bits, char_mode=False,high_only=False):
        sleep(0.001)
        if (char_mode):
            self.high(self.rs)
        else:
            self.low(self.rs)

        for pin in self.data_pins:
            self.low(pin)

        for i in range(8 - len(self.data_pins),8):
            if (bits & (1 << i)) == 1 << i:
                self.high(self.data_pins[i - (8 - len(self.data_pins))])

        if len(self.data_pins) == 4 and not high_only:
            self.pulse()
            for pin in self.data_pins:
                self.low(pin)

            for i in range(0, 4):
                if (bits & (1 << i)) == 1 << i:
                    self.high(self.data_pins[i])

        self.pulse()
        self.low(self.rs)

    def write(self, string):
        for c in string:
            self.write8bits(ord(c), True)

    def clear(self):
        self.write8bits(0x01)

    def home(self):
        self.write8bits(0x02)

    def set_display_cursor_blink(self, d, c, b):
        code = 0x08
        if d:
            code |= 0x04
        if c:
            code |= 0x02
        if b:
            code |= 0x01
        self.write8bits(code)

lcd = LCD()
lcd.pulseled()
#lcd.write("ciao")
lcd.write(sys.argv[1])
lcd.newline()
lcd.write(sys.argv[2])
#sleep(2)
#lcd.clear()
