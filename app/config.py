import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class AppSettings(object):
    """Configuration settings for the Flask application."""
    DEBUG = False
    
    # Security and File Uploads
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Dr1ftD@t3r_S3cr3t!')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Enforces a 16MB maximum upload size
    
    # Database Configuration settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False