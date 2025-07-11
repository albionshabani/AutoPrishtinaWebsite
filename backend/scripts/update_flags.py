# FILE: backend/scripts/update_flags.py
# This script pre-calculates the performance-intensive feature flags
# and saves them directly to the database.
# Run this script *after* the database has been populated by the scraper.

import sys
import os
from collections import defaultdict

# Add the project's root directory to the Python path to allow importing the app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db, Car
from sqlalchemy import func, and_

def update_feature_flags():
    """
    Connects to the database, calculates the feature flags for all cars,
    and updates the records in a single session.
    """
    app = create_app()
    with app.app_context():
        print("Starting feature flag calculation...")

        # --- Step 1: Calculate all necessary statistics in bulk ---

        # Calculate average price and mileage for each Model/Year combination
        print("Calculating average price and mileage by Model/Year...")
        stats_by_model_year = db.session.query(
            Car.Model,
            Car.Year,
            func.avg(Car.Price_EUR).label('avg_price'),
            func.avg(Car.Mileage_km).label('avg_mileage'),
            func.count(Car.ID).label('count')
        ).group_by(Car.Model, Car.Year).all()

        # Convert to a fast lookup dictionary: {(model, year): {stats}}
        avg_stats = {
            (s.Model, s.Year): {'price': s.avg_price, 'mileage': s.avg_mileage, 'count': s.count}
            for s in stats_by_model_year
        }
        print(f"  ... found {len(avg_stats)} unique Model/Year groups.")

        # Calculate rarity for each Model/Badge combination
        print("Calculating rarity by Model/Badge...")
        badge_counts = db.session.query(
            Car.Model,
            Car.Badge,
            func.count(Car.ID).label('count')
        ).group_by(Car.Model, Car.Badge).all()

        # Convert to a fast lookup dictionary: {(model, badge): count}
        rarity_stats = {(c.Model, c.Badge): c.count for c in badge_counts}
        print(f"  ... found {len(rarity_stats)} unique Model/Badge groups.")

        # --- Step 2: Iterate through all cars and update flags ---
        
        all_cars = Car.query.all()
        print(f"\nUpdating flags for {len(all_cars)} cars...")
        updated_count = 0

        for car in all_cars:
            # Get pre-calculated stats for this car's group
            model_year_stats = avg_stats.get((car.Model, car.Year))
            
            # --- Calculate individual flags ---
            is_great_price = False
            if model_year_stats and model_year_stats['count'] >= 3 and car.Price_EUR:
                if car.Price_EUR < (model_year_stats['price'] * 0.90):
                    is_great_price = True

            is_low_mileage = False
            if model_year_stats and model_year_stats['count'] >= 3 and car.Mileage_km:
                if car.Mileage_km < (model_year_stats['mileage'] * 0.80):
                    is_low_mileage = True

            rare_count = rarity_stats.get((car.Model, car.Badge))
            is_rare_find = rare_count is not None and rare_count <= 3

            # Update the car object in the session
            car.is_great_price = is_great_price
            car.is_low_mileage = is_low_mileage
            car.is_rare_find = is_rare_find
            car.is_well_maintained = (is_low_mileage and car.Owner_Changes == 1 and car.Accident_Count == 0)
            
            updated_count += 1
            # Print progress indicator
            if updated_count % 100 == 0:
                print(f"  ... processed {updated_count}/{len(all_cars)} cars")

        # --- Step 3: Commit all changes to the database ---
        
        print("\nCommitting changes to the database...")
        db.session.commit()
        print("✅ Feature flags updated successfully!")

if __name__ == '__main__':
    update_feature_flags()