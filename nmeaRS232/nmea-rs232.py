import aioserial
import asyncio
import configparser

config = configparser.ConfigParser()
config.read("/home/midnite/nmears232.config")
RS232_enabled = config.get("RS232", "RS232_enabled")
HOST = config.get("RS232", "dest_IP")
PORT = config.get("RS232", "dest_port")
SERIAL = config.get("RS232", "serial_device")
BAUD = config.get("RS232", "dest_baud")

if RS232_enabled == 'no':
    exit()

async def handle_echo():
    print("TCP start")
    global writer
    reader, writer = await asyncio.open_connection(
        HOST, PORT)
    while True:
          data = await reader.read(10000)
           #message = data.decode().strip()
          # print(data)
          await send_serial(data)
          await asyncio.sleep(0)


#async def read_and_print(aioserial_instance: aioserial.AioSerial):
async def read_and_print():
    global aioserial_instance
    aioserial_instance = aioserial.AioSerial(port=SERIAL,baudrate=BAUD)
    print("Serial start")
    while True:
        serial = await aioserial_instance.readline_async()
        print(serial)
        await send_tcp(serial)
        await asyncio.sleep(0)

async def send_tcp(serial):
  try:
    writer.write(serial)
  except:
    print("no tcp writer")
    pass

async def send_serial(data):
  try:
     await aioserial_instance.writelines_async(data)
     #print(data)
  except:
    print("No Serial writer")
    pass

async def main():
    await asyncio.gather(handle_echo(),read_and_print())


asyncio.run(main())
