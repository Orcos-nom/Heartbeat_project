from flask import Flask, render_template, request, jsonify
import subprocess
import json
import base64
import requests
import datetime

app = Flask(__name__)

# ---------------- GitHub Settings ----------------

GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"
REPO = "Orcos-nom/Heartbeat_project"
BRANCH = "main"

# ---------------- Model Script Paths ----------------

HEART_MODEL_SCRIPT = r"D:\hackathon\smartstetho_ML\src\predict.py"
LUNG_MODEL_SCRIPT = r"D:\hackathon\smartstetho_lung\predict_lung_disease.py"


# ---------------- Upload Audio to GitHub ----------------

def upload_to_github(file, prefix):

    print("\nUploading audio to GitHub...")

    content = base64.b64encode(file.read()).decode()

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{prefix}_{timestamp}.wav"

    path = f"recordings/{filename}"

    url = f"https://api.github.com/repos/{REPO}/contents/{path}"

    data = {
        "message": f"upload {filename}",
        "content": content,
        "branch": BRANCH
    }

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.put(url, json=data, headers=headers)

    if response.status_code == 201:
        print("Upload successful:", filename)
        return True
    else:
        print("Upload failed:", response.text)
        return False


# ---------------- Web Pages ----------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/heartbeat")
def heartbeat():
    return render_template("heartbeat.html")


@app.route("/lungsound")
def lungsound():
    return render_template("lungsound.html")


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


# ---------------- Run Prediction ----------------

def run_prediction(script_path):

    print("\n====================================")
    print("Starting AI Model:", script_path)
    print("====================================")

    try:

        process = subprocess.Popen(
            ["python", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        print("Model process started... waiting for output")

        stdout, stderr = process.communicate()

        print("\nModel finished running")

        if stderr:
            print("\nModel error output:")
            print(stderr)

        print("\nModel stdout:")
        print(stdout)

        lines = stdout.strip().split("\n")

        for line in reversed(lines):
            try:
                return json.loads(line)
            except:
                continue

        return {"error": "Prediction failed"}

    except Exception as e:
        print("Execution error:", e)
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


# ---------------- Start Server ----------------

if __name__ == "__main__":

    print("\n================================")
    print(" SmartStetho AI Server Started ")
    print("================================\n")

    app.run(debug=True)