import { FileText, Download } from "lucide-react";
import { SectionLabel } from "../components/ui/SectionLabel";

const REPORTS = [
  { id: "r1", title: "Weekly Fleet Reliability Summary", period: "Sep 15 – Sep 21, 2026", pages: 8, generated: "Sep 22, 06:00" },
  { id: "r2", title: "Critical Unit Deep-Dive · UNIT-091", period: "Single unit", pages: 4, generated: "Sep 26, 15:30" },
  { id: "r3", title: "Anomaly Detection Audit", period: "Sep 1 – Sep 26, 2026", pages: 12, generated: "Sep 26, 09:00" },
  { id: "r4", title: "Maintenance Action Log", period: "Q3 2026", pages: 6, generated: "Sep 20, 18:00" },
];

export default function Reports() {
  return (
    <div className="p-4 md:p-6 flex flex-col gap-5 max-w-[1600px] mx-auto">
      <SectionLabel index="07" title="Reports" meta="Generated intelligence documents" />

      <div className="rounded-sm border border-steel-700 bg-charcoal divide-y divide-steel-800">
        {REPORTS.map((r) => (
          <div key={r.id} className="flex items-center gap-4 p-4">
            <span className="flex items-center justify-center size-9 border border-steel-600 text-copper-400 shrink-0">
              <FileText size={16} strokeWidth={1.75} />
            </span>
            <div className="min-w-0 flex-1">
              <div className="text-[13px] text-ink-100 truncate">{r.title}</div>
              <div className="text-[11px] text-ink-700 font-mono">
                {r.period} · {r.pages} pages · generated {r.generated}
              </div>
            </div>
            <button className="flex items-center gap-1.5 text-[11px] font-mono text-ink-300 border border-steel-600 px-2.5 py-1.5 hover:border-copper-500/50 hover:text-copper-400 transition-colors shrink-0">
              <Download size={12} strokeWidth={2} />
              PDF
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
