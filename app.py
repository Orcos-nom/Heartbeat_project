import os
import base64
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify

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
        return "No audio"

    audio = request.files["audio_data"].read()

    filename = "audio_files/recording_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".webm"

    encoded = base64.b64encode(audio).decode()

    url = f"https://api.github.com/repos/{REPO}/contents/{filename}"

    data = {
        "message": "upload audio",
        "content": encoded,
        "branch": BRANCH
    }

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}"
    }

    response = requests.put(url, json=data, headers=headers)

    if response.status_code == 201:
        return jsonify({"status":"saved","file":filename})
    else:
        return jsonify({"error":response.text})


if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)