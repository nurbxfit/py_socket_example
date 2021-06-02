#!/usr/bin/python3

import socket
import getopt, sys


USAGE= f"Usage: {sys.argv[0]} -p <port> -a <host> -m <message>"

def main():
    HOST,PORT,MSG = parseOpts(sys.argv[1:])
    print("Starting Client..")
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print(f"Connecting to {HOST}...")
    sock.connect((HOST,PORT))
    try:
        print("Connected to server")
        if not MSG:
            MSG = str(input("client say=> "))
        sock.send(MSG.encode())
        recmsg = sock.recv(1024).decode()
        print(f"server say: {recmsg}")
    finally:
        print("Closing connection..")
        sock.close()

def parseOpts(argv):
    opts,args = getopt.getopt(
        argv,
        "hp:a:m:",
        ["port=","address=","message="]
    )

    HOST = None
    PORT = None
    MSG  = None

    for opt, value in opts:
        if opt in ("-h","--help"):
            print(USAGE)
            sys.exit()
        elif opt in ("-p","--port"):
            PORT = int(value)
        elif opt in ("-a","--address"):
            HOST = value
        elif opt in ("-m","--message"):
            # print(f"M:{value}")
            MSG = value
    if not opts or len(opts) > 4:
        raise SystemExit(USAGE)

    return HOST,PORT,MSG


if __name__ == '__main__':
    try:
        main()
    except ConnectionRefusedError as err:
        print(f"Error with server: {err.strerror}")
        exit()
    