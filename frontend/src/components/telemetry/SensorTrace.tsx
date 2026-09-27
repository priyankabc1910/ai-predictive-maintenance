import { ResponsiveContainer, LineChart, Line, YAxis } from "recharts";
import type { SensorTrace as SensorTraceType } from "../../types/telemetry";

export function SensorTrace({ trace }: { trace: SensorTraceType }) {
  const data = trace.values.map((v, i) => ({ i, v }));
  const latest = trace.values[trace.values.length - 1];
  const first = trace.values[0];
  const delta = latest - first;
  const rising = delta > 0;

  return (
    <div className="border border-steel-700 bg-steel-800/40 p-3">
      <div className="flex items-baseline justify-between mb-1">
        <span className="font-mono text-[11px] text-ink-300">{trace.label}</span>
        <span className="font-mono text-[10px] text-ink-700">{trace.unit}</span>
      </div>
      <div className="flex items-end justify-between">
        <span className="font-mono text-lg font-semibold text-ink-100 tabular">{latest}</span>
        <span className={`font-mono text-[10.5px] tabular ${rising ? "text-copper-400" : "text-sage-400"}`}>
          {rising ? "+" : ""}
          {delta.toFixed(1)}
        </span>
      </div>
      <div className="h-9 mt-1 -mx-1">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 2, right: 2, bottom: 0, left: 2 }}>
            <YAxis hide domain={["dataMin - 1", "dataMax + 1"]} />
            <Line
              type="monotone"
              dataKey="v"
              stroke={rising ? "#e2934f" : "#a8b894"}
              strokeWidth={1.4}
              dot={false}
              isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
