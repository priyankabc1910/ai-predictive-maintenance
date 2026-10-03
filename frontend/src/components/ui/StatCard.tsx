import type { MachineStatus } from "../../types";

interface StatCardProps {
  label: string;
  value: number;
  /** Optional status accent shown as a left rule + tinted value color. */
  accent?: MachineStatus;
  /** Optional context line under the value, e.g. share of fleet. */
  helperText?: string;
}

const ACCENT_STYLES: Record<MachineStatus, { rule: string; value: string }> = {
  healthy: { rule: "before:bg-status-healthy", value: "text-status-healthy" },
  warning: { rule: "before:bg-status-warning", value: "text-status-warning" },
  critical: { rule: "before:bg-status-critical", value: "text-status-critical" },
};

/**
 * Compact metric card used across the fleet overview.
 * Value is rendered in a monospace face to keep numerals aligned and
 * legible at a glance, matching the reading pattern of a gauge/readout.
 */
export default function StatCard({
  label,
  value,
  accent,
  helperText,
}: StatCardProps) {
  const accentStyles = accent ? ACCENT_STYLES[accent] : null;

  return (
    <div
      className={[
        "relative overflow-hidden rounded-lg border border-base-700 bg-base-850 p-4 shadow-panel",
        "before:absolute before:inset-y-0 before:left-0 before:w-[3px] before:content-['']",
        accentStyles ? accentStyles.rule : "before:bg-base-600",
      ].join(" ")}
    >
      <p className="text-xs font-medium uppercase tracking-wide text-text-tertiary">
        {label}
      </p>
      <p
        className={`mt-2 font-mono text-3xl font-semibold tabular-nums ${
          accentStyles ? accentStyles.value : "text-text-primary"
        }`}
      >
        {value.toLocaleString()}
      </p>
      {helperText && (
        <p className="mt-1 text-xs text-text-secondary">{helperText}</p>
      )}
    </div>
  );
}
