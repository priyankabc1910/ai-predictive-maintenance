import { SectionLabel } from "../components/ui/SectionLabel";
import { ActivityTimeline } from "../components/activity/ActivityTimeline";
import { fleetByRisk } from "../data/mockFleetData";

const GROUPS = ["Immediate", "Schedule", "Inspect", "Monitor"] as const;

const GROUP_STYLE: Record<string, string> = {
  Immediate: "border-l-status-critical",
  Schedule: "border-l-copper-500",
  Inspect: "border-l-status-warning",
  Monitor: "border-l-steel-500",
};

export default function Maintenance() {
  return (
    <div className="p-4 md:p-6 flex flex-col gap-5 max-w-[1600px] mx-auto">
      <SectionLabel index="05" title="Maintenance" meta="Work queue, generated from model output" />

      <div className="grid grid-cols-1 xl:grid-cols-[1fr_320px] gap-5">
        <div className="rounded-sm border border-steel-700 bg-charcoal p-5">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {GROUPS.map((g) => {
              const units = fleetByRisk.filter((m) => m.recommendation === g);
              if (units.length === 0) return null;
              return (
                <div key={g} className={`border-l-2 ${GROUP_STYLE[g]} pl-3`}>
                  <div className="flex items-baseline justify-between mb-2">
                    <span className="text-[12px] font-semibold uppercase tracking-wide text-ink-100">{g}</span>
                    <span className="font-mono text-[10.5px] text-ink-700">{units.length} units</span>
                  </div>
                  <div className="flex flex-col gap-1.5">
                    {units.slice(0, 6).map((m) => (
                      <div key={m.machine_id} className="flex items-center justify-between text-[11.5px]">
                        <span className="font-mono text-ink-100">{m.machine_id}</span>
                        <span className="text-ink-500">{m.signal}</span>
                      </div>
                    ))}
                    {units.length > 6 && (
                      <span className="font-mono text-[10.5px] text-ink-700">+{units.length - 6} more</span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <ActivityTimeline />
      </div>
    </div>
  );
}
