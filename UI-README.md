# SYN/ACK TRANSFER v1.0
**COSC 349: Reliable Multi-File TCP Streaming System**

## Overview
SYN/ACK TRANSFER is a full-stack file transfer application that leverages the reliability of the **TCP Three-Way Handshake**. This project integrates a modern Flask web interface with a custom-built TCP socket server to ensure secure, ordered, and verified multi-file uploads.

## Features
- **Cyber-Monochrome Palette:** Utilizing a deep `#000` background with neon green (`#00ff00`) accents to mimic terminal style feedback.
- **UX Intent:** The UI intentionally hides complex socket logic behind a single, bold "INITIALIZE TCP STREAM" action to streamline the user experience.
- **Visual Feedback:**  CSS notification bars provide immediate binary state feedback (Success/Error) based on the server's SYN/ACK response.
- **Branded UI:** High contrast minimalist design.
- **TCP Handshake Integration:** Named after the SYN-SYN/ACK-ACK protocol to reflect its connection oriented reliability.
- **Multi-File Streaming:** Support for batch uploading text and binary files.
- **Dynamic Notifications:** Real time feedback for successful transfers and connection errors.
- **Auto-Cleanup:** Temporary files are wiped immediately after the TCP stream completes to maintain system integrity.

## How to Test (Step-by-Step)
To test the system without modifying the source code, follow these steps in order:

Fetch the New Branch

Bash
git fetch origin
2. 

Bash
git checkout ui-development
3. 


Bash
source .venv/bin/activate
pip install -r multifileupload/requirements.txt
4. 

Terminal 1 (The Server): python multifileupload/server/server.py
(This starts the listener for the SYN/ACK handshake).

Terminal 2 (The Flask UI): python app.py
(This starts the web dashboard at http://127.0.0.1:5002).

5.
Open the browser to the local link.

Upload any file

Click INITIALIZE TCP STREAM.

Check the multifileupload/storage folder to confirm the file arrived safely