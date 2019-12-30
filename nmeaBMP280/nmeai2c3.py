import asyncio


async def tcp_echo_client(message):
    #reader, writer = await asyncio.open_connection(
    #    '127.0.0.1', 2000)
    reader2, writer2 = await asyncio.open_connection(
        '192.168.0.140', 2010)

    #print(f'Send: {message!r}')
    #writer.write(message.encode())
    #await writer.drain()

    #print(f'Send: {message!r}')
    #writer2.write(message.encode())
    #await writer2.drain()

    while True:
        data = "I,XDR,X,22,C,TempSensor1"
        endline = '\n'
        #print(f'Received: {data.decode()!r}')
        data = data.encode() + endline.encode()
        writer2.write(data)
        await writer2.drain()
        await asyncio.sleep(1)


    print('Close the connection')
    writer.close()
    await writer.wait_closed()

asyncio.run(tcp_echo_client('connecting'))
