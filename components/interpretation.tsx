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
      title="Which desk to staff"
      lede="The better allocation is the one that finishes more students before the desk closes. When two allocations finish the same number, the one that keeps the officer and the computer busier is the more efficient."
    >
      <div className="rounded-xl bg-secondary px-5 py-5 text-secondary-foreground">
        <p className="font-mono text-[0.72rem] tracking-[0.16em] text-[#d7ebe3] uppercase">
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
