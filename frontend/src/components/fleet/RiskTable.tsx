import type { MachineRecord } from "../../types/telemetry";
import { fleetByRisk } from "../../data/mockFleetData";

const RISK_TEXT: Record<string, string> = {
  LOW: "text-status-healthy",
  MEDIUM: "text-status-warning",
  HIGH: "text-copper-400",
  CRITICAL: "text-status-critical",
};

const TREND_TEXT: Record<string, string> = {
  Stable: "text-ink-500",
  Improving: "text-status-healthy",
  Declining: "text-status-warning",
  "Rapid decline": "text-status-critical",
};

const ACTION_STYLE: Record<string, string> = {
  Monitor: "border-steel-600 text-ink-500",
  Inspect: "border-status-warning/50 text-status-warning",
  Schedule: "border-copper-500/50 text-copper-400",
  Immediate: "border-status-critical/60 text-status-critical",
};

export function RiskTable({ rows }: { rows?: MachineRecord[] }) {
  const data = rows ?? fleetByRisk.slice(0, 12);

  return (
    <div className="rounded-sm border border-steel-700 bg-charcoal">
      <div className="p-5 pb-0">
        <div className="text-[13px] font-semibold uppercase tracking-wide text-ink-100">Risk Analysis</div>
        <div className="text-[11.5px] text-ink-500 mb-1">Ranked by predicted risk, highest first</div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full mt-3 border-collapse min-w-[720px]">
          <thead>
            <tr className="border-y border-steel-700 text-[10px] uppercase tracking-wide text-ink-700">
              <th className="text-left font-medium py-2 px-5">Unit</th>
              <th className="text-left font-medium py-2 px-3">Health</th>
              <th className="text-left font-medium py-2 px-3">RUL</th>
              <th className="text-left font-medium py-2 px-3">Risk</th>
              <th className="text-left font-medium py-2 px-3">Trend</th>
              <th className="text-left font-medium py-2 px-3">Signal</th>
              <th className="text-left font-medium py-2 px-5">Action</th>
            </tr>
          </thead>
          <tbody>
            {data.map((m) => (
              <tr key={m.machine_id} className="border-b border-steel-800 hover:bg-steel-800/60 transition-colors">
                <td className="py-2.5 px-5 font-mono text-[12px] text-ink-100">{m.machine_id}</td>
                <td className="py-2.5 px-3 font-mono text-[12px] tabular text-ink-300">{m.health_score}%</td>
                <td className="py-2.5 px-3 font-mono text-[12px] tabular text-ink-300">{m.rul}</td>
                <td className={`py-2.5 px-3 font-mono text-[11px] font-semibold ${RISK_TEXT[m.risk_level]}`}>
                  {m.risk_level}
                </td>
                <td className={`py-2.5 px-3 text-[12px] ${TREND_TEXT[m.trend]}`}>{m.trend}</td>
                <td className="py-2.5 px-3 text-[12px] text-ink-500">{m.signal}</td>
                <td className="py-2.5 px-5">
                  <span className={`inline-block px-2 py-0.5 text-[10.5px] font-mono border rounded-[2px] ${ACTION_STYLE[m.recommendation]}`}>
                    {m.recommendation}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
