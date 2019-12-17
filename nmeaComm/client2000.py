import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.0.140', 2000))
s.sendall('Hello, world')
data = s.recv(1024)
s.close()
print 'Received', repr(data)
