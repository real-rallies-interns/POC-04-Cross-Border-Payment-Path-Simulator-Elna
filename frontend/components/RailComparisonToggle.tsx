"use client";
import { useState } from "react";
import { RailComparison } from "@/lib/api";

interface Props { rails: RailComparison[]; }

const RAIL_COLORS: Record<string, string> = {
  "SWIFT": "#38BDF8",
  "RTP / Instant": "#22C55E",
  "Crypto / Stablecoin": "#818CF8",
};

const TRANSPARENCY_COLOR: Record<string, string> = {
  "Low": "#EF4444", "Medium": "#F59E0B", "High": "#22C55E", "Very High": "#38BDF8",
};

export default function RailComparisonToggle({ rails }: Props) {
  const [active, setActive] = useState<string | null>(null);

  return (
    <div className="glass-card p-4 mb-3">
      <p className="text-[10px] tracking-widest text-slate-500 uppercase mb-3">Rail Comparison Toggle</p>
      <div className="flex gap-2 mb-3">
        {rails.map((r) => (
          <button
            key={r.rail}
            onClick={() => setActive(active === r.rail ? null : r.rail)}
            className="flex-1 py-1.5 rounded text-[10px] font-semibold uppercase tracking-wider border transition-all"
            style={{
              borderColor: active === r.rail ? RAIL_COLORS[r.rail] ?? "#38BDF8" : "#1F2937",
              color: active === r.rail ? RAIL_COLORS[r.rail] ?? "#38BDF8" : "#64748B",
              background: active === r.rail ? `${RAIL_COLORS[r.rail] ?? "#38BDF8"}15` : "transparent",
            }}
          >
            {r.rail === "SWIFT" ? "SWIFT" : r.rail === "RTP / Instant" ? "RTP" : "Crypto"}
          </button>
        ))}
      </div>

      <div className="space-y-2">
        {(active ? rails.filter(r => r.rail === active) : rails).map((r) => {
          const color = RAIL_COLORS[r.rail] ?? "#38BDF8";
          return (
            <div key={r.rail} className="rounded p-3 border" style={{ borderColor: color + "40", background: color + "08" }}>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold" style={{ color }}>{r.rail}</span>
                <span className="text-[9px] text-slate-500">{r.settlement}</span>
              </div>
              <div className="grid grid-cols-3 gap-2 text-center">
                <div>
                  <p className="text-[9px] text-slate-500 mb-0.5">Fee</p>
                  <p className="text-xs font-bold text-red-400">{r.avg_fee_pct}%</p>
                </div>
                <div>
                  <p className="text-[9px] text-slate-500 mb-0.5">Speed</p>
                  <p className="text-xs font-bold text-amber-400">
                    {r.avg_hours < 1 ? `${Math.round(r.avg_hours * 60)}m` : `${r.avg_hours}h`}
                  </p>
                </div>
                <div>
                  <p className="text-[9px] text-slate-500 mb-0.5">Visibility</p>
                  <p className="text-[10px] font-bold" style={{ color: TRANSPARENCY_COLOR[r.transparency] ?? "#fff" }}>
                    {r.transparency}
                  </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}