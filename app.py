from flask import Flask, render_template, request, jsonify
import os
import subprocess
import json
import requests

app = Flask(__name__)

# ---------------- CONFIG ----------------

OPENROUTER_API_KEY = "YOUR_OPENROUTER_API_KEY"

UPLOAD_FOLDER = "uploads/audio"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- HOME PAGE ----------------

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


# ---------------- HOSPITAL PAGE ----------------

@app.route("/hospital")
def hospital():
    return render_template("hospital.html")


# ---------------- CHATBOT ----------------

@app.route("/chatbot", methods=["POST"])
def chatbot():

    user_message = request.json.get("message")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are SmartStetho medical assistant helping users with heart and lung health."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    data = response.json()

    reply = data["choices"][0]["message"]["content"]

    return jsonify({"reply": reply})


# ---------------- AUDIO UPLOAD ----------------

@app.route("/upload_heartbeat", methods=["POST"])
def upload_heartbeat():

    if "audio" not in request.files:
        return jsonify({"error": "No audio file"}), 400

    audio = request.files["audio"]

    filepath = os.path.join(UPLOAD_FOLDER, "recorded.wav")

    audio.save(filepath)

    ml_path = os.path.abspath(filepath)

    try:

        result = subprocess.check_output([
            "python",
            "SMARTSTETHO_ML/src/predict.py",
            ml_path
        ])

        result = result.decode("utf-8")

        data = json.loads(result)

        return jsonify(data)

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


# ---------------- RESULT PAGE ----------------

@app.route("/result")
def result():
    return render_template("result.html")


# ---------------- RUN SERVER ----------------

if __name__ == "__main__":
    app.run(debug=True)