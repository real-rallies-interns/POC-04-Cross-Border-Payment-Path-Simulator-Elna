"""
Synthetic Data Generator — PoC #04 Cross-Border Payment Path Simulator
Real Rails Intelligence Library
NOTE: All data is SYNTHETIC. Generated for demonstration purposes only.
"""

import pandas as pd
import numpy as np
import json
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(42)

COUNTRIES = {
    "USA": ("United States", "USD"),
    "GBR": ("United Kingdom", "GBP"),
    "DEU": ("Germany", "EUR"),
    "UAE": ("UAE", "AED"),
    "SGP": ("Singapore", "SGD"),
    "JPN": ("Japan", "JPY"),
    "IND": ("India", "INR"),
    "CHN": ("China", "CNY"),
    "NGA": ("Nigeria", "NGN"),
    "MEX": ("Mexico", "MXN"),
    "PAK": ("Pakistan", "PKR"),
    "IDN": ("Indonesia", "IDR"),
    "TUR": ("Turkey", "TRY"),
    "BRA": ("Brazil", "BRL"),
    "AUS": ("Australia", "AUD"),
    "CAN": ("Canada", "CAD"),
    "PHL": ("Philippines", "PHP"),
    "VNM": ("Vietnam", "VND"),
}

SANCTIONS_RISK = {
    "NGA": "HIGH", "PAK": "MEDIUM", "CHN": "MEDIUM",
    "TUR": "LOW", "VNM": "LOW", "IDN": "LOW",
    "IND": "LOW", "MEX": "LOW", "BRA": "LOW",
    "USA": "LOW", "GBR": "LOW", "DEU": "LOW",
    "UAE": "LOW", "SGP": "LOW", "JPN": "LOW",
    "AUS": "LOW", "CAN": "LOW", "PHL": "LOW",
}

# ── 1. CORRIDORS ──────────────────────────────────────────────────────────────
corridor_data = [
    ("USA","IND","USD/INR",83.5,6.2,3.1,"LOW","ACTIVE"),
    ("USA","MEX","USD/MXN",17.2,4.8,1.5,"LOW","ACTIVE"),
    ("USA","CHN","USD/CNY",7.25,5.5,2.8,"MEDIUM","ACTIVE"),
    ("GBR","IND","GBP/INR",106.0,5.9,2.7,"LOW","ACTIVE"),
    ("GBR","NGA","GBP/NGN",1650.0,8.4,4.2,"HIGH","ACTIVE"),
    ("UAE","IND","AED/INR",22.7,3.8,1.2,"LOW","ACTIVE"),
    ("UAE","PAK","AED/PKR",76.0,4.1,1.5,"MEDIUM","RESTRICTED"),
    ("SGP","IDN","SGD/IDR",11200.0,3.2,1.0,"LOW","ACTIVE"),
    ("DEU","TUR","EUR/TRY",32.5,4.6,1.8,"LOW","ACTIVE"),
    ("USA","BRA","USD/BRL",5.05,6.8,3.5,"LOW","ACTIVE"),
    ("AUS","IND","AUD/INR",54.2,5.1,2.4,"LOW","ACTIVE"),
    ("CAN","PHL","CAD/PHP",56.0,5.7,2.9,"LOW","ACTIVE"),
    ("JPN","VNM","JPY/VND",158.0,4.3,1.6,"LOW","ACTIVE"),
    ("USA","NGA","USD/NGN",1590.0,9.8,5.5,"HIGH","RESTRICTED"),
    ("GBR","PAK","GBP/PKR",348.0,7.2,3.8,"MEDIUM","RESTRICTED"),
    ("DEU","IND","EUR/INR",90.2,5.4,2.6,"LOW","ACTIVE"),
]

corridors_df = pd.DataFrame(corridor_data, columns=[
    "from_country","to_country","currency_pair","mid_rate",
    "avg_fee_pct","avg_days","sanctions_risk","status"
])
corridors_df["from_name"] = corridors_df["from_country"].map(lambda x: COUNTRIES[x][0])
corridors_df["to_name"] = corridors_df["to_country"].map(lambda x: COUNTRIES[x][0])
corridors_df["from_currency"] = corridors_df["from_country"].map(lambda x: COUNTRIES[x][1])
corridors_df["to_currency"] = corridors_df["to_country"].map(lambda x: COUNTRIES[x][1])
corridors_df["is_synthetic"] = True
corridors_df["data_source"] = "BIS CPMI Red Book + World Bank Remittance Matrix (Synthetic)"
corridors_df["corridor_id"] = ["COR-" + str(i+1).zfill(3) for i in range(len(corridors_df))]

corridors_df.to_csv(f"{OUTPUT_DIR}/corridors.csv", index=False)
corridors_df.to_json(f"{OUTPUT_DIR}/corridors.json", orient="records", indent=2)
print("corridors.csv + corridors.json generated!")