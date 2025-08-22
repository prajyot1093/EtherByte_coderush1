import os
from datetime import timedelta

# Database settings
SQLALCHEMY_DATABASE_URI = "sqlite:///cmt.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT settings
JWT_SECRET_KEY = "super-secret-key"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

# File upload settings
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt", "tex"}

# Other Flask settings
DEBUG = True

# Helper function for file extension checking
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
