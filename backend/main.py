from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import random
import math

app = FastAPI(title="Real Rails – Payment Path Simulator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Data Layer ──────────────────────────────────────────────────────────────
# BIS CPMI / World Bank grounded corridor data
CORRIDORS = {
    ("USA", "IND"): {"avg_fee_pct": 6.2, "avg_days": 3.1, "currency_pair": "USD/INR", "mid_rate": 83.5},
    ("USA", "MEX"): {"avg_fee_pct": 4.8, "avg_days": 1.5, "currency_pair": "USD/MXN", "mid_rate": 17.2},
    ("USA", "CHN"): {"avg_fee_pct": 5.5, "avg_days": 2.8, "currency_pair": "USD/CNY", "mid_rate": 7.25},
    ("GBR", "IND"): {"avg_fee_pct": 5.9, "avg_days": 2.7, "currency_pair": "GBP/INR", "mid_rate": 106.0},
    ("GBR", "NGA"): {"avg_fee_pct": 8.4, "avg_days": 4.2, "currency_pair": "GBP/NGN", "mid_rate": 1650.0},
    ("UAE", "IND"): {"avg_fee_pct": 3.8, "avg_days": 1.2, "currency_pair": "AED/INR", "mid_rate": 22.7},
    ("UAE", "PAK"): {"avg_fee_pct": 4.1, "avg_days": 1.5, "currency_pair": "AED/PKR", "mid_rate": 76.0},
    ("SGP", "IDN"): {"avg_fee_pct": 3.2, "avg_days": 1.0, "currency_pair": "SGD/IDR", "mid_rate": 11200.0},
    ("DEU", "TUR"): {"avg_fee_pct": 4.6, "avg_days": 1.8, "currency_pair": "EUR/TRY", "mid_rate": 32.5},
    ("USA", "BRA"): {"avg_fee_pct": 6.8, "avg_days": 3.5, "currency_pair": "USD/BRL", "mid_rate": 5.05},
    ("AUS", "IND"): {"avg_fee_pct": 5.1, "avg_days": 2.4, "currency_pair": "AUD/INR", "mid_rate": 54.2},
    ("CAN", "PHL"): {"avg_fee_pct": 5.7, "avg_days": 2.9, "currency_pair": "CAD/PHP", "mid_rate": 56.0},
    ("JPN", "VNM"): {"avg_fee_pct": 4.3, "avg_days": 1.6, "currency_pair": "JPY/VND", "mid_rate": 158.0},
}

CORRESPONDENT_BANKS = {
    "USA": ["JPMorgan Chase (New York)", "Citibank (New York)", "Bank of America (New York)"],
    "GBR": ["HSBC (London)", "Barclays (London)", "NatWest (London)"],
    "DEU": ["Deutsche Bank (Frankfurt)", "Commerzbank (Frankfurt)"],
    "UAE": ["Emirates NBD (Dubai)", "First Abu Dhabi Bank (Abu Dhabi)"],
    "SGP": ["DBS Bank (Singapore)", "OCBC (Singapore)", "Standard Chartered (Singapore)"],
    "JPN": ["MUFG Bank (Tokyo)", "Sumitomo Mitsui (Tokyo)"],
    "IND": ["State Bank of India (Mumbai)", "ICICI Bank (Mumbai)", "HDFC Bank (Mumbai)"],
    "MEX": ["BBVA Mexico (Mexico City)", "Banamex (Mexico City)"],
    "CHN": ["Bank of China (Shanghai)", "ICBC (Shanghai)"],
    "NGA": ["Zenith Bank (Lagos)", "GTBank (Lagos)"],
    "PAK": ["HBL (Karachi)", "MCB Bank (Karachi)"],
    "IDN": ["Bank Mandiri (Jakarta)", "BRI (Jakarta)"],
    "TUR": ["Garanti BBVA (Istanbul)", "Akbank (Istanbul)"],
    "BRA": ["Itaú (São Paulo)", "Bradesco (São Paulo)"],
    "AUS": ["Commonwealth Bank (Sydney)", "ANZ (Melbourne)"],
    "CAN": ["RBC (Toronto)", "TD Bank (Toronto)"],
    "PHL": ["BDO Unibank (Manila)", "BPI (Manila)"],
    "VNM": ["Vietcombank (Hanoi)", "BIDV (Hanoi)"],
}

SANCTIONS_RISK = {
    "NGA": "HIGH", "PAK": "MEDIUM", "VNM": "LOW",
    "CHN": "MEDIUM", "TUR": "LOW", "BRA": "LOW",
    "IND": "LOW", "MEX": "LOW", "IDN": "LOW",
    "USA": "LOW", "GBR": "LOW", "DEU": "LOW",
    "UAE": "LOW", "SGP": "LOW", "JPN": "LOW",
    "AUS": "LOW", "CAN": "LOW", "PHL": "LOW",
}

COUNTRY_NAMES = {
    "USA": "United States", "IND": "India", "MEX": "Mexico",
    "CHN": "China", "GBR": "United Kingdom", "NGA": "Nigeria",
    "UAE": "UAE", "PAK": "Pakistan", "SGP": "Singapore",
    "IDN": "Indonesia", "DEU": "Germany", "TUR": "Turkey",
    "BRA": "Brazil", "AUS": "Australia", "CAN": "Canada",
    "PHL": "Philippines", "JPN": "Japan", "VNM": "Vietnam",
}

# ── Models ───────────────────────────────────────────────────────────────────
class Hop(BaseModel):
    hop_number: int
    institution: str
    role: str
    country: str
    fee_usd: float
    delay_hours: float
    swift_code: str
    sanctions_flag: str
    cumulative_fee_usd: float
    cumulative_hours: float
    amount_after_hop: float

class FXBreakdown(BaseModel):
    mid_market_rate: float
    bank_rate: float
    spread_pct: float
    hidden_cost_usd: float
    currency_pair: str

class SimulationResult(BaseModel):
    from_country: str
    to_country: str
    from_name: str
    to_name: str
    send_amount: float
    hops: List[Hop]
    fx: FXBreakdown
    total_fee_usd: float
    total_fee_pct: float
    estimated_arrival_hours: float
    estimated_arrival_days: float
    amount_received: float
    sanctions_risk: str
    corridor_note: str

# ── Simulation Engine ────────────────────────────────────────────────────────
def build_swift_code(country: str, idx: int) -> str:
    letters = "ABCDEFGHJKLMNPQRSTUVWXYZ"
    return f"{country[:2]}{letters[idx % len(letters)]}{letters[(idx*3) % len(letters)]}XX"

def simulate_payment(from_c: str, to_c: str, amount: float) -> SimulationResult:
    key = (from_c, to_c)
    corridor = CORRIDORS.get(key, {
        "avg_fee_pct": 7.0, "avg_days": 4.0,
        "currency_pair": f"{from_c[:3]}/{to_c[:3]}", "mid_rate": 1.0
    })

    random.seed(hash(f"{from_c}{to_c}"))  # deterministic per corridor

    # Build correspondent chain
    src_banks = CORRESPONDENT_BANKS.get(from_c, [f"Central Bank ({from_c})"])
    dst_banks = CORRESPONDENT_BANKS.get(to_c, [f"Central Bank ({to_c})"])

    intermediaries = []
    # Pick 1-2 intermediary hubs depending on corridor
    if from_c in ["USA", "GBR", "SGP"] and to_c in ["IND", "PAK", "NGA", "PHL", "VNM"]:
        intermediaries = [("SGP" if from_c != "SGP" else "GBR",
                           CORRESPONDENT_BANKS.get("SGP", ["DBS Bank"])[0])]
    elif from_c == "UAE":
        intermediaries = []  # UAE has direct corridors
    elif from_c == "DEU":
        intermediaries = [("USA", "Citibank (New York)")]
    else:
        hub = "USA" if from_c not in ["USA"] else "GBR"
        intermediaries = [(hub, CORRESPONDENT_BANKS.get(hub, ["Citibank (New York)"])[0])]

    hops = []
    cumulative_fee = 0.0
    cumulative_hours = 0.0
    running_amount = amount

    # Hop 0: Originating Bank
    orig_fee = round(random.uniform(8, 25), 2)
    orig_delay = round(random.uniform(0.5, 2.0), 1)
    running_amount -= orig_fee
    cumulative_fee += orig_fee
    cumulative_hours += orig_delay
    hops.append(Hop(
        hop_number=1,
        institution=src_banks[0],
        role="Originating Bank",
        country=from_c,
        fee_usd=orig_fee,
        delay_hours=orig_delay,
        swift_code=build_swift_code(from_c, 0),
        sanctions_flag="CLEAR",
        cumulative_fee_usd=round(cumulative_fee, 2),
        cumulative_hours=round(cumulative_hours, 1),
        amount_after_hop=round(running_amount, 2),
    ))

    # Intermediary Hops
    for i, (hub_country, hub_bank) in enumerate(intermediaries):
        fee = round(random.uniform(15, 45), 2)
        delay = round(random.uniform(4, 18), 1)
        risk = SANCTIONS_RISK.get(to_c, "LOW")
        flag = "MANUAL_REVIEW" if risk == "HIGH" and i == 0 else "CLEAR"
        if flag == "MANUAL_REVIEW":
            delay += random.uniform(24, 48)
        running_amount -= fee
        cumulative_fee += fee
        cumulative_hours += delay
        hops.append(Hop(
            hop_number=len(hops) + 1,
            institution=hub_bank,
            role="Correspondent Bank",
            country=hub_country,
            fee_usd=fee,
            delay_hours=round(delay, 1),
            swift_code=build_swift_code(hub_country, i + 1),
            sanctions_flag=flag,
            cumulative_fee_usd=round(cumulative_fee, 2),
            cumulative_hours=round(cumulative_hours, 1),
            amount_after_hop=round(running_amount, 2),
        ))

    # Final Hop: Receiving Bank
    recv_fee = round(random.uniform(5, 20), 2)
    recv_delay = round(random.uniform(1.0, 4.0), 1)
    running_amount -= recv_fee
    cumulative_fee += recv_fee
    cumulative_hours += recv_delay
    hops.append(Hop(
        hop_number=len(hops) + 1,
        institution=dst_banks[0],
        role="Receiving Bank",
        country=to_c,
        fee_usd=recv_fee,
        delay_hours=recv_delay,
        swift_code=build_swift_code(to_c, 99),
        sanctions_flag="CLEAR",
        cumulative_fee_usd=round(cumulative_fee, 2),
        cumulative_hours=round(cumulative_hours, 1),
        amount_after_hop=round(running_amount, 2),
    ))

    # FX Spread
    mid_rate = corridor["mid_rate"]
    spread_pct = round(random.uniform(1.5, 3.8), 2)
    bank_rate = round(mid_rate * (1 - spread_pct / 100), 4)
    fx_hidden_cost = round(running_amount * (spread_pct / 100), 2)
    running_amount -= fx_hidden_cost

    total_fee = round(amount - running_amount, 2)
    total_fee_pct = round((total_fee / amount) * 100, 2)

    sanctions_risk = SANCTIONS_RISK.get(to_c, "LOW")
    corridor_note = (
        f"This {COUNTRY_NAMES.get(from_c, from_c)} → {COUNTRY_NAMES.get(to_c, to_c)} corridor "
        f"averages {corridor['avg_fee_pct']}% in total friction costs per the World Bank Remittance Matrix."
    )

    return SimulationResult(
        from_country=from_c,
        to_country=to_c,
        from_name=COUNTRY_NAMES.get(from_c, from_c),
        to_name=COUNTRY_NAMES.get(to_c, to_c),
        send_amount=amount,
        hops=hops,
        fx=FXBreakdown(
            mid_market_rate=mid_rate,
            bank_rate=bank_rate,
            spread_pct=spread_pct,
            hidden_cost_usd=fx_hidden_cost,
            currency_pair=corridor["currency_pair"],
        ),
        total_fee_usd=total_fee,
        total_fee_pct=total_fee_pct,
        estimated_arrival_hours=round(cumulative_hours, 1),
        estimated_arrival_days=round(cumulative_hours / 24, 1),
        amount_received=round(running_amount, 2),
        sanctions_risk=sanctions_risk,
        corridor_note=corridor_note,
    )


# ── Routes ───────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "Real Rails Payment Simulator API v1.0"}

@app.get("/corridors")
def list_corridors():
    return [
        {"from": k[0], "to": k[1],
         "from_name": COUNTRY_NAMES.get(k[0], k[0]),
         "to_name": COUNTRY_NAMES.get(k[1], k[1]),
         "avg_fee_pct": v["avg_fee_pct"],
         "avg_days": v["avg_days"]}
        for k, v in CORRIDORS.items()
    ]

@app.get("/countries")
def list_countries():
    countries = set()
    for k in CORRIDORS:
        countries.add(k[0])
        countries.add(k[1])
    return [{"code": c, "name": COUNTRY_NAMES.get(c, c)} for c in sorted(countries)]

@app.get("/simulate", response_model=SimulationResult)
def simulate(
    from_country: str = Query(..., description="ISO 3-letter country code"),
    to_country: str = Query(..., description="ISO 3-letter country code"),
    amount: float = Query(10000.0, ge=100, le=1_000_000),
):
    return simulate_payment(from_country.upper(), to_country.upper(), amount)
