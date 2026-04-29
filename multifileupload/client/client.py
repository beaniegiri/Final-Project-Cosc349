import socket
import os

SERVERIP= "127.0.0.1"
PORT=5001
BUFFERSIZE= 1024

#creating client socket fun
def createclient():
    client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVERIP, PORT))
    print("[CLIENT] Connected to server")
    return client

def sendnumoffiles(client, filelist):
    client.send(str(len(filelist)).encode())
    client.recv(BUFFERSIZE)


def sendfileinfo(client, filepath):
    filename= os.path.basename(filepath)
    filesize=os.path.getsize(filepath)

    client.send(filename.encode())
    client.recv(BUFFERSIZE)

    client.send(str(filesize).encode())
    client.recv(BUFFERSIZE)

    return filename, filesize

def sendfiledata(client, filepath, filesize):
    sent=0
    with open(filepath, "rb") as f:
        while True:
            data= f.read(BUFFERSIZE)
            if not data:
                break
            client.send(data)
            sent += len(data)

            progress= (sent/filesize)*100
            print(f"[UPLOAD] {filepath}: {progress:.2f}%")
    print(f"[DONE] {filepath} uploaded\n")


def list_files(client):
    client.send(b"LIST")
    files = client.recv(BUFFERSIZE).decode()
    print("\n[SERVER FILES]")
    print(files)


def download_file(client, filename):
    client.send(f"DOWNLOAD {filename}".encode())

    response = client.recv(BUFFERSIZE).decode()
    if response == "NOT_FOUND":
        print("[ERROR] File not found on server")
        return

    filesize = int(response)
    client.send(b"OK")

    filepath = f"downloaded_{filename}"
    received = 0

    with open(filepath, "wb") as f:
        while received < filesize:
            data = client.recv(BUFFERSIZE)
            if not data:
                break
            f.write(data)
            received += len(data)

            progress = (received / filesize) * 100
            print(f"[DOWNLOAD] {filename}: {progress:.2f}%")

    print(f"[DONE] {filename} downloaded\n")


def uploadfile(filelist):
    client=createclient()
    sendnumoffiles(client, filelist)
    for filepath in filelist:
        filename, filesize = sendfileinfo(client, filepath)
        sendfiledata(client, filepath, filesize)
    client.close()


if __name__ == "__main__":
    while True:
        print("\n1. Upload files")
        print("2. List server files") 
        print("3. Download file")
        print("4. Exit")
        
        choice = input("Choose option: ")
        
        if choice == "1":
            files = input("Enter file paths separated by comma: ").split(",")
            files = [f.strip() for f in files]
            uploadfile(files)
        elif choice == "2":
            client = createclient()
            list_files(client)
            client.close()
        elif choice == "3":
            filename = input("Enter filename to download: ")
            client = createclient()
            download_file(client, filename)
            client.close()
        elif choice == "4":
            break