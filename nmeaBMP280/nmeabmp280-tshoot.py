import asyncio
import pynmea2 
import smbus2
import bme280
import configparser
import time

## Allow 10 seconds for NmeaCommunicator, i2c to be active
time.sleep(10)

## Variables
config = configparser.ConfigParser()
config.read("/boot/nmeabmp280.config")
bmp280_enabled = config.get("BMP280", "bmp280_enabled")
HOST = config.get("BMP280", "dest_IP")
PORT = config.get("BMP280", "dest_port")
seconds = int(config.get("BMP280", "seconds"))
endline = "\n"
port = 1
address = 0x76
bus = smbus2.SMBus(port)


calibration_params = bme280.load_calibration_params(bus, address)


## Open a connection to Nmea Communicator
## While True collect pressure and tempreture
## Send the nmea string compiled by pynmea2 and wait seconds.

async def tcp_client(message):
    while True:
        try: 
            reader, writer = await asyncio.open_connection(
        HOST, PORT)
            data = bme280.sample(bus, address, calibration_params) 
            
            pressure = str(round(data.pressure))
            pressure = "1.0" + pressure ## conversion from bar to hPa
            airtemp = str(round(data.temperature,1))
            #print(data)

            ntemp = str(pynmea2.XDR('II','XDR',(('C',airtemp,'C','Temp Sensor',))))
            ntemp = ntemp + endline
            ntemp = ntemp.encode() 
 
            npres = str(pynmea2.XDR('II','XDR',(('P',pressure,'B','Pressure Sensor',))))
            npres = npres + endline
            npres = npres.encode()        
        
            writer.write(ntemp)
            writer.write(npres)
            await writer.drain()
            
            
            writer.close()
            await writer.wait_closed()
            
            time.sleep(seconds)
            #print("loop restarts")
            
        except:
            #print('Close the connection')
            await writer.wait_closed()
            exit()

asyncio.run(tcp_client('connecting'))
