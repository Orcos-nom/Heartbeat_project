from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "recordings"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    audio = request.files['audio_data']
    filepath = os.path.join(UPLOAD_FOLDER, "recorded_audio.wav")
    audio.save(filepath)
    return "Audio saved successfully"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)