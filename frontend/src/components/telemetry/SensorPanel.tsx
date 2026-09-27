import { sensorTraces, sensorFocusMachine } from "../../data/mockTelemetry";
import { SensorTrace } from "./SensorTrace";

export function SensorPanel() {
  return (
    <div className="rounded-sm border border-steel-700 bg-charcoal p-5">
      <div className="flex items-baseline justify-between mb-4">
        <div>
          <div className="text-[13px] font-semibold uppercase tracking-wide text-ink-100">Sensor Intelligence</div>
          <div className="text-[11.5px] text-ink-500">
            Live telemetry &middot; <span className="font-mono text-ink-300">{sensorFocusMachine}</span>
          </div>
        </div>
        <span className="font-mono text-[10.5px] text-ink-700">30s refresh</span>
      </div>

      <div className="grid grid-cols-2 gap-2.5">
        {sensorTraces.map((t) => (
          <SensorTrace key={t.sensor_id} trace={t} />
        ))}
      </div>
    </div>
  );
}
