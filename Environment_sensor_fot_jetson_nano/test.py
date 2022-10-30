#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import SH1106 #OLED
import ICM20948 #Gyroscope/Acceleration/Magnetometer
import BME280   #Atmospheric Pressure/Temperature and humidity
import SI1145   #UV
import TSL2591  #LIGHT
import SGP40
from PIL import Image,ImageDraw,ImageFont
import math


bme280 = BME280.BME280()
bme280.get_calib_param()
light = TSL2591.TSL2591()
si1145 = SI1145.SI1145()
sgp = SGP40.SGP40()

icm20948 = ICM20948.ICM20948()

try:
	oled = SH1106.SH1106()
	print("Comprehensive test program...")
	print("please Enter ctrl+c to end program")
	image = Image.new('1', (oled.width, oled.height), "BLACK")
	draw = ImageDraw.Draw(image)
	
	x = 0
	font = ImageFont.truetype('Font.ttc', 10)
	while True:
		x = x + 1
		time.sleep(0.2)
		if(x < 20):
			bme = []
			bme = bme280.readData()
			pressure = round(bme[0], 2) 
			temp = round(bme[1], 2) 
			hum = round(bme[2], 2)
			
			lux = round(light.Lux(), 2)
			
			uv = round(si1145.readdata()[0], 2) 
			ir = round(si1145.readdata()[1], 2)
            
			gas = round(sgp.raw(), 2)
			
			draw.rectangle((0, 0, 128, 64), fill = 0)
			
			draw.text((0, 0), str(pressure), font = font, fill = 1)
			draw.text((40, 0), 'hPa', font = font, fill = 1)
			draw.text((0, 15), str(temp), font = font, fill = 1)
			draw.text((40, 15), 'C', font = font, fill = 1)
			draw.text((0, 30), str(hum), font = font, fill = 1)
			draw.text((40, 30), '%RH', font = font, fill = 1)
			
			draw.text((0, 45), str(lux), font = font, fill = 1)
			draw.text((40, 45), 'Lux', font = font, fill = 1)
			
			draw.text((65, 0), str(uv), font = font, fill = 1)
			draw.text((105, 0), 'UV', font = font, fill = 1)
			draw.text((65, 15), str(ir), font = font, fill = 1)
			draw.text((105, 15), 'IR', font = font, fill = 1)
			
			draw.text((65, 30), str(gas), font = font, fill = 1)
			draw.text((105, 30), 'GAS', font = font, fill = 1)
            
			oled.display(image)
		elif(x<40):
			icm = []
			icm = icm20948.getdata()
			roll = round(icm[0], 2)
			pitch = round(icm[1], 2)
			yaw = round(icm[2], 2)
			
			draw.rectangle((0, 0, 128, 64), fill = 0)
			font8 = ImageFont.truetype('Font.ttc', 9)
			
			draw.text((0, 0), 'RPY', font = font8, fill = 1)
			draw.text((20, 0), str(roll), font = font8, fill = 1)
			draw.text((50, 0), str(pitch), font = font8, fill = 1)
			draw.text((90, 0), str(yaw), font = font8, fill = 1)
			
			draw.text((0, 15), 'Acc', font = font8, fill = 1)
			draw.text((20, 15), str(icm[3]), font = font8, fill = 1)
			draw.text((50, 15), str(icm[4]), font = font8, fill = 1)
			draw.text((90, 15), str(icm[5]), font = font8, fill = 1)

			draw.text((0, 30), 'Gyr', font = font8, fill = 1)
			draw.text((20, 30), str(icm[6]), font = font8, fill = 1)
			draw.text((50, 30), str(icm[7]), font = font8, fill = 1)
			draw.text((90, 30), str(icm[8]), font = font8, fill = 1)

			draw.text((0, 45), 'Mag', font = font8, fill = 1)
			draw.text((20, 45), str(icm[9]), font = font8, fill = 1)
			draw.text((50, 45), str(icm[10]), font = font8, fill = 1)
			draw.text((90, 45), str(icm[11]), font = font8, fill = 1)
			
			oled.display(image)
		elif(x >= 40):
			x = 0

except KeyboardInterrupt:
	image2 = Image.new('1', (oled.width, oled.height), "BLACK")
	oled.display(image2)
	exit()	



