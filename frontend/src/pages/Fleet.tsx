import { SectionLabel } from "../components/ui/SectionLabel";
import { FleetGrid } from "../components/fleet/FleetGrid";
import { RiskTable } from "../components/fleet/RiskTable";
import { fleetByRisk } from "../data/mockFleetData";

export default function Fleet() {
  return (
    <div className="p-4 md:p-6 flex flex-col gap-5 max-w-[1600px] mx-auto">
      <SectionLabel index="02" title="Fleet" meta={`${fleetByRisk.length} units`} />
      <FleetGrid />
      <RiskTable rows={fleetByRisk} />
    </div>
  );
}
