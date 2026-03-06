import os
from flask import Flask, render_template, request

app = Flask(__name__)

UPLOAD_FOLDER = "recordings"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():

    audio = request.files['audio_data']

    filepath = os.path.join(UPLOAD_FOLDER, "recorded.wav")

    audio.save(filepath)

    print("Audio saved:", filepath)

    return "saved"

if __name__ == "__main__":
    app.run(debug=True)