##########################################################################
#    This Program will read data from the Arduino temperature sensors    #
##########################################################################               

import serial
from datetime import datetime
from selenium import webdriver
import argparse
import os
import gspread
import numpy as np
from utilities.colors import *
import smtplib

# Constants
dataDir = "myDir"

#Set up email and local host to be ready to send alert
#NOTE - Email most likely will go to spam, make sure everyone marks it as not spam
sender = 'from@fromdomain.com'
receivers = ['eyanes2021@my.fit.edu','balsufyani2017@my.fit.edu','sbutalla2012@my.fit.edu']
message = """From: From GE 2/1 <from@fromdomain.com>
To: To Person <eyanes2021@my.fit.edu,balsufyani2017@my.fit.edu,sbutalla2012@my.fit.edu>
Subject: Alert From GE 2/1 Arduino
There is an alert from the GE 2/1 arduino, you may want to go check it.
"""
smtpObj = smtplib.SMTP('localhost')

def format():

	#Create file to write to
	dt = datetime.now()
	str_date = dt.strftime("%Y-%m-%d_%H-%M-%S")

	try:
		os.makedirs(dataDir) # create directory for data
		
	except FileExistsError: # skip if directory already exists
		pass

	fullPath = dataDir + "/" + "Chiller_Data_" + str_date + ".txt"

	file = open(fullPath, "a")
	file.write("time, humidity, ambient_temp, m8_temp, m5_temp\n") # File header

	return fullPath
	
def DewPoint(T,RH):
	
	#Calculate the Dew Point using Magnus-Tetens formula
	a = 17.625
	b = 243.04
	alpha = np.log(RH/100) + (a*T)/(b+T)
	dewpnt = (b*alpha) / (a - alpha)
	
	return dewpnt

def EmailAlert():
	
	#Sends out email alert to users
	try:
   		smtpObj.sendmail(sender, receivers, message)
   		print("Successfully sent email")
	except:
   		print("Error: unable to send email")



def getData(printData, writeData, googleSheet):

	fullPath = format()
	# Connect to serial (output) of ardruino
	# NOTE - String will change based on usb connection
	ser = serial.Serial('/dev/ttyUSB0' ,  9800, timeout = 2.1)
	
	if googleSheet == True:		
		
		try:		#Try to connect to google sheet
			sa = gspread.service_account(filename="service_account.json") #File with cridentials to allow writing to google sheet
			sh = sa.open("Chiller_Temperature_Monitoring")
			wks = sh.worksheet("Sheet1")
		except:
			print(colors.YELLOW + "Cannot Connect to Google Sheet" + colors.ENDC)
			sys.exit()
	else:
		pass
		
		
	counter = 0 # Make sure email is only sent once if dewpoint was reached
	while(True):
		
		#Data is sent as a byte object, change to string with decode(), then strip() to remove \r and \n
		line = ser.readline()
		string = line.decode()
		string = string.strip()
		
		if string != "":

			dt = datetime.now()
			str_date = dt.strftime("%Y-%m-%d_%H-%M-%S")
			

			Data = string.split(",") # Convert Data into list
			
			hum = float(Data[0])
			amb_temp = float(Data[1])
			M8_temp = float(Data[2])
			M5_temp = float(Data[3])
			
			dewpnt = DewPoint(amb_temp, hum)
			
			if (dewpnt > M8_temp or dewpnt > M5_temp) and counter == 0:
				EmailAlert()
				print("\nDew Point has been reached!")
				counter = 1
			else:
				pass
			
			

			if printData == True:
				# Data is a comma separated list in this order:
				# Humidity, Ambient Temperature, M8 Temperature, M5 Temperature
				print(("%s, %f, %f, %f, %f\n" % (str_date, hum, amb_temp, M8_temp, M5_temp)))
			else:
				pass

			if writeData == True:
				with open(fullPath, 'a') as file: # write data and close file to save
					file.write("%s, %f, %f, %f, %f\n" % (str_date, hum, amb_temp, M8_temp, M5_temp))
			else:
				pass
			if googleSheet == True: # Write data to google sheets, sent as a list
				wks.append_row([str_date, amb_temp, hum, M5_temp, M8_temp])
			else:
				pass

	

if __name__ == "__main__":

    # arg parser
    parser = argparse.ArgumentParser(description="Retrieve cooling circuit temperature and ambient condition data and optionally send to a Google Sheet")
    parser.add_argument("-p", "--printData", action="store_true", dest="printData", default=False, help="Print data to standard out")
    parser.add_argument("-w", "--write", action="store_true", dest="writeData", default=False, help="Write data to a file")
    parser.add_argument("-g", "--googleSheet", action="store_true", dest="googleSheet", default=False, help="Send data to Google Sheet")
    parser.add_argument("-t", "--testEmail", action="store_true", dest="testEmail", default=False, help="Send an email alert to all users")    

    args = parser.parse_args()    
    
    # Check arguments
    if args.googleSheet is True and args.writeData is False:
        print(colors.YELLOW + "Must write data to a file to send it to a Google Sheet" + colors.ENDC)
        sys.exit()

    if args.testEmail is False:
        try:
            getData(args.printData, args.writeData, args.googleSheet)
        except KeyboardInterrupt:
            print(colors.RED + "\nKeyboard Interrupt encountered" + colors.ENDC)

    if args.testEmail is True:
        EmailAlert()
