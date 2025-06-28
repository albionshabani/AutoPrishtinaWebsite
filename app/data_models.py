# FILE: EncarScraper/app/data_models.py
# FINAL, DEFINITIVE VERSION 2.1

import re
import pandas as pd
from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict

class CarData(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra='ignore', populate_by_name=True)

    ID: str
    Enrichment_ID: str = Field(alias='Enrichment ID')
    Image_URL: str = Field(alias='Image URL')
    Year: str
    Brand: str
    Model: str
    Badge: str
    Mileage_km: int = Field(alias='Mileage (km)')
    Price_KRW: int = Field(alias='Price (KRW)')
    Price_EUR: int = Field(alias='Price (EUR)')
    Fuel: Optional[str] = None # Set to Optional for robustness
    Transmission: Optional[str] = None # CORRECTED: Set to Optional
    First_Registration_Date: Optional[str] = Field(None, alias='First Registration Date')
    Displacement_cc: Optional[int] = Field(None, alias='Displacement (cc)')
    Usage_Type: Optional[str] = Field(None, alias='Usage Type')
    Owner_Changes: Optional[int] = Field(None, alias='Owner Changes')
    Owner_Change_History: Optional[str] = Field(None, alias='Owner Change History')
    Accident_Count: Optional[int] = Field(None, alias='Accident Count')
    Total_Accident_Cost_KRW: Optional[int] = Field(None, alias='Total Accident Cost (KRW)')
    Total_Accident_Cost_EUR: Optional[int] = Field(None, alias='Total Accident Cost (EUR)')
    Accident_History: Optional[str] = Field(None, alias='Accident History')
    Diagnosis_Result: Optional[str] = Field(None, alias='Diagnosis Result')
    Diagnosis_Items: Optional[str] = Field(None, alias='Diagnosis Details')
    VIN: Optional[str] = None
    Motor_Type: Optional[str] = Field(None, alias='Motor Type')
    Sale_Type: Optional[str] = Field(None, alias='Sale Type')
    Seller_Comment: Optional[str] = Field(None, alias='Seller Comment')
    Total_Loss_Count: Optional[int] = Field(None, alias='Total Loss Count')
    Flood_Count: Optional[int] = Field(None, alias='Flood Count')
    Theft_History_Count: Optional[int] = Field(None, alias='Theft History Count')
    Has_Tuning: Optional[bool] = Field(None, alias='Has Tuning')
    Has_Open_Recall: Optional[bool] = Field(None, alias='Has Open Recall')

    @field_validator('*', mode='before')
    def clean_nan(cls, v: Any) -> Optional[Any]:
        if isinstance(v, float) and pd.isna(v): return None
        return v

    @field_validator('VIN', mode='before')
    def validate_vin(cls, v: Any) -> Optional[str]:
        if v and isinstance(v, str):
            cleaned_vin = re.sub(r'[^A-HJ-NPR-Z0-9]', '', v.upper())
            return cleaned_vin if len(cleaned_vin) == 17 else v
        return v