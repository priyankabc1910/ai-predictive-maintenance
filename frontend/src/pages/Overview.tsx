import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { FleetSpectrum } from "../components/fleet/FleetSpectrum";
import { RULTrajectoryChart } from "../components/rul/RULTrajectoryChart";
import { AlertRail } from "../components/alerts/AlertRail";
import { FleetGrid } from "../components/fleet/FleetGrid";
import { RiskTable } from "../components/fleet/RiskTable";
import { SensorPanel } from "../components/telemetry/SensorPanel";
import { ActivityTimeline } from "../components/activity/ActivityTimeline";

import {
  getFleetMaintenance,
  type FleetMaintenanceItem,
} from "../api/predictiveMaintenance";

export default function Overview() {
  const [fleet, setFleet] = useState<FleetMaintenanceItem[]>([]);

  useEffect(() => {
    async function loadFleet() {
      try {
        const result = await getFleetMaintenance();
        setFleet(result);
      } catch (error) {
        console.error("Failed to load fleet maintenance data:", error);
      }
    }

    loadFleet();
  }, []);

  return (
    <div className="p-4 md:p-6 flex flex-col gap-4 md:gap-5 max-w-[1600px] mx-auto">
      <FleetSpectrum />

      <div className="grid grid-cols-1 xl:grid-cols-[1fr_320px] gap-4 md:gap-5">
        <RULTrajectoryChart />
        <AlertRail />
      </div>

      <div className="flex flex-col gap-2">
        <FleetGrid fleet={fleet} />

        <div className="flex justify-end">
          <Link
            to="/fleet"
            className="text-[11.5px] font-mono text-copper-400 hover:text-copper-300"
          >
            View full fleet &rarr;
          </Link>
        </div>
      </div>

      <RiskTable rows={fleet} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-5">
        <SensorPanel />
        <ActivityTimeline />
      </div>
    </div>
  );
}
