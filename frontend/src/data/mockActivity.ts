import type { ActivityEvent } from "../types/telemetry";

export const activityLog: ActivityEvent[] = [
  { id: "a1", time: "15:28", title: "RUL analysis completed", detail: "100 machines processed" },
  { id: "a2", time: "15:26", title: "Anomaly detected", detail: "UNIT-091" },
  { id: "a3", time: "15:24", title: "Sensor batch ingested", detail: "22,300 records" },
  { id: "a4", time: "15:20", title: "Model inference started", detail: "FD001 · RUL-XGB v2.3" },
  { id: "a5", time: "15:15", title: "Data pipeline check", detail: "All systems healthy" },
];
