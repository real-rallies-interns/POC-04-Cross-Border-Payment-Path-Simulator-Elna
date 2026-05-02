"use client";
import { useEffect, useState } from "react";
import { fetchControlMap, ControlNode } from "@/lib/api";

const COUNTRY_NAMES: Record<string, string> = {
  USA:"United States",IND:"India",MEX:"Mexico",CHN:"China",GBR:"UK",
  NGA:"Nigeria",UAE:"UAE",PAK:"Pakistan",SGP:"Singapore",IDN:"Indonesia",
  DEU:"Germany",TUR:"Turkey",BRA:"Brazil",AUS:"Australia",CAN:"Canada",
  PHL:"Philippines",JPN:"Japan",VNM:"Vietnam",
};

export default function ControlMap() {
  const [nodes, setNodes] = useState<ControlNode[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<ControlNode | null>(null);

  useEffect(() => {
    fetchControlMap().then(setNodes).catch(console.error).finally(() => setLoading(false));
  }, []);

  const tier1 = nodes.filter(n => n.is_tier1);
  const tier2 = nodes.filter(n => !n.is_tier1);

  if (loading) return (
    <div className="glass-card p-4 mb-3 animate-pulse">
      <p className="text-[10px] tracking-widest text-slate-500 uppercase mb-2">Control Map</p>
      <div className="space-y-2">
        {[...Array(4)].map((_,i) => <div key={i} className="h-4 bg-[#1F2937] rounded" />)}
      </div>
    </div>
  );

  return (
    <div className="glass-card p-4 mb-3">
      <p className="text-[10px] tracking-widest text-slate-500 uppercase mb-1">Control Map</p>
      <p className="text-[10px] text-slate-600 mb-3">Dominant banks per corridor node</p>

      <div className="mb-3">
        <p className="text-[9px] text-[#38BDF8] uppercase tracking-wider mb-2">● Tier 1 — Global Rail Controllers</p>
        <div className="flex flex-wrap gap-1.5">
          {tier1.map((n) => (
            <button
              key={n.country}
              onClick={() => setSelected(selected?.country === n.country ? null : n)}
              className="px-2 py-1 rounded text-[10px] border transition-all"
              style={{
                borderColor: selected?.country === n.country ? "#38BDF8" : "#1F2937",
                color: selected?.country === n.country ? "#38BDF8" : "#94A3B8",
                background: selected?.country === n.country ? "#38BDF815" : "transparent",
              }}
            >
              {COUNTRY_NAMES[n.country] ?? n.country}
            </button>
          ))}
        </div>
      </div>

      <div className="mb-3">
        <p className="text-[9px] text-[#818CF8] uppercase tracking-wider mb-2">○ Tier 2 — Regional Nodes</p>
        <div className="flex flex-wrap gap-1.5">
          {tier2.map((n) => (
            <button
              key={n.country}
              onClick={() => setSelected(selected?.country === n.country ? null : n)}
              className="px-2 py-1 rounded text-[10px] border transition-all"
              style={{
                borderColor: selected?.country === n.country ? "#818CF8" : "#1F2937",
                color: selected?.country === n.country ? "#818CF8" : "#64748B",
                background: selected?.country === n.country ? "#818CF815" : "transparent",
              }}
            >
              {COUNTRY_NAMES[n.country] ?? n.country}
            </button>
          ))}
        </div>
      </div>

      {selected && (
        <div className="rounded p-3 border border-[#1F2937] bg-[#030712]">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-slate-200">{COUNTRY_NAMES[selected.country] ?? selected.country}</span>
            <span className={`text-[9px] px-1.5 py-0.5 rounded ${selected.is_tier1 ? "bg-cyan-900/40 text-cyan-400" : "bg-indigo-900/40 text-indigo-400"}`}>
              {selected.is_tier1 ? "TIER 1" : "TIER 2"}
            </span>
          </div>
          <p className="text-[11px] text-slate-400 mb-2">{selected.bank}</p>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <p className="text-[9px] text-slate-500">Dominance Score</p>
              <div className="flex items-center gap-1 mt-0.5">
                <div className="flex-1 h-1.5 bg-[#1F2937] rounded-full overflow-hidden">
                  <div className="h-full rounded-full bg-[#38BDF8]" style={{ width: `${selected.dominance_score}%` }} />
                </div>
                <span className="text-[10px] text-[#38BDF8] font-bold">{selected.dominance_score}</span>
              </div>
            </div>
            <div>
              <p className="text-[9px] text-slate-500">Market Share</p>
              <p className="text-xs font-bold text-[#818CF8]">{selected.market_share_pct}%</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}