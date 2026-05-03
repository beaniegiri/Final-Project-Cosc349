This is the final project for COSC 349. The topic of this project is Multi FIle Upload System.
This project consists of a TCP Server + client that uploads files. It has three main folders as of now.
The Server, The Client, and The Storage
The server folder contains "server.py file which does the following:
Start server,
Accept client,
Receives files,
Save files.
The client folder contains "client.py" which does the following:
Connect to server,
Send file name,
send file size,
Send file data,
The storage folder does the following:
whenever a client uploads any files it the server accepts it and stores it in the storage folder.
To test the server.py : run "python server.py" in the terminal.
To test the client.py: run "python client.py" in the terminal.
"""Before uploading the files make sure the server is active by running the "python server.py".
when uploading multiple files upload it by using the following input way.ie(using commas after one filepath)
file1.txt, file2.jpg, file3.pdf.
when done the expected output looks like:
CLIENT SIDE
[UPLOAD] file1.txt: 45.23%
[UPLOAD] file1.txt: 100.00%
[DONE] file1.txt uploaded
...
SERVER SIDE
[INFO] Receiving 3 files
[INFO] Receiving file1.txt (1234 bytes)
[DONE] File saved...
