# PoC #04 — Cross-Border Payment Path Simulator
**Real Rails Intelligence Library**

---

## What This Builds

A full-stack intelligence dashboard that simulates the hidden journey of a cross-border payment through the global SWIFT correspondent network — exposing fees, delays, FX spreads, and sanctions risks at every hop.

---

## Project Structure

```
poc-04-payment-simulator/
├── backend/
│   ├── main.py           ← FastAPI simulation engine
│   ├── requirements.txt
│   └── .env.example
└── frontend/
    ├── app/
    │   ├── layout.tsx
    │   ├── page.tsx      ← Main dashboard page
    │   └── globals.css
    ├── components/
    │   ├── CorridorSelector.tsx   ← From/To/Amount controls
    │   ├── PaymentFlowStage.tsx   ← React Flow hop visualization
    │   └── IntelligenceSidebar.tsx ← 30% sidebar
    ├── lib/
    │   └── api.ts        ← API client
    └── ...config files
```

---

## Setup & Run

### 1. Backend (FastAPI) — Terminal 1

```bash
cd poc-04-payment-simulator/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
# OR: venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload --port 8000
```

API will be live at: http://localhost:8000
Swagger docs at: http://localhost:8000/docs

---

### 2. Frontend (Next.js) — Terminal 2

```bash
cd poc-04-payment-simulator/frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

Frontend will be live at: http://localhost:3000

---

## How to Use

1. Open http://localhost:3000
2. Select **Origin Country** and **Destination Country** from the dropdowns
3. Set the **Send Amount** (default $10,000)
4. Click **▶ Simulate Payment Path**
5. The React Flow canvas will render the full hop-by-hop journey
6. Click any hop node to see detailed fee/delay/sanctions info
7. Check the right sidebar for FX spread analysis and corridor intelligence
8. Download the full simulation as JSON using the button at the bottom of the sidebar

---

## Supported Corridors (v1)

| From | To | Avg Fee | Avg Days |
|------|----|---------|----------|
| USA | India | 6.2% | 3.1 |
| USA | Mexico | 4.8% | 1.5 |
| USA | China | 5.5% | 2.8 |
| UK | India | 5.9% | 2.7 |
| UK | Nigeria | 8.4% | 4.2 |
| UAE | India | 3.8% | 1.2 |
| UAE | Pakistan | 4.1% | 1.5 |
| Singapore | Indonesia | 3.2% | 1.0 |
| Germany | Turkey | 4.6% | 1.8 |
| USA | Brazil | 6.8% | 3.5 |
| Australia | India | 5.1% | 2.4 |
| Canada | Philippines | 5.7% | 2.9 |
| Japan | Vietnam | 4.3% | 1.6 |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, TypeScript, Tailwind CSS |
| Visualization | React Flow (hop-by-hop DAG) |
| Backend | Python FastAPI |
| Data | Synthetic (BIS CPMI / World Bank grounded) |
| Design | Real Rails DNA — #030712 Obsidian, Cyan accent |

---

## Data Sources (Synthetic v1)

- **BIS CPMI Red Book** — Corridor average fee benchmarks
- **World Bank Remittance Prices** — Global remittance cost data
- **Synthetic Hop Logic** — Correspondent bank chains are simulated based on real institutional topology

---

*Real Rails Intelligence Library · PoC #04*
