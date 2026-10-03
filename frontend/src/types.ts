// Shared types for the app shell. Kept small and framework-agnostic
// so they can be reused once real API responses replace mock data.

/** The three health states used across status badges, cards, and future charts. */
export type MachineStatus = "healthy" | "warning" | "critical";

export interface NavItem {
  id: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
}

export interface FleetOverview {
  totalMachines: number;
  healthy: number;
  atRisk: number;
  critical: number;
}
