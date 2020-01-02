import asyncio
import configparser
import time
## Variables

config = configparser.ConfigParser()
config.read("/boot/nmeahp33a.config")
hp33a_enabled = config.get("HP33A", "hp33a_enabled")
GPSDHOST = config.get("HP33A", "gpsd_IP")
GPSDPORT = config.get("HP33A", "gpsd_port")
HOST = config.get("HP33A", "dest_IP")
PORT = config.get("HP33A", "dest_port")
## Below sets GPSD to output in nmea
nmeaconfig='?WATCH={"enable":true,"json":false,"nmea":true,"raw":0,"scaled":false,"timing":false,"split24":false,"pps":false}' 

## Check for enabled
if hp33a_enabled == 'no':
    exit()

## Allow 10 seconds for NmeaCommunicator to be active
time.sleep(10)

## Open two connections. 
## connection one to collect from GPSD port
## connection two to connect to nmeaComm 
##
async def tcp_client(message):
    reader, writer = await asyncio.open_connection(
        GPSDHOST, GPSDPORT)
    reader2, writer2 = await asyncio.open_connection(
        HOST, PORT)

##  print(f'Send: {message!r}')
##  Send the nmea config to GPSD > GPSD to output in nmea
    writer.write(message.encode())
    await writer.drain()

##  Read a line from GPSD
##  Write the Line to nmeaComm
## Wait for writer to drain
## If we recieve empty data exit (This only happens on data recieving errors)
    while True:
        data = await reader.readline()
##      print(f'Received: {data.decode()!r}')
        writer2.write(data)
        await writer2.drain()
        if data is b'':
##          print("I die now")
            quit()
          

asyncio.run(tcp_client(nmeaconfig))
