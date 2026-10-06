import type { FleetMaintenanceItem } from "../../api/predictiveMaintenance";

const PRIORITY_TEXT: Record<string, string> = {
  IMMEDIATE: "text-status-critical",
  URGENT: "text-copper-400",
  PLANNED: "text-status-warning",
  ROUTINE: "text-ink-400",
};

const PRIORITY_BORDER: Record<string, string> = {
  IMMEDIATE: "border-status-critical/60 text-status-critical",
  URGENT: "border-copper-500/50 text-copper-400",
  PLANNED: "border-status-warning/50 text-status-warning",
  ROUTINE: "border-steel-600 text-ink-500",
};

export function RiskTable({
  rows,
}: {
  rows: FleetMaintenanceItem[];
}) {
  return (
    <div className="rounded-sm border border-steel-700 bg-charcoal">
      <div className="p-5 pb-0">
        <div className="text-[13px] font-semibold uppercase tracking-wide text-ink-100">
          Fleet Maintenance Ranking
        </div>

        <div className="text-[11.5px] text-ink-500 mb-1">
          Ranked by maintenance priority and maintenance score
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full mt-3 border-collapse min-w-[720px]">
          <thead>
            <tr className="border-y border-steel-700 text-[10px] uppercase tracking-wide text-ink-700">
              <th className="text-left font-medium py-2 px-5">
                Rank
              </th>

              <th className="text-left font-medium py-2 px-3">
                Unit
              </th>

              <th className="text-left font-medium py-2 px-3">
                Maintenance Score
              </th>

              <th className="text-left font-medium py-2 px-3">
                RUL
              </th>

              <th className="text-left font-medium py-2 px-3">
                Priority
              </th>

              <th className="text-left font-medium py-2 px-5">
                Action
              </th>
            </tr>
          </thead>

          <tbody>
            {rows.slice(0, 20).map((item) => {
              const priority = item.priority.toUpperCase();

              return (
                <tr
                  key={item.machine_id}
                  className="border-b border-steel-800 hover:bg-steel-800/60 transition-colors"
                >
                  <td className="py-2.5 px-5 font-mono text-[12px] text-ink-500">
                    #{item.fleet_rank}
                  </td>

                  <td className="py-2.5 px-3 font-mono text-[12px] text-ink-100">
                    {item.machine_id}
                  </td>

                  <td className="py-2.5 px-3 font-mono text-[12px] tabular text-ink-300">
                    {item.maintenance_score.toFixed(1)}
                  </td>

                  <td className="py-2.5 px-3 font-mono text-[12px] tabular text-ink-300">
                    {item.rul.toFixed(1)}
                  </td>

                  <td
                    className={`py-2.5 px-3 font-mono text-[11px] font-semibold ${
                      PRIORITY_TEXT[priority] ?? "text-ink-400"
                    }`}
                  >
                    {priority}
                  </td>

                  <td className="py-2.5 px-5">
                    <span
                      className={`inline-block px-2 py-0.5 text-[10.5px] font-mono border rounded-[2px] ${
                        PRIORITY_BORDER[priority] ??
                        "border-steel-600 text-ink-500"
                      }`}
                    >
                      {priority === "IMMEDIATE"
                        ? "Immediate maintenance"
                        : priority === "URGENT"
                          ? "Schedule soon"
                          : priority === "PLANNED"
                            ? "Plan maintenance"
                            : "Routine monitoring"}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}