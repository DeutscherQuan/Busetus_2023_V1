#!/usr/bin/python
# -*- coding:utf-8 -*-
# initial set up of imports

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
import pyrebase

# Declare Firebase address to connect to Python
config = {
  "apiKey": "AIzaSyCwBgvqH-j_TFMXijSNxnI2lC4f_l5zd3s",
  "authDomain": "smarttrap2022-9f9e7.firebaseapp.com",
  "databaseURL": "https://smarttrap2022-9f9e7-default-rtdb.firebaseio.com",
  "projectId": "smarttrap2022-9f9e7",
  "storageBucket": "smarttrap2022-9f9e7.appspot.com",
  "messagingSenderId": "656616970547",
  "appId": "1:656616970547:web:8e3fff03575ab683078646",
  "measurementId": "G-WXQGYY33DX"
 }

firebase = pyrebase.initialize_app(config)


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
#gyros = 0
#accel = 0
#magnetic = 0
#pressu = 0
#temp = 0
#humi = 0
#ss_uv = 0
#ss_ir = 0
#ss_light = 0
#ss_voc = 0        
   
    while True:
        
	# Send data of ICM20948 to Firebase Realtime Database
        #database = firebase.database()
        #e = database.child("Environment Sensor").child("ICM20948").child("Gyros").set(gyros)
        #database.child("Environment Sensor Storage").child("ICM20948 Storage").child("Gyros").push(e)
        #f = database.child("Environment Sensor").child("ICM20948").child("Accel").set(accel)        
        #database.child("Environment Sensor Storage").child("ICM20948 Storage").child("Accel").push(f)
        #g = database.child("Environment Sensor").child("ICM20948").child("Magnetic").set(magnetic)        
        #database.child("Environment Sensor Storage").child("ICM20948 Storage").child("Magnetic").push(g)

	#Send data of SI1145 to Firebase Realtime Database
        #database = firebase.database()
        #h = database.child("Environment Sensor").child("SI1145").child("ss_uv").set(ss_uv)
        #database.child("Environment Sensor Storage").child("SI1145 Storage").child("ss_uv").push(h)
        #i = database.child("Environment Sensor").child("SI1145").child("ss_ir").set(ss_ir)        
        #database.child("Environment Sensor Storage").child("SI1145 Storage").child("ss_ir").push(i)

	# Send data of light(TSL2591)to Firebase Realtime Database
        #database = firebase.database()
        #j = database.child("Environment Sensor").child("light(TSL2591)").child("ss_light").set(ss_light)
        #database.child("Environment Sensor Storage").child("light(TSL2591) Storage").child("ss_light").push(j)

	# Send data of VOC(SGP40) to Firebase Realtime Database
        #database = firebase.database()
        #k = database.child("Environment Sensor").child("VOC(SGP40)").child("ss_voc").set(ss_voc)
        #database.child("Environment Sensor Storage").child("VOC(SGP40) Storage").child("ss_voc").push(k)

     	# Send data of BME to Firebase Realtime Database
         
        database = firebase.database()
        l = database.child("Environment Sensor").child("BME").child("Pressure").set(pressu)
        database.child("Environment Sensor Storage").child("BME Storage").child("Pressure").push(l)
        m = database.child("Environment Sensor").child("BME").child("Temperature").set(temp)        
        database.child("Environment Sensor Storage").child("BME Storage").child("Temperature").push(m)
        n = database.child("Environment Sensor").child("BME").child("Humidity").set(humi)
        database.child("Environment Sensor Storage").child("BME Storage").child("Humidity").push(n)

	#remove database
        database = firebase.database()
        today = datetime.datetime.now()
        if (today.minute % 15 == 0):
          database.child("Environment Sensor").remove()
          database.child("Environment Sensor Storage").remove()
          #database.remove()
        
        with open('ss.csv', mode='a') as sensor_readings:
            sensor_write = csv.writer(sensor_readings, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            write_to_log = sensor_write.writerow([day_time(),gyros,accel,magnetic,pressu,temp,humi,ss_uv,ss_ir,ss_light,ss_voc])
        print('Writing.....')     
        
        time.sleep(5)

except KeyboardInterrupt:
    pass
	


