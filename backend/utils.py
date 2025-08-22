import os
import uuid
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from models import Paper

ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}

# 1. File upload helper
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_file_path(filename, upload_folder="uploads"):
    ext = filename.rsplit('.', 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join(upload_folder, unique_name)

def save_file(file, upload_folder="uploads"):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = generate_file_path(filename, upload_folder)
        os.makedirs(upload_folder, exist_ok=True)
        file.save(file_path)
        return file_path
    else:
        raise ValueError("Invalid file type. Only PDF, DOC, DOCX allowed.")

# 2. Authentication helpers
def hash_password(password):
    return generate_password_hash(password)

def verify_password(hashed_password, input_password):
    return check_password_hash(hashed_password, input_password)

# 3. Utility functions for papers
def get_user_papers(user_id):
    return Paper.query.filter_by(author_id=user_id).all()

# 4. Optional helpers
def send_email_notification(to_email, subject, message):
    # Dummy function for now
    print(f"Sending email to {to_email}: {subject}\n{message}")

def simulate_plagiarism_check(file_path):
    # Dummy logic: randomly return a score between 0.1 and 0.99
    import random
    return round(random.uniform(0.1, 0.99), 2)

def simulate_ai_analysis(file_path):
    # Dummy logic: randomly return a score between 0.1 and 0.99
    import random
    return round(random.uniform(0.1, 0.99), 2)

# 5. Combined analysis helper
def analyze_paper(file_path):
    plagiarism_score = simulate_plagiarism_check(file_path)
    ai_score = simulate_ai_analysis(file_path)
    return {
        "plagiarism_score": plagiarism_score,
        "ai_analysis_score": ai_score,
        "status": "Passed" if plagiarism_score < 0.7 else "Review Required"
    }
