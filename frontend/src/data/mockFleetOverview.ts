import type { FleetOverview } from "../types";

/**
 * MOCK DATA — UI placeholder only.
 *
 * This stands in for a future API response, e.g. `GET /api/fleet/overview`.
 * Replace this module's export with a data-fetching hook (React Query, SWR,
 * or a plain fetch call) once the RUL/anomaly backend is available. The
 * shape here (`FleetOverview`) is the intended response contract — keep it
 * in sync with the real API instead of changing consumers when that lands.
 */
export const mockFleetOverview: FleetOverview = {
  totalMachines: 100,
  healthy: 72,
  atRisk: 20,
  critical: 8,
};
