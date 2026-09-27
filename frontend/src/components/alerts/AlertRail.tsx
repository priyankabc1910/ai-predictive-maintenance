import { AlertTriangle } from "lucide-react";
import { alerts } from "../../data/mockAlerts";
import type { AlertSeverity } from "../../types/telemetry";

const SEVERITY_STYLE: Record<AlertSeverity, { border: string; text: string; bg: string }> = {
  CRITICAL: { border: "border-l-status-critical", text: "text-status-critical", bg: "bg-status-critical/[0.06]" },
  HIGH: { border: "border-l-copper-500", text: "text-copper-400", bg: "bg-copper-500/[0.05]" },
  MEDIUM: { border: "border-l-status-warning", text: "text-status-warning", bg: "bg-status-warning/[0.05]" },
};

export function AlertRail() {
  return (
    <div className="rounded-sm border border-steel-700 bg-charcoal p-5 h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <div className="text-[13px] font-semibold uppercase tracking-wide text-ink-100">Active Alerts</div>
        <span className="font-mono text-[10.5px] text-ink-700">{alerts.length} open</span>
      </div>

      <div className="flex flex-col gap-2 flex-1">
        {alerts.map((a) => {
          const s = SEVERITY_STYLE[a.severity];
          return (
            <div key={a.id} className={`border-l-2 ${s.border} ${s.bg} pl-3 pr-2.5 py-2.5`}>
              <div className="flex items-center justify-between gap-2">
                <span className={`text-[10px] font-mono font-semibold tracking-wide ${s.text}`}>
                  {a.severity}
                </span>
                <span className="font-mono text-[10px] text-ink-700">{a.timestamp}</span>
              </div>
              <div className="flex items-center gap-1.5 mt-1">
                <AlertTriangle size={11} className={s.text} strokeWidth={2} />
                <span className="font-mono text-[11.5px] text-ink-100">{a.machine_id}</span>
              </div>
              <p className="text-[11.5px] text-ink-500 mt-1 leading-snug">{a.message}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
