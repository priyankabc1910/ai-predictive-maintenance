import StatusBadge from "../ui/StatusBadge";
import { IconBell, IconChevronDown } from "../ui/icons";

interface TopbarProps {
  title: string;
  description: string;
}

export default function Topbar({ title, description }: TopbarProps) {
  return (
    <header className="flex h-16 shrink-0 items-center justify-between border-b border-base-700 bg-base-900 px-6">
      <div className="min-w-0">
        <h1 className="truncate text-base font-semibold text-text-primary">
          {title}
        </h1>
        <p className="truncate text-xs text-text-secondary">{description}</p>
      </div>

      <div className="flex items-center gap-4">
        <StatusBadge status="healthy" label="System Operational" />

        <button
          type="button"
          aria-label="Notifications"
          className="relative flex h-9 w-9 items-center justify-center rounded-md border border-base-700 text-text-secondary transition-colors hover:bg-base-800 hover:text-text-primary"
        >
          <IconBell className="h-[18px] w-[18px]" />
          <span className="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-status-warning" />
        </button>

        <button
          type="button"
          className="flex items-center gap-2 rounded-md border border-base-700 py-1.5 pl-1.5 pr-2.5 transition-colors hover:bg-base-800"
        >
          <span className="flex h-[26px] w-[26px] items-center justify-center rounded bg-base-700 text-xs font-medium text-text-primary">
            RE
          </span>
          <span className="text-sm text-text-primary">R. Ellison</span>
          <IconChevronDown className="h-4 w-4 text-text-tertiary" />
        </button>
      </div>
    </header>
  );
}
