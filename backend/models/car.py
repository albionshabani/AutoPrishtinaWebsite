from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Car(db.Model):
    __tablename__ = 'cars'
    
    ID = db.Column(db.String, primary_key=True)
    Enrichment_ID = db.Column(db.String, name='Enrichment ID')
    Image_URL = db.Column(db.String, name='Image URL')
    Year = db.Column(db.String)
    Brand = db.Column(db.String)
    Model = db.Column(db.String)
    Badge = db.Column(db.String)
    Mileage_km = db.Column(db.Integer, name='Mileage (km)')
    Price_KRW = db.Column(db.Integer, name='Price (KRW)')
    Price_EUR = db.Column(db.Integer, name='Price (EUR)')
    Fuel = db.Column(db.String)
    Transmission = db.Column(db.String)
    First_Registration_Date = db.Column(db.String, name='First Registration Date')
    Displacement_cc = db.Column(db.Integer, name='Displacement (cc)')
    Usage_Type = db.Column(db.String, name='Usage Type')
    Owner_Changes = db.Column(db.Integer, name='Owner Changes')
    Owner_Change_History = db.Column(db.String, name='Owner Change History')
    Accident_Count = db.Column(db.Integer, name='Accident Count')
    Total_Accident_Cost_KRW = db.Column(db.Integer, name='Total Accident Cost (KRW)')
    Total_Accident_Cost_EUR = db.Column(db.Integer, name='Total Accident Cost (EUR)')
    Accident_History = db.Column(db.String, name='Accident History')
    Diagnosis_Result = db.Column(db.String, name='Diagnosis Result')
    Diagnosis_Items = db.Column(db.String, name='Diagnosis Details')
    VIN = db.Column(db.String)
    Motor_Type = db.Column(db.String, name='Motor Type')
    Sale_Type = db.Column(db.String, name='Sale Type')
    Seller_Comment = db.Column(db.String, name='Seller Comment')
    Total_Loss_Count = db.Column(db.Integer, name='Total Loss Count')
    Flood_Count = db.Column(db.Integer, name='Flood Count')
    Theft_History_Count = db.Column(db.Integer, name='Theft History Count')
    Has_Tuning = db.Column(db.Boolean, name='Has Tuning')
    Has_Open_Recall = db.Column(db.Boolean, name='Has Open Recall')

    def to_dict(self):
        """
        A robust, explicit helper method to serialize the Car object to a dictionary.
        This method is guaranteed to work by manually mapping each database column
        name to its corresponding Python attribute.
        """
        return {
            'ID': self.ID,
            'Enrichment ID': self.Enrichment_ID,
            'Image URL': self.Image_URL,
            'Year': self.Year,
            'Brand': self.Brand,
            'Model': self.Model,
            'Badge': self.Badge,
            'Mileage (km)': self.Mileage_km,
            'Price (KRW)': self.Price_KRW,
            'Price (EUR)': self.Price_EUR,
            'Fuel': self.Fuel,
            'Transmission': self.Transmission,
            'First Registration Date': self.First_Registration_Date,
            'Displacement (cc)': self.Displacement_cc,
            'Usage Type': self.Usage_Type,
            'Owner Changes': self.Owner_Changes,
            'Owner Change History': self.Owner_Change_History,
            'Accident Count': self.Accident_Count,
            'Total Accident Cost (KRW)': self.Total_Accident_Cost_KRW,
            'Total Accident Cost (EUR)': self.Total_Accident_Cost_EUR,
            'Accident History': self.Accident_History,
            'Diagnosis Result': self.Diagnosis_Result,
            'Diagnosis Details': self.Diagnosis_Items,
            'VIN': self.VIN,
            'Motor Type': self.Motor_Type,
            'Sale Type': self.Sale_Type,
            'Seller Comment': self.Seller_Comment,
            'Total Loss Count': self.Total_Loss_Count,
            'Flood Count': self.Flood_Count,
            'Theft History Count': self.Theft_History_Count,
            'Has Tuning': self.Has_Tuning,
            'Has Open Recall': self.Has_Open_Recall
        }