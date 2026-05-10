"""
Synthetic Banks Data — PoC #04 Cross-Border Payment Path Simulator
NOTE: All data is SYNTHETIC.
"""

import pandas as pd
import numpy as np
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(99)

COUNTRIES = {
    "USA": "United States", "GBR": "United Kingdom", "DEU": "Germany",
    "UAE": "UAE", "SGP": "Singapore", "JPN": "Japan", "IND": "India",
    "CHN": "China", "NGA": "Nigeria", "MEX": "Mexico", "PAK": "Pakistan",
    "IDN": "Indonesia", "TUR": "Turkey", "BRA": "Brazil", "AUS": "Australia",
    "CAN": "Canada", "PHL": "Philippines", "VNM": "Vietnam",
}

SANCTIONS_RISK = {
    "NGA": "HIGH", "PAK": "MEDIUM", "CHN": "MEDIUM",
    "TUR": "LOW", "VNM": "LOW", "IDN": "LOW",
    "IND": "LOW", "MEX": "LOW", "BRA": "LOW",
    "USA": "LOW", "GBR": "LOW", "DEU": "LOW",
    "UAE": "LOW", "SGP": "LOW", "JPN": "LOW",
    "AUS": "LOW", "CAN": "LOW", "PHL": "LOW",
}

bank_data = [
    ("BNK-001","JPMorgan Chase","New York","USA","JPUS33XX",95,True,"ACTIVE"),
    ("BNK-002","Citibank","New York","USA","CITIUSXX",92,True,"ACTIVE"),
    ("BNK-003","Bank of America","New York","USA","BOFAUS3N",88,True,"ACTIVE"),
    ("BNK-004","HSBC","London","GBR","MIDLGB22",94,True,"ACTIVE"),
    ("BNK-005","Barclays","London","GBR","BARCGB22",90,True,"ACTIVE"),
    ("BNK-006","NatWest","London","GBR","NWBKGB2L",85,False,"ACTIVE"),
    ("BNK-007","Deutsche Bank","Frankfurt","DEU","DEUTDEBB",93,True,"ACTIVE"),
    ("BNK-008","Commerzbank","Frankfurt","DEU","COBADEFF",87,True,"ACTIVE"),
    ("BNK-009","Emirates NBD","Dubai","UAE","EBILAEAD",89,True,"ACTIVE"),
    ("BNK-010","First Abu Dhabi","Abu Dhabi","UAE","NBADAEAA",86,False,"ACTIVE"),
    ("BNK-011","DBS Bank","Singapore","SGP","DBSSSGSG",96,True,"ACTIVE"),
    ("BNK-012","OCBC","Singapore","SGP","OCBCSGSG",88,True,"ACTIVE"),
    ("BNK-013","Standard Chartered","Singapore","SGP","SCBLSGSG",91,True,"ACTIVE"),
    ("BNK-014","MUFG Bank","Tokyo","JPN","BOTKJPJT",92,True,"ACTIVE"),
    ("BNK-015","Sumitomo Mitsui","Tokyo","JPN","SMBCJPJT",89,True,"ACTIVE"),
    ("BNK-016","State Bank of India","Mumbai","IND","SBININBB",84,False,"ACTIVE"),
    ("BNK-017","ICICI Bank","Mumbai","IND","ICICINBB",82,False,"ACTIVE"),
    ("BNK-018","HDFC Bank","Mumbai","IND","HDFCINBB",83,False,"ACTIVE"),
    ("BNK-019","BBVA Mexico","Mexico City","MEX","BCMRMXMM",80,False,"ACTIVE"),
    ("BNK-020","Banamex","Mexico City","MEX","BNMXMXMM",78,False,"ACTIVE"),
    ("BNK-021","Bank of China","Shanghai","CHN","BKCHCNBJ",87,True,"ACTIVE"),
    ("BNK-022","ICBC","Shanghai","CHN","ICBKCNBJ",89,True,"ACTIVE"),
    ("BNK-023","Zenith Bank","Lagos","NGA","ZEIBNGLA",72,False,"RESTRICTED"),
    ("BNK-024","GTBank","Lagos","NGA","GTBINGLA",70,False,"RESTRICTED"),
    ("BNK-025","HBL","Karachi","PAK","HABBPKKA",68,False,"RESTRICTED"),
    ("BNK-026","MCB Bank","Karachi","PAK","MUCBPKKA",65,False,"RESTRICTED"),
    ("BNK-027","Bank Mandiri","Jakarta","IDN","BMRIIDJA",76,False,"ACTIVE"),
    ("BNK-028","BRI","Jakarta","IDN","BRINIDJA",74,False,"ACTIVE"),
    ("BNK-029","Garanti BBVA","Istanbul","TUR","TGBATRIS",79,False,"ACTIVE"),
    ("BNK-030","Akbank","Istanbul","TUR","AKBKTRIS",77,False,"ACTIVE"),
    ("BNK-031","Itau","Sao Paulo","BRA","ITAUBRSP",85,True,"ACTIVE"),
    ("BNK-032","Bradesco","Sao Paulo","BRA","BBDEBRSP",83,False,"ACTIVE"),
    ("BNK-033","Commonwealth Bank","Sydney","AUS","CTBAAU2S",90,True,"ACTIVE"),
    ("BNK-034","ANZ","Melbourne","AUS","ANZBAU3M",88,True,"ACTIVE"),
    ("BNK-035","RBC","Toronto","CAN","ROYCCAT2",91,True,"ACTIVE"),
    ("BNK-036","TD Bank","Toronto","CAN","TDOMCATT",89,True,"ACTIVE"),
    ("BNK-037","BDO Unibank","Manila","PHL","BNORPHMM",75,False,"ACTIVE"),
    ("BNK-038","BPI","Manila","PHL","BOPIPHMM",73,False,"ACTIVE"),
    ("BNK-039","Vietcombank","Hanoi","VNM","BFTVVNVX",71,False,"ACTIVE"),
    ("BNK-040","BIDV","Hanoi","VNM","BIDVVNVX",69,False,"ACTIVE")]

banks_df = pd.DataFrame(bank_data, columns=[
    "bank_id","name","city","country","swift_bic",
    "dominance_score","is_tier1","status"])
banks_df["country_name"] = banks_df["country"].map(COUNTRIES)
banks_df["sanctions_risk"] = banks_df["country"].map(SANCTIONS_RISK)
banks_df["base_fee_usd"] = rng.uniform(8, 45, len(banks_df)).round(2)
banks_df["base_delay_hours"] = rng.uniform(0.5, 18, len(banks_df)).round(1)
banks_df["market_share_pct"] = rng.uniform(5, 38, len(banks_df)).round(1)
banks_df["is_synthetic"] = True
banks_df["data_source"] = "BIS CPMI Red Book (Synthetic)"

banks_df.to_csv(f"{OUTPUT_DIR}/banks.csv", index=False)
banks_df.to_json(f"{OUTPUT_DIR}/banks.json", orient="records", indent=2)
print("banks.csv + banks.json generated!")