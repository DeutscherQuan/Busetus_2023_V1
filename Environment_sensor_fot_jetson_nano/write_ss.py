#!/usr/bin/python
# -*- coding:utf-8 -*-
# initial set up of imports

import threading
import time
import datetime
import ICM20948 #Gyroscope/Acceleration/Magnetometer
import BME280   #Atmospheric Pressure/Temperature and humidity
import SI1145   #UV
import TSL2591  #LIGHT
import SGP40
from PIL import Image,ImageDraw,ImageFont
import math
import csv
import ina219


bme280 = BME280.BME280()
bme280.get_calib_param()
light = TSL2591.TSL2591()
light.SET_LuxInterrupt(20, 200)
si1145 = SI1145.SI1145()
sgp = SGP40.SGP40()
icm20948 = ICM20948.ICM20948()

#ina219_ = ina219.INA219()

#time
def day_time():
    today = datetime.datetime.now()
    date_time = today.strftime("%y%m%d%H%M")
    date_time = str(date_time)
    return(date_time)

def ssWrite():
    with open('ss.csv', mode='a') as sensor_readings:
        sensor_write = csv.writer(sensor_readings, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        write_to_log = sensor_write.writerow([day_time(),gyros,accel,magnetic,pressu,temp,humi,ss_uv,ss_ir,ss_light,ss_voc])
        print('Writing.....')


try:
    # sensor.setup()
    #BME
    data_bme280 = []
    data_bme280 = bme280.readData()
    pressu = str(round(data_bme280[0], 2))
    temp = str(round(data_bme280[1], 2))
    humi = str(round(data_bme280[2], 2))


    #ICM20948
    icm = []
    icm = icm20948.getdata()
    gyros = str(("x=%d,y=%d,z=%d")%(icm[6],icm[7],icm[8]))
    accel = str(("x=%d,y=%d,z=%d")%(icm[3],icm[4],icm[5]))
    magnetic = str(("x=%d,y=%d,z=%d")%(icm[9],icm[10],icm[11]))
    #SI1145
    ss_uv = str((round(si1145.readdata()[0], 2)))
    ss_ir = str((round(si1145.readdata()[1], 2)))
    #light(TSL2591)
    lux = light.Lux()
    ss_light = str(round(lux, 2))
    #VOC(SGP40)
    ss_voc = str(sgp.measureRaw(25,50))
    # #current
    # ina = ina219_(addr=0x42)

    # bus_voltage = str(round(ina.getBusVoltage_V(), 2))            # voltage on V- (load side)
    # shunt_voltage = str(round((ina.getShuntVoltage_mV() / 1000), 2)) # voltage between V+ and V- across the shunt
    # current = str(round((ina.getCurrent_mA()/1000),  2))                  # current in mA
    # power = str(round(ina.getPower_W(), 2))                     # power in W
    # p = (bus_voltage - 6)/2.4*100
    # if(p > 100):p = 100
    # if(p < 0):p = 0

    #bus_voltage,current,power,p


    while True:
        timer = threading.Timer(2.0, ssWrite)
        timer.start()
except KeyboardInterrupt:
    pass
	


