import { useMemo, useState } from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
} from "recharts";
import { rulTrajectories } from "../../data/mockRULData";
import { getMachine } from "../../data/mockFleetData";

const LINE_COLORS: Record<string, string> = {
  "UNIT-001": "#7c9473", // healthy - sage
  "UNIT-024": "#c9b06a", // borderline - muted amber-olive
  "UNIT-067": "#d9a441", // warning - amber
  "UNIT-083": "#c1652f", // high - copper
  "UNIT-091": "#c1443a", // critical - red
};

function buildChartData() {
  const maxCycle = Math.max(...rulTrajectories.map((t) => t.points[t.points.length - 1]?.cycle ?? 0));
  const cycles = Array.from({ length: 25 }, (_, i) => Math.round((i / 24) * maxCycle));

  return cycles.map((cycle) => {
    const row: Record<string, number | null> = { cycle };
    rulTrajectories.forEach((traj) => {
      const point = traj.points.reduce((closest, p) =>
        Math.abs(p.cycle - cycle) < Math.abs(closest.cycle - cycle) ? p : closest
      , traj.points[0]);
      row[traj.machine_id] = point ? point.predicted_rul : null;
    });
    return row;
  });
}

export function RULTrajectoryChart() {
  const data = useMemo(() => buildChartData(), []);
  const [hidden, setHidden] = useState<Set<string>>(new Set());

  function toggle(id: string) {
    setHidden((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  }

  return (
    <div className="rounded-sm border border-steel-700 bg-charcoal p-5">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-1">
        <div>
          <div className="text-[13px] font-semibold uppercase tracking-wide text-ink-100">Remaining Useful Life</div>
          <div className="text-[11.5px] text-ink-500">Predicted degradation trajectories, five representative units</div>
        </div>
        <div className="flex items-center gap-1.5 font-mono text-[10.5px]">
          <span className="text-ink-700">MODEL</span>
          <span className="text-copper-400">RUL-XGB v2.3</span>
        </div>
      </div>

      <div className="h-[260px] md:h-[300px] mt-3">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 8, right: 12, bottom: 0, left: -12 }}>
            <CartesianGrid stroke="#262b27" vertical={false} />
            <XAxis
              dataKey="cycle"
              stroke="#454d46"
              tick={{ fill: "#6b6a60", fontSize: 10.5, fontFamily: "JetBrains Mono" }}
              tickLine={false}
              axisLine={{ stroke: "#333a34" }}
              label={{ value: "OPERATING CYCLE", position: "insideBottom", offset: -4, fill: "#454d46", fontSize: 9.5 }}
            />
            <YAxis
              stroke="#454d46"
              tick={{ fill: "#6b6a60", fontSize: 10.5, fontFamily: "JetBrains Mono" }}
              tickLine={false}
              axisLine={false}
              width={38}
              label={{ value: "RUL", angle: -90, position: "insideLeft", fill: "#454d46", fontSize: 9.5 }}
            />
            <ReferenceLine y={10} stroke="#c1443a" strokeDasharray="3 3" strokeOpacity={0.5} />
            <Tooltip
              contentStyle={{
                background: "#171a18",
                border: "1px solid #333a34",
                borderRadius: 2,
                fontSize: 11.5,
                fontFamily: "JetBrains Mono",
              }}
              labelStyle={{ color: "#9a978a", fontSize: 10 }}
              itemStyle={{ padding: 0 }}
              labelFormatter={(v) => `CYCLE ${v}`}
            />
            {rulTrajectories.map((t) => (
              <Line
                key={t.machine_id}
                type="monotone"
                dataKey={t.machine_id}
                stroke={LINE_COLORS[t.machine_id]}
                strokeWidth={t.machine_id === "UNIT-091" ? 2.25 : 1.6}
                dot={false}
                hide={hidden.has(t.machine_id)}
                connectNulls
                isAnimationActive={false}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="flex flex-wrap gap-x-5 gap-y-2 mt-3 pt-3 border-t border-steel-700">
        {rulTrajectories.map((t) => {
          const machine = getMachine(t.machine_id);
          const isHidden = hidden.has(t.machine_id);
          return (
            <button
              key={t.machine_id}
              onClick={() => toggle(t.machine_id)}
              className={`flex items-center gap-1.5 text-[11px] font-mono transition-opacity ${
                isHidden ? "opacity-35" : "opacity-100"
              }`}
            >
              <span className="size-2 rounded-full" style={{ backgroundColor: LINE_COLORS[t.machine_id] }} />
              <span className="text-ink-100">{t.machine_id}</span>
              <span className="text-ink-700">{machine?.rul} cyc</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
