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