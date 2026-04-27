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

def sendfiledata(client, filepath, filesize, progress_callback=None):
    sent=0
    with open(filepath, "rb") as f:
        while True:
            data= f.read(BUFFERSIZE)
            if not data:
                break
            client.send(data)
            sent += len(data)

            progress= int((sent/filesize)*100)
            print(f"[UPLOAD] {filepath}: {progress:.2f}%")

            if progress_callback:
                progress_callback(filepath, progress)
    print("[DONE] {file_path} uploaded\n")

def uploadfile(filelist, progress_callback= None):
    client=createclient()
    sendnumoffiles(client, filelist)
    for filepath in filelist:
        filename, filesize = sendfileinfo(client, filepath)
        sendfiledata(client, filepath, filesize)
    client.close()

def upload_files_from_list(file_paths):
    print("[DEBUG] Sending files:", file_paths)
    uploadfile(file_paths)

if __name__ == "__main__":
    files = input("Enter file path sepearted by comma: ").split(",")
    files = [f.strip() for f in files]

    uploadfile(files)