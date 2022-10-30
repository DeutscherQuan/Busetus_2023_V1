#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time
import smbus
from PIL import Image,ImageDraw,ImageFont
#from past.builtins import xrange

I2C_addr = 0x3c

class device(object):
    """
    Base class for OLED driver classes
    """
    def __init__(self, port=1, address=I2C_addr, cmd_mode=0x00, data_mode=0x40):
        self.cmd_mode = cmd_mode
        self.data_mode = data_mode
        self.bus = smbus.SMBus(1)
        self.addr = address

    def command(self, *cmd):
        """
        Sends a command or sequence of commands through to the
        device - maximum allowed is 32 bytes in one go.
        """
        assert(len(cmd) <= 32)
        self.bus.write_i2c_block_data(self.addr, self.cmd_mode, list(cmd))

    def data(self, data):
        """
        Sends a data byte or sequence of data bytes through to the
        device - maximum allowed in one transaction is 32 bytes, so if
        data is larger than this it is sent in chunks.
        """
        for i in range(0, len(data), 32):
            self.bus.write_i2c_block_data(self.addr,
                                          self.data_mode,
                                          list(data[i:i+32]))

class SH1106(device):
    """class for SH1106  240*240 1.3inch OLED displays."""

    def __init__(self,rst = 24, port=1, address=I2C_addr):
        super(SH1106, self).__init__(port, address)
        self.width = 128
        self.height = 64
        self.pages = self.height / 8
        
        #Initialize RST pin
        self._rst = rst
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self._rst, GPIO.OUT)

        self.i2c = smbus.SMBus(1)
        self.address = I2C_addr
        
        GPIO.output(self._rst, GPIO.HIGH)
        time.sleep(0.01)
        GPIO.output(self._rst, GPIO.LOW)
        time.sleep(0.01)
        GPIO.output(self._rst, GPIO.HIGH)
        time.sleep(0.01)
        
        self.command(
            const.DISPLAYOFF,
            const.MEMORYMODE,
            const.SETHIGHCOLUMN,      0xB0, 0xC8,
            const.SETLOWCOLUMN,       0x10, 0x40,
            const.SETCONTRAST,        0x7F,
            const.SETSEGMENTREMAP,
            const.NORMALDISPLAY,
            const.SETMULTIPLEX,       0x3F,
            const.DISPLAYALLON_RESUME,
            const.SETDISPLAYOFFSET,   0x00,
            const.SETDISPLAYCLOCKDIV, 0xF0,
            const.SETPRECHARGE,       0x22,
            const.SETCOMPINS,         0x12,
            const.SETVCOMDETECT,      0x20,
            const.CHARGEPUMP,         0x14,
            )

    def display(self, image):
        """
        Takes a 1-bit image and dumps it to the SH1106 OLED display.
        """
        
        
        assert(image.mode == '1')
        assert(image.size[0] == self.width)
        assert(image.size[1] == self.height)

        page = 0xB0
        pix = list(image.getdata())
        step = self.width * 8
        for y in range(0, self.pages * step, step):

            # move to given page, then reset the column address
            self.command(page, 0x02, 0x10)
            page += 1

            buf = []
            for x in range(self.width):
                byte = 0
                for n in range(0, step, self.width):
                    byte |= (pix[x + y + n] & 0x01) << 8
                    byte >>= 1

                buf.append(byte)

            self.data(buf)
        self.command(const.DISPLAYON)
		
class const:
    CHARGEPUMP = 0x8D
    COLUMNADDR = 0x21
    COMSCANDEC = 0xC8
    COMSCANINC = 0xC0
    DISPLAYALLON = 0xA5
    DISPLAYALLON_RESUME = 0xA4
    DISPLAYOFF = 0xAE
    DISPLAYON = 0xAF
    EXTERNALVCC = 0x1
    INVERTDISPLAY = 0xA7
    MEMORYMODE = 0x20
    NORMALDISPLAY = 0xA6
    PAGEADDR = 0x22
    SEGREMAP = 0xA0
    SETCOMPINS = 0xDA
    SETCONTRAST = 0x81
    SETDISPLAYCLOCKDIV = 0xD5
    SETDISPLAYOFFSET = 0xD3
    SETHIGHCOLUMN = 0x10
    SETLOWCOLUMN = 0x00
    SETMULTIPLEX = 0xA8
    SETPRECHARGE = 0xD9
    SETSEGMENTREMAP = 0xA1
    SETSTARTLINE = 0x40
    SETVCOMDETECT = 0xDB
    SWITCHCAPVCC = 0x2
	
	
if __name__ == '__main__':
	oled = SH1106()
	try:
		image1 = Image.new('1', (oled.width, oled.height), "BLACK")
		draw = ImageDraw.Draw(image1)

		draw.line([(0,0),(127,0)], fill = 1)
		draw.line([(0,0),(0,63)], fill = 1)
		draw.line([(0,63),(127,63)], fill = 1)
		draw.line([(127,0),(127,63)], fill = 1)

		font = ImageFont.truetype('Font.ttc', 20)
		font10 = ImageFont.truetype('Font.ttc',13)
		draw.text((30,0), 'Waveshare ', font = font10, fill = 1)
		draw.text((28,20), u'微雪电子 ', font = font, fill = 1)

		oled.display(image1)
	except KeyboardInterrupt:
		image2 = Image.new('1', (oled.width, oled.height), "BLACK")
		oled.display(image2)
		exit()	


