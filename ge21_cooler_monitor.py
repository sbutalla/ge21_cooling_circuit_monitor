##############################################################################
#    This Program will read data from the Arduino temperature sensors
##############################################################################               

import serial
from datetime import datetime
from selenium import webdriver

def format()
	# Constants
	dataDir = "myDir"

	# Connect to serial (output) of ardruino
	# NOTE - COM will change based on usb connection
	ser = serial.Serial('COM3' ,  9800, timeout = 2.1)

	#Create file to write to
	dt = datetime.now()
	str_date = dt.strftime("%Y-%m-%d_%H-%M-%S")

	try:
		os.makedirs(dataDir) # create directory for data
	except FileExistsError: # skip if directory already exists
		pass

	fullPath = massScanDir + "/" + "Chiller_Data_" + str_date + ".txt"

	try:
		os.makedirs(fullPath) # create 
	except FileExistsError: # skip if directory already exists
		pass

	file = open("Chiller_Data_" + str_date + ".txt", "a")

	#File header
	file.write("Humidity (%), Ambient Temperature (°C), M8 Temperature (°C), M5 Temperature (°C)\n")

def getData():

	while(True):
		
		#Data is sent as a byte object, change to string with decode(), then strip() to remove \r and \n
		line = ser.readline()
		string = line.decode()
		string = string.strip()
		
		if string != "":
			
			#Write to file
			file.write(string)
			file.write("\n")
			
			#Data is a comma separated list in this order:
			# Humidity, Ambient Temperature, M8 Temperature, M5 Temperature
			Data = string.split(",")
		
			#Not really needed
			hum = Data[0]
			amb_temp = Data[1]
			M8_temp = Data[2]
			M5_temp = Data[3]
		
		#Write url to be search (sends data to google sheet)
		vars = "amb_temp=" + Data[1] + "&amb_hum=" + Data[0] + "&M5_temp=" + Data[3] + "&M8_temp=" + Data[2]
		
		
		url = "https://script.google.com/a/macros/my.fit.edu/s/AKfycbwDQ6exDZfzg7RUe-XzhgUyNaDWZx-hU1dZAxDUg_60yBzjZVjW/exec?" + vars
		
		#Need to download geckodriver
		driver = webdriver.Firefox()
		driver.get(url)
		driver.close()

if __name__ == "__main__":

    # arg parser
    parser = argparse.ArgumentParser(description="Retrieve data and optionally send to a Google Sheet")
    parser.add_argument("-g", "--googleSheet", action="store_true", dest="googleSheet", help="Send data to Google Sheet")
    parser.add_argument("-p", "--printData", action="store_true", dest="printData", help="Print data to standard out")
    parser.add_argument("-w", "--write", action="store_true", dest="writeData", help="Write data to a file")
    

    args = parser.parse_args()    
    
    # Check arguments
    if args.googleSheet is not None and args.write is None:
        print(colors.YELLOW + "Must write data to a file to send it to a Google Sheet" + colors.ENDC)
        sys.exit()

    if args.massInc is None:
        print (colors.YELLOW + "Must specify the mass increment" + colors.ENDC)
        sys.exit()

    try:
        runScans()
    except KeyboardInterrupt:
        print(Colors.RED + "\nKeyboard Interrupt encountered" + Colors.ENDC)
