import asyncio
from asyncserial import Serial


message = "testing callum"

async def tcp_client(message, loop):
	
	while True:
		reader, writer = await asyncio.open_connection('192.168.0.140', 2010, loop=loop)

		print('Send: %r' % message)
		writer.write(message.encode())
		await asyncio.sleep(100)
		#data = await reader.read(100)
		#print('Received: %r' % data.decode())

		#print('Close the socket')
		#writer.close()


async def serial_in():
	await serial.read() # Drop anything that was already received
	while True:
		#print("mark one")
		line = await serial.readline() # Read a line
		#print("mark two")
		print(line)
		await asyncio.sleep(0) # Let's be a bit greedy, should be adjust to your needs

loop = asyncio.get_event_loop()
serial = Serial(loop, "/dev/ais", baudrate=34800)

#loop.create_task(connect('first hello', 15))
#asyncio.ensure_future(test())
loop.create_task((tcp_client(message, loop)))
loop.create_task(serial_in())

loop.run_forever()
loop.close()
