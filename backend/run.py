# FILE: EncarScraper/backend/run.py

import os
from dotenv import load_dotenv

# This finds the .env file in the same directory as this script.
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# CORRECT IMPORT: Use the relative import. This is the correct way inside a package.
from . import create_app

# Create an instance of the app
app = create_app()

if __name__ == '__main__':
    host = os.getenv('FLASK_RUN_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_RUN_PORT', 5000))
    app.run(host=host, port=port, debug=True)