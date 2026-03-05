import pdfplumber
import pytesseract
from PIL import Image
from job_roles import job_roles
import os
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def analyze_resume(resume_path, role):
    text = ""
    file_extension = os.path.splitext(resume_path)[1].lower()
    if file_extension == ".pdf":
        with pdfplumber.open(resume_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
    elif file_extension in [".png", ".jpg", ".jpeg"]:
        image = Image.open(resume_path)
        text = pytesseract.image_to_string(image)
    text = text.lower()
    required_skills = job_roles.get(role, [])
    matched = []
    missing = []
    for skill in required_skills:
        if skill in text:
            matched.append(skill)
        else:
            missing.append(skill)
    score = (len(matched) / len(required_skills)) * 100 if required_skills else 0
    experience_keywords = ["experience", "internship", "worked", "company"]
    experience_found = any(word in text for word in experience_keywords)
    suggestions = []
    if missing:
        suggestions.append("Learn the missing skills for this role.")
    if not experience_found:
        suggestions.append("Add internship or project experience.")
    if "github" not in text:
        suggestions.append("Add your GitHub profile to showcase projects.")
    return round(score,2), matched, missing, experience_found, suggestions