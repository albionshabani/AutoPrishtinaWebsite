// FILE: frontend/src/types.ts
// THIS IS THE FINAL, CORRECT TYPE DEFINITION. I WILL NOT FUCK THIS UP.

export interface CarFlags {
  isGreatPrice: boolean | null;
  isWellMaintained: boolean | null;
  isLowMileage: boolean | null;
  isFirstOwner: boolean | null;
  isRareFind: boolean | null;
  isFullyLoaded: boolean | null;
  isFuelEfficient: boolean | null;
}

export interface Car {
  // Using quoted keys to exactly match the JSON from the backend's to_dict()
  "Accident Count": number | null;
  "Accident History": string | null;
  "Badge": string;
  "Brand": string;
  "Body Type": string | null;
  "Color": string | null;
  "Displacement (cc)": number | null;
  "First Registration Date": string | null;
  "Flood Count": number | null;
  "Fuel": string | null;
  "ID": string;
  "Image URL": string | null;
  "Mileage (km)": number;
  "Model": string;
  "Options": string | null;
  "Owner Change History": string | null;
  "Owner Changes": number | null;
  "Price (EUR)": number;
  "Price (KRW)": number;
  "Theft History Count": number | null;
  "Total Accident Cost (EUR)": number | null;
  "Total Accident Cost (KRW)": number | null;
  "Total Loss Count": number | null;
  "Transmission": string | null;
  "Usage Type": string | null;
  "VIN": string | null;
  "View Count": number | null;
  "Year": string;
  "flags": Partial<CarFlags>;
}