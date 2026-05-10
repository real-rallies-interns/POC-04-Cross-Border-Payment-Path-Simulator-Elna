# Data Dictionary — PoC #04: Cross-Border Payment Path Simulator
**Real Rails Intelligence Library**
> ⚠️ All data in this package is SYNTHETIC. Generated for demonstration purposes only.
> Sources referenced: BIS CPMI Red Book, ECB Data Portal, World Bank Remittance Prices.

---

## Entity 1: Corridors (`corridors.csv` / `corridors.json`)
Payment corridors between origin and destination countries.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| corridor_id | string | Unique corridor identifier | COR-001 |
| from_country | string | ISO 3-letter origin country code | USA |
| to_country | string | ISO 3-letter destination country code | IND |
| from_name | string | Origin country full name | United States |
| to_name | string | Destination country full name | India |
| from_currency | string | Origin currency code | USD |
| to_currency | string | Destination currency code | INR |
| currency_pair | string | FX pair notation | USD/INR |
| mid_rate | float | Mid-market exchange rate | 83.5 |
| avg_fee_pct | float | Average total friction cost % | 6.2 |
| avg_days | float | Average settlement days | 3.1 |
| sanctions_risk | string | Risk level: LOW / MEDIUM / HIGH | LOW |
| status | string | ACTIVE / RESTRICTED | ACTIVE |
| is_synthetic | boolean | Always true — synthetic data flag | true |
| data_source | string | Reference source | BIS CPMI Red Book (Synthetic) |

**Edge Cases:**
- `sanctions_risk = HIGH` → corridors to Nigeria, Pakistan flagged for manual review
- `status = RESTRICTED` → UAE→PAK, USA→NGA, GBR→PAK corridors

---

## Entity 2: Banks (`banks.csv` / `banks.json`)
Correspondent and receiving banks in the global SWIFT network.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| bank_id | string | Unique bank identifier | BNK-001 |
| name | string | Bank name | JPMorgan Chase |
| city | string | Headquarters city | New York |
| country | string | ISO 3-letter country code | USA |
| country_name | string | Full country name | United States |
| swift_bic | string | SWIFT/BIC code | JPUS33XX |
| dominance_score | int | Rail dominance score (0-100) | 95 |
| is_tier1 | boolean | True = Global Tier-1 correspondent bank | true |
| status | string | ACTIVE / RESTRICTED | ACTIVE |
| sanctions_risk | string | Country-level sanctions risk | LOW |
| base_fee_usd | float | Synthetic base fee per transaction | 24.5 |
| base_delay_hours | float | Synthetic base processing delay | 3.2 |
| market_share_pct | float | Synthetic market share % | 32.5 |
| is_synthetic | boolean | Always true — synthetic data flag | true |
| data_source | string | Reference source | BIS CPMI Red Book (Synthetic) |

**Edge Cases:**
- Nigerian and Pakistani banks have `status = RESTRICTED`
- Tier-1 banks (is_tier1 = true) control most global liquidity

---

## Entity 3: FX Rates (`fx_rates.csv` / `fx_rates.json`)
Foreign exchange rate data per corridor.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| fx_id | string | Unique FX record identifier | FX-COR-001 |
| corridor_id | string | Linked corridor ID | COR-001 |
| currency_pair | string | FX pair notation | USD/INR |
| from_country | string | Origin country code | USA |
| to_country | string | Destination country code | IND |
| mid_market_rate | float | True mid-market rate | 83.5 |
| bank_rate | float | Rate offered by bank (lower) | 80.8 |
| spread_pct | float | Bank spread percentage | 3.2 |
| rate_volatility | float | Synthetic volatility indicator | 1.4 |
| extreme_spread | boolean | True if spread > 3% | false |
| is_synthetic | boolean | Always true — synthetic data flag | true |
| data_source | string | Reference source | ECB Data Portal (Synthetic) |

**Edge Cases:**
- `extreme_spread = true` → hidden cost alert triggered
- High-risk corridors (NGA, PAK) show wider spreads

---

## Entity 4: Transactions (`transactions.csv` / `transactions.json`)
Simulated payment transactions with status and edge cases.

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| transaction_id | string | Unique transaction ID | TXN-0001 |
| corridor_id | string | Linked corridor ID | COR-001 |
| from_country | string | Origin country code | USA |
| to_country | string | Destination country code | IND |
| send_amount_usd | float | Amount sent in USD | 10000.00 |
| total_fee_usd | float | Total fees deducted | 620.00 |
| total_fee_pct | float | Fee as % of send amount | 6.2 |
| amount_received_usd | float | Amount received after fees | 9380.00 |
| estimated_delay_hours | float | Total estimated delay in hours | 74.4 |
| num_hops | int | Number of correspondent bank hops | 3 |
| status | string | COMPLETED / PENDING / FAILED / DELAYED / MANUAL_REVIEW | COMPLETED |
| sanctions_risk | string | LOW / MEDIUM / HIGH | LOW |
| corridor_status | string | ACTIVE / RESTRICTED | ACTIVE |
| is_edge_case | boolean | True if status is FAILED or MANUAL_REVIEW | false |
| edge_case_reason | string | Reason for edge case or null | Sanctions compliance hold |
| is_synthetic | boolean | Always true — synthetic data flag | true |
| data_source | string | Reference source | World Bank Remittance (Synthetic) |

**Edge Cases:**
- `status = MANUAL_REVIEW` → sanctions compliance hold, adds 24-72h delay
- `status = FAILED` → correspondent bank timeout
- `status = DELAYED` → regulatory delay
- High-risk corridors (HIGH sanctions) have 50% chance of MANUAL_REVIEW

---

## How to Run the Generators

```bash
cd data
pip install pandas numpy
python generate_synthetic_data.py
python generate_banks.py
python generate_fx_rates.py
python generate_transactions.py
```

## File Summary

| File | Rows | Format |
|------|------|--------|
| corridors.csv / .json | 16 | CSV + JSON |
| banks.csv / .json | 40 | CSV + JSON |
| fx_rates.csv / .json | 16 | CSV + JSON |
| transactions.csv / .json | 50 | CSV + JSON |