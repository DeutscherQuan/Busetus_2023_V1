#!/usr/bin/python
# -*- coding:UTF-8 -*-
import smbus
import time

# COMMANDS 
PARAM_QUERY    = 0x80
PARAM_SET      = 0xA0
NOP            = 0x0
RESET          = 0x01
BUSADDR        = 0x02
PS_FORCE       = 0x05
ALS_FORCE      = 0x06
PSALS_FORCE    = 0x07
PS_PAUSE       = 0x09
ALS_PAUSE      = 0x0A
PSALS_PAUSE    = 0xB
PS_AUTO        = 0x0D
ALS_AUTO       = 0x0E
PSALS_AUTO     = 0x0F
GET_CAL        = 0x12

# Parameters 
PARAM_I2CADDR          = 0x00
PARAM_CHLIST           = 0x01
PARAM_CHLIST_ENUV      = 0x80
PARAM_CHLIST_ENAUX     = 0x40
PARAM_CHLIST_ENALSIR   = 0x20
PARAM_CHLIST_ENALSVIS  = 0x10
PARAM_CHLIST_ENPS1     = 0x01
PARAM_CHLIST_ENPS2     = 0x02
PARAM_CHLIST_ENPS3     = 0x04

PARAM_PSLED12SEL           = 0x02
PARAM_PSLED12SEL_PS2NONE   = 0x00
PARAM_PSLED12SEL_PS2LED1   = 0x10
PARAM_PSLED12SEL_PS2LED2   = 0x20
PARAM_PSLED12SEL_PS2LED3   = 0x40
PARAM_PSLED12SEL_PS1NONE   = 0x00
PARAM_PSLED12SEL_PS1LED1   = 0x01
PARAM_PSLED12SEL_PS1LED2   = 0x02
PARAM_PSLED12SEL_PS1LED3   = 0x04

PARAM_PSLED3SEL    = 0x03
PARAM_PSENCODE     = 0x05
PARAM_ALSENCODE    = 0x06

PARAM_PS1ADCMUX        = 0x07
PARAM_PS2ADCMUX        = 0x08
PARAM_PS3ADCMUX        = 0x09
PARAM_PSADCOUNTER      = 0x0A
PARAM_PSADCGAIN        = 0x0B
PARAM_PSADCMISC        = 0x0C
PARAM_PSADCMISC_RANGE  = 0x20
PARAM_PSADCMISC_PSMODE = 0x04

PARAM_ALSIRADCMUX  = 0x0E
PARAM_AUXADCMUX    = 0x0F

PARAM_ALSVISADCOUNTER          = 0x10
PARAM_ALSVISADCGAIN            = 0x11
PARAM_ALSVISADCMISC            = 0x12
PARAM_ALSVISADCMISC_VISRANGE   = 0x20

PARAM_ALSIRADCOUNTER       = 0x1D
PARAM_ALSIRADCGAIN         = 0x1E
PARAM_ALSIRADCMISC         = 0x1F
PARAM_ALSIRADCMISC_RANGE   = 0x20

PARAM_ADCCOUNTER_511CLK    = 0x70

PARAM_ADCMUX_SMALLIR       = 0x00
PARAM_ADCMUX_LARGEIR       = 0x03

# REGISTERS
REG_PARTID = 0x00
REG_REVID  = 0x01
REG_SEQID  = 0x02

REG_INTCFG         = 0x03
REG_INTCFG_INTOE   = 0x01
REG_INTCFG_INTMODE = 0x02

REG_IRQEN  = 0x04
REG_IRQEN_ALSEVERYSAMPLE   = 0x01
REG_IRQEN_PS1EVERYSAMPLE   = 0x04
REG_IRQEN_PS2EVERYSAMPLE   = 0x08
REG_IRQEN_PS3EVERYSAMPLE   = 0x10


REG_IRQMODE1   = 0x05
REG_IRQMODE2   = 0x06

REG_HWKEY      = 0x07
REG_MEASRATE0  = 0x08
REG_MEASRATE1  = 0x09
REG_PSRATE     = 0x0A
REG_PSLED21    = 0x0F
REG_PSLED3     = 0x10
REG_UCOEFF0    = 0x13
REG_UCOEFF1    = 0x14
REG_UCOEFF2    = 0x15
REG_UCOEFF3    = 0x16
REG_PARAMWR    = 0x17
REG_COMMAND    = 0x18
REG_RESPONSE   = 0x20
REG_IRQSTAT    = 0x21
REG_IRQSTAT_ALS= 0x01

REG_ALSVISDATA0= 0x22
REG_ALSVISDATA1= 0x23
REG_ALSIRDATA0 = 0x24
REG_ALSIRDATA1 = 0x25
REG_PS1DATA0   = 0x26
REG_PS1DATA1   = 0x27
REG_PS2DATA0   = 0x28
REG_PS2DATA1   = 0x29
REG_PS3DATA0   = 0x2A
REG_PS3DATA1   = 0x2B
REG_UVINDEX0   = 0x2C
REG_UVINDEX1   = 0x2D
REG_PARAMRD    = 0x2E
REG_CHIPSTAT   = 0x30

I2C_ADDRESS    = 0x60

class SI1145:
	def __init__(self, address = I2C_ADDRESS):
		self.i2c = smbus.SMBus(1)
		self.address = address

		id = self.read8(REG_PARTID)
		if(id != 0x45):
			print ("Si1145 ID error ! Now you read is: ", id)
			while(1):
				time.sleep(1)

		#Reset
		self.write8(REG_MEASRATE0, 0)
		self.write8(REG_MEASRATE1, 0)
		self.write8(REG_IRQEN, 0)
		self.write8(REG_IRQMODE1, 0)
		self.write8(REG_IRQMODE2, 0)
		self.write8(REG_INTCFG, 0)
		self.write8(REG_IRQSTAT, 0xFF)

		self.write8(REG_COMMAND, RESET)
		time.sleep(0.01)
		self.write8(REG_HWKEY, 0x17)
		time.sleep(0.01)
		
		#***********************************
		# enable UVindex measurement coefficients!
		self.write8(REG_UCOEFF0, 0x29)
		self.write8(REG_UCOEFF1, 0x89)
		self.write8(REG_UCOEFF2, 0x02)
		self.write8(REG_UCOEFF3, 0x00)

		# enable UV sensor
		self.writeParam(PARAM_CHLIST, PARAM_CHLIST_ENUV |\
		PARAM_CHLIST_ENALSIR | PARAM_CHLIST_ENALSVIS |\
		PARAM_CHLIST_ENPS1)
		# enable interrupt on every sample
		self.write8(REG_INTCFG, REG_INTCFG_INTOE)
		self.write8(REG_IRQEN, REG_IRQEN_ALSEVERYSAMPLE)

		# program LED current
		self.write8(REG_PSLED21, 0x03)  # 20mA for LED 1 only
		self.writeParam(PARAM_PS1ADCMUX, PARAM_ADCMUX_LARGEIR)
		# prox sensor #1 uses LED #1
		self.writeParam(PARAM_PSLED12SEL, PARAM_PSLED12SEL_PS1LED1)
		# fastest clocks, clock div 1
		self.writeParam(PARAM_PSADCGAIN, 0)
		# take 511 clocks to measure
		self.writeParam(PARAM_PSADCOUNTER, PARAM_ADCCOUNTER_511CLK)
		# in prox mode, high range
		self.writeParam(PARAM_PSADCMISC, PARAM_PSADCMISC_RANGE|PARAM_PSADCMISC_PSMODE)

		self.writeParam(PARAM_ALSIRADCMUX, PARAM_ADCMUX_SMALLIR)
		
		# fastest clocks, clock div 1
		self.writeParam(PARAM_ALSIRADCGAIN, 0)
		# take 511 clocks to measure
		self.writeParam(PARAM_ALSIRADCOUNTER, PARAM_ADCCOUNTER_511CLK)
		# in high range mode
		self.writeParam(PARAM_ALSIRADCMISC, PARAM_ALSIRADCMISC_RANGE)
		# fastest clocks, clock div 1
		self.writeParam(PARAM_ALSVISADCGAIN, 0)
		# take 511 clocks to measure
		self.writeParam(PARAM_ALSVISADCOUNTER, PARAM_ADCCOUNTER_511CLK)
		# in high range mode (not normal signal)
		self.writeParam(PARAM_ALSVISADCMISC, PARAM_ALSVISADCMISC_VISRANGE)
		# measurement rate for auto
		self.write8(REG_MEASRATE0, 0xFF) # 255 * 31.25uS = 8ms

		# auto run
		self.write8(REG_COMMAND, PSALS_AUTO)
		# print "Si145 Init success !"

	def writeParam(self, p, v):
		self.write8(REG_PARAMWR, v)
		self.write8(REG_COMMAND, p | PARAM_SET)
		return self.read8(REG_PARAMRD)

	def read8(self, addr):
		return self.i2c.read_byte_data(self.address, addr)

	def read16(self, addr):
		return self.i2c.read_word_data(self.address, addr)

	def write8(self, addr, val):
		self.i2c.write_byte_data(self.address, addr, val)

	def close(self):
		self.i2c.close()

	def readdata(self):# UV IR VIS
		UV = self.read16(0x2C) / 100.0
		IR = self.read16(0x24)
		VIS = self.read16(0x22)
		# print("UV: %d" %(UV))
		# print("IR: %d" %IR)
		# print("Vis: %d" %VIS)
		return [UV, IR, VIS]

if __name__ == '__main__':
	try:
		sensor = SI1145()
		while True:
			print("===================")
			print("UV: %.2f" %(sensor.readdata()[0]))
			print("IR: %d" %sensor.readdata()[1])
			# print("Vis: %d" %sensor.readdata[2])
			time.sleep(1)
	except KeyboardInterrupt:
		sensor.close()
		pass
