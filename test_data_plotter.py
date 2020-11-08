#!/usr/bin/python3
# -*- coding:utf-8 -*-

import sys
import os
import glob
import logging
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker


def read_data_table( file_name):
    header_list = \
        ["DateTime", "Acc", "IAQ", "IAQs", "Temp", "Feucht", \
        "Druck", "Gas", "BSECs", "CO2e", "bVOCe"]

    # load recent file    
    df = pd.read_csv( file_name, index_col=header_list[0], \
        parse_dates=True, header=None, names=header_list)  

    # load additional older files
    try:
        file_name_add = sorted(glob.glob( file_name+".*"))[-1]
        df_add = pd.read_csv( file_name_add, index_col=header_list[0], \
            parse_dates=True, header=None, names=header_list)  
        combined = [ df_add, df]
        df = pd.concat(combined)
    except:
        pass

    # limit data
    last_idx = df.index[-1]
    first_idx = df.index[-1] - pd.Timedelta(hours=36)
    df = df.loc[ str(first_idx):str(last_idx) ]

    # select columns
    #df2 = df[ [ "Temp", "Feucht", "Druck", "IAQ", "CO2e", "bVOCe"] ]
    df2 = df[ [ "Temp", "Feucht", "Druck", "IAQ"] ]
    # resample
    df2 = df2.resample('5min', label='right').mean().dropna()
    return df2

def creat_table_plot( table, w=400, h=300, dpi=90):
    # plot settings
    plt.rcParams['text.antialiased'] = False
    plt.rcParams['lines.antialiased'] = False
    plt.rcParams['font.family'] = 'cmss10'
    plt.rcParams['font.size'] = 16
    #plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10    
    plt.rcParams['lines.linewidth'] = 1.0
    plt.rcParams["legend.frameon"] = False
    plt.rcParams["legend.handlelength"] = 0.1
    plt.rcParams['grid.linestyle'] = ':'
    plt.rcParams['grid.linewidth'] = 0.5
    # create figure and axis layout
    fig, axs=plt.subplots( figsize=( w/dpi, h/dpi), dpi=dpi, 
        nrows=len(table.columns), ncols=1, 
        sharex=True, gridspec_kw={'hspace': 0.05, 'wspace': 0})
    fig.subplots_adjust(top=0.92, bottom=0.12, left=0.12, right=0.97)


    t2 = table.rolling('6h').mean()

    # plot table data    
    # to Object for matplotlib axis ticks
    table.index = table.index.astype('O')
    table.plot(  ax=axs, subplots=True)

    t2.index = t2.index.astype('O')
    t2.plot(  ax=axs, subplots=True, legend=False, linestyle='dotted')

    plt.xlabel('')
    #fig.autofmt_xdate()
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
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f"))
        ax.legend( loc='lower left')

    # current data at bottom    
    last = table.tail(1)
    temp = last['Temp'].values[0] 
    humi = last['Feucht'].values[0]
    pres = last['Druck'].values[0]
    iaq  = last['IAQ'].values[0]
    current_data = "T=%0.1f'C  H=%0.1f%%  P=%0.1fhPa  IAQ=%d" % ( temp, humi, pres, iaq)
    plt.text( 0.01, 0.94, current_data, 
        transform=plt.gcf().transFigure, color='r',
        fontsize=14)


try:


    # data file name
    file_name = 'bme680.csv'

    # read data
    table = read_data_table( file_name)

    # plot table data
    w, h = (400, 300)
    dpi = 100
    creat_table_plot( table, w, h, dpi)
    plt.savefig("data_plot_3.png")
      
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")  
    exit()    









 