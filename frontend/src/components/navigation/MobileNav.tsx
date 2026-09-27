import { NavLink } from "react-router-dom";
import { Gauge, LayoutGrid, TrendingDown, Siren, Wrench } from "lucide-react";

const ITEMS = [
  { to: "/", label: "Overview", icon: Gauge },
  { to: "/fleet", label: "Fleet", icon: LayoutGrid },
  { to: "/rul", label: "RUL", icon: TrendingDown },
  { to: "/anomalies", label: "Alerts", icon: Siren },
  { to: "/maintenance", label: "Work", icon: Wrench },
];

export function MobileNav() {
  return (
    <nav className="md:hidden flex border-t border-steel-700 bg-charcoal shrink-0">
      {ITEMS.map(({ to, label, icon: Icon }) => (
        <NavLink
          key={to}
          to={to}
          end={to === "/"}
          className={({ isActive }) =>
            `flex-1 flex flex-col items-center gap-0.5 py-2 ${
              isActive ? "text-copper-400" : "text-ink-500"
            }`
          }
        >
          <Icon size={16} strokeWidth={1.75} />
          <span className="text-[9px] uppercase tracking-wide">{label}</span>
        </NavLink>
      ))}
    </nav>
  );
}
