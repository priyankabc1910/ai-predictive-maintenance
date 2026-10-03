import type { MachineStatus } from "../../types";

interface StatusBadgeProps {
  status: MachineStatus;
  label: string;
}

const STATUS_STYLES: Record<
  MachineStatus,
  { dot: string; text: string; bg: string; border: string }
> = {
  healthy: {
    dot: "bg-status-healthy",
    text: "text-status-healthy",
    bg: "bg-status-healthy-soft",
    border: "border-status-healthy/30",
  },
  warning: {
    dot: "bg-status-warning",
    text: "text-status-warning",
    bg: "bg-status-warning-soft",
    border: "border-status-warning/30",
  },
  critical: {
    dot: "bg-status-critical",
    text: "text-status-critical",
    bg: "bg-status-critical-soft",
    border: "border-status-critical/30",
  },
};

/** Small pill used to communicate machine/system health at a glance. */
export default function StatusBadge({ status, label }: StatusBadgeProps) {
  const styles = STATUS_STYLES[status];

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-medium ${styles.bg} ${styles.border} ${styles.text}`}
    >
      <span className={`h-1.5 w-1.5 rounded-full ${styles.dot}`} />
      {label}
    </span>
  );
}
