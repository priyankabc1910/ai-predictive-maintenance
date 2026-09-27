import { useState } from "react";
import { fleetByRisk } from "../../data/mockFleetData";
import { MachineTile } from "./MachineTile";

const FILTERS = ["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"] as const;
type Filter = (typeof FILTERS)[number];

export function FleetGrid({ limit }: { limit?: number }) {
  const [filter, setFilter] = useState<Filter>("ALL");

  const filtered = fleetByRisk.filter((m) => filter === "ALL" || m.risk_level === filter);
  const shown = limit ? filtered.slice(0, limit) : filtered;

  return (
    <div className="rounded-sm border border-steel-700 bg-charcoal p-5">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
        <div>
          <div className="text-[13px] font-semibold uppercase tracking-wide text-ink-100">Machine Fleet</div>
          <div className="text-[11.5px] text-ink-500">{shown.length} of {fleetByRisk.length} units shown</div>
        </div>
        <div className="flex gap-1">
          {FILTERS.map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-2.5 py-1 text-[10.5px] font-mono border transition-colors ${
                filter === f
                  ? "border-copper-500/60 text-copper-400 bg-copper-500/10"
                  : "border-steel-600 text-ink-700 hover:text-ink-300"
              }`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-2.5">
        {shown.map((m) => (
          <MachineTile key={m.machine_id} machine={m} />
        ))}
      </div>
    </div>
  );
}
