from flask import Flask, render_template, request, jsonify
import os
import subprocess
import json
import requests

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads", "audio")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ML_SCRIPT = os.path.abspath(
    os.path.join(BASE_DIR, "..", "smartstetho_ML", "src", "predict.py")
)

OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- HEARTBEAT PAGE ----------------

@app.route("/heartbeat")
def heartbeat():
    return render_template("heartbeat.html")


# ---------------- LUNG PAGE ----------------

@app.route("/lungsound")
def lungsound():
    return render_template("lungsound.html")


# ---------------- MEDIC STORE ----------------

@app.route("/medic_store")
def medic_store():
    return render_template("medic_store.html")


# ---------------- HOSPITAL ----------------

@app.route("/hospital")
def hospital():
    return render_template("hospital.html")


# ---------------- CHATBOT ----------------

@app.route("/chatbot", methods=["POST"])
def chatbot():

    message = request.json.get("message")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role":"system","content":"You are SmartStetho medical assistant."},
            {"role":"user","content":message}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    data = response.json()

    reply = data["choices"][0]["message"]["content"]

    return jsonify({"reply": reply})


# ---------------- HEARTBEAT ML ROUTE ----------------

@app.route("/upload_heartbeat", methods=["POST"])
def upload_heartbeat():

    try:

        audio = request.files["audio"]

        filepath = os.path.join(UPLOAD_FOLDER, "heartbeat.webm")

        audio.save(filepath)

        result = subprocess.check_output(["python", ML_SCRIPT])

        result = result.decode("utf-8")

        data = json.loads(result)

        return jsonify(data)

    except Exception as e:

        return jsonify({"error": str(e)})


# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)