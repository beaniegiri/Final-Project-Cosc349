import socket
import os

HOST= '0.0.0.0'
PORT= 5001
BUFFERSIZE= 1024
STORAGEPATH= "../storage/"

# creating server socket fun
def createserver():
    server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[SERVER] Listening on {HOST}: {PORT}")
    return server

def acceptclient(server):
    conn, addr= server.accept()
    print(f"[CONNECTED] {addr}")
    return conn

def receivefileinfo(conn): 
    filename= conn.recv(BUFFERSIZE).decode()
    conn.send("OK".encode())

    filesize=int(conn.recv(BUFFERSIZE).decode())
    conn.send("OK".encode())

    print(f"[INFO] Receiving {filename} ({filesize} bytes)")
    return filename, filesize

def receivefiledata(conn, filename, filesize):
    os.makedirs(STORAGEPATH, exist_ok= True)
    filepath=os.path.join(STORAGEPATH, filename)

    received=0
    with open(filepath, "wb") as f:
        while received < filesize:
            data= conn.recv(BUFFERSIZE)
            if not data:
                break
            f.write(data)
            received+=len(data)
    print(f"[DONE] File saved: {filepath}")

def receivenumofiles(conn):
    numfiles= int(conn.recv(BUFFERSIZE).decode())
    conn.send("OK".encode())
    return numfiles

def handleclient(conn):
    try:
        
        numfiles=receivenumofiles(conn)
        print(f"[INFO] Receiving {numfiles} files")

        for _ in range(numfiles):
            filename, filesize= receivefileinfo(conn)
            receivefiledata(conn, filename, filesize)
    except Exception as e:
        print("ERROR", e)
    finally:
        conn.close()

#main server loop fun
def startserver():
    server=createserver()
    while True:
        conn= acceptclient(server)
        handleclient(conn)

if __name__ == "__main__":
    startserver()