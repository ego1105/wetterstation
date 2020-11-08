#!/usr/bin/python3
# -*- coding:utf-8 -*-

# for systemd service:
# sudo cp bme680.service /etc/systemd/system/.
# sudo systemctl start bme680.service
# sudo systemctl stop bme680.service
# sudo systemctl enable bme680.service

import time
import subprocess
import select
import logging
from logging.handlers import TimedRotatingFileHandler


logging.basicConfig(
    handlers=[TimedRotatingFileHandler('./bme680.csv', when='midnight', backupCount=180)],
    format='%(message)s',
    level=logging.INFO)
logger = logging.getLogger()    

f = subprocess.Popen( './bsec_bme680',\
        cwd='/home/pi/devel/bsec_bme680_linux', \
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
p = select.poll()
p.register(f.stdout)

try:
    while True:
        if p.poll(100):
            while True:
                line = f.stdout.readline().strip().decode('UTF-8')
                if line:
                    #print(line)
                    logger.info(line)
                else:
                    break

except IOError as e:
    print(e)
    
except KeyboardInterrupt:    
    print("ctrl + c:")    
    exit()