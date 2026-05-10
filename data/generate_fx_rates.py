"""
Synthetic FX Rates Data — PoC #04 Cross-Border Payment Path Simulator
NOTE: All data is SYNTHETIC.
"""

import pandas as pd
import numpy as np
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(77)

corridor_data = [
    ("COR-001","USA","IND","USD/INR",83.5),
    ("COR-002","USA","MEX","USD/MXN",17.2),
    ("COR-003","USA","CHN","USD/CNY",7.25),
    ("COR-004","GBR","IND","GBP/INR",106.0),
    ("COR-005","GBR","NGA","GBP/NGN",1650.0),
    ("COR-006","UAE","IND","AED/INR",22.7),
    ("COR-007","UAE","PAK","AED/PKR",76.0),
    ("COR-008","SGP","IDN","SGD/IDR",11200.0),
    ("COR-009","DEU","TUR","EUR/TRY",32.5),
    ("COR-010","USA","BRA","USD/BRL",5.05),
    ("COR-011","AUS","IND","AUD/INR",54.2),
    ("COR-012","CAN","PHL","CAD/PHP",56.0),
    ("COR-013","JPN","VNM","JPY/VND",158.0),
    ("COR-014","USA","NGA","USD/NGN",1590.0),
    ("COR-015","GBR","PAK","GBP/PKR",348.0),
    ("COR-016","DEU","IND","EUR/INR",90.2),
]

fx_data = []
for corridor_id, from_c, to_c, pair, mid in corridor_data:
    spread = round(float(rng.uniform(1.2, 3.8)), 2)
    bank_rate = round(mid * (1 - spread / 100), 4)
    fx_data.append({
        "fx_id": f"FX-{corridor_id}",
        "corridor_id": corridor_id,
        "currency_pair": pair,
        "from_country": from_c,
        "to_country": to_c,
        "mid_market_rate": mid,
        "bank_rate": bank_rate,
        "spread_pct": spread,
        "rate_volatility": round(float(rng.uniform(0.1, 2.5)), 2),
        "extreme_spread": spread > 3.0,
        "is_synthetic": True,
        "data_source": "ECB Data Portal + World Bank (Synthetic)",
    })

fx_df = pd.DataFrame(fx_data)

fx_df.to_csv(f"{OUTPUT_DIR}/fx_rates.csv", index=False)
fx_df.to_json(f"{OUTPUT_DIR}/fx_rates.json", orient="records", indent=2)
print("fx_rates.csv + fx_rates.json generated!")