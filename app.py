import os
import base64
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from pydub import AudioSegment
from io import BytesIO

app = Flask(__name__)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO = "Orcos-nom/Heartbeat_project"
BRANCH = "main"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "audio_data" not in request.files:
        return jsonify({"error": "No audio received"}), 400

    audio_file = request.files["audio_data"]

    # Read audio bytes
    audio_bytes = audio_file.read()

    try:
        # Convert webm to wav
        audio = AudioSegment.from_file(BytesIO(audio_bytes), format="webm")

        wav_buffer = BytesIO()
        audio.export(wav_buffer, format="wav")
        wav_buffer.seek(0)

        wav_bytes = wav_buffer.read()

    except Exception as e:
        return jsonify({"error": f"Conversion failed: {str(e)}"})

    filename = "audio_files/recording_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".wav"

    encoded_audio = base64.b64encode(wav_bytes).decode("utf-8")

    url = f"https://api.github.com/repos/{REPO}/contents/{filename}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "message": "Upload WAV audio recording",
        "content": encoded_audio,
        "branch": BRANCH
    }

    response = requests.put(url, json=data, headers=headers)

    print("GitHub Status:", response.status_code)
    print("GitHub Response:", response.text)

    if response.status_code in [200, 201]:
        return jsonify({"status": "saved", "file": filename})
    else:
        return jsonify({"error": response.text})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)