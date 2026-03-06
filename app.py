from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "recordings"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/heartbeat")
def heartbeat():
    return render_template("heartbeat.html")

@app.route("/lungsound")
def lungsound():
    return render_template("lungsound.html")

@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["file"]
    type_folder = request.form["type"]

    filename = f"{type_folder}_{file.filename}"

    path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(path)

    return {"status":"saved"}

if __name__ == "__main__":
    app.run(debug=True)