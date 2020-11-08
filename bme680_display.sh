#!/bin/bash

# change into directory
cd /home/pi/devel/wetterstation

# evaluate data and create plot
./data_plotter.py > data_plotter.log 2>&1


