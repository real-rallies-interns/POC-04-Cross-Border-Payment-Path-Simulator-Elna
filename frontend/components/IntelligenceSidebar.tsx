"use client";
import { SimulationResult } from "@/lib/api";
import FeeStackBreakdown from "./FeeStackBreakdown";
import RailComparisonToggle from "./RailComparisonToggle";
import ControlMap from "./ControlMap";

interface Props {
  result: SimulationResult | null;
  loading: boolean;
  onDownload: () => void;
}

function MetricPill({ label, value, accent }: { label: string; value: string; accent?: string }) {
  return (
    <div className="flex items-center justify-between py-2 border-b border-[#1F2937]">
      <span className="text-[10px] text-slate-500 uppercase tracking-wider">{label}</span>
      <span className="text-sm font-semibold" style={{ color: accent ?? "#e2e8f0" }}>{value}</span>
    </div>
  );
}

function SectionLabel({ children }: { children: React.ReactNode }) {
  return <p className="text-[9px] tracking-widest text-slate-500 uppercase mb-2 pt-4">{children}</p>;
}

export default function IntelligenceSidebar({ result, loading, onDownload }: Props) {
  return (
    <aside className="h-full overflow-y-auto px-4 py-4 flex flex-col">
      <div className="mb-4">
        <div className="flex items-center gap-2 mb-1">
          <span className="w-1.5 h-1.5 rounded-full bg-[#38BDF8] pulse-cyan" />
          <span className="text-[9px] tracking-widest text-slate-500 uppercase">Real Rails Intelligence</span>
        </div>
        <h1 className="text-base font-bold text-slate-100 leading-tight">Cross-Border Payment<br />Path Simulator</h1>
        <p className="text-[10px] text-slate-500 mt-1">Payments Rail · PoC #04</p>
      </div>

      <SectionLabel>Section A — Rail Intelligence</SectionLabel>
      <div className="glass-card p-3 mb-2">
        {loading ? (
          <div className="space-y-2 animate-pulse">{[...Array(4)].map((_,i) => <div key={i} className="h-4 bg-[#1F2937] rounded" />)}</div>
        ) : result ? (
          <>
            <MetricPill label="Send Amount" value={`$${result.send_amount.toLocaleString()}`} accent="#38BDF8" />
            <MetricPill label="Amount Received" value={`$${result.amount_received.toLocaleString()}`} accent="#818CF8" />
            <MetricPill label="Total Friction Cost" value={`$${result.total_fee_usd.toFixed(2)} (${result.total_fee_pct}%)`} accent="#EF4444" />
            <MetricPill label="Estimated Arrival" value={`${result.estimated_arrival_days} days (${result.estimated_arrival_hours}h)`} accent="#F59E0B" />
            <MetricPill label="Hops" value={`${result.hops.length} banks`} />
            <MetricPill label="Sanctions Risk" value={result.sanctions_risk} accent={result.sanctions_risk==="HIGH"?"#EF4444":result.sanctions_risk==="MEDIUM"?"#F59E0B":"#22C55E"} />
          </>
        ) : (
          <p className="text-[11px] text-slate-600 italic">Run a simulation to see metrics.</p>
        )}
      </div>

      {result && (
        <>
          <SectionLabel>FX Spread Analysis</SectionLabel>
          <div className="glass-card p-3 mb-2">
            <MetricPill label="Pair" value={result.fx.currency_pair} accent="#38BDF8" />
            <MetricPill label="Mid-Market Rate" value={result.fx.mid_market_rate.toFixed(4)} />
            <MetricPill label="Bank Rate" value={result.fx.bank_rate.toFixed(4)} accent="#F59E0B" />
            <MetricPill label="Spread" value={`${result.fx.spread_pct}%`} accent="#EF4444" />
            <MetricPill label="Hidden FX Cost" value={`$${result.fx.hidden_cost_usd.toFixed(2)}`} accent="#EF4444" />
          </div>

          <SectionLabel>Fee Stack Breakdown</SectionLabel>
          <FeeStackBreakdown result={result} />

          <SectionLabel>Rail Comparison</SectionLabel>
          <RailComparisonToggle rails={result.rail_comparisons} />
        </>
      )}

      <SectionLabel>Section B — Why This Matters</SectionLabel>
      <div className="glass-card p-3 mb-2">
        <p className="text-[11px] text-slate-400 leading-relaxed">
          Unlike domestic transfers, cross-border payments travel through a{" "}
          <span className="text-[#38BDF8] font-semibold">multi-hop correspondent network</span>{" "}
          where each intermediary bank charges fees and introduces delays. An exporter in Kochi sending $10,000 may receive only{" "}
          <span className="text-[#EF4444] font-semibold">$9,300–$9,700</span> after 2–4 days — with zero visibility into where the money is or why it was delayed.
        </p>
        {result && <p className="text-[10px] text-slate-500 mt-2 italic border-t border-[#1F2937] pt-2">{result.corridor_note}</p>}
      </div>

      <SectionLabel>Section C — Who Controls the Rail</SectionLabel>
      <div className="glass-card p-3 mb-2">
        <p className="text-[11px] text-slate-400 leading-relaxed">
          <span className="text-[#818CF8] font-semibold">SWIFT</span> provides the messaging standard, but the real power sits with{" "}
          <span className="text-[#818CF8] font-semibold">Tier-1 Correspondent Banks</span> —
          JPMorgan, Citi, HSBC, Deutsche Bank — who hold the nostro/vostro accounts that clear most of global liquidity.{" "}
          <span className="text-[#38BDF8] font-semibold">Central Banks</span> set settlement windows and compliance rules that determine how long each hop takes.
        </p>
      </div>

      <SectionLabel>Control Map</SectionLabel>
      <ControlMap />

      <SectionLabel>Section D — Data Source Status</SectionLabel>
      <div className="glass-card p-3 mb-4">
        {[
          ["BIS CPMI Red Book","SYNTHETIC"],
          ["World Bank Remittance Data","SYNTHETIC"],
          ["ECB Data Portal","SYNTHETIC"],
          ["Corridor Hops","SIMULATED"],
        ].map(([label,badge]) => (
          <div key={label} className="flex items-center justify-between mb-1">
            <span className="text-[10px] text-slate-500">{label}</span>
            <span className={`text-[9px] px-1.5 py-0.5 rounded ${badge==="SIMULATED"?"bg-blue-900/30 text-blue-400":"bg-amber-900/30 text-amber-400"}`}>{badge}</span>
          </div>
        ))}
      </div>

      <button
        onClick={onDownload}
        disabled={!result}
        className="mt-auto w-full py-2 rounded text-xs font-semibold tracking-wider uppercase border border-[#1F2937] text-slate-400 hover:border-[#38BDF8] hover:text-[#38BDF8] transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
      >
        ↓ Download Sample Data
      </button>
    </aside>
  );
}