import asyncio
import configparser

## Variables
config = configparser.ConfigParser()
config.read("/boot/nmeacomm.config")
ncomm_enabled = config.get("nmeaCOMM", "ncomm_enalbed")
HOST = config.get("nmeaCOMM", "IP")
PORT = config.get("nmeaCOMM", "port")

## List for the attached devices.
writers = []

## Check for enabled
if ncomm_enabled == 'no':
    exit()

## Function for sending to all devices except the source
## Do we need/want an async and await w.wrote here
def forward(writer, addr, message):
    for w in writers:
        if w != writer:
            try:
                #w.write(f"{addr!r}: {message!r}\n".encode())
                w.write(message.encode())
            except:
                #print("Failure to send")
                break

## Function to append new devices to writers list
## Read anyline recieved from device to the data variable
## Send the data to the forwar function for sending
## If the data recieved is empty remove the writer.
async def handle(reader, writer):
    writers.append(writer)
    addr = writer.get_extra_info('peername')
    while True:
        data = await reader.readline()
        message = data.decode().strip()
        forward(writer, addr, message)
        await writer.drain()
        
        if data is b'':
            try:
                print(addr)
                writers.remove(writer)
                writer.close()
                break
                #writer.close()
            except:
                break

async def main():
    server = await asyncio.start_server(
        handle, HOST, PORT)
    addr = server.sockets[0].getsockname()
    #print(f'Serving on {addr}')
    async with server:
        await server.serve_forever()

asyncio.run(main())
