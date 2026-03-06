import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

UPLOAD_FOLDER = "recordings"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_audio():
    if "audio_data" not in request.files:
        return jsonify({"status": "error", "message": "No audio file received"}), 400

    audio_file = request.files["audio_data"]

    if audio_file.filename == "":
        return jsonify({"status": "error", "message": "Empty filename"}), 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recording_{timestamp}.wav"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    audio_file.save(filepath)

    return jsonify({
        "status": "success",
        "message": "Audio saved",
        "file": filename
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # required for Render
    app.run(host="0.0.0.0", port=port)