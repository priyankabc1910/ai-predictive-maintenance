// Shared data contracts.
// These mirror the shape the FastAPI/ML service will eventually return,
// so mock data and real API responses can be swapped in without touching components.

export type RiskLevel = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
export type FleetStatus = "HEALTHY" | "MONITORING" | "CRITICAL";
export type Trend = "Stable" | "Improving" | "Declining" | "Rapid decline";

export interface MachineRecord {
  machine_id: string;
  health_score: number; // 0-100
  rul: number; // remaining useful life, in cycles
  risk_level: RiskLevel;
  status: FleetStatus;
  anomaly_score: number; // 0-1
  trend: Trend;
  signal: string; // short description of the dominant signal, e.g. "Sensor drift"
  recommendation: string; // "Monitor" | "Inspect" | "Schedule" | "Immediate"
}

export interface RULTrajectoryPoint {
  cycle: number;
  predicted_rul: number;
}

export interface RULTrajectory {
  machine_id: string;
  points: RULTrajectoryPoint[];
  current_rul: number;
}

export type AlertSeverity = "CRITICAL" | "HIGH" | "MEDIUM";

export interface AlertRecord {
  id: string;
  severity: AlertSeverity;
  machine_id: string;
  message: string;
  timestamp: string;
}

export interface SensorTrace {
  sensor_id: string;
  label: string;
  unit: string;
  values: number[];
}

export interface ActivityEvent {
  id: string;
  time: string;
  title: string;
  detail: string;
}
