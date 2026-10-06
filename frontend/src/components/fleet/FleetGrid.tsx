import { useState } from "react";

import type { FleetMaintenanceItem } from "../../api/predictiveMaintenance";

const FILTERS = [
  "ALL",
  "IMMEDIATE",
  "URGENT",
  "PLANNED",
  "ROUTINE",
] as const;

type Filter = (typeof FILTERS)[number];

const PRIORITY_STYLE: Record<string, string> = {
  IMMEDIATE:
    "border-status-critical/50 bg-status-critical/5 text-status-critical",

  URGENT:
    "border-copper-500/40 bg-copper-500/5 text-copper-400",

  PLANNED:
    "border-status-warning/40 bg-status-warning/5 text-status-warning",

  ROUTINE:
    "border-steel-600 bg-steel-800/30 text-ink-400",
};

const PRIORITY_DOT: Record<string, string> = {
  IMMEDIATE: "bg-status-critical",
  URGENT: "bg-copper-400",
  PLANNED: "bg-status-warning",
  ROUTINE: "bg-ink-600",
};

export function FleetGrid({
  fleet,
}: {
  fleet: FleetMaintenanceItem[];
}) {
  const [filter, setFilter] = useState<Filter>("ALL");

  const filtered =
    filter === "ALL"
      ? fleet
      : fleet.filter(
          (item) => item.priority.toUpperCase() === filter
        );

  return (
    <div className="rounded-sm border border-steel-700 bg-charcoal p-5">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
        <div>
          <div className="text-[13px] font-semibold uppercase tracking-wide text-ink-100">
            Machine Fleet
          </div>

          <div className="text-[11.5px] text-ink-500">
            {filtered.length} of {fleet.length} units shown
          </div>
        </div>

        <div className="flex flex-wrap gap-1">
          {FILTERS.map((filterOption) => (
            <button
              key={filterOption}
              onClick={() => setFilter(filterOption)}
              className={`px-2.5 py-1 text-[10.5px] font-mono border transition-colors ${
                filter === filterOption
                  ? "border-copper-500/60 text-copper-400 bg-copper-500/10"
                  : "border-steel-600 text-ink-700 hover:text-ink-300"
              }`}
            >
              {filterOption}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-2.5">
        {filtered.map((machine) => {
          const priority = machine.priority.toUpperCase();

          return (
            <div
              key={machine.machine_id}
              className={`rounded-sm border p-3 transition-colors hover:bg-steel-800/50 ${
                PRIORITY_STYLE[priority] ??
                "border-steel-700 bg-charcoal"
              }`}
            >
              <div className="flex items-center justify-between gap-2">
                <span className="font-mono text-[11px] text-ink-100">
                  {machine.machine_id}
                </span>

                <span
                  className={`w-1.5 h-1.5 rounded-full ${
                    PRIORITY_DOT[priority] ?? "bg-ink-600"
                  }`}
                />
              </div>

              <div className="mt-3">
                <div className="text-[9px] uppercase tracking-wide text-ink-600">
                  Maintenance Score
                </div>

                <div className="mt-0.5 font-mono text-lg text-ink-200 tabular">
                  {machine.maintenance_score.toFixed(1)}
                </div>
              </div>

              <div className="mt-2 flex items-end justify-between">
                <div>
                  <div className="text-[9px] uppercase tracking-wide text-ink-600">
                    RUL
                  </div>

                  <div className="font-mono text-[12px] text-ink-300 tabular">
                    {machine.rul.toFixed(1)}
                  </div>
                </div>

                <div className="text-right">
                  <div className="text-[9px] uppercase tracking-wide text-ink-600">
                    Rank
                  </div>

                  <div className="font-mono text-[12px] text-ink-300 tabular">
                    #{machine.fleet_rank}
                  </div>
                </div>
              </div>

              <div className="mt-3 pt-2 border-t border-steel-700/70">
                <span className="font-mono text-[9px] uppercase tracking-wide">
                  {priority}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {filtered.length === 0 && (
        <div className="py-10 text-center text-[12px] text-ink-600">
          No machines match this priority.
        </div>
      )}
    </div>
  );
}
