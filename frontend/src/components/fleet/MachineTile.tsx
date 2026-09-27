import type { MachineRecord } from "../../types/telemetry";

const RISK_BAR: Record<string, string> = {
  LOW: "bg-status-healthy",
  MEDIUM: "bg-status-warning",
  HIGH: "bg-copper-500",
  CRITICAL: "bg-status-critical",
};

const RISK_TEXT: Record<string, string> = {
  LOW: "text-status-healthy",
  MEDIUM: "text-status-warning",
  HIGH: "text-copper-400",
  CRITICAL: "text-status-critical",
};

export function MachineTile({ machine }: { machine: MachineRecord }) {
  return (
    <div className="group relative border border-steel-700 bg-charcoal hover:border-steel-500 transition-colors p-3 flex flex-col gap-2.5">
      <div className={`absolute left-0 top-0 bottom-0 w-[2.5px] ${RISK_BAR[machine.risk_level]}`} />
      <div className="flex items-start justify-between pl-1.5">
        <span className="font-mono text-[12px] font-medium text-ink-100">{machine.machine_id}</span>
        <span className={`text-[9.5px] font-mono font-semibold ${RISK_TEXT[machine.risk_level]}`}>
          {machine.risk_level}
        </span>
      </div>

      <div className="pl-1.5">
        <div className="flex items-end justify-between mb-1">
          <span className="font-mono text-lg font-semibold text-ink-100 tabular">{machine.health_score}%</span>
          <span className="font-mono text-[10.5px] text-ink-700 tabular">{machine.rul} cyc</span>
        </div>
        <div className="h-1 w-full bg-steel-800 rounded-full overflow-hidden">
          <div
            className={`h-full ${RISK_BAR[machine.risk_level]}`}
            style={{ width: `${machine.health_score}%` }}
          />
        </div>
      </div>
    </div>
  );
}
