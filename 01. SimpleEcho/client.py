#!/usr/bin/python3

import socket
import getopt, sys

HOST = '127.0.0.1'
PORT = 4444
USAGE= f"Usage: {sys.argv[0]} -p <port> -a <host> -m <message>"
MSG = None
# sock.connect((HOST,PORT))

# sock.send('Hello, World'.encode())
# data = sock.recv(1024)

# print(f"received: {data.decode()}")
# sock.close()

def main():
    print("Starting Client..")
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print(f"Connecting to {HOST}...")
    sock.connect((HOST,PORT))
    try:
        print("Connected to server")
        msg = getMsg()
        sock.send(msg.encode())
        recmsg = sock.recv(1024).decode()
        print(f"server say: {recmsg}")
    finally:
        print("Closing connection..")
        sock.close()

def getMsg():
    if not MSG:
        #if user not specify msg as args, we receive from console
        return str(input("client say=> "))
    else:
        return MSG


def parseOpts(argv):
    opts,args = getopt.getopt(
        argv,
        "hp:a:m:",
        ["port=","address=","message="]
    )

    for opt, value in opts:
        if opt in ("-h","--help"):
            print(USAGE)
            sys.exit()
        elif opt in ("-p","--port"):
            global PORT
            PORT = int(value)
        elif opt in ("-a","--address"):
            global HOST
            HOST = value
        elif opt in ("-m","--message"):
            # print(f"M:{value}")
            global MSG
            MSG = value
    if not opts or len(opts) > 4:
        raise SystemExit(USAGE)


if __name__ == '__main__':
    try:
        parseOpts(sys.argv[1:])
        main()
    except ConnectionRefusedError as err:
        print(f"Error with server: {err.strerror}")
        exit()
    