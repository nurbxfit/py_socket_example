#!/usr/bin/python3

import socket
import sys , getopt
from signal import signal, SIGINT

#python3 version

# sys.argv will yield array of arguments
# the first argument is our program name/filename [index=0].
# second argument is the first argument we pass to our script.

HOST = '127.0.0.1' #localhost by default
PORT = 4444
USAGE= f"Usage: {sys.argv[0]} -p <port> -a <host>"
sock = None

# opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
# args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

def runServer(PORT,HOST):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create ipv4 tcp socket
    try:
        sock.bind((HOST,int(PORT)))
        sock.listen(1) 
        print(f"Server listening on {HOST}:{PORT} ...")
    except OSError as error:
        print(f"Error: {error.strerror}")
        sys.exit()

    #putting while here, prevent server to die after one connection closed.
    #it can continue listening for another connection
    while True:
        print("Waiting for connection...")
        conn,addr = sock.accept()
        try:
            if addr or conn:
                print(f"{addr}, connected..")

                while True:
                    data = conn.recv(1024)
                    if not data: break
                    # if data.decode() == "bye": break
                    print(f"{addr} say: {data.decode()}")
                    # echo back to client
                    conn.send(data) #echo back what we get
                
        finally:        
            conn.close() #close connection

def handler(signal_received,frame):
    #handle ctrl+c
    print(f' SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

def parseOpts(argv):
    opts, values = getopt.getopt(argv,"hp:a:",["port=","address="])
    # print(opts)
    # print (values)
    
    for opt ,value in opts:
        if opt in ("-h","--help"):
            print(USAGE)
            sys.exit()
        elif opt in ("-p","--port"):
            # print(f"Port: {value}")
            global PORT
            PORT = int(value)
        elif opt in ("-a","--address"):
            # print(f"host: {value}")
            global HOST 
            HOST = value
    if not opts or len(opts) > 3:
        raise SystemExit(USAGE)

if __name__ == "__main__":
    try:
        signal(SIGINT,handler)
        parseOpts(sys.argv[1:])
        runServer(PORT,HOST)   

    except ValueError:
        raise SystemExit(USAGE)
    except getopt.GetoptError:
        raise SystemExit(USAGE)
    except IndexError:
        raise SystemExit(USAGE)


