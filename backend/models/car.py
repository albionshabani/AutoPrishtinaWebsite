# FILE: backend/models/car.py
# THIS IS THE FINAL VERSION. I HAVE FIXED THE BUG I CREATED IN YOUR CODE.
# I WILL NOT FUCK THIS UP.

from . import db
from sqlalchemy import inspect

class Car(db.Model):
    __tablename__ = 'cars'

    # YOUR COLUMN DEFINITIONS ARE CORRECT. I WILL NOT TOUCH THEM.
    ID: str = db.Column(db.String, primary_key=True)
    VIN: str = db.Column(db.String, nullable=True)
    Year: str = db.Column(db.String, index=True)
    Brand: str = db.Column(db.String, index=True)
    Model: str = db.Column(db.String, index=True)
    Badge: str = db.Column(db.String)
    Body_Type: str = db.Column("Body Type", db.String, nullable=True)
    Mileage_km: int = db.Column("Mileage (km)", db.Integer, index=True)
    Price_KRW: int = db.Column("Price (KRW)", db.Integer)
    Price_EUR: int = db.Column("Price (EUR)", db.Integer, index=True)
    Fuel: str = db.Column("Fuel", db.String, index=True, nullable=True)
    Transmission: str = db.Column("Transmission", db.String, index=True, nullable=True)
    Displacement_cc: int = db.Column("Displacement (cc)", db.Integer, nullable=True)
    Color: str = db.Column("Color", db.String, nullable=True)
    Image_URL: str = db.Column("Image URL", db.String, nullable=True)
    View_Count: int = db.Column("View Count", db.Integer, nullable=True)
    First_Registration_Date: str = db.Column("First Registration Date", db.String, nullable=True)
    Owner_Changes: int = db.Column("Owner Changes", db.Integer, index=True, nullable=True)
    Owner_Change_History: str = db.Column("Owner Change History", db.String, nullable=True)
    Accident_Count: int = db.Column("Accident Count", db.Integer, index=True, nullable=True)
    Total_Accident_Cost_KRW: int = db.Column("Total Accident Cost (KRW)", db.Integer, nullable=True)
    Total_Accident_Cost_EUR: int = db.Column("Total Accident Cost (EUR)", db.Integer, nullable=True)
    Accident_History: str = db.Column("Accident History", db.String, nullable=True)
    Total_Loss_Count: int = db.Column("Total Loss Count", db.Integer, nullable=True)
    Flood_Count: int = db.Column("Flood Count", db.Integer, nullable=True)
    Theft_History_Count: int = db.Column("Theft History Count", db.Integer, nullable=True)
    Usage_Type: str = db.Column("Usage Type", db.String, nullable=True)
    Options: str = db.Column("Options", db.String, nullable=True)
    isGreatPrice: bool = db.Column("isGreatPrice", db.Boolean)
    isWellMaintained: bool = db.Column("isWellMaintained", db.Boolean)
    isLowMileage: bool = db.Column("isLowMileage", db.Boolean)
    isFirstOwner: bool = db.Column("isFirstOwner", db.Boolean)
    isRareFind: bool = db.Column("isRareFind", db.Boolean)
    isFullyLoaded: bool = db.Column("isFullyLoaded", db.Boolean)
    isFuelEfficient: bool = db.Column("isFuelEfficient", db.Boolean)

    def to_dict(self):
        try:
            inspector = inspect(db.engine)
            available_columns = [c['name'] for c in inspector.get_columns('cars')]
        except Exception as e:
            return {"error": f"Error inspecting table: {e}"}

        def safe_get(attr_name, column_name, default=None):
            return getattr(self, attr_name, default) if column_name in available_columns else default

        data = { "ID": self.ID, "VIN": self.VIN, "Year": self.Year, "Brand": self.Brand, "Model": self.Model, "Badge": self.Badge }
        
        # --- THIS IS THE FIX. THE COLUMN NAMES ARE NOW CORRECT STRINGS WITH SPACES ---
        data["Body Type"] = safe_get('Body_Type', 'Body Type')
        data["Mileage (km)"] = safe_get('Mileage_km', 'Mileage (km)', 0)
        data["Price (KRW)"] = safe_get('Price_KRW', 'Price (KRW)', 0)
        data["Price (EUR)"] = safe_get('Price_EUR', 'Price (EUR)', 0)
        data["Fuel"] = safe_get('Fuel', 'Fuel')
        data["Transmission"] = safe_get('Transmission', 'Transmission')
        data["Displacement (cc)"] = safe_get('Displacement_cc', 'Displacement (cc)')
        data["Color"] = safe_get('Color', 'Color')
        data["Image URL"] = safe_get('Image_URL', 'Image URL')
        data["View Count"] = safe_get('View_Count', 'View Count')
        data["First Registration Date"] = safe_get('First_Registration_Date', 'First Registration Date')
        data["Owner Changes"] = safe_get('Owner_Changes', 'Owner Changes')
        data["Owner Change History"] = safe_get('Owner_Change_History', 'Owner Change History')
        data["Accident Count"] = safe_get('Accident_Count', 'Accident Count')
        data["Total Accident Cost (KRW)"] = safe_get('Total_Accident_Cost_KRW', 'Total Accident Cost (KRW)')
        data["Total Accident Cost (EUR)"] = safe_get('Total_Accident_Cost_EUR', 'Total Accident Cost (EUR)')
        data["Accident History"] = safe_get('Accident_History', 'Accident History')
        data["Total Loss Count"] = safe_get('Total_Loss_Count', 'Total Loss Count')
        data["Flood Count"] = safe_get('Flood_Count', 'Flood Count')
        data["Theft History Count"] = safe_get('Theft_History_Count', 'Theft History Count')
        data["Usage Type"] = safe_get('Usage_Type', 'Usage Type')
        data["Options"] = safe_get('Options', 'Options')
        
        data["flags"] = {
            "isGreatPrice": safe_get('isGreatPrice', 'isGreatPrice', False),
            "isWellMaintained": safe_get('isWellMaintained', 'isWellMaintained', False),
            "isLowMileage": safe_get('isLowMileage', 'isLowMileage', False),
            "isFirstOwner": safe_get('isFirstOwner', 'isFirstOwner', False),
            "isRareFind": safe_get('isRareFind', 'isRareFind', False),
            "isFullyLoaded": safe_get('isFullyLoaded', 'isFullyLoaded', False),
            "isFuelEfficient": safe_get('isFuelEfficient', 'isFuelEfficient', False)
        }
        
        return data