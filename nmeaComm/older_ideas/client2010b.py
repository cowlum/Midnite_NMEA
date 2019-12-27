import socket;

try:
    s = socket.socket();
    s.connect(('192.168.0.140',2010));
    while True:
        str = raw_input("S: ");
        s.send(str.encode());
        if(str == "Bye" or str == "bye"):
            break;
    s.close();
except KeyboardInterrupt:
    print "Closing Connection and freeing the port."
    s.close();
    sys.exit();
