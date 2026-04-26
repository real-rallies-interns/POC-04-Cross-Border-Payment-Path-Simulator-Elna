const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface Hop {
  hop_number: number;
  institution: string;
  role: string;
  country: string;
  fee_usd: number;
  delay_hours: number;
  swift_code: string;
  sanctions_flag: string;
  cumulative_fee_usd: number;
  cumulative_hours: number;
  amount_after_hop: number;
}

export interface FXBreakdown {
  mid_market_rate: number;
  bank_rate: number;
  spread_pct: number;
  hidden_cost_usd: number;
  currency_pair: string;
}

export interface SimulationResult {
  from_country: string;
  to_country: string;
  from_name: string;
  to_name: string;
  send_amount: number;
  hops: Hop[];
  fx: FXBreakdown;
  total_fee_usd: number;
  total_fee_pct: number;
  estimated_arrival_hours: number;
  estimated_arrival_days: number;
  amount_received: number;
  sanctions_risk: string;
  corridor_note: string;
}

export interface Country {
  code: string;
  name: string;
}

export async function fetchCountries(): Promise<Country[]> {
  const res = await fetch(`${BASE}/countries`);
  if (!res.ok) throw new Error("Failed to fetch countries");
  return res.json();
}

export async function fetchSimulation(
  from: string,
  to: string,
  amount: number
): Promise<SimulationResult> {
  const url = `${BASE}/simulate?from_country=${from}&to_country=${to}&amount=${amount}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Simulation failed");
  return res.json();
}
