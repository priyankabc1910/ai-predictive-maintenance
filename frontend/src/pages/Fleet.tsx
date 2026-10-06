import { useEffect, useMemo, useState } from "react";

import { SectionLabel } from "../components/ui/SectionLabel";
import { FleetGrid } from "../components/fleet/FleetGrid";
import { RiskTable } from "../components/fleet/RiskTable";

import {
  getFleetMaintenance,
  type FleetMaintenanceItem,
} from "../api/predictiveMaintenance";

export default function Fleet() {
  const [fleet, setFleet] = useState<FleetMaintenanceItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadFleet() {
      try {
        setLoading(true);
        setError(null);

        const result = await getFleetMaintenance();

        setFleet(result);
      } catch (err) {
        setError(
          err instanceof Error
            ? err.message
            : "Failed to load fleet maintenance data."
        );
      } finally {
        setLoading(false);
      }
    }

    loadFleet();
  }, []);

  const summary = useMemo(() => {
    return {
      immediate: fleet.filter(
        (item) => item.priority === "IMMEDIATE"
      ).length,

      urgent: fleet.filter(
        (item) => item.priority === "URGENT"
      ).length,

      planned: fleet.filter(
        (item) => item.priority === "PLANNED"
      ).length,

      routine: fleet.filter(
        (item) => item.priority === "ROUTINE"
      ).length,
    };
  }, [fleet]);

  if (loading) {
    return (
      <div className="p-4 md:p-6 max-w-[1600px] mx-auto">
        <SectionLabel
          index="02"
          title="Fleet"
          meta="Loading fleet..."
        />

        <div className="mt-5 rounded-sm border border-steel-700 bg-charcoal p-8 text-center text-sm text-ink-500">
          Loading fleet maintenance intelligence...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 md:p-6 max-w-[1600px] mx-auto">
        <SectionLabel
          index="02"
          title="Fleet"
          meta="Unavailable"
        />

        <div className="mt-5 rounded-sm border border-status-critical/40 bg-charcoal p-8 text-center">
          <div className="text-sm text-status-critical">
            {error}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-4 md:p-6 flex flex-col gap-5 max-w-[1600px] mx-auto">
      <SectionLabel
        index="02"
        title="Fleet"
        meta={`${fleet.length} units`}
      />

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="rounded-sm border border-status-critical/30 bg-charcoal p-4">
          <div className="text-[10px] uppercase tracking-wide text-ink-600">
            Immediate
          </div>
          <div className="mt-1 text-2xl font-mono text-status-critical">
            {summary.immediate}
          </div>
        </div>

        <div className="rounded-sm border border-copper-500/30 bg-charcoal p-4">
          <div className="text-[10px] uppercase tracking-wide text-ink-600">
            Urgent
          </div>
          <div className="mt-1 text-2xl font-mono text-copper-400">
            {summary.urgent}
          </div>
        </div>

        <div className="rounded-sm border border-status-warning/30 bg-charcoal p-4">
          <div className="text-[10px] uppercase tracking-wide text-ink-600">
            Planned
          </div>
          <div className="mt-1 text-2xl font-mono text-status-warning">
            {summary.planned}
          </div>
        </div>

        <div className="rounded-sm border border-steel-600 bg-charcoal p-4">
          <div className="text-[10px] uppercase tracking-wide text-ink-600">
            Routine
          </div>
          <div className="mt-1 text-2xl font-mono text-ink-300">
            {summary.routine}
          </div>
        </div>
      </div>

      <FleetGrid fleet={fleet} />

      <RiskTable rows={fleet} />
    </div>
  );
}
