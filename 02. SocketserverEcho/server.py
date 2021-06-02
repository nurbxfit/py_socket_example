#!/usr/bin/python3

import sys, getopt
import socketserver

#import threading

#simple example of Socketserver module.
#socketserver is a module that provide more easy way for developer to create a server
#it use the OOP approch. we just need to overide the classes provided by socketserver

USAGE= f"Usage: {sys.argv[0]} -p <port> -a <host>"

#this class will handle the TCP connection
class MySimpleTCPHandler(socketserver.BaseRequestHandler):
    #BaseRequestHandler is the base class provided by socketserver
    def __init__(self,request,client_address,server):
        print("inside constructor")

        super().__init__(request,client_address,server)

    def handle(self):
        #this handler will handle the TCP request
        print(f"client connected:{self.client_address}")
        data = self.request.recv(1024)
        print(f"client say: {data.decode()}")
        #echo back to client
        self.request.sendall(data)

#example for threading we pass socketserver.ThreadingMixIn
# class ThreadsServer(socketserver.ThreadingMixIn,socketserver.TCPServer):
#     pass

def main():
    # HOST = "127.0.0.1"
    # PORT = 4444

    HOST,PORT = parseOpts(sys.argv[1:])
    print("starting server..")

    # here we can use our ThreadsServer instead if we want threading,
    # server = ThreadsServer((HOST,PORT),MySimpleTCPHandler)
    server = socketserver.TCPServer((HOST,PORT),MySimpleTCPHandler)

    #then instead of serve_forever(), we pass our server.serve_forever() to threading 
    # t = threading.Thread(target=server.serve_forever)
    server.serve_forever()#server will run in infinite loop.



def parseOpts(argv):
    opts, rem = getopt.getopt(argv,"hp:a:",["port=","address="])
    HOST = None
    PORT = None

    for opt, value in opts:
        if opt in ("-h","--help"):
            print(USAGE)
            sys.exit()
        elif opt in ("-p","--port"):
            PORT = int(value)
        elif opt in ("-a","--address"):
            HOST = value
    
    if not opts or len(opts) > 3:
        raise SystemExit(USAGE)

    return HOST,PORT

if __name__ == "__main__":
    try:
        main()
    except OSError as error:
        print(f"Error:{error.strerror}")