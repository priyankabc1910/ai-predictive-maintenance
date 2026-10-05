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

export interface MaintenanceDecision {
  engine_id: number;
  machine_id: string;
  rul: number;
  risk_level: string;
  anomaly_rate: number;
  anomaly_severity: string;
  critical_sensor_count: number;
  high_sensor_count: number;
  maintenance_score: number;
  priority: string;
  action: string;
}

export async function getMaintenanceDecision(
  engineId: number
): Promise<MaintenanceDecision> {
  const response = await fetch(
    `${API_BASE_URL}/maintenance/${engineId}`
  );

  if (!response.ok) {
    throw new Error(
      `Failed to fetch maintenance decision for engine ${engineId}`
    );
  }

  return response.json();
}

export interface ExplanationEvidence {
  factor: string;
  value: number;
  unit?: string;
  severity: string;
  explanation: string;
}

export interface SensorContributor {
  sensor: string;
  deviation_score: number;
  trend_slope: number;
  trend_direction: string;
  severity: string;
}

export interface MaintenanceExplanation {
  engine_id: number;
  machine_id: string;
  risk_level: string;
  summary: string;
  reasons: string[];
  evidence: ExplanationEvidence[];
  top_sensor_contributors: SensorContributor[];
}

export async function getMaintenanceExplanation(
  engineId: number
): Promise<MaintenanceExplanation> {
  const response = await fetch(
    `${API_BASE_URL}/explain/${engineId}`
  );

  if (!response.ok) {
    throw new Error(
      `Failed to fetch explanation for engine ${engineId}`
    );
  }

  return response.json();
}

/* ==================================================
   Maintenance Knowledge / Retrieval
   ================================================== */

export interface MaintenanceGuidance {
  id: string;
  title: string;
  category: string;
  score: number;
  guidance: string;
  recommended_actions: string[];
}

export interface MaintenanceKnowledge {
  engine_id: number;
  machine_id: string;
  risk_level: string;
  retrieval_count: number;
  guidance: MaintenanceGuidance[];
}

export async function getMaintenanceKnowledge(
  engineId: number
): Promise<MaintenanceKnowledge> {
  const response = await fetch(
    `${API_BASE_URL}/knowledge/${engineId}`
  );

  if (!response.ok) {
    throw new Error(
      `Failed to fetch maintenance knowledge for engine ${engineId}`
    );
  }

  return response.json();
}
export interface MaintenanceIntelligence {
  engine_id: number;
  machine_id: string;

  prediction: {
    rul: number;
    health_score: number;
    risk_level: string;
    recommendation: string;
  };

  anomaly: {
    anomaly_rate: number;
    severity: string;
  };

  sensor_health: {
    critical_sensor_count: number;
    high_sensor_count: number;
    sensors: {
      sensor: string;
      baseline_mean: number;
      current_mean: number;
      absolute_change: number;
      deviation_score: number;
      trend_slope: number;
      trend_direction: string;
      severity: string;
    }[];
  };

  maintenance_decision: {
    maintenance_score: number;
    priority: string;
    action: string;
  };

  explainability: MaintenanceExplanation;

  knowledge: MaintenanceKnowledge;
}

export async function getMaintenanceIntelligence(
  engineId: number
): Promise<MaintenanceIntelligence> {
  const response = await fetch(
    `${API_BASE_URL}/maintenance/intelligence/${engineId}`
  );

  if (!response.ok) {
    throw new Error(
      `Failed to fetch maintenance intelligence for engine ${engineId}`
    );
  }

  return response.json();
}