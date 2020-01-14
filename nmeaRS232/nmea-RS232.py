## Very likely not working
## Just a template for what may run

import asyncio
import configparser
import time

## Allow 10 seconds for NmeaCommunicator, i2c to be active
time.sleep(10)

## Variables
config = configparser.ConfigParser()
config.read("/home/midnite/nmeaRS232.config")
RS232_enabled = config.get("RS232", "bmp280_enabled")
HOST = config.get("RS232", "dest_IP")
PORT = config.get("RS232", "dest_port")
seconds = int(config.get("RS232", "seconds"))
endline = "\n"


## Check for enabled
if RS232_enabled == 'no':
    exit()

## Open a connection to Nmea Communicator
## While True collect pressure and tempreture
## Send the nmea string compiled by pynmea2 and wait seconds.

## Connect to port

async def handle_echo(reader, writer):
    asyncio.start_server(handle_echo, HOST, PORT, loop=loop)
    while True:
            data = await reader.readline()
            message = data.decode()
            addr = writer.get_extra_info('peername')
            print("Received %r from %r" % (message, addr))

            print("Send: %r" % message)
            ## Send to Serial
            connection_made(self, transport):
      

class Output(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False
        #transport.write(b'hello world\n')

    def data_received(self, data):
        print('data received', repr(data))
        ## Send to TCP
        writer.write(data)
        self.transport.close()

    def connection_lost(self, exc):
        print('port closed')
        asyncio.get_event_loop().stop()

loop = asyncio.get_event_loop()
tasks = [
    serial.aio.create_serial_connection(loop, Output, '/dev/ttyUSB0', baudrate=115200),
    asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)]
loop.run_until_complete(tasks)
loop.run_forever()
loop.close()
