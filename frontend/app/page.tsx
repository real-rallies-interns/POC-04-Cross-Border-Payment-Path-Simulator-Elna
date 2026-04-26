"use client";

import { useEffect, useState, useCallback } from "react";
import dynamic from "next/dynamic";
import { fetchCountries, fetchSimulation, Country, SimulationResult } from "@/lib/api";
import CorridorSelector from "@/components/CorridorSelector";
import IntelligenceSidebar from "@/components/IntelligenceSidebar";

// React Flow must be client-side only
const PaymentFlowStage = dynamic(() => import("@/components/PaymentFlowStage"), { ssr: false });

export default function Home() {
  const [countries, setCountries] = useState<Country[]>([]);
  const [from, setFrom] = useState("USA");
  const [to, setTo] = useState("IND");
  const [amount, setAmount] = useState(10000);
  const [result, setResult] = useState<SimulationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeHop, setActiveHop] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchCountries()
      .then(setCountries)
      .catch(() => setError("Cannot connect to backend. Is FastAPI running on port 8000?"));
  }, []);

  const simulate = useCallback(async () => {
    if (from === to) return;
    setLoading(true);
    setError(null);
    setActiveHop(null);
    try {
      const data = await fetchSimulation(from, to, amount);
      setResult(data);
    } catch {
      setError("Simulation failed — check backend connection.");
    } finally {
      setLoading(false);
    }
  }, [from, to, amount]);

  const handleDownload = useCallback(() => {
    if (!result) return;
    const blob = new Blob([JSON.stringify(result, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `poc04_${from}_to_${to}_${amount}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }, [result, from, to, amount]);

  return (
    <div
      className="flex flex-col"
      style={{ height: "100vh", background: "#030712", overflow: "hidden" }}
    >
      {/* Top Bar */}
      <header
        className="flex items-center justify-between px-5 py-2 border-b border-[#1F2937]"
        style={{ background: "#0B1117", minHeight: 40 }}
      >
        <div className="flex items-center gap-3">
          <span className="text-[10px] tracking-widest text-[#38BDF8] font-semibold uppercase">
            ● REAL RAILS
          </span>
          <span className="text-[#1F2937]">/</span>
          <span className="text-[10px] tracking-widest text-slate-500 uppercase">
            Real Rails Intelligence
          </span>
          <span className="text-[#1F2937]">/</span>
          <span className="text-[10px] tracking-widest text-slate-400 uppercase">
            Payments Rail — Cross-Border Path Simulator
          </span>
        </div>
        <div className="flex items-center gap-2">
          {result && (
            <>
              <span className="text-[10px] text-slate-500 border border-[#1F2937] rounded px-2 py-0.5">
                {result.hops.length} Hops
              </span>
              <span className="text-[10px] text-[#38BDF8] border border-[#38BDF8]/40 rounded px-2 py-0.5">
                {result.from_name} → {result.to_name}
              </span>
            </>
          )}
          <span className="text-[10px] text-amber-400 border border-amber-900/50 rounded px-2 py-0.5">
            UTIL: SYNTHETIC
          </span>
        </div>
      </header>

      {/* Error Banner */}
      {error && (
        <div className="bg-red-950 border-b border-red-900 px-5 py-2">
          <p className="text-red-400 text-xs">⚠ {error}</p>
        </div>
      )}

      {/* Main Layout: 70/30 */}
      <div className="flex flex-1 overflow-hidden">
        {/* Main Stage 70% */}
        <main className="flex flex-col border-r border-[#1F2937]" style={{ width: "70%" }}>
          {/* Selector strip */}
          <div className="p-4 border-b border-[#1F2937]" style={{ background: "#0B1117" }}>
            <CorridorSelector
              countries={countries}
              from={from}
              to={to}
              amount={amount}
              loading={loading}
              onFrom={setFrom}
              onTo={setTo}
              onAmount={setAmount}
              onSimulate={simulate}
            />

            {/* Hop summary strip */}
            {result && (
              <div className="flex gap-2 overflow-x-auto pb-1 mt-2">
                {result.hops.map((hop, i) => (
                  <button
                    key={i}
                    onClick={() => setActiveHop(activeHop === i ? null : i)}
                    className={`flex-shrink-0 px-3 py-1.5 rounded text-[10px] border transition-all ${
                      activeHop === i
                        ? "border-[#38BDF8] text-[#38BDF8] bg-[#38BDF8]/10"
                        : "border-[#1F2937] text-slate-500 hover:border-slate-600"
                    }`}
                  >
                    <span className="font-semibold">{hop.role.split(" ")[0]}</span>{" "}
                    <span className="opacity-60">{hop.country}</span>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Flow Stage */}
          <div className="flex-1 relative">
            <PaymentFlowStage
              hops={result?.hops ?? []}
              activeHop={activeHop}
              onHopClick={i => setActiveHop(activeHop === i ? null : i)}
            />

            {/* Active hop detail overlay */}
            {result && activeHop !== null && result.hops[activeHop] && (
              <div
                className="absolute bottom-4 left-4 glass-card p-4 glow-cyan"
                style={{ minWidth: 280, maxWidth: 360 }}
              >
                {(() => {
                  const hop = result.hops[activeHop];
                  return (
                    <>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-[10px] tracking-widest text-[#38BDF8] uppercase">
                          Hop {hop.hop_number} Detail
                        </span>
                        <button
                          onClick={() => setActiveHop(null)}
                          className="text-slate-600 hover:text-slate-400 text-xs"
                        >
                          ✕
                        </button>
                      </div>
                      <p className="text-sm font-semibold text-slate-200 mb-0.5">
                        {hop.institution}
                      </p>
                      <p className="text-[10px] text-slate-500 mb-3">
                        {hop.role} · {hop.swift_code}
                      </p>
                      <div className="grid grid-cols-3 gap-3 text-center">
                        <div>
                          <p className="text-[9px] text-slate-500 mb-0.5">Fee</p>
                          <p className="text-sm text-red-400 font-bold">−${hop.fee_usd}</p>
                        </div>
                        <div>
                          <p className="text-[9px] text-slate-500 mb-0.5">Delay</p>
                          <p className="text-sm text-amber-400 font-bold">{hop.delay_hours}h</p>
                        </div>
                        <div>
                          <p className="text-[9px] text-slate-500 mb-0.5">After Hop</p>
                          <p className="text-sm text-[#38BDF8] font-bold">
                            ${hop.amount_after_hop.toLocaleString()}
                          </p>
                        </div>
                      </div>
                      {hop.sanctions_flag === "MANUAL_REVIEW" && (
                        <div className="mt-3 p-2 bg-red-950 rounded border border-red-900">
                          <p className="text-[10px] text-red-400">
                            ⚠ Compliance hold — payment queued for manual AML/sanctions review.
                            Adds 24–48h to settlement time.
                          </p>
                        </div>
                      )}
                      <div className="mt-2 pt-2 border-t border-[#1F2937]">
                        <div className="flex justify-between">
                          <span className="text-[9px] text-slate-500">Cumulative Fee</span>
                          <span className="text-[10px] text-red-400">
                            ${hop.cumulative_fee_usd}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-[9px] text-slate-500">Cumulative Time</span>
                          <span className="text-[10px] text-amber-400">
                            {hop.cumulative_hours}h
                          </span>
                        </div>
                      </div>
                    </>
                  );
                })()}
              </div>
            )}
          </div>
        </main>

        {/* Intelligence Sidebar 30% */}
        <div style={{ width: "30%", background: "#0B1117" }}>
          <IntelligenceSidebar
            result={result}
            loading={loading}
            onDownload={handleDownload}
          />
        </div>
      </div>
    </div>
  );
}
