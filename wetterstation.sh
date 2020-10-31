#!/bin/bash

# change into directory of co2_monitor
cd /home/pi/devel/wetterstation

# get last 2000 records, keeping the header
head -n 1 data/dht22_log.csv > data/dht22_log_last.csv
tail -n 2000 data/dht22_log.csv | grep -v Datetime >> data/dht22_log_last.csv

# evaluate data and create plot
./data_plotter.py > data_plotter.log 2>&1


