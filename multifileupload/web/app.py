from flask import Flask, render_template, request, redirect, session, url_for
from flask import jsonify
import os
import sys
import threading

# allow import from client folder
sys.path.append("../client")
from client import uploadfile

app = Flask(__name__)
progress_data={"current_file": "",
               "progress" :0

}
app.secret_key = "secret123" 
USER = {
    "username": "admin",
    "password": "1234"
}

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

def update_progress(file, percent):
    global progress_data
    print("[DEBUG]", file, percent)
    progress_data["current_file"]=file
    progress_data['progress']=percent

# -----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect(url_for('login'))
    if request.method == "POST":
        files = request.files.getlist("files")

        paths = save_uploaded_files(files)
        # send via socket
        progress_data["progress"] = 0
        progress_data["current_file"] = ""

    # run upload in background
        thread = threading.Thread(
            target=uploadfile,
            args=(paths,),
            kwargs={"progress_callback": update_progress}
        )
        thread.start()

        return redirect("/")

    uploaded_files = get_uploaded_files()
    return render_template("index.html", files=uploaded_files)

@app.route("/progress")
def progress():
    return jsonify(progress_data)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USER["username"] and password == USER["password"]:
            session["user"] = username
            return redirect(url_for("index"))
        else:
            return "Invalid credentials"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)