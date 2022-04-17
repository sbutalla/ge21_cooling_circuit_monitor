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

		
	

def plot(file):
	reader = csv.reader(file)
	
	#Defile path to directory to save plots
	path = file.name.replace(".txt", "/")
	os.mkdir(path)

	#Extract header
	header = []
	header = next(reader)
	
	#Extract Data
	rows = []
	for row in reader:
		rows.append(row)
	Data = np.array(rows)
	#Data comes in as:
	#Timestamp, Humidity, Ambient Temperature, M8 Temperature, M5 Temperature
	timestamp = Data[0:, 0]
	hum = Data[0:, 1].astype('float64')
	amb_temp = Data[0:, 2].astype('float64')
	m8_temp = Data[0:, 3].astype('float64')
	m5_temp = Data[0:, 4].astype('float64')
	
	
	#Convert timestamp into time elasped
	timestamp = [datetime.strptime(stamp, "%Y-%m-%d_%H-%M-%S") for stamp in timestamp]
	time_elapsed = [(tdt.day - timestamp[0].day)*24 + (tdt.hour - timestamp[0].hour) + (tdt.minute - timestamp[0].minute)/60 + (tdt.second - timestamp[0].second)/3600 for tdt in timestamp]
	
	
	#Start plotting
	fig = plt.figure()
	fig, ax = plt.subplots()
	fig.set_size_inches(14,6)
	
	
	
	plt.plot(time_elapsed, hum)
	plt.title("Relative Humidity")
	ax.set_xlabel("Elapsed Time (hrs)")
	ax.set_ylabel("Reletive Humidity (%)")
	plt.grid()
	plt.savefig(path + "Humidity.pdf")
	plt.cla()
	
	plt.plot(time_elapsed, amb_temp)
	plt.title("Ambient Temperature")
	ax.set_xlabel("Elapsed Time (hrs)")
	ax.set_ylabel("Temperature (" + u'\N{DEGREE SIGN}' + 'C)')
	plt.grid()
	plt.savefig(path + "Ambient_Temperature.pdf")
	plt.cla()
	
	plt.plot(time_elapsed, m8_temp)
	plt.title("M8 Temperature")
	ax.set_xlabel("Elapsed Time (hrs)")
	ax.set_ylabel("Temperature (" + u'\N{DEGREE SIGN}' + 'C)')
	plt.grid()
	plt.savefig(path + "M8_Temperature.pdf")
	plt.cla()
	
	plt.plot(time_elapsed, m5_temp)
	plt.title("M5 Temperature")
	ax.set_xlabel("Elapsed Time (hrs)")
	ax.set_ylabel("Temperature (" + u'\N{DEGREE SIGN}' + 'C)')
	plt.grid()
	plt.savefig(path + "M5_Temperature.pdf")
	
	
	
	



if __name__ == "__main__":
	
	# arg parser
	parser = argparse.ArgumentParser(description="Plot cooling circuit temperuature data from .txt file")
	parser.add_argument("-f", "--filename", action="store", dest="filename", default="", help="Name of the file to be read")
	
	args = parser.parse_args()
	
	#Chech Arguments
	if args.filename == "":
		print(colors.YELLOW + "Must include File Name" + colors.ENDC)
		sys.exit()

	try:
		with open(args.filename, "r") as file:
			plot(file)
	except:
		print(colors.RED + "File not found" + colors.ENDC)
	