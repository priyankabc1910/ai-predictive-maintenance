// A minimal, hand-drawn icon set for the app shell.
// Deliberately not pulling in an icon library for ~8 glyphs; each icon is a
// small stroke-based SVG sharing the same viewBox/strokeWidth conventions so
// they stay visually consistent.

type IconProps = { className?: string };

const base = {
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.6,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
};

export function IconDashboard({ className }: IconProps) {
  return (
    <svg {...base} className={className}>
      <rect x="3.5" y="3.5" width="7.5" height="9" rx="1.2" />
      <rect x="13" y="3.5" width="7.5" height="5.5" rx="1.2" />
      <rect x="13" y="11.5" width="7.5" height="9" rx="1.2" />
      <rect x="3.5" y="15" width="7.5" height="5.5" rx="1.2" />
    </svg>
  );
}

export function IconMachines({ className }: IconProps) {
  return (
    <svg {...base} className={className}>
      <rect x="3.5" y="7" width="17" height="12" rx="1.2" />
      <path d="M8 7V4.5h8V7" />
      <path d="M7.5 12.5h3.5v3.5H7.5z" />
      <path d="M14 12.5h2.5M14 16h2.5" />
    </svg>
  );
}

export function IconPredictions({ className }: IconProps) {
  return (
    <svg {...base} className={className}>
      <path d="M3.5 18.5 9 12l3.5 3.5L20.5 7" />
      <path d="M15 7h5.5v5.5" />
    </svg>
  );
}

export function IconAnomalies({ className }: IconProps) {
  return (
    <svg {...base} className={className}>
      <path d="M12 3.5 21 19.5H3z" />
      <path d="M12 9.5v4" />
      <circle cx="12" cy="16.3" r="0.4" fill="currentColor" stroke="none" />
    </svg>
  );
}

export function IconMaintenance({ className }: IconProps) {
  return (
    <svg {...base} className={className}>
      <path d="M14.5 6.5a3.5 3.5 0 0 1-4.6 4.6L4.5 16.5a1.7 1.7 0 0 0 2.4 2.4l5.4-5.4a3.5 3.5 0 0 1 4.6-4.6l-2.3 2.3-1.6-1.6z" />
    </svg>
  );
}

export function IconReports({ className }: IconProps) {
  return (
    <svg {...base} className={className}>
      <path d="M7 3.5h7l3.5 3.5V20a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4.5a1 1 0 0 1 1-1Z" />
      <path d="M14 3.5V7h3.5" />
      <path d="M9 12.5h6M9 16h6" />
    </svg>
  );
}

export function IconSettings({ className }: IconProps) {
  return (
    <svg {...base} className={className}>
      <circle cx="12" cy="12" r="3" />
      <path d="M12 3.5v2.2M12 18.3v2.2M20.5 12h-2.2M5.7 12H3.5M17.8 6.2l-1.6 1.6M7.8 16.2l-1.6 1.6M17.8 17.8l-1.6-1.6M7.8 7.8 6.2 6.2" />
    </svg>
  );
}

export function IconBell({ className }: IconProps) {
  return (
    <svg {...base} className={className}>
      <path d="M6 10a6 6 0 0 1 12 0c0 4 1.5 5.5 1.5 5.5h-15S6 14 6 10Z" />
      <path d="M10 18.5a2 2 0 0 0 4 0" />
    </svg>
  );
}

export function IconChevronDown({ className }: IconProps) {
  return (
    <svg {...base} className={className}>
      <path d="m6 9 6 6 6-6" />
    </svg>
  );
}
