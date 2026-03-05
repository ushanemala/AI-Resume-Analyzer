from flask import Flask, render_template, request
import os
from analyzer import analyze_resume
app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}
def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/upload")
def upload():
    return render_template("upload.html")
@app.route("/result", methods=["POST"])
def result():
    role = request.form["role"]
    resume_file = request.files["resume"]
    if resume_file and allowed_file(resume_file.filename):
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], resume_file.filename)
        resume_file.save(filepath)
        score, matched, missing, experience_found, suggestions = analyze_resume(filepath, role)
        return render_template(
            "result.html",
            role=role,
            score=score,
            matched=matched,
            missing=missing,
            experience_found=experience_found,
            suggestions=suggestions
        )
    return "Invalid file type. Please upload PDF or Image."
if __name__ == "__main__":
    app.run(debug=True)