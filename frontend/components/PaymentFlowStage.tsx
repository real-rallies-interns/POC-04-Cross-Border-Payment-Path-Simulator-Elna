"use client";

import ReactFlow, {
  Background,
  Controls,
  MarkerType,
  type Node,
  type Edge,
} from "reactflow";
import "reactflow/dist/style.css";
import { Hop } from "@/lib/api";

interface Props {
  hops: Hop[];
  activeHop: number | null;
  onHopClick: (idx: number) => void;
}

function roleColor(role: string) {
  if (role === "Originating Bank") return "#38BDF8";
  if (role === "Receiving Bank") return "#818CF8";
  return "#F59E0B"; // correspondent = amber
}

function flagBg(flag: string) {
  if (flag === "MANUAL_REVIEW") return "#7F1D1D";
  return "#0B1117";
}

function buildNodes(hops: Hop[], activeHop: number | null): Node[] {
  return hops.map((hop, i) => ({
    id: `hop-${i}`,
    position: { x: i * 240, y: 120 },
    data: { hop, index: i, active: activeHop === i },
    type: "hopNode",
  }));
}

function buildEdges(hops: Hop[]): Edge[] {
  return hops.slice(0, -1).map((hop, i) => ({
    id: `e-${i}`,
    source: `hop-${i}`,
    target: `hop-${i + 1}`,
    animated: true,
    style: {
      stroke: hop.sanctions_flag === "MANUAL_REVIEW" ? "#EF4444" : "#38BDF8",
      strokeWidth: 2,
    },
    markerEnd: {
      type: MarkerType.ArrowClosed,
      color: hop.sanctions_flag === "MANUAL_REVIEW" ? "#EF4444" : "#38BDF8",
    },
    label: `$${hop.fee_usd} · ${hop.delay_hours}h`,
    labelStyle: { fill: "#94A3B8", fontSize: 9, fontFamily: "Inter" },
    labelBgStyle: { fill: "#030712", fillOpacity: 0.8 },
  }));
}

function HopNode({ data }: { data: { hop: Hop; index: number; active: boolean } }) {
  const { hop, active } = data;
  const color = roleColor(hop.role);
  return (
    <div
      className="rounded-lg p-3 cursor-pointer transition-all"
      style={{
        background: flagBg(hop.sanctions_flag),
        border: `1px solid ${active ? color : "#1F2937"}`,
        boxShadow: active ? `0 0 0 0.5px ${color}, 0 0 16px ${color}33` : "none",
        width: 180,
        minHeight: 120,
      }}
    >
      <div className="flex items-center justify-between mb-2">
        <span
          className="text-[9px] tracking-widest uppercase font-semibold"
          style={{ color }}
        >
          {hop.role}
        </span>
        {hop.sanctions_flag === "MANUAL_REVIEW" && (
          <span className="text-[8px] bg-red-900 text-red-300 px-1.5 py-0.5 rounded">
            ⚠ REVIEW
          </span>
        )}
      </div>
      <p className="text-xs font-semibold text-slate-200 leading-tight mb-1">
        {hop.institution}
      </p>
      <p className="text-[10px] text-slate-500 mb-2">{hop.country} · {hop.swift_code}</p>
      <div className="grid grid-cols-2 gap-1">
        <div>
          <p className="text-[9px] text-slate-500">Fee</p>
          <p className="text-xs text-red-400 font-semibold">−${hop.fee_usd}</p>
        </div>
        <div>
          <p className="text-[9px] text-slate-500">Delay</p>
          <p className="text-xs text-amber-400 font-semibold">{hop.delay_hours}h</p>
        </div>
      </div>
      <div className="mt-2 pt-2 border-t border-[#1F2937]">
        <p className="text-[9px] text-slate-500">After hop</p>
        <p className="text-xs text-[#38BDF8] font-semibold">${hop.amount_after_hop.toLocaleString()}</p>
      </div>
    </div>
  );
}

const nodeTypes = { hopNode: HopNode };

export default function PaymentFlowStage({ hops, activeHop, onHopClick }: Props) {
  if (!hops.length) {
    return (
      <div className="w-full h-full flex flex-col items-center justify-center gap-4">
        <div className="text-6xl opacity-20">↗</div>
        <p className="text-slate-500 text-sm tracking-wider">
          Select a corridor and simulate to see the payment path
        </p>
      </div>
    );
  }

  const nodes = buildNodes(hops, activeHop);
  const edges = buildEdges(hops);

  const stageWidth = hops.length * 240 + 60;

  return (
    <div style={{ width: "100%", height: "100%" }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        onNodeClick={(_, node) => {
          const idx = parseInt(node.id.split("-")[1]);
          onHopClick(idx);
        }}
        fitView
        fitViewOptions={{ padding: 0.3 }}
        minZoom={0.3}
        defaultViewport={{ x: 0, y: 0, zoom: 0.85 }}
        proOptions={{ hideAttribution: true }}
      >
        <Background color="#1F2937" gap={24} size={1} />
        <Controls showInteractive={false} />
      </ReactFlow>
    </div>
  );
}
