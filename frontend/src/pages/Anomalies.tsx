import { useEffect, useMemo, useState } from "react";

import { SectionLabel } from "../components/ui/SectionLabel";
import { AlertRail } from "../components/alerts/AlertRail";
import { SensorPanel } from "../components/telemetry/SensorPanel";
import {
  getFleetAnomalies,
  type AnomalyResult,
} from "../api/predictiveMaintenance";


function severityRank(severity: string): number {
  switch (severity) {
    case "CRITICAL":
      return 4;
    case "HIGH":
      return 3;
    case "MEDIUM":
      return 2;
    case "LOW":
      return 1;
    default:
      return 0;
  }
}


function severityBarClass(severity: string): string {
  switch (severity) {
    case "CRITICAL":
      return "bg-status-critical";
    case "HIGH":
      return "bg-copper-500";
    case "MEDIUM":
      return "bg-status-warning";
    default:
      return "bg-status-healthy";
  }
}


export default function Anomalies() {
  const [anomalies, setAnomalies] = useState<AnomalyResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadAnomalies() {
      try {
        const data = await getFleetAnomalies();
        setAnomalies(data);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load anomaly data"
        );
      } finally {
        setLoading(false);
      }
    }

    loadAnomalies();
  }, []);


  const ranked = useMemo(() => {
    return [...anomalies]
      .sort((a, b) => {
        const severityDifference =
          severityRank(b.severity) -
          severityRank(a.severity);

        if (severityDifference !== 0) {
          return severityDifference;
        }

        return b.anomaly_rate - a.anomaly_rate;
      })
      .slice(0, 10);
  }, [anomalies]);


  const anomalySummary = useMemo(() => {
    return {
      critical: anomalies.filter(
        (item) => item.severity === "CRITICAL"
      ).length,

      high: anomalies.filter(
        (item) => item.severity === "HIGH"
      ).length,

      medium: anomalies.filter(
        (item) => item.severity === "MEDIUM"
      ).length,

      low: anomalies.filter(
        (item) => item.severity === "LOW"
      ).length,
    };
  }, [anomalies]);


  if (loading) {
    return (
      <div className="p-4 md:p-6 max-w-[1600px] mx-auto">
        <SectionLabel
          index="04"
          title="Anomalies"
          meta="Anomaly detection layer"
        />

        <div className="mt-5 rounded-sm border border-steel-700 bg-charcoal p-5">
          <div className="font-mono text-xs text-ink-500">
            Loading live Isolation Forest anomaly data...
          </div>
        </div>
      </div>
    );
  }


  if (error) {
    return (
      <div className="p-4 md:p-6 max-w-[1600px] mx-auto">
        <SectionLabel
          index="04"
          title="Anomalies"
          meta="Anomaly detection layer"
        />

        <div className="mt-5 rounded-sm border border-status-critical/40 bg-charcoal p-5">
          <div className="font-mono text-xs text-status-critical">
            {error}
          </div>
        </div>
      </div>
    );
  }


  return (
    <div className="p-4 md:p-6 flex flex-col gap-5 max-w-[1600px] mx-auto">

      <SectionLabel
        index="04"
        title="Anomalies"
        meta="Live Isolation Forest detection"
      />


      {/* ------------------------------------------------ */}
      {/* Summary */}
      {/* ------------------------------------------------ */}

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">

        <div className="rounded-sm border border-steel-700 bg-charcoal p-4">
          <div className="text-[10px] uppercase tracking-wide text-ink-700">
            Critical
          </div>

          <div className="mt-1 font-mono text-2xl text-status-critical">
            {anomalySummary.critical}
          </div>

          <div className="mt-1 text-[10px] text-ink-500">
            highly deviant
          </div>
        </div>


        <div className="rounded-sm border border-steel-700 bg-charcoal p-4">
          <div className="text-[10px] uppercase tracking-wide text-ink-700">
            High
          </div>

          <div className="mt-1 font-mono text-2xl text-copper-400">
            {anomalySummary.high}
          </div>

          <div className="mt-1 text-[10px] text-ink-500">
            elevated deviation
          </div>
        </div>


        <div className="rounded-sm border border-steel-700 bg-charcoal p-4">
          <div className="text-[10px] uppercase tracking-wide text-ink-700">
            Medium
          </div>

          <div className="mt-1 font-mono text-2xl text-status-warning">
            {anomalySummary.medium}
          </div>

          <div className="mt-1 text-[10px] text-ink-500">
            monitor closely
          </div>
        </div>


        <div className="rounded-sm border border-steel-700 bg-charcoal p-4">
          <div className="text-[10px] uppercase tracking-wide text-ink-700">
            Normal
          </div>

          <div className="mt-1 font-mono text-2xl text-status-healthy">
            {anomalySummary.low}
          </div>

          <div className="mt-1 text-[10px] text-ink-500">
            within baseline
          </div>
        </div>

      </div>


      {/* ------------------------------------------------ */}
      {/* Main anomaly ranking */}
      {/* ------------------------------------------------ */}

      <div className="grid grid-cols-1 xl:grid-cols-[1fr_320px] gap-5">

        <div className="rounded-sm border border-steel-700 bg-charcoal p-5">

          <div className="flex flex-wrap items-start justify-between gap-3 mb-1">

            <div>
              <div className="text-[13px] font-semibold uppercase tracking-wide text-ink-100">
                Anomaly Severity Ranking
              </div>

              <div className="text-[11.5px] text-ink-500">
                Latest 30 operating cycles compared against the healthy baseline
              </div>
            </div>


            <div className="text-right font-mono text-[10px]">
              <div className="text-ink-700">
                MODEL
              </div>

              <div className="text-copper-400">
                ISOLATION FOREST
              </div>
            </div>

          </div>


          <div className="mt-4 flex flex-col gap-2">

            {ranked.map((machine) => {

              const percentage = Math.round(
                machine.anomaly_rate * 100
              );

              return (
                <div
                  key={machine.machine_id}
                  className="flex items-center gap-3"
                >

                  <span className="font-mono text-[12px] text-ink-100 w-20 shrink-0">
                    {machine.machine_id}
                  </span>


                  <div className="flex-1 h-2 bg-steel-800 overflow-hidden">

                    <div
                      className={`h-full ${severityBarClass(
                        machine.severity
                      )}`}
                      style={{
                        width: `${percentage}%`,
                      }}
                    />

                  </div>


                  <span className="font-mono text-[12px] tabular text-ink-300 w-14 text-right shrink-0">
                    {percentage}%
                  </span>


                  <span
                    className={`text-[10px] font-mono w-20 text-right ${
                      machine.severity === "CRITICAL"
                        ? "text-status-critical"
                        : machine.severity === "HIGH"
                        ? "text-copper-400"
                        : machine.severity === "MEDIUM"
                        ? "text-status-warning"
                        : "text-status-healthy"
                    }`}
                  >
                    {machine.severity}
                  </span>

                </div>
              );
            })}

          </div>


          <div className="mt-4 pt-3 border-t border-steel-700 flex flex-wrap justify-between gap-2 text-[10px] text-ink-700 font-mono">

            <span>
              {anomalies.length} ENGINES ANALYZED
            </span>

            <span>
              WINDOW 30 CYCLES
            </span>

            <span>
              BASELINE: FIRST 30 CYCLES
            </span>

          </div>

        </div>


        <AlertRail />

      </div>


      {/* ------------------------------------------------ */}
      {/* Sensor panel */}
      {/* ------------------------------------------------ */}

      <SensorPanel />

    </div>
  );
}
