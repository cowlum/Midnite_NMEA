import asyncio
import pynmea2 
import smbus2
import bme280
import configparser


config = configparser.ConfigParser()
config.read("/boot/nmeabmp280.config")
bmp280_enabled = config.get("BMP280", "bmp280_enabled")
HOST = config.get("BMP280", "dest_IP")
PORT = config.get("BMP280", "dest_port")
seconds = int(config.get("BMP280", "seconds"))

## Variables

print(HOST)
print(PORT)

endline = "\n"
port = 1
address = 0x76
bus = smbus2.SMBus(port)


calibration_params = bme280.load_calibration_params(bus, address)
data = bme280.sample(bus, address, calibration_params)





async def tcp_client(message):
    #reader, writer = await asyncio.open_connection(
    #    '127.0.0.1', 2000)
    reader2, writer2 = await asyncio.open_connection(
        HOST, PORT)

    #print(f'Send: {message!r}')
    #writer.write(message.encode())
    #await writer.drain()

    #print(f'Send: {message!r}')
    #writer2.write(message.encode())
    #await writer2.drain()

    while True:

        pressure = str(round(data.pressure))
        pressure = "1.0" + pressure ## conversion from bar to hPa
        airtemp = str(round(data.temperature,1))

        ntemp = str(pynmea2.XDR('II','XDR',(('C',airtemp,'C','Temp Sensor',))))
        ntemp = ntemp + endline
        ntemp = ntemp.encode() 
 
        npres = str(pynmea2.XDR('II','XDR',(('P',pressure,'B','Pressure Sensor',))))
        npres = npres + endline
        npres = npres.encode()        
        print(pressure)

        writer2.write(ntemp)
        writer2.write(npres)
        await writer2.drain()
        await asyncio.sleep(seconds)


    print('Close the connection')
    writer.close()
    await writer.wait_closed()

asyncio.run(tcp_client('connecting'))
