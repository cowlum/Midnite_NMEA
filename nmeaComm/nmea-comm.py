import asyncio
import configparser

## Variables

config = ConfigParser.ConfigParser()
config.read("/boot/nmeacomm.config")
hp33a_enalbed = config.get("nmeaCOMM", "ncomm_enalbed")
HOST = config.get("nmeaCOMM", "IP")
PORT = config.get("nmeaCOMM", "port")

## List for the attached devices.
writers = []

## Check for enabled

if ncomm_enalbed == 'yes':
    break
else:
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
                print("Failure to send")
                break

## Function to append new devices to writers list
## Read anyline recieved from device to the data variable
## Send the data to the forwar function for sending
## If the data recieved is empty remove the writer.
async def handle(reader, writer):
    writers.append(writer)
    addr = writer.get_extra_info('peername')
    message = f"{addr!r} is connected !!!!"
    print(message)
    #forward(writer, addr, message)
    while True:
        data = await reader.readline()
        print(data)
        message = data.decode().strip()
        forward(writer, addr, message)
        await writer.drain()
        
        if data is b'':
            try:
                #print("removing writer")
                print(addr)
                writers.remove(writer)
                writer.close()
                break
                #writer.close()
            except:
                print("data b exceptoin")


async def main():
    server = await asyncio.start_server(
        handle, IP, port)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    async with server:
        await server.serve_forever()

asyncio.run(main())
