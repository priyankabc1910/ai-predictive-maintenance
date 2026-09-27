import { Outlet } from "react-router-dom";
import { NavRail } from "../navigation/NavRail";
import { MobileNav } from "../navigation/MobileNav";
import { SystemHeader } from "./SystemHeader";

export function AppShell() {
  return (
    <div className="h-svh w-full flex bg-graphite text-ink-100 overflow-hidden">
      <NavRail />
      <div className="flex-1 flex flex-col min-w-0">
        <SystemHeader />
        <main className="flex-1 overflow-y-auto">
          <Outlet />
        </main>
        <MobileNav />
      </div>
    </div>
  );
}
