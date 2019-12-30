import asyncio

writers = []

def forward(writer, addr, message):
    for w in writers:
        if w != writer:
            try:
                #w.write(f"{addr!r}: {message!r}\n".encode())
                w.write(message.encode())
            except:
                break
            #   w.close()

         #   print("closing")
          #  w.close()

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
#        except:
#            print("drain fail")
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
#            return
#        if message == "exit":
#            message = f"{addr!r} wants to close the connection."
#            print(message)
#            forward(writer, "Server", message)
#            break
    #print("marker two")
    #writers.remove(writer)
    #writer.close()

async def main():
    server = await asyncio.start_server(
        handle, '0.0.0.0', 2010)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    async with server:
        await server.serve_forever()

asyncio.run(main())