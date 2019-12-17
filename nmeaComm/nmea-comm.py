# NMEA cCommunicator
# Accepts multpile connections on listening port 2010.
# Receives sentences (strings) on from 2010 to queue
# Sends items from queue to conencted devices on port 2000


######################################## FURUTE TO DO ####################################################
# 
# Send out signalk json on a seperate port
# close any existing connections on port on system start
####################################### ENV SETTINGS ###################################################

import socket
import sys
import threading
import time
import pynmea2
from queue import Queue

NUMBER_OF_THREADS = 4
JOB_NUMBER = [1, 2, 3, 4]
queue = Queue()
dataqueue = Queue()
in_connections = []
in_address = []
host='0.0.0.0'
inport=2010
out_connections = []
out_address = []
outport=2000



################################### TCP HANDLING ##########################################
# In connections

def create_in_socket():
    try:
        global inhost
        global inport
        global ins
        inhost = ""
        inport = 2010
        ins = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_in_socket():
    try:
        global inhost
        global inport
        global ins
        print("Binding the in Port: " + str(inport))

        ins.bind((inhost, inport))
        ins.listen(5)

    except socket.error as msg:
        print("In Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()

# Handling connection from multiple clients and saving to a list

def accepting_in_connections():
    global inconn
    global inaddress
    for c in in_connections:
        c.close()

    del in_connections[:]
    del in_address[:]

    while True:
        try:
            inconn, inaddress = ins.accept()
            ins.setblocking(1)  # prevents timeout

            in_connections.append(inconn)
            in_address.append(inaddress)

            print("In Connection has been established :" + inaddress[0])

        except:
            print("Error accepting In connections")

###




def create_out_socket():
    try:
        global outhost
        global outport
        global outs
        outhost = ""
        outport = 2000
        outs = socket.socket()

    except socket.error as msg:
        print("Out Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_out_socket():
    try:
        global outhost
        global outport
        global outs
        print("Binding the Out Port: " + str(outport))

        outs.bind((outhost, outport))
        outs.listen(5)

    except socket.error as msg:
        print("Out Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()

# Handling connection from multiple clients and saving to a list

def accepting_out_connections():
    global outconn
    global outaddress
    for c in out_connections:
        c.close()

    del out_connections[:]
    del out_address[:]

    while True:
        try:
            outconn, outaddress = outs.accept()
            outs.setblocking(1)  # prevents timeout

            out_connections.append(outconn)
            out_address.append(outaddress)

            print("Out Connection has been established :" + outaddress[0])

        except:
            print("Error accepting out connections")






def nmea_send():
    while True:
        time.sleep(0.5)
        for i in out_connections:
            try:
                # Make the variable conn equal to the connection from the list all_connections we are curretly itterating through
                outconn = i
                for j in dataqueue:
                    try:
                        # For each instance (j) in nmea_sentence_list move it to variable j which is then supplied to conn.send. 
                        # turned to string and encoded.
                        # can we remove msj=j and just put j into the lin below? likely
                        msg2 = j
                        conn.send(str.encode(msg2))
                    except:
                        print("failure to conn.send msg2")
                        # Remove the conn that failed conn.send from all_connections, close that connection and end the loop
                        all_connections.remove(conn)
                        conn.close()
                        break
            except:
                Print("Error with msg2 = j")

################################## THREAD CONTROLL ##########################################

# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:  ## Create Listner (2010) Connections and Sender (2000) connections
            # create_listner()
            create_in_socket()
            bind_in_socket()
            accepting_in_connections()


        if x == 2:  ## For Listners add to queue
            create_out_socket()
            bind_out_socket()
            accepting_out_connections()
      #      nmea_sentence_list_append()
      #      meas_list_refresh()

       # if x == 3:  ## Send Queue data to connections in list
       #     nmea_send()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


create_workers()
create_jobs()