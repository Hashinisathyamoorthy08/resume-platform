from flask import Flask, render_template, request, jsonify, send_from_directory
from modules.analyzer import analyze_resume
from modules.builder  import build_resume
from modules.matcher  import match_resume
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ── Pages ─────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyzer")
def analyzer():
    return render_template("analyzer.html")

@app.route("/builder")
def builder():
    return render_template("builder.html")

@app.route("/matcher")
def matcher():
    return render_template("matcher.html")

# ── API Routes ────────────────────────────────────────────────

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("resume")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)
    result = analyze_resume(path)
    return jsonify(result)

@app.route("/build", methods=["POST"])
def build():
    data     = request.get_json()
    filename = build_resume(data, OUTPUT_FOLDER)
    return jsonify({"file": filename})

@app.route("/match", methods=["POST"])
def match():
    file     = request.files.get("resume")
    job_desc = request.form.get("job_desc", "")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)
    result = match_resume(path, job_desc)
    return jsonify(result)

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

# ── Run ───────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)