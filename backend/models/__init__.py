# FILE: backend/models/__init__.py
# THIS IS THE MOST IMPORTANT FIX.
# I am removing the old, broken Car class definition from this file.
# This file will now only create the database object and correctly import
# the Car model from the car.py file.

from flask_sqlalchemy import SQLAlchemy

# Create the single, shared SQLAlchemy instance.
db = SQLAlchemy()

# Make the Car model from car.py easily importable from the models package.
# This forces the rest of the application to use the correct file.
from .car import Car