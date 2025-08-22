from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), nullable=False, default='Author')  # Author, Reviewer, Conference Chair
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    papers = db.relationship('Paper', backref='author', lazy=True)
    reviews = db.relationship('Review', backref='reviewer', lazy=True)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', role='{self.role}')>"

class Paper(db.Model):
    __tablename__ = 'paper'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    abstract = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(256), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(32), nullable=False, default='Submitted')  # Submitted, Under Review, Accepted, Rejected
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    reviews = db.relationship('Review', backref='paper', lazy=True)

    def __repr__(self):
        return f"<Paper(id={self.id}, title='{self.title}', author_id={self.author_id}, status='{self.status}')>"

class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('paper.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.Column(db.Text, nullable=True)
    score = db.Column(db.Integer, nullable=False)
    review_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Review(id={self.id}, paper_id={self.paper_id}, reviewer_id={self.reviewer_id}, score={self.score})>"

# Optional: Add more models (e.g., ConferenceSession, Notification)