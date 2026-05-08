from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from app.config import AppSettings
from app.models import db

# Initialize the core application
app = Flask(__name__)

# Apply the configurations from config.py
app.config.from_object(AppSettings)

# Bind extensions to the app
db.init_app(app)
Migrate(app, db)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}, supports_credentials=True) # Ensures the Vue frontend can talk to this API

# Import routing logic (placed at the bottom to prevent circular imports)
from app import views