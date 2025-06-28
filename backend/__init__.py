# FILE: EncarScraper/backend/__init__.py
from flask import Flask
from flask_cors import CORS
from .config import Config
from .models.car import db
from .api.listings import listings_bp

def create_app(config_class=Config):
    """
    The Flask Application Factory.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app)  # Enable Cross-Origin Resource Sharing
    db.init_app(app) # Connect the SQLAlchemy instance to the app
    
    # Register Blueprints (your API routes)
    app.register_blueprint(listings_bp)
    
    return app