#!/usr/bin/python3
import socket
import sys, getopt , os
from multiprocessing import Process

# our multiprocess server is just like threading server.
# the diff is in multiprocess our worker spawn as new process in the OS, 
# instead of a lightweight  child threads spawn from our main program process.
# it's mean our worker is a new process with their own sperate threads
# it can take advantage of CPU hardware parallelism.
# the downside is, Process take more work for OS to set up.
# our code basically look almost the same as our threading example.
# the diff is we call Process class instead of Thread

USAGE= f"Usage: {sys.argv[0]} -p <port> -a <host>"

def main():
    HOST,PORT = parseOpts(sys.argv[1:])
    print(f"main_pid:{os.getpid()}")
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
            p = Process(target=process_handler,args=(conn,addr))
            p.start()
            #if we write something here like print("disconnected")
            # disconnected will printed out even if the process worker not finish executing yet
            # unlike threads, where, after a thread finish, then disconnected will be print out

def process_handler(conn,addr):
    try:
        print(f"worker_pid:{os.getpid()}\nparent:{os.getppid()}")
        print(f"{addr}, connected..")
        while True:
            data = conn.recv(1024)
            if not data : break
            print(f"{addr} say: {data.decode()}")
            #echo back
            conn.send(data)
    finally:
        conn.close()
        print(f"{addr} disconnected..\n")
        

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