import { SectionLabel } from "../components/ui/SectionLabel";
import { RULTrajectoryChart } from "../components/rul/RULTrajectoryChart";
import { fleetByRisk } from "../data/mockFleetData";

export default function RULPredictions() {
  const ranked = [...fleetByRisk].sort((a, b) => a.rul - b.rul).slice(0, 15);

  return (
    <div className="p-4 md:p-6 flex flex-col gap-5 max-w-[1600px] mx-auto">
      <SectionLabel index="03" title="RUL Predictions" meta="Model RUL-XGB v2.3" />

      <RULTrajectoryChart />

      <div className="rounded-sm border border-steel-700 bg-charcoal p-5">
        <div className="text-[13px] font-semibold uppercase tracking-wide text-ink-100 mb-1">Shortest Remaining Life</div>
        <div className="text-[11.5px] text-ink-500 mb-4">Units ranked by ascending predicted RUL, in cycles</div>

        <div className="flex flex-col">
          {ranked.map((m, i) => {
            const maxRul = ranked[ranked.length - 1].rul || 1;
            const pct = Math.max(4, Math.round((m.rul / maxRul) * 100));
            return (
              <div key={m.machine_id} className="flex items-center gap-3 py-2 border-b border-steel-800 last:border-0">
                <span className="font-mono text-[10px] text-ink-700 w-5 shrink-0">{i + 1}</span>
                <span className="font-mono text-[12px] text-ink-100 w-20 shrink-0">{m.machine_id}</span>
                <div className="flex-1 h-1.5 bg-steel-800 rounded-full overflow-hidden">
                  <div
                    className={`h-full ${
                      m.rul <= 10 ? "bg-status-critical" : m.rul <= 25 ? "bg-copper-500" : "bg-status-warning"
                    }`}
                    style={{ width: `${pct}%` }}
                  />
                </div>
                <span className="font-mono text-[12px] tabular text-ink-300 w-16 text-right shrink-0">{m.rul} cyc</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
