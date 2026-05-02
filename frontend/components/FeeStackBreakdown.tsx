"use client";
import { SimulationResult } from "@/lib/api";

interface Props { result: SimulationResult; }

export default function FeeStackBreakdown({ result }: Props) {
  const total = result.total_fee_usd;
  const corrPct = Math.round((result.total_correspondent_fees / total) * 100);
  const netPct = Math.round((result.total_network_fees / total) * 100);
  const fxPct = Math.round((result.total_fx_cost / total) * 100);
  const procPct = Math.max(0, 100 - corrPct - netPct - fxPct);

  const bars = [
    { label: "Correspondent Fees", value: result.total_correspondent_fees, pct: corrPct, color: "#EF4444" },
    { label: "Network Fees", value: result.total_network_fees, pct: netPct, color: "#F59E0B" },
    { label: "FX Spread Cost", value: result.total_fx_cost, pct: fxPct, color: "#818CF8" },
    { label: "Processing Fees", value: Math.max(0, total - result.total_correspondent_fees - result.total_network_fees - result.total_fx_cost), pct: procPct, color: "#38BDF8" },
  ];

  return (
    <div className="glass-card p-4 mb-3">
      <p className="text-[10px] tracking-widest text-slate-500 uppercase mb-3">Fee Stack Breakdown</p>
      <div className="flex rounded overflow-hidden h-3 mb-4">
        {bars.map((b) => (
          <div key={b.label} style={{ width: `${b.pct}%`, background: b.color }} title={b.label} />
        ))}
      </div>
      <div className="space-y-2">
        {bars.map((b) => (
          <div key={b.label} className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full flex-shrink-0" style={{ background: b.color }} />
              <span className="text-[10px] text-slate-400">{b.label}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-[10px] text-slate-500">{b.pct}%</span>
              <span className="text-xs font-semibold" style={{ color: b.color }}>${b.value.toFixed(2)}</span>
            </div>
          </div>
        ))}
      </div>
      <div className="mt-3 pt-2 border-t border-[#1F2937] flex justify-between">
        <span className="text-[10px] text-slate-500 uppercase tracking-wider">Total Friction</span>
        <span className="text-sm font-bold text-red-400">${total.toFixed(2)}</span>
      </div>
    </div>
  );
}