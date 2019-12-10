## Python Script to read temp and baromertic pressure from from bmp180
## Then convert it to nmea and send to the NMEA communicator 
## Variables to be pulled from /boot/nmea-bmp180.config

import socket
import sys
import time
import pynmea2 ## Not likelt required
import configparser
from Adafruit_BMP085 import BMP085

##--------------------------- Variables -------------------
config = ConfigParser.ConfigParser()
config.read("/boot/bmpnmea.config")
bmp180_enalbed = config.get("BMP180", "bmp180_enalbed")
HOST = config.get("BMP180", "dest_IP")
PORT = config.get("BMP180", "dest_port")
bmp_ic2 = config.get("BMP180", "bmp_ic2")
bmp = BMP085(bmp_ic2)  ## This will require ic2tools to check

## check to see if this script should run

if bmp180_enabled == 'yes':
	break
	else:
	sys.exit()

## Functions to receive data

def get_pressure():
    global pressure
    pressure = str(round(bmp.readPressure(),2))
    #pressure = str(pressure)

def get_temp():
    global airtemp
    airtemp = str(round(bmp.readTemperature(),2))
    #airtemp = str(airtemp)

while True:
	time.sleep(60)
	ntemp = pynmea2(nmea_xdr("II", "XDR", "C", get_temp(), "C", "TempSensor"))
	npres = pynmea2(nmea_xdr("II", "XDR", "P", get_pressure(), "B", "Barometer"))

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
	    conn.connect((HOST, PORT))
	    #s.sendall(b'Hello, world')
	    conn.send(str.encode(ntemp))
	    conn.send(str.encode(npres))
   
