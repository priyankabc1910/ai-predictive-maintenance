import { useEffect, useState } from "react";
import { Bell, ChevronDown } from "lucide-react";
import { StatusLED } from "../ui/StatusLED";
import { alerts } from "../../data/mockAlerts";

function useClock() {
  const [now, setNow] = useState(new Date());
  useEffect(() => {
    const t = setInterval(() => setNow(new Date()), 1000 * 30);
    return () => clearInterval(t);
  }, []);
  return now;
}

function fmt(d: Date) {
  return d.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit", hour12: false });
}

export function SystemHeader() {
  const now = useClock();

  return (
    <header className="h-16 shrink-0 border-b border-steel-700 bg-charcoal px-4 md:px-6 flex items-center justify-between gap-4">
      <div className="flex items-center gap-4 md:gap-8 min-w-0">
        <div className="min-w-0">
          <div className="text-[13px] md:text-[14px] font-semibold tracking-tight leading-tight truncate">
            Predictive Maintenance
          </div>
          <div className="text-[10.5px] text-ink-700 leading-tight font-mono truncate">
            Reliability engineering console
          </div>
        </div>

        <div className="hidden lg:flex items-center gap-6 pl-6 border-l border-steel-700">
          <Field label="AI Engine">
            <span className="flex items-center gap-1.5">
              <StatusLED level="ONLINE" pulse />
              <span className="font-mono text-[11px] text-status-healthy">ONLINE</span>
            </span>
          </Field>
          <Field label="Dataset">
            <span className="font-mono text-[11px] text-ink-100">FD001 / NASA C-MAPSS</span>
          </Field>
          <Field label="Last Analysis">
            <span className="font-mono text-[11px] text-ink-100 tabular">{fmt(now)}</span>
          </Field>
        </div>
      </div>

      <div className="flex items-center gap-3 md:gap-5 shrink-0">
        <button
          aria-label="System alerts"
          className="relative flex items-center justify-center size-8 rounded-sm border border-steel-600 text-ink-300 hover:text-copper-400 hover:border-copper-500/50 transition-colors"
        >
          <Bell size={15} strokeWidth={1.75} />
          {alerts.length > 0 && (
            <span className="absolute -top-1 -right-1 size-3.5 rounded-full bg-status-critical text-[8px] font-bold text-graphite flex items-center justify-center">
              {alerts.length}
            </span>
          )}
        </button>

        <button className="flex items-center gap-2 pl-2 md:pl-3 border-l border-steel-700">
          <span className="hidden sm:flex flex-col items-end leading-tight">
            <span className="text-[11.5px] font-medium text-ink-100">R. Alvarez</span>
            <span className="text-[10px] text-ink-700 font-mono">Reliability Eng.</span>
          </span>
          <span className="size-7 rounded-sm bg-steel-700 border border-steel-600 flex items-center justify-center text-[11px] font-semibold text-copper-400">
            RA
          </span>
          <ChevronDown size={13} className="text-ink-700 hidden sm:block" />
        </button>
      </div>
    </header>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="flex flex-col leading-tight">
      <span className="text-[9.5px] uppercase tracking-wide text-ink-700">{label}</span>
      {children}
    </div>
  );
}
