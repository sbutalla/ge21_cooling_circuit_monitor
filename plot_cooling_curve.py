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




def plot(file):
	reader = csv.reader(file)
	
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
	hum = Data[0:, 1]
	amb_temp = Data[0:, 2]
	m8_temp = Data[0:, 3]
	m5_temp = Data[0:, 4]
	
	#Convert timestamp into time elasped
	time_elapsed = np.linspace(0, timestamp.shape[0] * 2.1 / (60*60), timestamp.shape[0])
	
	#Start plotting
	fig = plt.figure()
	fig, ax = plt.subplots()
	fig.set_size_inches(14,6)
	
	
	plt.plot(time_elapsed, hum)
	ax.set_xlabel("Elapsed Time (hrs)")
	ax.set_ylabel("Reletive Humidity (%)")
	plt.savefig(path + "Humidity.pdf")
	plt.cla()
	
	plt.plot(time_elapsed, amb_temp)
	ax.set_xlabel("Elapsed Time (hrs)")
	ax.set_ylabel("Temperature (" + u'\N{DEGREE SIGN}' + 'C)')
	plt.savefig(path + "Ambient_Temperature.pdf")
	plt.cla()
	
	plt.plot(time_elapsed, m8_temp)
	ax.set_xlabel("Elapsed Time (hrs)")
	ax.set_ylabel("Temperature (" + u'\N{DEGREE SIGN}' + 'C)')
	plt.savefig(path + "M8_Temperature.pdf")
	plt.cla()
	
	plt.plot(time_elapsed, m5_temp)
	ax.set_xlabel("Elapsed Time (hrs)")
	ax.set_ylabel("Temperature (" + u'\N{DEGREE SIGN}' + 'C)')
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
	with open(args.filename, "r") as file:
		plot(file)
	"""
	try:
		with open(args.filename, "r") as file:
			plot(file)
	except:
		print(colors.RED + "File not found" + colors.ENDC)
	"""	