const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export interface Prediction {
  machine_id: string;
  engine_id: number;
  rul: number;
  health_score: number;
  risk_level: string;
  recommendation: string;
}

export interface FleetSummary {
  total_machines: number;
  critical: number;
  high: number;
  medium: number;
  low: number;
  average_health_score: number;
  average_rul: number;
}

export async function getHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new Error("Backend health check failed");
  }

  return response.json();
}

export async function getPrediction(
  engineId: number
): Promise<Prediction> {
  const response = await fetch(
    `${API_BASE_URL}/predict/${engineId}`
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch engine ${engineId}`);
  }

  return response.json();
}

export async function getFleet(): Promise<Prediction[]> {
  const response = await fetch(`${API_BASE_URL}/fleet`);

  if (!response.ok) {
    throw new Error("Failed to fetch fleet predictions");
  }

  return response.json();
}

export async function getFleetSummary(): Promise<FleetSummary> {
  const response = await fetch(
    `${API_BASE_URL}/fleet/summary`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch fleet summary");
  }

  return response.json();
}

export interface RULTrajectoryPoint {
  cycle: number;
  predicted_rul: number;
}

export interface RULTrajectory {
  engine_id: number;
  machine_id: string;
  model: string;
  window_size: number;
  trajectory: RULTrajectoryPoint[];
}

export async function getRULTrajectory(
  engineId: number
): Promise<RULTrajectory> {
  const response = await fetch(
    `${API_BASE_URL}/rul/trajectory/${engineId}`
  );

  if (!response.ok) {
    throw new Error(
      `Failed to fetch RUL trajectory for engine ${engineId}`
    );
  }

  return response.json();
}

export interface AnomalyResult {
  machine_id: string;
  engine_id: number;
  model: string;
  baseline: string;
  cycles_analyzed: number;
  latest_cycle: number;
  anomalous_cycles: number;
  anomaly_rate: number;
  mean_decision_score: number;
  minimum_decision_score: number;
  severity: string;
  recommendation: string;
}

export async function getAnomaly(
  engineId: number
): Promise<AnomalyResult> {
  const response = await fetch(
    `${API_BASE_URL}/anomaly/${engineId}`
  );

  if (!response.ok) {
    throw new Error(
      `Failed to fetch anomaly data for engine ${engineId}`
    );
  }

  return response.json();
}

export async function getFleetAnomalies(): Promise<AnomalyResult[]> {
  const response = await fetch(
    `${API_BASE_URL}/anomaly/fleet`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch fleet anomaly data");
  }

  return response.json();
}