from flask import Flask, render_template, request, redirect
import os
import sys

# allow import from client folder
sys.path.append("../client")
from client import upload_files_from_list

app = Flask(__name__)

UPLOAD_FOLDER = "temp_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------------
def save_uploaded_files(files):
    paths = []
    for file in files:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        paths.append(filepath)
    return paths

# -----------------------------
def get_uploaded_files():
    storage_path = "../storage"
    if not os.path.exists(storage_path):
        return []
    return os.listdir(storage_path)

# -----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        files = request.files.getlist("files")

        paths = save_uploaded_files(files)

        # send via socket
        upload_files_from_list(paths)

        return redirect("/")

    uploaded_files = get_uploaded_files()
    return render_template("index.html", files=uploaded_files)

# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)