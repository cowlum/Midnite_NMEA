## Python Script to read temp and baromertic pressure from from bmp180
## Then convert it to nmea and send to the NMEA communicator 
## Variables to be pulled from /boot/nmea-bmp180.config

import socket
import sys
import pynmea2 
import configparser
import board
import digitalio
import busio
import time
from adafruit_bmp280 import adafruit_bmp280


##--------------------------- Variables -------------------
config = ConfigParser.ConfigParser()
config.read("/boot/bmpnmea.config")
bmp280_enalbed = config.get("BMP280", "bmp280_enalbed")
HOST = config.get("BMP280", "dest_IP")
PORT = config.get("BMP280", "dest_port")
#bmp_ic2 = config.get("BMP280", "bmp_ic2")
#bmp = BMP085(bmp_ic2)  ## This will require ic2tools to check
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)


## -------check to see if this script should run
if bmp280_enabled == 'yes':
	break
	else:
	sys.exit()

## --- Functions to receive data ---
def get_pressure():
    global pressure
    pressure = str(round(sensor.Pressure(),2))
    #pressure = str(pressure)

def get_temp():
    global airtemp
    airtemp = str(round(sensor.Temperature(),2))
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
   
