import { Link } from "react-router-dom";
import { FleetSpectrum } from "../components/fleet/FleetSpectrum";
import { RULTrajectoryChart } from "../components/rul/RULTrajectoryChart";
import { AlertRail } from "../components/alerts/AlertRail";
import { FleetGrid } from "../components/fleet/FleetGrid";
import { RiskTable } from "../components/fleet/RiskTable";
import { SensorPanel } from "../components/telemetry/SensorPanel";
import { ActivityTimeline } from "../components/activity/ActivityTimeline";

export default function Overview() {
  return (
    <div className="p-4 md:p-6 flex flex-col gap-4 md:gap-5 max-w-[1600px] mx-auto">
      <FleetSpectrum />

      <div className="grid grid-cols-1 xl:grid-cols-[1fr_320px] gap-4 md:gap-5">
        <RULTrajectoryChart />
        <AlertRail />
      </div>

      <div className="flex flex-col gap-2">
        <FleetGrid limit={24} />
        <div className="flex justify-end">
          <Link to="/fleet" className="text-[11.5px] font-mono text-copper-400 hover:text-copper-300">
            View full fleet &rarr;
          </Link>
        </div>
      </div>

      <RiskTable rows={undefined} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-5">
        <SensorPanel />
        <ActivityTimeline />
      </div>
    </div>
  );
}
