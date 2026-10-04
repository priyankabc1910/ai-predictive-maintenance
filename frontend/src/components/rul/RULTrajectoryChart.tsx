import { useEffect, useMemo, useState } from "react";
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

import {
  getRULTrajectory,
  type RULTrajectory,
} from "../../api/predictiveMaintenance";

const LINE_COLORS: Record<string, string> = {
  "UNIT-001": "#7c9473",
  "UNIT-024": "#c9b06a",
  "UNIT-067": "#d9a441",
  "UNIT-083": "#c1652f",
  "UNIT-091": "#c1443a",
};

const REPRESENTATIVE_ENGINES = [1, 24, 67, 83, 91];

export function RULTrajectoryChart() {
  const [trajectories, setTrajectories] = useState<RULTrajectory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [hidden, setHidden] = useState<Set<string>>(new Set());

  useEffect(() => {
    async function loadTrajectories() {
      try {
        const results = await Promise.all(
          REPRESENTATIVE_ENGINES.map((engineId) =>
            getRULTrajectory(engineId)
          )
        );

        setTrajectories(results);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load RUL trajectories"
        );
      } finally {
        setLoading(false);
      }
    }

    loadTrajectories();
  }, []);

  const data = useMemo(() => {
    const cycles = Array.from(
      new Set(
        trajectories.flatMap((trajectory) =>
          trajectory.trajectory.map((point) => point.cycle)
        )
      )
    ).sort((a, b) => a - b);

    return cycles.map((cycle) => {
      const row: Record<string, number | null> = {
        cycle,
      };

      trajectories.forEach((trajectory) => {
        const point = trajectory.trajectory.find(
          (item) => item.cycle === cycle
        );

        row[trajectory.machine_id] =
          point?.predicted_rul ?? null;
      });

      return row;
    });
  }, [trajectories]);

  function toggle(machineId: string) {
    setHidden((previous) => {
      const next = new Set(previous);

      if (next.has(machineId)) {
        next.delete(machineId);
      } else {
        next.add(machineId);
      }

      return next;
    });
  }

  if (loading) {
    return (
      <div className="rounded-sm border border-steel-700 bg-charcoal p-5">
        <div className="font-mono text-xs text-ink-500">
          Loading live LSTM RUL trajectories...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-sm border border-status-critical/40 bg-charcoal p-5">
        <div className="font-mono text-xs text-status-critical">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-sm border border-steel-700 bg-charcoal p-5">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-1">
        <div>
          <div className="text-[13px] font-semibold uppercase tracking-wide text-ink-100">
            Remaining Useful Life
          </div>

          <div className="text-[11.5px] text-ink-500">
            LSTM-predicted degradation trajectories across representative units
          </div>
        </div>

        <div className="flex items-center gap-1.5 font-mono text-[10.5px]">
          <span className="text-ink-700">
            MODEL
          </span>

          <span className="text-copper-400">
            LSTM · 30C · 12S
          </span>
        </div>
      </div>

      <div className="h-[260px] md:h-[300px] mt-3">
        <ResponsiveContainer
          width="100%"
          height="100%"
        >
          <LineChart
            data={data}
            margin={{
              top: 8,
              right: 12,
              bottom: 0,
              left: -12,
            }}
          >
            <CartesianGrid
              stroke="#262b27"
              vertical={false}
            />

            <XAxis
              dataKey="cycle"
              stroke="#454d46"
              tick={{
                fill: "#6b6a60",
                fontSize: 10.5,
                fontFamily: "JetBrains Mono",
              }}
              tickLine={false}
              axisLine={{
                stroke: "#333a34",
              }}
              label={{
                value: "OPERATING CYCLE",
                position: "insideBottom",
                offset: -4,
                fill: "#454d46",
                fontSize: 9.5,
              }}
            />

            <YAxis
              stroke="#454d46"
              tick={{
                fill: "#6b6a60",
                fontSize: 10.5,
                fontFamily: "JetBrains Mono",
              }}
              tickLine={false}
              axisLine={false}
              width={45}
              label={{
                value: "RUL",
                angle: -90,
                position: "insideLeft",
                fill: "#454d46",
                fontSize: 9.5,
              }}
            />

            <ReferenceLine
              y={10}
              stroke="#c1443a"
              strokeDasharray="3 3"
              strokeOpacity={0.5}
            />

            <Tooltip
              contentStyle={{
                background: "#171a18",
                border: "1px solid #333a34",
                borderRadius: 2,
                fontSize: 11.5,
                fontFamily: "JetBrains Mono",
              }}
              labelStyle={{
                color: "#9a978a",
                fontSize: 10,
              }}
              itemStyle={{
                padding: 0,
              }}
              labelFormatter={(value) =>
                `CYCLE ${value}`
              }
            />

            {trajectories.map(
              (trajectory, index) => {
                const color =
                  LINE_COLORS[
                    trajectory.machine_id
                  ] ??
                  [
                    "#7c9473",
                    "#c9b06a",
                    "#d9a441",
                    "#c1652f",
                    "#c1443a",
                  ][index];

                return (
                  <Line
                    key={trajectory.machine_id}
                    type="monotone"
                    dataKey={trajectory.machine_id}
                    stroke={color}
                    strokeWidth={
                      index === 4
                        ? 2.25
                        : 1.6
                    }
                    dot={false}
                    hide={hidden.has(
                      trajectory.machine_id
                    )}
                    connectNulls
                    isAnimationActive={false}
                  />
                );
              }
            )}
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="flex flex-wrap gap-x-5 gap-y-2 mt-3 pt-3 border-t border-steel-700">
        {trajectories.map(
          (trajectory, index) => {
            const isHidden = hidden.has(
              trajectory.machine_id
            );

            const latest =
              trajectory.trajectory[
                trajectory.trajectory.length - 1
              ];

            const color =
              LINE_COLORS[
                trajectory.machine_id
              ] ??
              [
                "#7c9473",
                "#c9b06a",
                "#d9a441",
                "#c1652f",
                "#c1443a",
              ][index];

            return (
              <button
                key={trajectory.machine_id}
                onClick={() =>
                  toggle(
                    trajectory.machine_id
                  )
                }
                className={`flex items-center gap-1.5 text-[11px] font-mono transition-opacity ${
                  isHidden
                    ? "opacity-35"
                    : "opacity-100"
                }`}
              >
                <span
                  className="size-2 rounded-full"
                  style={{
                    backgroundColor: color,
                  }}
                />

                <span className="text-ink-100">
                  {trajectory.machine_id}
                </span>

                <span className="text-ink-700">
                  {latest?.predicted_rul ?? "--"} cyc
                </span>
              </button>
            );
          }
        )}
      </div>
    </div>
  );
}