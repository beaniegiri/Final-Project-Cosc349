from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

STORAGE_PATH = "../storage/"

@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "No files provided"}), 400

    os.makedirs(STORAGE_PATH, exist_ok=True)

    uploaded = []
    for file in files:
        if file.filename == "":
            continue
        filepath = os.path.join(STORAGE_PATH, file.filename)
        file.save(filepath)
        uploaded.append(file.filename)

    return jsonify({"uploaded": uploaded, "count": len(uploaded)})

@app.route("/files", methods=["GET"])
def list_files():
    os.makedirs(STORAGE_PATH, exist_ok=True)
    files = os.listdir(STORAGE_PATH)
    return jsonify({"files": files})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
