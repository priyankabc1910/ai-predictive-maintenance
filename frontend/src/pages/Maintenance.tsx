import { useEffect, useState } from "react";

import { SectionLabel } from "../components/ui/SectionLabel";
import { ActivityTimeline } from "../components/activity/ActivityTimeline";
import {
  getMaintenanceDecision,
  getMaintenanceExplanation,
  type MaintenanceDecision,
  type MaintenanceExplanation,
} from "../api/predictiveMaintenance";

const GROUP_STYLE: Record<string, string> = {
  Immediate: "border-l-status-critical",
  Urgent: "border-l-copper-500",
  Planned: "border-l-status-warning",
  Routine: "border-l-steel-500",
};

function getGroup(priority: string) {
  switch (priority.toUpperCase()) {
    case "IMMEDIATE":
      return "Immediate";
    case "URGENT":
      return "Urgent";
    case "PLANNED":
      return "Planned";
    default:
      return "Routine";
  }
}

export default function Maintenance() {
  const [decision, setDecision] =
    useState<MaintenanceDecision | null>(null);

  const [explanation, setExplanation] =
    useState<MaintenanceExplanation | null>(null);

  const [loading, setLoading] = useState(true);

  const [error, setError] =
    useState<string | null>(null);

  useEffect(() => {
    async function loadMaintenanceData() {
      try {
        setLoading(true);
        setError(null);

        const result =
          await getMaintenanceDecision(1);

        setDecision(result);

        const explanationResult =
          await getMaintenanceExplanation(1);

        setExplanation(explanationResult);

      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load maintenance intelligence."
        );
      } finally {
        setLoading(false);
      }
    }

    loadMaintenanceData();
  }, []);

  const group = decision
    ? getGroup(decision.priority)
    : null;

  return (
    <div className="p-4 md:p-6 flex flex-col gap-5 max-w-[1600px] mx-auto">

      <SectionLabel
        index="05"
        title="Maintenance"
        meta="Work queue, generated from model output"
      />

      <div className="grid grid-cols-1 xl:grid-cols-[1fr_320px] gap-5">

        {/* ================================================= */}
        {/* MAIN MAINTENANCE PANEL */}
        {/* ================================================= */}

        <div className="rounded-sm border border-steel-700 bg-charcoal p-5">

          {/* Loading */}

          {loading && (
            <div className="py-12 text-center font-mono text-[11px] text-ink-500">
              Loading maintenance intelligence...
            </div>
          )}

          {/* Error */}

          {error && (
            <div className="border border-status-critical/40 bg-status-critical/5 p-4">

              <div className="text-[12px] font-semibold text-status-critical">
                MAINTENANCE DATA UNAVAILABLE
              </div>

              <div className="mt-1 font-mono text-[10.5px] text-ink-500">
                {error}
              </div>

            </div>
          )}

          {/* ================================================= */}
          {/* MAINTENANCE DECISION */}
          {/* ================================================= */}

          {decision && group && (
            <>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">

                {/* Priority */}

                <div
                  className={`border-l-2 ${GROUP_STYLE[group]} pl-3`}
                >

                  <div className="flex items-baseline justify-between mb-2">

                    <span className="text-[12px] font-semibold uppercase tracking-wide text-ink-100">
                      {group}
                    </span>

                    <span className="font-mono text-[10.5px] text-ink-700">
                      1 unit
                    </span>

                  </div>

                  <div className="flex flex-col gap-1.5">

                    <div className="flex items-center justify-between text-[11.5px]">

                      <span className="font-mono text-ink-100">
                        {decision.machine_id}
                      </span>

                      <span className="text-status-critical">
                        {decision.risk_level}
                      </span>

                    </div>

                    <div className="text-[10.5px] text-ink-500">
                      {decision.action}
                    </div>

                  </div>

                </div>

                {/* Maintenance Score */}

                <div className="border border-steel-700 bg-black/10 p-4">

                  <div className="text-[10px] uppercase tracking-wider text-ink-600">
                    Maintenance Score
                  </div>

                  <div className="mt-1 font-mono text-3xl text-ink-100">
                    {decision.maintenance_score}
                  </div>

                  <div className="mt-1 text-[10.5px] text-ink-500">
                    Priority:{" "}
                    <span className="text-ink-200">
                      {decision.priority}
                    </span>
                  </div>

                </div>

                {/* RUL */}

                <div className="border border-steel-700 bg-black/10 p-4">

                  <div className="text-[10px] uppercase tracking-wider text-ink-600">
                    Remaining Useful Life
                  </div>

                  <div className="mt-1 font-mono text-2xl text-ink-100">
                    {decision.rul}
                  </div>

                  <div className="mt-1 text-[10.5px] text-ink-500">
                    cycles remaining
                  </div>

                </div>

                {/* Condition Signals */}

                <div className="border border-steel-700 bg-black/10 p-4">

                  <div className="text-[10px] uppercase tracking-wider text-ink-600">
                    Condition Signals
                  </div>

                  <div className="mt-2 grid grid-cols-2 gap-3">

                    <div>

                      <div className="font-mono text-lg text-status-critical">
                        {decision.critical_sensor_count}
                      </div>

                      <div className="text-[9px] uppercase text-ink-600">
                        Critical Sensors
                      </div>

                    </div>

                    <div>

                      <div className="font-mono text-lg text-copper-500">
                        {decision.high_sensor_count}
                      </div>

                      <div className="text-[9px] uppercase text-ink-600">
                        High Sensors
                      </div>

                    </div>

                  </div>

                </div>

                {/* Anomaly Detection */}

                <div className="border border-steel-700 bg-black/10 p-4">

                  <div className="text-[10px] uppercase tracking-wider text-ink-600">
                    Anomaly Detection
                  </div>

                  <div className="mt-1 font-mono text-2xl text-ink-100">
                    {(decision.anomaly_rate * 100).toFixed(1)}%
                  </div>

                  <div className="mt-1 text-[10.5px] text-ink-500">

                    Severity:{" "}

                    <span className="text-status-critical">
                      {decision.anomaly_severity}
                    </span>

                  </div>

                </div>

                {/* Recommended Action */}

                <div className="border border-steel-700 bg-black/10 p-4">

                  <div className="text-[10px] uppercase tracking-wider text-ink-600">
                    Recommended Action
                  </div>

                  <div className="mt-2 text-[12px] leading-relaxed text-ink-200">
                    {decision.action}
                  </div>

                </div>

              </div>

              {/* ================================================= */}
              {/* EXPLAINABILITY */}
              {/* ================================================= */}

              {explanation && (
                <div className="mt-5 border border-steel-700 bg-black/10 p-5">

                  {/* Header */}

                  <div className="flex items-center justify-between mb-4">

                    <div>

                      <div className="text-[10px] uppercase tracking-wider text-ink-600">
                        Explainability
                      </div>

                      <div className="mt-1 text-sm font-semibold text-ink-100">
                        Why is this engine at risk?
                      </div>

                    </div>

                    <span className="font-mono text-[10px] text-status-critical">
                      {explanation.risk_level}
                    </span>

                  </div>

                  {/* Summary */}

                  <div className="border-l-2 border-status-critical pl-3 mb-5">

                    <p className="text-[11.5px] leading-relaxed text-ink-300">
                      {explanation.summary}
                    </p>

                  </div>

                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">

                    {/* Risk Factors */}

                    <div>

                      <div className="mb-2 text-[10px] uppercase tracking-wider text-ink-600">
                        Risk Factors
                      </div>

                      <div className="flex flex-col gap-2">

                        {explanation.reasons.map(
                          (reason, index) => (
                            <div
                              key={index}
                              className="border border-steel-700 p-3 text-[11px] text-ink-300"
                            >

                              <span className="mr-2 font-mono text-status-critical">
                                {String(index + 1).padStart(
                                  2,
                                  "0"
                                )}
                              </span>

                              {reason}

                            </div>
                          )
                        )}

                      </div>

                    </div>

                    {/* Sensor Contributors */}

                    <div>

                      <div className="mb-2 text-[10px] uppercase tracking-wider text-ink-600">
                        Top Sensor Contributors
                      </div>

                      <div className="flex flex-col gap-1.5">

                        {explanation.top_sensor_contributors.map(
                          (sensor) => (
                            <div
                              key={sensor.sensor}
                              className="flex items-center justify-between border border-steel-700 px-3 py-2"
                            >

                              <span className="font-mono text-[11px] text-ink-100">
                                {sensor.sensor}
                              </span>

                              <span className="font-mono text-[10px] text-status-critical">

                                {sensor.deviation_score > 0
                                  ? "+"
                                  : ""}

                                {sensor.deviation_score.toFixed(
                                  2
                                )}
                                σ

                              </span>

                              <span className="text-[10px] text-ink-500">
                                {sensor.trend_direction}
                              </span>

                            </div>
                          )
                        )}

                      </div>

                    </div>

                  </div>

                  {/* Evidence */}

                  <div className="mt-5">

                    <div className="mb-2 text-[10px] uppercase tracking-wider text-ink-600">
                      Decision Evidence
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">

                      {explanation.evidence.map(
                        (item, index) => (
                          <div
                            key={index}
                            className="border border-steel-700 p-3"
                          >

                            <div className="flex items-center justify-between">

                              <span className="text-[11px] font-semibold text-ink-200">
                                {item.factor}
                              </span>

                              <span className="font-mono text-[10px] text-status-critical">
                                {item.value}
                                {item.unit
                                  ? ` ${item.unit}`
                                  : ""}
                              </span>

                            </div>

                            <div className="mt-1 text-[10px] leading-relaxed text-ink-500">
                              {item.explanation}
                            </div>

                          </div>
                        )
                      )}

                    </div>

                  </div>

                </div>
              )}

            </>
          )}

        </div>

        {/* ================================================= */}
        {/* ACTIVITY */}
        {/* ================================================= */}

        <ActivityTimeline />

      </div>

    </div>
  );
}