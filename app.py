import os
from flask import Flask, render_template, request
# We reach into the teammate's folder to get their upload logic
from multifileupload.client.client import uploadfile 

app = Flask(__name__)
UPLOAD_FOLDER = 'temp_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def handle_upload():
#     if 'file_list' not in request.files:
#         return "No files selected", 400
    
#     files = request.files.getlist('file_list')
#     saved_paths = []

#     for file in files:
#         if file.filename == '':
#             continue
#         # Save the file locally so the TCP client can find it
#         path = os.path.join(UPLOAD_FOLDER, file.filename)
#         file.save(path)
#         saved_paths.append(path)

#     if saved_paths:
#         # TRIGGER THE TCP STREAM!
#         try:
#             uploadfile(saved_paths)
#             return "<h1>SUCCESS: Files streamed over TCP!</h1><a href='/'>Go Back</a>"
#         except Exception as e:
#             return f"<h1>TCP Error: {e}</h1><a href='/'>Try Again</a>"
    
#     return "No files were processed", 400
@app.route('/upload', methods=['POST'])
def handle_upload():
    files = request.files.getlist('file_list')
    saved_paths = []

    for file in files:
        if file.filename:
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
            saved_paths.append(path)

    if saved_paths:
        try:
            uploadfile(saved_paths)
            # Cleanup: delete temp files after sending to TCP server
            for p in saved_paths:
                os.remove(p)
            return render_template('index.html', message="TRANSFER COMPLETE", status="success")
        except Exception as e:
            return render_template('index.html', message=f"ERROR: {e}", status="error")
    
    return render_template('index.html', message="NO FILES SELECTED", status="error")
if __name__ == '__main__':
    app.run(debug=True, port=5002)