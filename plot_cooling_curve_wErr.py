##########################################################################
#     This Program will plot the temperature curves from a text file     #
##########################################################################

import csv
import argparse
import sys
from utilities.colors import *
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

plt.rcParams.update({"font.size": 24}) # Increase font size

dh22_temp_err = 0.5 # deg. C
dh22_hum_err  = 2.0 # 2% accuracy
ds18b20_err   = 0.5 # deg. C


def DewErr (dewpnt, temp, hum): # Give array of Dew Point error through propagation
    error = []
    a = 17.625
    b = 243.04
    for i in range(len(dewpnt)):     
        alpha = np.log(hum[i] / 100) + (a*temp[i]/(b+temp[i]))
        sigalpha = (((dh22_hum_err/hum[i])**2) + ((b+temp[i]-a*temp[i]-1)/(b+temp[i])**2)**2 * dh22_temp_err**2)**0.5
        err = dewpnt[i] * np.sqrt(2) * sigalpha/alpha
        error.append(err)
    
    return np.array(error) 
        
def plot(filename, all_data, all_temp):

    with open(filename, "r") as file:

        path = file.name.replace(".txt", "/") # path to directory to save plots
    
        try:
            os.makedirs(path) # create directory for plots/analysis
        except FileExistsError: # skip if directory already exists
            pass

        reader = csv.reader(file)

        #Extract header
        header = []
        header = next(reader)
        
        #Extract Data
        rows = []
        for row in reader:
            rows.append(row)
        Data = np.array(rows)

    #Data comes in as:
    #Timestamp, Humidity, Ambient Temperature, M8 Temperature, M5 Temperature, Dew Point
    timestamp = Data[0:, 0]
    hum       = Data[0:, 1].astype('float64')
    amb_temp  = Data[0:, 2].astype('float64')
    m8_temp   = Data[0:, 3].astype('float64')
    m5_temp   = Data[0:, 4].astype('float64')
    dewpnt    = Data[0:, 5].astype('float64')

    hum_err      = np.full((len(hum),),dh22_hum_err, dtype = float)
    amb_temp_err = np.full((len(amb_temp),), dh22_temp_err, dtype = float)
    m8_temp_err  = np.full((len(m8_temp),), ds18b20_err, dtype = float)
    m5_temp_err  = np.full((len(m5_temp),), ds18b20_err, dtype = float)
    dewpnt_err   = DewErr(dewpnt, amb_temp, hum)
    
    
    #Convert timestamp into time elasped
    timestamp = [datetime.strptime(stamp, "%Y-%m-%d_%H-%M-%S") for stamp in timestamp]
    time_elapsed = [(tdt.day - timestamp[0].day)*24 + (tdt.hour - timestamp[0].hour) + (tdt.minute - timestamp[0].minute)/60 + (tdt.second - timestamp[0].second)/3600 for tdt in timestamp]
    
    dataset        = [hum, amb_temp, m8_temp, m5_temp, dewpnt] 
    errors         = [hum_err, amb_temp_err, m8_temp_err, m5_temp_err, dewpnt_err]
#LD_LIBRARY_PATH=/opt/wiscrpcsvc/lib:$LD_LIBRARY_PATH
    x_label        = "Elapsed Time (hrs)"
    y_labels       = ["Relative humidity (%)", r'Temperature ($^{\circ}$C)']
    leg_labels     = ["Ambient relative humidity", r'Ambient temperature', r'M8 ambient temperature', r'M5 ambient temperature', r'Dew point']
    leg_labels_err = ["Ambient relative humidity error", r'Ambient temperature error', r'M8 ambient temperature error', r'M5 ambient temperature error', 'Dew point error']
    color          = ["tab:blue", "tab:red", "tab:green", "tab:orange", "tab:purple"]


    fig, ax = plt.subplots()
        
    # plot humidity
    plt.plot(time_elapsed, hum, color = color[0], label = leg_labels[0])
    plt.grid()
    plt.title("Relative Humidity")
    ax.set_xlabel(x_label, loc = "right")
    ax.set_ylabel(y_labels[0], loc = "top")
    ax.legend(loc = 1)

    ax.text(-0.09, 1.01, 'CMS', fontweight='bold', fontsize=38, transform=ax.transAxes)
    ax.text(-0.01, 1.01, 'Muon R&D',fontstyle='italic', fontsize=34, transform=ax.transAxes)
    plt.tight_layout()
    plt.savefig(path + "Humidity.pdf")
    plt.cla()
    
    # plot ambient temp
    plt.plot(time_elapsed, amb_temp, color = color[1], label = leg_labels[1])
    plt.grid()
    plt.title("Ambient Temperature")
    ax.set_xlabel(x_label, loc = "right")
    ax.set_ylabel(y_labels[1], loc = "top")
    ax.legend(loc = 1)

    ax.text(-0.09, 1.01, 'CMS', fontweight='bold', fontsize=38, transform=ax.transAxes)
    ax.text(-0.01, 1.01, 'Muon R&D',fontstyle='italic', fontsize=34, transform=ax.transAxes)
    plt.tight_layout()
    plt.savefig(path + "Ambient_Temperature.pdf")
    plt.cla()
    
    # plot m8 temp
    plt.plot(time_elapsed, m8_temp,  color = color[2],label = leg_labels[2])
    plt.grid()
    plt.title("M8 Temperature")
    ax.set_xlabel(x_label, loc = "right")
    ax.set_ylabel(y_labels[1], loc = "top")
    ax.legend(loc = 1)

    ax.text(-0.09, 1.01, 'CMS', fontweight='bold', fontsize=38, transform=ax.transAxes)
    ax.text(-0.01, 1.01, 'Muon R&D',fontstyle='italic', fontsize=34, transform=ax.transAxes)
    plt.tight_layout()
    plt.savefig(path + "M8_Temperature.pdf")
    plt.cla()

    # plot m5 temp
    plt.plot(time_elapsed, m5_temp,  color = color[3], label = leg_labels[3])
    plt.grid()
    plt.title("M5 Temperature")
    ax.set_xlabel(x_label, loc = "right")
    ax.set_ylabel(y_labels[1], loc = "top")
    ax.legend(loc = 1)

    ax.text(-0.09, 1.01, 'CMS', fontweight='bold', fontsize=38, transform=ax.transAxes)
    ax.text(-0.01, 1.01, 'Muon R&D',fontstyle='italic', fontsize=34, transform=ax.transAxes)

    plt.tight_layout()
    plt.savefig(path + "M5_Temperature.pdf")
    
    # plot dew point
    plt.plot(time_elapsed, dewpnt,  color = color[4], label = leg_labels[4])
    plt.grid()
    plt.title("Dew Point")
    ax.set_xlabel(x_label, loc = "right")
    ax.set_ylabel(y_labels[1], loc = "top")
    ax.legend(loc = 1)

    ax.text(-0.09, 1.01, 'CMS', fontweight='bold', fontsize=38, transform=ax.transAxes)
    ax.text(-0.01, 1.01, 'Muon R&D',fontstyle='italic', fontsize=34, transform=ax.transAxes)

    plt.tight_layout()
    plt.savefig(path + "Dew_Point")

    
    if all_temp == True:
        fig, ax0 = plt.subplots(figsize = (16, 12))
        plt.grid()
        ax0.set_xlabel(x_label, loc = "right")
        #ax1.set_xlim(510, 680)
        ax0.set_ylabel(y_labels[1], loc = "top")
        for temp in range(1, len(dataset)):
            ax0.plot(time_elapsed,  dataset[temp], marker='o', markersize=4, label = leg_labels[temp])
            plt.fill_between(time_elapsed, dataset[temp] - errors[temp],  dataset[temp] + errors[temp], alpha = 0.5, label = leg_labels_err[temp])
        ax0.text(-0.09, 1.01, 'CMS', fontweight='bold', fontsize=30, transform=ax0.transAxes)
        ax0.text(-0.01, 1.01, 'Muon R&D',fontstyle='italic', fontsize=26, transform=ax0.transAxes)
        ax0.legend(loc = 0, fontsize = 18)
       

        plt.tight_layout()  
        plt.savefig(path + "all_temps_wErr.pdf")

    else:
        pass
    
    if all_data == True:
        fig, ax0 = plt.subplots(figsize = (16, 12))
        plt.grid()
        ax0.set_xlabel(x_label, loc = "right")
        #ax1.set_xlim(510, 680)
        ax0.set_ylabel(y_labels[1], loc = "top")
        for temp in range(1, len(dataset)):
            ax0.errorbar(time_elapsed,  dataset[temp], errors[temp], marker='o', markersize=4, label = leg_labels[temp])


        ax1 = ax0.twinx() 
        ax1.set_ylabel(y_labels[0], loc = "top")  # we already handled the x-label with ax1
        ax1.errorbar(time_elapsed,  dataset[0], marker='o', markersize=4, label = leg_labels[0])

        ax0.text(-0.09, 1.01, 'CMS', fontweight='bold', fontsize=30, transform=ax0.transAxes)
        ax0.text(-0.01, 1.01, 'Muon R&D',fontstyle='italic', fontsize=26, transform=ax0.transAxes)
        ax0.legend(loc = 0, fontsize = 18)
        ax1.legend(loc = 1, fontsize = 18)

        plt.tight_layout()  
        plt.savefig(path + "humidity_and_allTemps.pdf")

    else:
        pass
    
    print(colors.GREEN + "Plots saved at {}".format(path) + colors.ENDC)
    


if __name__ == "__main__":
    
    # arg parser
    parser = argparse.ArgumentParser(description="Plot cooling circuit temperuature data from .txt file")
    parser.add_argument("-f", "--filename", action="store", dest="filename", help="Name of the file to be read")
    parser.add_argument("-ad", "--all_data", action="store_true", dest="all_data", default=False, help="Plot all curves (hum. and temp.) on same plot")
    parser.add_argument("-at", "--all_temp", action="store_true", dest="all_temp", default=False, help="Plot all temp. curves on same plot")
    args = parser.parse_args()
    
    #Chech Arguments
    if args.filename is None:
        print(colors.YELLOW + "Must include File Name" + colors.ENDC)
        sys.exit()

    try:
        plot(args.filename, args.all_data, args.all_temp)
    except KeyboardInterrupt:
        print(Colors.RED + "\nKeyboard interrupt encountered" + Colors.ENDC)
    
