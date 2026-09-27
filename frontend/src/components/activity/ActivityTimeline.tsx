import { activityLog } from "../../data/mockActivity";

export function ActivityTimeline() {
  return (
    <div className="rounded-sm border border-steel-700 bg-charcoal p-5">
      <div className="text-[13px] font-semibold uppercase tracking-wide text-ink-100 mb-4">System Activity</div>

      <div className="flex flex-col">
        {activityLog.map((e, i) => (
          <div key={e.id} className="flex gap-3 relative">
            <div className="flex flex-col items-center">
              <span className="font-mono text-[10px] text-ink-700 pt-0.5 w-10 text-right shrink-0">{e.time}</span>
            </div>
            <div className="flex flex-col items-center pt-1">
              <span className="size-1.5 rounded-full bg-copper-500 shrink-0" />
              {i < activityLog.length - 1 && <span className="w-px flex-1 bg-steel-700 my-1" />}
            </div>
            <div className="pb-4 min-w-0">
              <div className="text-[12.5px] text-ink-100">{e.title}</div>
              <div className="text-[11px] text-ink-700 font-mono">{e.detail}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
