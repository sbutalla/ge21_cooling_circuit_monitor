##############################################################################
#    This Program will read data from the Arduino temperature sensors
##############################################################################               

import serial
from datetime import datetime
from selenium import webdriver

# Constants
dataDir = "myDir"

def format()

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

def getData(printData, writeData, googleSheet):

	fullPath = format()
	# Connect to serial (output) of ardruino
	# NOTE - COM will change based on usb connection
	ser = serial.Serial('COM3' ,  9800, timeout = 2.1)

	counter = 0
	while(True):
		
		#Data is sent as a byte object, change to string with decode(), then strip() to remove \r and \n
		line = ser.readline()
		string = line.decode()
		string = string.strip()
		
		if string != "":

			dt = datetime.now()
			str_date = dt.strftime("%Y-%m-%d_%H-%M-%S")
			#Write to file
			#file.write(string + "n")

			Data = string.split(",")
			
			#Not really needed
			hum = float(Data[0])
			amb_temp = float(Data[1])
			M8_temp = float(Data[2])
			M5_temp = float(Data[3])

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


			
		'''
		if counter % 1000 == 0:
			if googleSheet == True:
				# write to google sheet here
				#Write url to be search (sends data to google sheet)
				vars = "amb_temp=" + Data[1] + "&amb_hum=" + Data[0] + "&M5_temp=" + Data[3] + "&M8_temp=" + Data[2]
		
				url = "https://script.google.com/a/macros/my.fit.edu/s/AKfycbwDQ6exDZfzg7RUe-XzhgUyNaDWZx-hU1dZAxDUg_60yBzjZVjW/exec?" + vars
		
				#Need to download geckodriver
				driver = webdriver.Firefox()
				driver.get(url)
				driver.close()
		else:
			pass
		'''


		

if __name__ == "__main__":

    # arg parser
    parser = argparse.ArgumentParser(description="Retrieve cooling circuit temperature and ambient condition data and optionally send to a Google Sheet")
    parser.add_argument("-p", "--printData", action="store_true", dest="printData", default=False help="Print data to standard out")
    parser.add_argument("-w", "--write", action="store_true", dest="writeData", default=False, help="Write data to a file")
    parser.add_argument("-g", "--googleSheet", action="store_true", dest="googleSheet", default=False, help="Send data to Google Sheet")
    
    args = parser.parse_args()    
    
    # Check arguments
    if args.googleSheet is True and args.write isFalse:
        print(colors.YELLOW + "Must write data to a file to send it to a Google Sheet" + colors.ENDC)
        sys.exit()

    try:
        getData(args.printData, args.writeData, args.googleSheet)
    except KeyboardInterrupt:
        print(Colors.RED + "\nKeyboard Interrupt encountered" + Colors.ENDC)
