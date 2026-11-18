import type { ScenarioRun } from "@/lib/types"

import { SectionBlock } from "./section_block"

export function Interpretation({
  paragraphs,
  recommended,
}: {
  paragraphs: string[]
  recommended: ScenarioRun
}) {
  return (
    <SectionBlock
      id="reading"
      kicker="Reading"
      title="Which allocation earns its desks"
      lede="Efficiency here means clearing as many students as possible before the session closes, then keeping officers and computers busy. A larger pool is preferred only when the extra time it consumes is paid back."
    >
      <div className="rounded-xl bg-secondary px-5 py-5 text-secondary-foreground">
        <p className="font-mono text-[0.72rem] tracking-[0.16em] text-[#f0d3a2] uppercase">
          Most efficient in this study
        </p>
        <p className="font-heading mt-2 text-3xl tracking-tight">{recommended.scenario.name}</p>
        <p className="mt-2 max-w-2xl text-sm leading-relaxed text-secondary-foreground/80">
          {recommended.scenario.officer_count} officers and {recommended.scenario.computer_count} computers.
          Score {recommended.metrics.efficiency_score.toFixed(3)}. Makespan {recommended.metrics.makespan_minutes} minutes.
          Average wait {recommended.metrics.average_waiting_minutes.toFixed(1)} minutes.
        </p>
      </div>
      <div className="mt-5 max-w-3xl space-y-4">
        {paragraphs.map((paragraph) => (
          <p key={paragraph} className="text-[0.98rem] leading-7">
            {paragraph}
          </p>
        ))}
      </div>
    </SectionBlock>
  )
}
