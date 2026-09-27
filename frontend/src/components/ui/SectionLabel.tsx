export function SectionLabel({
  index,
  title,
  meta,
}: {
  index?: string;
  title: string;
  meta?: string;
}) {
  return (
    <div className="flex items-baseline justify-between gap-4 border-b border-steel-600 pb-2.5 mb-4">
      <div className="flex items-baseline gap-2.5">
        {index && (
          <span className="font-mono text-[11px] text-copper-500 tracking-wider">{index}</span>
        )}
        <h2 className="text-[13px] font-semibold tracking-wide text-ink-100 uppercase">{title}</h2>
      </div>
      {meta && <span className="font-mono text-[11px] text-ink-700">{meta}</span>}
    </div>
  );
}
