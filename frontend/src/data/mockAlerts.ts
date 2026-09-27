import type { AlertRecord } from "../types/telemetry";

export const alerts: AlertRecord[] = [
  {
    id: "alert-091-1",
    severity: "CRITICAL",
    machine_id: "UNIT-091",
    message: "Estimated RUL has fallen below the critical threshold of 5 cycles.",
    timestamp: "15:26",
  },
  {
    id: "alert-083-1",
    severity: "HIGH",
    machine_id: "UNIT-083",
    message: "Abnormal sensor behavior detected on the vibration channel.",
    timestamp: "14:52",
  },
  {
    id: "alert-067-1",
    severity: "MEDIUM",
    machine_id: "UNIT-067",
    message: "RUL degradation trend is accelerating beyond the expected envelope.",
    timestamp: "13:40",
  },
];
