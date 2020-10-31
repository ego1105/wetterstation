#!/usr/bin/python3
# -*- coding:utf-8 -*-

from time import sleep
import csv
import os.path
from datetime import datetime

# import sensor
import Adafruit_DHT

# data file name
file_name = 'data/dht22_log.csv'

# sensor settings
dht_sensor = Adafruit_DHT.DHT22
dht_pin = 4

try:
    #if the file does not already exist, create a new file with headers
    if not os.path.isfile(file_name):
        csv_headers = ['Datetime', 'Temperatur/°C', 'Luftfeuchte/%']
        with open(file_name, 'w') as new_data_file:
            datawriter = csv.writer(new_data_file)
            datawriter.writerow(csv_headers)

    # datetime
    now = datetime.now()       
            
    # sensor humidity and temp
    humidity, temperature = Adafruit_DHT.read_retry(dht_sensor, dht_pin)

    # combine data in list
    new_log = []
    new_log.append(now)
    new_log.append( "%0.1f" % temperature )
    new_log.append( "%0.1f" % humidity)        
    
    #write results to log
    with open(file_name, 'a') as data_log:
        logwriter = csv.writer(data_log)
        logwriter.writerow(new_log)

except IOError as e:
    print(e)
    
except KeyboardInterrupt:    
    print("ctrl + c:")    
    exit()

