import type { FleetStatus, RiskLevel } from "../../types/telemetry";

type Level = FleetStatus | RiskLevel | "ONLINE";

const COLOR: Record<string, string> = {
  HEALTHY: "bg-status-healthy",
  LOW: "bg-status-healthy",
  MONITORING: "bg-status-warning",
  MEDIUM: "bg-status-warning",
  HIGH: "bg-copper-500",
  CRITICAL: "bg-status-critical",
  ONLINE: "bg-status-healthy",
};

export function StatusLED({ level, pulse = false, size = "sm" }: { level: Level; pulse?: boolean; size?: "sm" | "md" }) {
  const dim = size === "md" ? "size-2.5" : "size-1.5";
  return (
    <span className="relative inline-flex items-center justify-center">
      <span className={`${dim} rounded-full ${COLOR[level] ?? "bg-status-offline"} ${pulse ? "led-pulse" : ""}`} />
    </span>
  );
}
