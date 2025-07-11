# FILE: EncarScraper/app/data_models.py
# FINAL SCHEMA (v4.2)

import re
import pandas as pd
from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict

class CarData(BaseModel):
    model_config = ConfigDict(validate_assignment=True, extra='ignore', populate_by_name=True)

    # --- Core Vehicle Data ---
    ID: str
    VIN: Optional[str] = None
    Year: str
    Brand: str
    Model: str
    Badge: str
    Body_Type: Optional[str] = Field(None, alias='Body Type')
    Mileage_km: int = Field(alias='Mileage (km)')
    Price_KRW: int = Field(alias='Price (KRW)')
    Price_EUR: int = Field(alias='Price (EUR)')
    Fuel: Optional[str] = None
    Transmission: Optional[str] = None
    Displacement_cc: Optional[int] = Field(None, alias='Displacement (cc)')
    Color: Optional[str] = None
    Image_URL: Optional[str] = Field(None, alias='Image URL')
    View_Count: Optional[int] = Field(None, alias='View Count')
    
    # --- Historical Data ---
    First_Registration_Date: Optional[str] = Field(None, alias='First Registration Date')
    Owner_Changes: Optional[int] = Field(None, alias='Owner Changes')
    Owner_Change_History: Optional[str] = Field(None, alias='Owner Change History')
    Accident_Count: Optional[int] = Field(None, alias='Accident Count')
    Total_Accident_Cost_KRW: Optional[int] = Field(None, alias='Total Accident Cost (KRW)')
    Total_Accident_Cost_EUR: Optional[int] = Field(None, alias='Total Accident Cost (EUR)')
    Accident_History: Optional[str] = Field(None, alias='Accident History')
    Total_Loss_Count: Optional[int] = Field(None, alias='Total Loss Count')
    Flood_Count: Optional[int] = Field(None, alias='Flood Count')
    Theft_History_Count: Optional[int] = Field(None, alias='Theft History Count')
    Usage_Type: Optional[str] = Field(None, alias='Usage Type')

    # --- Detailed Features ---
    Options: Optional[str] = Field(None, alias='Options')

    # --- Flags ---
    isGreatPrice: Optional[bool] = Field(None, alias='isGreatPrice')
    isWellMaintained: Optional[bool] = Field(None, alias='isWellMaintained')
    isLowMileage: Optional[bool] = Field(None, alias='isLowMileage')
    isFirstOwner: Optional[bool] = Field(None, alias='isFirstOwner')
    isRareFind: Optional[bool] = Field(None, alias='isRareFind')
    isFullyLoaded: Optional[bool] = Field(None, alias='isFullyLoaded')
    isFuelEfficient: Optional[bool] = Field(None, alias='isFuelEfficient')

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