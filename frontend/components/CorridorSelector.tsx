"use client";

import { Country } from "@/lib/api";

interface Props {
  countries: Country[];
  from: string;
  to: string;
  amount: number;
  loading: boolean;
  onFrom: (v: string) => void;
  onTo: (v: string) => void;
  onAmount: (v: number) => void;
  onSimulate: () => void;
}

const selectClass =
  "w-full bg-[#030712] border border-[#1F2937] text-slate-200 text-sm rounded px-3 py-2 " +
  "focus:outline-none focus:border-[#38BDF8] focus:shadow-[0_0_0_0.5px_#38BDF8] transition-all";

export default function CorridorSelector({
  countries, from, to, amount, loading,
  onFrom, onTo, onAmount, onSimulate,
}: Props) {
  return (
    <div className="glass-card p-4 mb-4">
      <p className="text-[10px] tracking-widest text-slate-500 uppercase mb-3">
        Corridor Configuration
      </p>
      <div className="grid grid-cols-2 gap-3 mb-3">
        <div>
          <label className="block text-[10px] text-slate-500 mb-1 uppercase tracking-wider">
            Origin Country
          </label>
          <select className={selectClass} value={from} onChange={e => onFrom(e.target.value)}>
            {countries.map(c => (
              <option key={c.code} value={c.code}>{c.name}</option>
            ))}
          </select>
        </div>
        <div>
          <label className="block text-[10px] text-slate-500 mb-1 uppercase tracking-wider">
            Destination Country
          </label>
          <select className={selectClass} value={to} onChange={e => onTo(e.target.value)}>
            {countries.map(c => (
              <option key={c.code} value={c.code} disabled={c.code === from}>
                {c.name}
              </option>
            ))}
          </select>
        </div>
      </div>
      <div className="mb-3">
        <label className="block text-[10px] text-slate-500 mb-1 uppercase tracking-wider">
          Send Amount (USD)
        </label>
        <input
          type="number"
          min={100}
          max={1000000}
          step={500}
          value={amount}
          onChange={e => onAmount(Number(e.target.value))}
          className={selectClass}
        />
      </div>
      <button
        onClick={onSimulate}
        disabled={loading || from === to}
        className="w-full py-2 rounded text-sm font-semibold tracking-wider uppercase
          bg-[#38BDF8] text-[#030712] hover:bg-[#7DD3FC] transition-colors
          disabled:opacity-40 disabled:cursor-not-allowed glow-cyan"
      >
        {loading ? "Simulating…" : "▶ Simulate Payment Path"}
      </button>
    </div>
  );
}
