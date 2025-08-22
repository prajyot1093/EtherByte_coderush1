from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import datetime
import random

# --- CONFIGURATION ---
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt", "tex"}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cmt.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret-key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = SQLAlchemy(app)
jwt = JWTManager(app)

# --- DATABASE MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ai_score = db.Column(db.Float)
    plagiarism_score = db.Column(db.Float)
    stylometric_score = db.Column(db.Float)
    ai_generated = db.Column(db.Boolean)
    plagiarism = db.Column(db.Boolean)
    stylometric_inconsistency = db.Column(db.Boolean)
    language = db.Column(db.String(32))
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    filename = db.Column(db.String(256))
    upload_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analysis.id'))

# --- HELPERS ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def simulate_analysis():
    ai_score = round(random.uniform(0.1, 0.99), 2)
    plagiarism_score = round(random.uniform(0.1, 0.99), 2)
    stylometric_score = round(random.uniform(0.1, 0.99), 2)
    return {
        "ai_score": ai_score,
        "plagiarism_score": plagiarism_score,
        "stylometric_score": stylometric_score,
        "ai_generated": ai_score > 0.7,
        "plagiarism": plagiarism_score > 0.6,
        "stylometric_inconsistency": stylometric_score > 0.65,
        "language": random.choice(["en", "hi", "fr", "de", "es"]),
        "details": "Simulated analysis. Replace with real AI/ML logic."
    }

# --- ROUTES ---
@app.route("/")
def root():
    return jsonify({"message": "CMT Flask API is running."})

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return {"msg": "Username and password required."}, 400
    if User.query.filter_by(username=username).first():
        return {"msg": "Username already exists."}, 400
    user = User(username=username, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return {"msg": "Registration successful."}, 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return {"msg": "Invalid credentials."}, 401
    access_token = create_access_token(identity=user.id)
    return {"access_token": access_token}

@app.route("/upload", methods=["POST"])
@jwt_required()
def upload_paper():
    if 'file' not in request.files:
        return {"msg": "No file part."}, 400
    file = request.files['file']
    if file.filename == '':
        return {"msg": "No selected file."}, 400
    if not allowed_file(file.filename):
        return {"msg": "File type not allowed."}, 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    analysis_data = simulate_analysis()
    analysis = Analysis(**analysis_data)
    db.session.add(analysis)
    db.session.commit()

    paper = Paper(user_id=get_jwt_identity(), filename=filename, analysis_id=analysis.id)
    db.session.add(paper)
    db.session.commit()

    return {"msg": "File uploaded and analyzed.", "paper_id": paper.id, "analysis": analysis_data}

@app.route("/analyze-text", methods=["POST"])
@jwt_required()
def analyze_text():
    data = request.json
    text = data.get("text")
    if not text:
        return {"msg": "No text provided."}, 400

    analysis_data = simulate_analysis()
    analysis = Analysis(**analysis_data)
    db.session.add(analysis)
    db.session.commit()

    paper = Paper(user_id=get_jwt_identity(), filename="(text submission)", analysis_id=analysis.id)
    db.session.add(paper)
    db.session.commit()

    return {"msg": "Text analyzed.", "paper_id": paper.id, "analysis": analysis_data}

@app.route("/stats", methods=["GET"])
@jwt_required()
def stats():
    total_papers = Paper.query.count()
    total_analyses = Analysis.query.count()
    avg_ai = db.session.query(db.func.avg(Analysis.ai_score)).scalar() or 0
    avg_plag = db.session.query(db.func.avg(Analysis.plagiarism_score)).scalar() or 0
    avg_style = db.session.query(db.func.avg(Analysis.stylometric_score)).scalar() or 0
    return {
        "papers_processed": total_papers,
        "analyses": total_analyses,
        "avg_ai_score": round(avg_ai, 2),
        "avg_plagiarism_score": round(avg_plag, 2),
        "avg_stylometric_score": round(avg_style, 2)
    }

@app.route("/recent", methods=["GET"])
@jwt_required()
def recent_detections():
    papers = Paper.query.order_by(Paper.upload_time.desc()).limit(10).all()
    result = []
    for paper in papers:
        analysis = Analysis.query.get(paper.analysis_id)
        result.append({
            "filename": paper.filename,
            "upload_time": paper.upload_time,
            "ai_generated": analysis.ai_generated,
            "plagiarism": analysis.plagiarism,
            "stylometric_inconsistency": analysis.stylometric_inconsistency,
            "ai_score": analysis.ai_score,
            "plagiarism_score": analysis.plagiarism_score,
            "stylometric_score": analysis.stylometric_score,
            "language": analysis.language
        })
    return jsonify(result)

@app.route("/paper/<int:paper_id>", methods=["GET", "DELETE"])
@jwt_required()
def paper_crud(paper_id):
    paper = Paper.query.get_or_404(paper_id)
    analysis = Analysis.query.get(paper.analysis_id)
    if request.method == "GET":
        return {
            "filename": paper.filename,
            "upload_time": paper.upload_time,
            "analysis": {
                "ai_generated": analysis.ai_generated,
                "plagiarism": analysis.plagiarism,
                "stylometric_inconsistency": analysis.stylometric_inconsistency,
                "ai_score": analysis.ai_score,
                "plagiarism_score": analysis.plagiarism_score,
                "stylometric_score": analysis.stylometric_score,
                "language": analysis.language,
                "details": analysis.details
            }
        }
    elif request.method == "DELETE":
        db.session.delete(paper)
        db.session.delete(analysis)
        db.session.commit()
        return {"msg": "Paper and analysis deleted."}

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# --- RUN APP ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
