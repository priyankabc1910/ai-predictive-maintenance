import {
  IconAnomalies,
  IconDashboard,
  IconMachines,
  IconMaintenance,
  IconPredictions,
  IconReports,
  IconSettings,
} from "../ui/icons";
import type { NavItem } from "../../types";

// Static nav structure for now — no router wired up yet. Each id is the
// future route slug (e.g. `/machines`), so this list can be mapped to
// <Link> elements without changing anything else in this component.
const NAV_ITEMS: NavItem[] = [
  { id: "dashboard", label: "Dashboard", icon: IconDashboard },
  { id: "machines", label: "Machines", icon: IconMachines },
  { id: "predictions", label: "Predictions", icon: IconPredictions },
  { id: "anomalies", label: "Anomalies", icon: IconAnomalies },
  { id: "maintenance", label: "Maintenance", icon: IconMaintenance },
  { id: "reports", label: "Reports", icon: IconReports },
];

interface SidebarProps {
  activeItemId: string;
}

export default function Sidebar({ activeItemId }: SidebarProps) {
  return (
    <aside className="flex h-full w-60 flex-col border-r border-base-700 bg-base-900">
      <div className="flex h-16 shrink-0 items-center gap-2.5 border-b border-base-700 px-5">
        <div className="flex h-7 w-7 items-center justify-center rounded-md bg-accent/15">
          <span className="h-2.5 w-2.5 rounded-sm bg-accent" />
        </div>
        <div className="leading-tight">
          <p className="text-sm font-semibold text-text-primary">
            Predictive Maintenance
          </p>
        </div>
      </div>

      <nav className="flex-1 overflow-y-auto px-3 py-4">
        <ul className="space-y-0.5">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = item.id === activeItemId;
            return (
              <li key={item.id}>
                <button
                  type="button"
                  aria-current={isActive ? "page" : undefined}
                  className={[
                    "flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors",
                    isActive
                      ? "bg-accent-soft text-text-primary"
                      : "text-text-secondary hover:bg-base-800 hover:text-text-primary",
                  ].join(" ")}
                >
                  <Icon className="h-[18px] w-[18px] shrink-0" />
                  <span>{item.label}</span>
                </button>
              </li>
            );
          })}
        </ul>
      </nav>

      <div className="border-t border-base-700 p-3">
        <button
          type="button"
          className="flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm text-text-secondary transition-colors hover:bg-base-800 hover:text-text-primary"
        >
          <IconSettings className="h-[18px] w-[18px] shrink-0" />
          <span>Settings</span>
        </button>
      </div>
    </aside>
  );
}
