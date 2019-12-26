import asyncio
from asyncserial import Serial


async def tcp_client(line, loop):
	reader, writer = await asyncio.open_connection('192.168.0.140', 2010, loop=loop)

async def tcp_send(line)
	#while True:
		print('Send: %r' % line)
		writer.write(line.encode())
		await writer.drain()
		await asyncio.sleep(0)
		#data = await reader.read(100)
		#print('Received: %r' % data.decode())

		#print('Close the socket')
		#writer.close()


async def serial_in():\
	global line
	await serial.read() # Drop anything that was already received
	while True:
		#try to send and except run tcp_client again.
		line = await serial.readline() # Read a line
		print(line)
		tcp_send(line)
		await asyncio.sleep(0) # Let's be a bit greedy, should be adjust to your needs

loop = asyncio.get_event_loop()
serial = Serial(loop, "/dev/ais", baudrate=34800)
line = ""

#loop.create_task(connect('first hello', 15))
#asyncio.ensure_future(test())
loop.create_task((tcp_client(line, loop)))
loop.create_task(serial_in())

loop.run_forever()
loop.close()
