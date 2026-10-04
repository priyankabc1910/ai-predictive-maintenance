import { useEffect, useState } from "react";
import { getFleet, getFleetSummary, type FleetSummary, type Prediction } from "../../api/predictiveMaintenance";

const STATUS_COLOR: Record<string, string> = {
  HEALTHY: "bg-status-healthy",
  MONITORING: "bg-status-warning",
  CRITICAL: "bg-status-critical",
};

function getStatus(riskLevel: string) {
  if (riskLevel === "CRITICAL") return "CRITICAL";
  if (riskLevel === "HIGH" || riskLevel === "MEDIUM") return "MONITORING";
  return "HEALTHY";
}

export function FleetSpectrum() {
  const [summary, setSummary] = useState<FleetSummary | null>(null);
  const [fleet, setFleet] = useState<Prediction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadFleetData() {
      try {
        const [summaryData, fleetData] = await Promise.all([
          getFleetSummary(),
          getFleet(),
        ]);

        setSummary(summaryData);
        setFleet(fleetData);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load fleet data"
        );
      } finally {
        setLoading(false);
      }
    }

    loadFleetData();
  }, []);

  if (loading) {
    return (
      <div className="rounded-sm border border-steel-700 bg-charcoal p-7">
        <div className="font-mono text-xs text-ink-500">
          Loading live fleet intelligence...
        </div>
      </div>
    );
  }

  if (error || !summary) {
    return (
      <div className="rounded-sm border border-status-critical/40 bg-charcoal p-7">
        <div className="font-mono text-xs text-status-critical">
          {error ?? "Fleet data unavailable"}
        </div>
      </div>
    );
  }

  const healthy = summary.low;
  const monitoring = summary.medium + summary.high;
  const critical = summary.critical;

  const healthyPct = Math.round(
    (healthy / summary.total_machines) * 100
  );

  const fleetByRisk = [...fleet].sort(
    (a, b) => a.rul - b.rul
  );

  return (
    <div className="relative overflow-hidden rounded-sm border border-steel-700 bg-charcoal">
      <div className="absolute inset-0 grid-motif pointer-events-none" />

      <div className="relative p-5 md:p-7">
        <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6 mb-6">
          <div>
            <div className="text-[11px] font-mono text-copper-500 tracking-wide mb-1">
              FLEET-01 / LIVE
            </div>

            <h1 className="text-2xl md:text-[28px] font-semibold tracking-tight text-ink-100">
              Fleet Reliability
            </h1>

            <p className="text-[13px] text-ink-500 mt-1 max-w-md">
              {summary.total_machines} monitored machines across dataset
              FD001. Health computed from live LSTM RUL predictions.
            </p>
          </div>

          <div className="flex items-baseline gap-6 md:gap-10 shrink-0">
            <BigStat
              value={`${healthyPct}%`}
              label="Fleet health index"
              accent="text-copper-400"
            />

            <BigStat
              value={String(healthy)}
              label="Healthy"
              dot="HEALTHY"
            />

            <BigStat
              value={String(monitoring)}
              label="Monitoring"
              dot="MONITORING"
            />

            <BigStat
              value={String(critical)}
              label="Critical"
              dot="CRITICAL"
            />
          </div>
        </div>

        <div className="flex h-9 w-full gap-px rounded-[2px] overflow-hidden">
          {fleetByRisk.map((machine) => {
            const status = getStatus(machine.risk_level);

            return (
              <div
                key={machine.machine_id}
                title={`${machine.machine_id} · ${machine.health_score}% · RUL ${machine.rul}`}
                className={`flex-1 min-w-[2px] ${STATUS_COLOR[status]} opacity-90 hover:opacity-100 transition-opacity`}
              />
            );
          })}
        </div>

        <div className="flex justify-between mt-1.5 font-mono text-[10px] text-ink-700">
          <span>HIGHEST RISK</span>
          <span>LOWEST RISK</span>
        </div>
      </div>
    </div>
  );
}

function BigStat({
  value,
  label,
  dot,
  accent,
}: {
  value: string;
  label: string;
  dot?: string;
  accent?: string;
}) {
  return (
    <div className="flex flex-col items-start">
      <div className="flex items-center gap-1.5">
        {dot && (
          <span
            className={`size-2 rounded-full ${STATUS_COLOR[dot]}`}
          />
        )}

        <span
          className={`font-mono text-2xl md:text-[26px] font-semibold tabular ${
            accent ?? "text-ink-100"
          }`}
        >
          {value}
        </span>
      </div>

      <span className="text-[10.5px] text-ink-700 uppercase tracking-wide mt-0.5">
        {label}
      </span>
    </div>
  );
}