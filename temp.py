#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys

# import sensors
import Adafruit_DHT

dht_sensor = Adafruit_DHT.DHT22
dht_pin = 4

humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)

if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)
   
