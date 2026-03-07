from flask import Flask, render_template, request, jsonify
import subprocess
import json
import base64
import requests
import datetime
import sys
import os

app = Flask(__name__)

# ---------------- GitHub Configuration ----------------

GITHUB_TOKEN = "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"
REPO = "Orcos-nom/Heartbeat_project"
BRANCH = "main"

# ---------------- OpenRouter Chatbot ----------------

OPENROUTER_API_KEY = "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"

# ---------------- Model Script Paths ----------------

HEART_MODEL_SCRIPT = r"D:\hackathon\smartstetho_ML\src\predict.py"
LUNG_MODEL_SCRIPT = r"D:\hackathon\smartstetho_lung\predict_lung_disease.py"


# ---------------- Upload Audio to GitHub ----------------

def upload_to_github(file, prefix):

    print("\nUploading audio to GitHub...")

    try:
        file.seek(0)

        content = base64.b64encode(file.read()).decode()

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"{prefix}_{timestamp}.wav"

        path = f"recordings/{filename}"

        url = f"https://api.github.com/repos/{REPO}/contents/{path}"

        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }

        # check if file already exists to get SHA
        get_resp = requests.get(url, headers=headers)

        payload = {
            "message": f"upload {filename}",
            "content": content,
            "branch": BRANCH
        }

        if get_resp.status_code == 200:
            sha = get_resp.json()["sha"]
            payload["sha"] = sha

        response = requests.put(url, json=payload, headers=headers)

        print("GitHub status:", response.status_code)
        print("GitHub response:", response.text)

        if response.status_code in [200, 201]:
            print("Upload successful:", filename)
            return True

        return False

    except Exception as e:
        print("Upload error:", e)
        return False


# ---------------- Pages ----------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/heartbeat")
def heartbeat():
    return render_template("heartbeat.html")


@app.route("/lungsound")
def lungsound():
    return render_template("lungsound.html")


@app.route("/report")
def report():
    return render_template("report.html")


@app.route("/med_store")
def med_store():
    return render_template("med_store.html")


@app.route("/hospital")
def hospital():
    return render_template("hospital.html")


# ---------------- API STATUS ROUTE (NEW) ----------------

@app.route("/api_status")
def api_status():
    return jsonify({
        "status": "SmartStetho AI Server Running",
        "routes": [
            "/predict_heart",
            "/predict_lung",
            "/chat",
            "/upload_heartbeat",
            "/upload_lung"
        ]
    })


# ---------------- Upload Routes ----------------

@app.route("/upload_heartbeat", methods=["POST"])
def upload_heartbeat():

    print("Heartbeat audio received")

    file = request.files["file"]

    success = upload_to_github(file, "heartbeat")

    if success:
        return jsonify({"status": "uploaded"})
    else:
        return jsonify({"status": "error"})


@app.route("/upload_lung", methods=["POST"])
def upload_lung():

    print("Lung audio received")

    file = request.files["file"]

    success = upload_to_github(file, "lung")

    if success:
        return jsonify({"status": "uploaded"})
    else:
        return jsonify({"status": "error"})


# ---------------- Run AI Model ----------------

def run_prediction(script_path):

    print("\n==============================")
    print("Running AI Model:", script_path)
    print("==============================")

    try:

        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(script_path)
        )

        stdout = result.stdout
        stderr = result.stderr

        if stderr:
            print("Model error:")
            print(stderr)

        print("Model output:")
        print(stdout)

        # TensorFlow prints warnings before JSON
        lines = stdout.strip().split("\n")

        for line in reversed(lines):
            try:
                return json.loads(line)
            except:
                continue

        return {"error": "Prediction JSON not found"}

    except Exception as e:
        return {"error": str(e)}


# ---------------- Prediction Routes ----------------

@app.route("/predict_heart")
def predict_heart():

    result = run_prediction(HEART_MODEL_SCRIPT)

    return jsonify(result)


@app.route("/predict_lung")
def predict_lung():

    result = run_prediction(LUNG_MODEL_SCRIPT)

    return jsonify(result)


# ---------------- Chatbot Route ----------------

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get("message")

    response = requests.post(

        "https://openrouter.ai/api/v1/chat/completions",

        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },

        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful medical assistant."},
                {"role": "user", "content": user_message}
            ]
        }

    )

    data = response.json()

    reply = data["choices"][0]["message"]["content"]

    return jsonify({"reply": reply})


# ---------------- Start Server ----------------

if __name__ == "__main__":

    print("\n================================")
    print(" SmartStetho AI Server Started ")
    print("================================\n")

    print("Main App URL:")
    print("http://127.0.0.1:5000")

    print("\nAPI Status URL:")
    print("http://127.0.0.1:5000/api_status\n")

    app.run(host="0.0.0.0", port=5000, debug=True)