import type { FleetStatus, MachineRecord, RiskLevel, Trend } from "../types/telemetry";

// Small seeded PRNG so the mock fleet is stable across reloads instead of
// reshuffling every render.
function mulberry32(seed: number) {
  return function () {
    seed |= 0;
    seed = (seed + 0x6d2b79f5) | 0;
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const rand = mulberry32(11291);

function unitId(n: number): string {
  return `UNIT-${String(n).padStart(3, "0")}`;
}

const SIGNALS_LOW = ["Normal", "Normal", "Normal", "Nominal drift"];
const SIGNALS_MED = ["Sensor drift", "Elevated vibration", "Load imbalance"];
const SIGNALS_HIGH = ["Vibration anomaly", "Pressure deviation", "Bearing wear signature"];
const SIGNALS_CRIT = ["Thermal anomaly", "Rapid vibration escalation", "Multi-sensor fault"];

function buildMachine(n: number, status: FleetStatus): MachineRecord {
  let health: number;
  let rul: number;
  let risk: RiskLevel;
  let trend: Trend;
  let signal: string;
  let recommendation: string;

  if (status === "HEALTHY") {
    health = 78 + Math.round(rand() * 20); // 78-98
    rul = 55 + Math.round(rand() * 90); // 55-145
    risk = "LOW";
    trend = rand() > 0.15 ? "Stable" : "Improving";
    signal = SIGNALS_LOW[Math.floor(rand() * SIGNALS_LOW.length)];
    recommendation = "Monitor";
  } else if (status === "MONITORING") {
    health = 42 + Math.round(rand() * 30); // 42-72
    rul = 15 + Math.round(rand() * 45); // 15-60
    risk = rand() > 0.5 ? "MEDIUM" : "HIGH";
    trend = "Declining";
    signal = risk === "MEDIUM"
      ? SIGNALS_MED[Math.floor(rand() * SIGNALS_MED.length)]
      : SIGNALS_HIGH[Math.floor(rand() * SIGNALS_HIGH.length)];
    recommendation = risk === "MEDIUM" ? "Inspect" : "Schedule";
  } else {
    health = 8 + Math.round(rand() * 24); // 8-32
    rul = 2 + Math.round(rand() * 16); // 2-18
    risk = health < 20 ? "CRITICAL" : "HIGH";
    trend = "Rapid decline";
    signal = SIGNALS_CRIT[Math.floor(rand() * SIGNALS_CRIT.length)];
    recommendation = risk === "CRITICAL" ? "Immediate" : "Schedule";
  }

  return {
    machine_id: unitId(n),
    health_score: health,
    rul,
    risk_level: risk,
    status,
    anomaly_score: Math.round(rand() * (status === "HEALTHY" ? 20 : status === "MONITORING" ? 55 : 90)) / 100,
    trend,
    signal,
    recommendation,
  };
}

function generateFleet(): MachineRecord[] {
  const fleet: MachineRecord[] = [];
  const ids = Array.from({ length: 100 }, (_, i) => i + 1);

  // fixed distribution requested by the brief: 72 healthy / 20 monitoring / 8 critical
  const healthyCount = 72;
  const monitoringCount = 20;
  const criticalCount = 8;

  const statuses: FleetStatus[] = [
    ...Array(healthyCount).fill("HEALTHY"),
    ...Array(monitoringCount).fill("MONITORING"),
    ...Array(criticalCount).fill("CRITICAL"),
  ];

  // shuffle statuses (seeded) so critical units aren't always the same IDs,
  // except for the five hero units the brief names explicitly.
  for (let i = statuses.length - 1; i > 0; i--) {
    const j = Math.floor(rand() * (i + 1));
    [statuses[i], statuses[j]] = [statuses[j], statuses[i]];
  }

  ids.forEach((n, idx) => {
    fleet.push(buildMachine(n, statuses[idx]));
  });

  // pin the five machines referenced throughout the brief to specific values
  // so the narrative in the RUL / risk sections lines up exactly.
  const pinned: Record<string, Partial<MachineRecord>> = {
    "UNIT-001": { health_score: 92, rul: 84, risk_level: "LOW", status: "HEALTHY", trend: "Stable", signal: "Normal", recommendation: "Monitor" },
    "UNIT-024": { health_score: 71, rul: 42, risk_level: "LOW", status: "HEALTHY", trend: "Stable", signal: "Normal", recommendation: "Monitor" },
    "UNIT-067": { health_score: 48, rul: 18, risk_level: "MEDIUM", status: "MONITORING", trend: "Declining", signal: "Sensor drift", recommendation: "Inspect" },
    "UNIT-083": { health_score: 29, rul: 9, risk_level: "HIGH", status: "MONITORING", trend: "Declining", signal: "Vibration anomaly", recommendation: "Schedule" },
    "UNIT-091": { health_score: 14, rul: 4, risk_level: "CRITICAL", status: "CRITICAL", trend: "Rapid decline", signal: "Thermal anomaly", recommendation: "Immediate" },
  };

  return fleet.map((m) => (pinned[m.machine_id] ? { ...m, ...pinned[m.machine_id] } : m));
}

export const fleetData: MachineRecord[] = generateFleet();

export const fleetSummary = {
  total: fleetData.length,
  healthy: fleetData.filter((m) => m.status === "HEALTHY").length,
  monitoring: fleetData.filter((m) => m.status === "MONITORING").length,
  critical: fleetData.filter((m) => m.status === "CRITICAL").length,
};

export const highlightedMachines = ["UNIT-001", "UNIT-024", "UNIT-067", "UNIT-083", "UNIT-091"];

export function getMachine(id: string): MachineRecord | undefined {
  return fleetData.find((m) => m.machine_id === id);
}

// sorted by descending risk, for the risk-analysis table
export const riskOrder: Record<RiskLevel, number> = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3 };
export const fleetByRisk = [...fleetData].sort((a, b) => riskOrder[a.risk_level] - riskOrder[b.risk_level]);
