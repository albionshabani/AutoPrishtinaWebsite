# FILE: backend/__init__.py

from flask import Flask
from flask_cors import CORS
from .config import Config

# Import the db object from your models package
from .models import db

def create_app(config_class=Config):
    """
    Application Factory Function.
    This pattern prevents circular imports by configuring the app within the function.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS for the entire app
    CORS(app)
    
    # Connect the db instance to the app
    db.init_app(app)

    # --- CRITICAL FIX ---
    # Import blueprints *inside* the function. This is the key to breaking the import cycle.
    from .api.listings import listings_bp
    app.register_blueprint(listings_bp, url_prefix='/api')

    @app.route('/test')
    def test_route():
        return "Backend is running!"

    return app