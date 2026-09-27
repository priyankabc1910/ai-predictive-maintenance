import type { RULTrajectory } from "../types/telemetry";

// Degradation curves for the five machines called out in the brief.
// Each series runs from cycle 0 to the machine's current operating cycle,
// with predicted RUL decaying at a rate characteristic of that unit.
function buildCurve(startRul: number, cycles: number, noise: number, decayShape: number): RULTrajectory["points"] {
  const points: RULTrajectory["points"] = [];
  for (let c = 0; c <= cycles; c += Math.max(1, Math.round(cycles / 24))) {
    const progress = c / cycles;
    const decayed = startRul * Math.pow(1 - progress, decayShape);
    const jitter = (Math.sin(c * 1.7) * noise);
    points.push({ cycle: c, predicted_rul: Math.max(0, Math.round(decayed + jitter)) });
  }
  return points;
}

export const rulTrajectories: RULTrajectory[] = [
  { machine_id: "UNIT-001", current_rul: 84, points: buildCurve(210, 130, 4, 1.15) },
  { machine_id: "UNIT-024", current_rul: 42, points: buildCurve(160, 150, 5, 1.35) },
  { machine_id: "UNIT-067", current_rul: 18, points: buildCurve(140, 165, 4, 1.7) },
  { machine_id: "UNIT-083", current_rul: 9, points: buildCurve(120, 175, 3, 2.1) },
  { machine_id: "UNIT-091", current_rul: 4, points: buildCurve(95, 180, 2, 2.8) },
];
