import asyncio
import time
import configparser

config = ConfigParser.ConfigParser()
config.read("/boot/nmeahp33a.config")
hp33a_enalbed = config.get("HP33A", "hp33a_enalbed")
GPSDHOST = config.get("HP33A", "gpsd_IP")
GPSDPORT = config.get("HP33A", "gpsd_port")
HOST = config.get("HP33A", "dest_IP")
PORT = config.get("HP33A", "dest_port")

time.sleep(10) ## Allow 10 seconds for NmeaCommunicator to be active

nmeaconfig='?WATCH={"enable":true,"json":false,"nmea":true,"raw":0,"scaled":false,"timing":false,"split24":false,"pps":false}'

async def tcp_client(message):
    reader, writer = await asyncio.open_connection(
        GPSDHOST, GPSDPORT)
    reader2, writer2 = await asyncio.open_connection(
        HOST, PORT)

    print(f'Send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

    #print(f'Send: {message!r}')
    #writer2.write(message.encode())
    #await writer2.drain()

    while True:
        data = await reader.readline()
        print(f'Received: {data.decode()!r}')
        writer2.write(data)
        await writer2.drain()
        if data is b'':
            print("I die now")
            quit()
            
    print('Close the connection')
    writer.close()
    await writer.wait_closed()

asyncio.run(tcp_client(nmeaconfig))
