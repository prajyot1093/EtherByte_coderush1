from flask import (
    render_template, request, redirect, url_for, flash, session, send_from_directory
)
import os
from werkzeug.utils import secure_filename
from models import db, User, Paper, Review
from werkzeug.security import generate_password_hash, check_password_hash

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {"pdf", "docx", "txt", "tex"}

def init_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session["user_id"] = user.id
                session["username"] = user.username
                session["role"] = user.role
                flash("Login successful!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid username or password.", "danger")
        return render_template("login.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            role = request.form.get("role", "Author")
            if User.query.filter_by(username=username).first():
                flash("Username already exists.", "danger")
            elif User.query.filter_by(email=email).first():
                flash("Email already registered.", "danger")
            else:
                hashed_pw = generate_password_hash(password)
                user = User(username=username, email=email, password=hashed_pw, role=role)
                db.session.add(user)
                db.session.commit()
                flash("Registration successful! Please log in.", "success")
                return redirect(url_for("login"))
        return render_template("register.html")

    @app.route("/dashboard")
    def dashboard():
        if "user_id" not in session:
            flash("Please log in to access the dashboard.", "warning")
            return redirect(url_for("login"))
        user = User.query.get(session["user_id"])
        papers = Paper.query.filter_by(author_id=user.id).all()
        return render_template("dashboard.html", user=user, papers=papers)

    @app.route("/upload", methods=["POST"])
    def upload():
        if "user_id" not in session:
            flash("Please log in to upload papers.", "warning")
            return redirect(url_for("login"))
        file = request.files.get("file")
        title = request.form.get("title")
        abstract = request.form.get("abstract")
        if not file or not allowed_file(file.filename):
            flash("Invalid or missing file.", "danger")
            return redirect(url_for("dashboard"))
        filename = secure_filename(file.filename)
        upload_folder = app.config.get("UPLOAD_FOLDER", "uploads")
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        paper = Paper(
            title=title,
            abstract=abstract,
            file_path=file_path,
            author_id=session["user_id"],
            status="Submitted"
        )
        db.session.add(paper)
        db.session.commit()
        flash("Paper uploaded successfully!", "success")
        return redirect(url_for("dashboard"))

    @app.route("/papers")
    def papers():
        if "user_id" not in session:
            flash("Please log in to view papers.", "warning")
            return redirect(url_for("login"))
        papers = Paper.query.all()
        return render_template("papers.html", papers=papers)

    @app.route("/review/<int:paper_id>", methods=["GET", "POST"])
    def review(paper_id):
        if "user_id" not in session:
            flash("Please log in to review papers.", "warning")
            return redirect(url_for("login"))
        paper = Paper.query.get_or_404(paper_id)
        if request.method == "POST":
            comments = request.form.get("comments")
            score = request.form.get("score")
            review = Review(
                paper_id=paper.id,
                reviewer_id=session["user_id"],
                comments=comments,
                score=int(score)
            )
            db.session.add(review)
            db.session.commit()
            flash("Review submitted successfully!", "success")
            return redirect(url_for("papers"))
        return render_template("review.html", paper=paper)

    # Serve uploaded files
    @app.route("/uploads/<filename>")
    def uploaded_file(filename):
        upload_folder = app.config.get("UPLOAD_FOLDER", "uploads")
        return