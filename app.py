import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

UPLOAD_FOLDER = "recordings"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_audio():
    if "audio_data" not in request.files:
        return jsonify({"status": "error", "message": "No audio received"}), 400

    audio = request.files["audio_data"]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recording_{timestamp}.wav"

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    audio.save(filepath)

    print("Saved:", filepath)

    return jsonify({
        "status": "success",
        "file": filename
    })


@app.route("/recordings/<filename>")
def get_recording(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)