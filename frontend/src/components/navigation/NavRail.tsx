import { NavLink } from "react-router-dom";
import {
  Gauge,
  LayoutGrid,
  TrendingDown,
  Siren,
  Wrench,
  BrainCircuit,
  FileBarChart,
} from "lucide-react";

const ITEMS = [
  { to: "/", label: "Overview", icon: Gauge },
  { to: "/fleet", label: "Fleet", icon: LayoutGrid },
  { to: "/rul", label: "RUL Predictions", icon: TrendingDown },
  { to: "/anomalies", label: "Anomalies", icon: Siren },
  { to: "/maintenance", label: "Maintenance", icon: Wrench },
  { to: "/intelligence", label: "Intelligence", icon: BrainCircuit },
  { to: "/reports", label: "Reports", icon: FileBarChart },
];

export function NavRail() {
  return (
    <nav className="hidden md:flex flex-col w-16 shrink-0 border-r border-steel-700 bg-charcoal py-3 items-center gap-1">
      <div className="mb-2 size-8 rounded-sm bg-copper-500/15 border border-copper-500/40 flex items-center justify-center">
        <span className="font-mono text-[11px] font-semibold text-copper-400">PM</span>
      </div>
      {ITEMS.map(({ to, label, icon: Icon }) => (
        <NavLink
          key={to}
          to={to}
          end={to === "/"}
          title={label}
          className={({ isActive }) =>
            `group relative flex flex-col items-center gap-1 w-14 py-2.5 transition-colors ${
              isActive ? "text-copper-400" : "text-ink-500 hover:text-ink-100"
            }`
          }
        >
          {({ isActive }) => (
            <>
              <span
                className={`absolute left-0 top-1/2 -translate-y-1/2 h-5 w-[2px] rounded-r ${
                  isActive ? "bg-copper-500" : "bg-transparent"
                }`}
              />
              <Icon size={17} strokeWidth={1.75} />
              <span className="text-[8.5px] font-medium tracking-wide leading-none uppercase text-center px-0.5">
                {label.split(" ")[0]}
              </span>
            </>
          )}
        </NavLink>
      ))}
    </nav>
  );
}
