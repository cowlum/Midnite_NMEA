## Python Script to read temp and baromertic pressure from from bmp180
## Then convert it to nmea and send to the NMEA communicator 
## Variables to be pulled from /boot/nmea-bmp180.config

import socket
import sys
import pynmea2 
import configparser
import time
import smbus2
import bme280



##--------------------------- Variables -------------------
config = configparser.ConfigParser()
config.read("/home/midnite/python_scripts/nmeaic2/nmeabmp280.config")
bmp280_enalbed = config.get("BMP280", "bmp280_enabled")
HOST = config.get("BMP280", "dest_IP")
PORT = config.get("BMP280", "dest_port")
#bmp_ic2 = config.get("BMP280", "bmp_ic2")
#bmp = BMP085(bmp_ic2)  ## This will require ic2tools to check
#i2c = busio.I2C(board.SCL, board.SDA)
#sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
port = 1
address = 0x76
bus = smbus2.SMBus(port)

print(HOST)
print(PORT)

calibration_params = bme280.load_calibration_params(bus, address)

# the sample method will take a single reading and return a
# compensated_reading object
data = bme280.sample(bus, address, calibration_params)

## -------check to see if this script should run
#if bmp280_enabled == 'yes':
#	break
#else:
#	sys.exit()

## --- Functions to receive data ---


def get_pressure():
    global pressure
    #pressure = round(str(data.pressure()),2)
    pressure = round(data.pressure,1)

def get_temp():
    global airtemp
    #airtemp = round(str(data.temperature()),2)
    airtemp = round(data.temperature,1)
	
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
	conn.connect(('192.168.0.140', 2010))
	while True:
		time.sleep(2)
		#ntemp = pynmea2(nmea_xdr("II", "XDR", "C", get_temp(), "C", "TempSensor"))
		#npres = pynmea2(nmea_xdr("II", "XDR", "P", get_pressure(), "B", "Barometer"))
		get_temp()
		get_pressure()
		print(airtemp)
		print(pressure)
		#ntemp = pynmea2("II", "XDR", "C", airtemp, "C", "TempSensor")
		#npres = pynmea2("II", "XDR", "P", pressure, "B", "Barometer")
		ntemp = "II,XDR,X,22,C,TempSensor1"
		npres = 'II,XDR,X,22,C,TempSensor2 \n'


		#conn.sendall(b'Hello, world')
		conn.send(str.encode(npres))
		conn.send(str.encode(npres))
	    #conn.connect((HOST, PORT))



   
