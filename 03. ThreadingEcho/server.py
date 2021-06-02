#!/usr/bin/python3
import socket
import sys, getopt
from threading import Thread

# threading version for simlpleEcho server.
# in simpleEcho, if there are two connection to server, client A and B.
# our server, will serves whoever come first (let say A).
# it will handle anything from B only after A finished and terminate the connection.
# by using threading, we create worker thread that can handle any client, so other client don't have to wait.

USAGE= f"Usage: {sys.argv[0]} -p <port> -a <host>"

def main():
    HOST,PORT = parseOpts(sys.argv[1:])
    print("starting server...")
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        sock.bind((HOST,PORT))
        sock.listen()
        print(f"Server listening on {HOST}:{PORT} ...")

    except OSError as error:
        print(f"Error: {error.strerror}")
        sys.exit()

    while True:
            print("Waiting for connection....")
            conn,addr = sock.accept()
            t = Thread(target=thread_handler,args=(conn,addr))
            tname = t.getName()
            print(f"Created: {tname}")
            t.start()
            t.join()
            print(f"{addr} disconnected..")

def thread_handler(conn,addr):
    try:
        print(f"{addr}, connected..")
        while True:
            data = conn.recv(1024)
            if not data : break
            print(f"{addr} say: {data.decode()}")
            #echo back
            conn.send(data)
    finally:
        conn.close()

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
    except ValueError:
        raise SystemExit(USAGE)
    except getopt.GetoptError:
        raise SystemExit(USAGE)
    except IndexError:
        raise SystemExit(USAGE)