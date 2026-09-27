import { SectionLabel } from "../components/ui/SectionLabel";
import { AlertRail } from "../components/alerts/AlertRail";
import { SensorPanel } from "../components/telemetry/SensorPanel";
import { fleetData } from "../data/mockFleetData";

export default function Anomalies() {
  const ranked = [...fleetData].sort((a, b) => b.anomaly_score - a.anomaly_score).slice(0, 10);

  return (
    <div className="p-4 md:p-6 flex flex-col gap-5 max-w-[1600px] mx-auto">
      <SectionLabel index="04" title="Anomalies" meta="Anomaly detection layer" />

      <div className="grid grid-cols-1 xl:grid-cols-[1fr_320px] gap-5">
        <div className="rounded-sm border border-steel-700 bg-charcoal p-5">
          <div className="text-[13px] font-semibold uppercase tracking-wide text-ink-100 mb-1">Anomaly Score Ranking</div>
          <div className="text-[11.5px] text-ink-500 mb-4">Deviation from expected sensor envelope, 0&ndash;1 scale</div>

          <div className="flex flex-col gap-2">
            {ranked.map((m) => (
              <div key={m.machine_id} className="flex items-center gap-3">
                <span className="font-mono text-[12px] text-ink-100 w-20 shrink-0">{m.machine_id}</span>
                <div className="flex-1 h-2 bg-steel-800 overflow-hidden">
                  <div
                    className={`h-full ${
                      m.anomaly_score > 0.7 ? "bg-status-critical" : m.anomaly_score > 0.4 ? "bg-copper-500" : "bg-status-warning"
                    }`}
                    style={{ width: `${Math.round(m.anomaly_score * 100)}%` }}
                  />
                </div>
                <span className="font-mono text-[12px] tabular text-ink-300 w-12 text-right shrink-0">
                  {m.anomaly_score.toFixed(2)}
                </span>
                <span className="text-[11.5px] text-ink-500 w-40 truncate hidden sm:block">{m.signal}</span>
              </div>
            ))}
          </div>
        </div>

        <AlertRail />
      </div>

      <SensorPanel />
    </div>
  );
}
