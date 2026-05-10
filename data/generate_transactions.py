"""
Synthetic Transactions Data — PoC #04 Cross-Border Payment Path Simulator
NOTE: All data is SYNTHETIC. Includes edge cases for error states.
"""

import pandas as pd
import numpy as np
import os

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(55)

corridor_data = [
    ("COR-001","USA","IND",6.2,"LOW","ACTIVE"),
    ("COR-002","USA","MEX",4.8,"LOW","ACTIVE"),
    ("COR-003","USA","CHN",5.5,"MEDIUM","ACTIVE"),
    ("COR-004","GBR","IND",5.9,"LOW","ACTIVE"),
    ("COR-005","GBR","NGA",8.4,"HIGH","ACTIVE"),
    ("COR-006","UAE","IND",3.8,"LOW","ACTIVE"),
    ("COR-007","UAE","PAK",4.1,"MEDIUM","RESTRICTED"),
    ("COR-008","SGP","IDN",3.2,"LOW","ACTIVE"),
    ("COR-009","DEU","TUR",4.6,"LOW","ACTIVE"),
    ("COR-010","USA","BRA",6.8,"LOW","ACTIVE"),
    ("COR-011","AUS","IND",5.1,"LOW","ACTIVE"),
    ("COR-012","CAN","PHL",5.7,"LOW","ACTIVE"),
    ("COR-013","JPN","VNM",4.3,"LOW","ACTIVE"),
    ("COR-014","USA","NGA",9.8,"HIGH","RESTRICTED"),
    ("COR-015","GBR","PAK",7.2,"MEDIUM","RESTRICTED"),
    ("COR-016","DEU","IND",5.4,"LOW","ACTIVE"),
]

tx_data = []
for i in range(50):
    corridor = corridor_data[i % len(corridor_data)]
    corridor_id, from_c, to_c, avg_fee_pct, sanctions, status = corridor

    amount = round(float(rng.uniform(500, 100000)), 2)
    fee_pct = avg_fee_pct + float(rng.uniform(-1.0, 1.5))
    total_fee = round(amount * fee_pct / 100, 2)
    delay_hrs = avg_fee_pct * 24 / 6 + float(rng.uniform(-5, 10))
    num_hops = int(rng.integers(2, 5))

    # Determine status with edge cases
    if sanctions == "HIGH":
        tx_status = str(rng.choice(
            ["MANUAL_REVIEW", "DELAYED", "COMPLETED"],
            p=[0.5, 0.3, 0.2]
        ))
        delay_hrs += float(rng.uniform(24, 72))
    elif sanctions == "MEDIUM":
        tx_status = str(rng.choice(
            ["COMPLETED", "PENDING", "MANUAL_REVIEW"],
            p=[0.6, 0.3, 0.1]
        ))
    else:
        tx_status = str(rng.choice(
            ["COMPLETED", "PENDING", "FAILED", "DELAYED"],
            p=[0.75, 0.15, 0.05, 0.05]
        ))

    is_edge = tx_status in ["FAILED", "MANUAL_REVIEW"]
    edge_reason = (
        "Sanctions compliance hold" if tx_status == "MANUAL_REVIEW"
        else "Correspondent bank timeout" if tx_status == "FAILED"
        else "Regulatory delay" if tx_status == "DELAYED"
        else None
    )

    tx_data.append({
        "transaction_id": f"TXN-{str(i+1).zfill(4)}",
        "corridor_id": corridor_id,
        "from_country": from_c,
        "to_country": to_c,
        "send_amount_usd": amount,
        "total_fee_usd": total_fee,
        "total_fee_pct": round(fee_pct, 2),
        "amount_received_usd": round(amount - total_fee, 2),
        "estimated_delay_hours": round(delay_hrs, 1),
        "num_hops": num_hops,
        "status": tx_status,
        "sanctions_risk": sanctions,
        "corridor_status": status,
        "is_edge_case": is_edge,
        "edge_case_reason": edge_reason,
        "is_synthetic": True,
        "data_source": "World Bank Remittance Prices + BIS CPMI (Synthetic)",
    })

tx_df = pd.DataFrame(tx_data)

tx_df.to_csv(f"{OUTPUT_DIR}/transactions.csv", index=False)
tx_df.to_json(f"{OUTPUT_DIR}/transactions.json", orient="records", indent=2)
print(f"transactions.csv + transactions.json generated! ({len(tx_df)} rows)")
print(f"Edge cases: {tx_df['is_edge_case'].sum()} transactions")
print(f"Status breakdown:\n{tx_df['status'].value_counts()}")