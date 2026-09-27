import { SectionLabel } from "../components/ui/SectionLabel";
import { getMachine } from "../data/mockFleetData";

const FEATURES = [
  { name: "Sensor 11 · vibration RMS", weight: 0.34 },
  { name: "Sensor 4 · exhaust temperature", weight: 0.22 },
  { name: "Sensor 7 · pressure ratio", weight: 0.18 },
  { name: "Operating cycles since overhaul", weight: 0.14 },
  { name: "Sensor 15 · rotational speed", weight: 0.12 },
];

export default function Intelligence() {
  const unit = getMachine("UNIT-091");

  return (
    <div className="p-4 md:p-6 flex flex-col gap-5 max-w-[1600px] mx-auto">
      <SectionLabel index="06" title="Intelligence" meta="Explainable AI &middot; model attribution" />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <div className="rounded-sm border border-steel-700 bg-charcoal p-5">
          <div className="text-[13px] font-semibold uppercase tracking-wide text-ink-100 mb-1">Feature Attribution</div>
          <div className="text-[11.5px] text-ink-500 mb-4">
            Aggregate SHAP contribution to RUL prediction, fleet-wide
          </div>
          <div className="flex flex-col gap-3">
            {FEATURES.map((f) => (
              <div key={f.name}>
                <div className="flex items-baseline justify-between mb-1">
                  <span className="text-[12px] text-ink-300">{f.name}</span>
                  <span className="font-mono text-[11px] text-copper-400 tabular">{Math.round(f.weight * 100)}%</span>
                </div>
                <div className="h-1.5 bg-steel-800 overflow-hidden">
                  <div className="h-full bg-copper-500" style={{ width: `${f.weight * 100 * 2.6}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-sm border border-steel-700 bg-charcoal p-5">
          <div className="text-[13px] font-semibold uppercase tracking-wide text-ink-100 mb-1">
            Evidence Summary &middot; <span className="font-mono text-copper-400">{unit?.machine_id}</span>
          </div>
          <div className="text-[11.5px] text-ink-500 mb-4">Grounded reasoning behind the current prediction</div>

          <div className="flex flex-col gap-3 text-[12.5px] text-ink-300 leading-relaxed">
            <p>
              Predicted RUL of <span className="font-mono text-ink-100">{unit?.rul} cycles</span> is driven primarily
              by a sustained rise in vibration RMS on sensor 11, now 2.4 standard deviations above the healthy
              baseline for this unit class.
            </p>
            <p>
              Exhaust temperature has trended upward over the last 40 cycles, consistent with the vibration
              signature and supporting the model&rsquo;s thermal anomaly classification rather than a transient
              sensor fault.
            </p>
            <p>
              Historical units with a similar signature reached functional failure within{" "}
              <span className="font-mono text-ink-100">3&ndash;6 cycles</span> of this profile, which anchors the
              current confidence interval.
            </p>
          </div>

          <div className="mt-4 pt-3 border-t border-steel-700 flex items-center justify-between">
            <span className="font-mono text-[10.5px] text-ink-700">CONFIDENCE</span>
            <span className="font-mono text-[12px] text-status-critical">HIGH &middot; 0.91</span>
          </div>
        </div>
      </div>
    </div>
  );
}
