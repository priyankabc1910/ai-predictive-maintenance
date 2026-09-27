import type { SensorTrace } from "../types/telemetry";

function series(base: number, drift: number, noise: number, points: number): number[] {
  const out: number[] = [];
  for (let i = 0; i < points; i++) {
    const t = i / points;
    out.push(Number((base + drift * t + Math.sin(i * 0.6) * noise + (Math.random() - 0.5) * noise * 0.4).toFixed(2)));
  }
  return out;
}

export const sensorTraces: SensorTrace[] = [
  { sensor_id: "s2", label: "Sensor 2", unit: "°C", values: series(42, 6.5, 0.8, 48) },
  { sensor_id: "s7", label: "Sensor 7", unit: "bar", values: series(3.1, -0.4, 0.12, 48) },
  { sensor_id: "s11", label: "Sensor 11", unit: "mm/s", values: series(1.2, 1.9, 0.3, 48) },
  { sensor_id: "s15", label: "Sensor 15", unit: "rpm", values: series(2380, -95, 18, 48) },
];

export const sensorFocusMachine = "UNIT-067";
