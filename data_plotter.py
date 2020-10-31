#!/usr/bin/python3
# -*- coding:utf-8 -*-

import sys
import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from PIL import Image
from waveshare_epd import epd4in2

def read_data_table( file_name):
    table = pd.read_csv( file_name, index_col=0, parse_dates=True)

    # limit data
    last_idx = table.index[-1]
    first_idx = table.index[-1] - pd.Timedelta(hours=24)
    table = table.loc[ str(first_idx):str(last_idx) ]

    # outlier removal
    table2 = table.copy()
    Q1 = table2.quantile(0.05)
    Q3 = table2.quantile(0.95)
    IQR = Q3 - Q1
    table2 = table2[~((table2 < (Q1 - 1.5 * IQR)) |(table2 > (Q3 + 1.5 * IQR))).any(axis=1)]

    # create copy of table and modify
    table3 = table2.copy()        
    table3 = table3.resample('5min', label='right').mean()

    # to Object for matplotlib axis ticks
    table3.index = table3.index.astype('O')
    print( table3.tail(10) )
    print( table3.describe() )
    
    return table3


def creat_table_plot( table, w, h, dpi):
    # plot settings
    plt.rcParams['text.antialiased'] = False
    plt.rcParams['lines.antialiased'] = False
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['font.size'] = 12
    #plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12    
    plt.rcParams['lines.linewidth'] = 1.0
    plt.rcParams["legend.frameon"] = False
    plt.rcParams["legend.handlelength"] = 0.1
    plt.rcParams['grid.linestyle'] = ':'
    plt.rcParams['grid.linewidth'] = 0.5

    # create figure and axis layout
    fig, axs=plt.subplots( figsize=( w/dpi, h/dpi), dpi=dpi, 
        nrows=2, sharex=True, gridspec_kw={'hspace': 0.05, 'wspace': 0})
    fig.subplots_adjust(top=1.0, bottom=0.12, left=0.15, right=1.0)
    
    # plot table data
    table.plot( ax=axs, subplots=True, style='k-')    
    plt.xlabel('')
    fig.autofmt_xdate()
    xfmt = mdates.DateFormatter("%H:%M")

    for ax in fig.get_axes():
        ax.tick_params(
            axis='both',
            which='both',
            left=False,
            right=False,
            bottom=False,
            top=False)
        ax.label_outer()
        ax.autoscale(enable=True, axis='both', tight=True)
        ax.grid(True, 'major', 'both')        
        ax.set_frame_on(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.xaxis.set_major_formatter(xfmt)

    # # current data at bottom    
    # last = table.tail(1)
    # temp = last['Temp/°C'].values[0] 
    # humi = last['Feucht/%'].values[0]
    # current_data = "%0.1f°C  %0.1f%%  %0.0fppm" % ( temp, humi, co2)
    # plt.text( 0.01, 0.01, current_data, transform=plt.gcf().transFigure, color='r')
    # return co2    


def fig2img(plt):
    """Convert a Matplotlib figure to a PIL Image and return it"""
    import io
    buf = io.BytesIO()
    plt.savefig( buf)
    buf.seek(0)
    img = Image.open(buf)
    return img


try:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.disabled = True

    logging.info("starting e-paper data logger")
    
    # get epaper handle
    epd = epd4in2.EPD()

    # data file name
    file_name = 'data/dht22_log_last.csv'

    # read data
    table = read_data_table( file_name)

    # plot table data
    w, h = (epd.width, epd.height)
    dpi = 120
    creat_table_plot( table, w, h, dpi)
    plt.savefig("data/dht22_plot_1.png")
      
    # convert plot to image
    img = fig2img(plt)
    img = img.convert('RGB', dither=0 )

    # split into black and red pixels
    imgB = Image.new('1', img.size, 255)  
    imgR = Image.new('1', img.size, 255)  
    redData = []
    blackData = []
    for color in img.getdata():
        r, g, b = color    
        if r>b and r>g:
            redData.append( 0)      
        else:
            redData.append( 255)      
                
        if r<200 and b<200 and g<200:
            blackData.append( 0)  
        else:
            blackData.append( 255)  
    imgB.putdata(blackData)
    imgR.putdata(redData)

    # save images
    img.save("data/dht22_plot_2.png")
    #imgB.save("data_plotB.png")
    #imgR.save("data_plotR.png")

    # display images on e-paper
    logging.info("init and clear display " + str(epd.width) + "x" + str(epd.height) )
    epd.init()
    logging.info("Drawing") 
    epd.display(epd.getbuffer(imgB))   
    logging.info("Goto Sleep...")
    epd.sleep()
    epd.Dev_exit()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd4in2.epdconfig.module_exit()
    exit()    