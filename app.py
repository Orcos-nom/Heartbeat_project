import os
import base64
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Read token from environment variable
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# Repository information
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
    audio_bytes = audio_file.read()

    # Generate unique filename
    filename = "audio_files/recording_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".webm"

    # Convert audio to base64
    encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")

    url = f"https://api.github.com/repos/{REPO}/contents/{filename}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "message": "Upload audio recording",
        "content": encoded_audio,
        "branch": BRANCH
    }

    try:
        response = requests.put(url, json=data, headers=headers)

        print("GitHub Status:", response.status_code)
        print("GitHub Response:", response.text)

        if response.status_code in [200, 201]:
            return jsonify({
                "status": "success",
                "file": filename
            })
        else:
            return jsonify({
                "status": "error",
                "details": response.text
            })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)