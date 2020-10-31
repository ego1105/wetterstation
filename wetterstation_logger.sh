#!/bin/bash

# change into directory of co2_monitor
cd /home/pi/devel/wetterstation

# log sensor data
./data_logger.py > data_logger.log 2>&1




