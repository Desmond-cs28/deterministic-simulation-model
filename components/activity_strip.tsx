import { ACTIVITY_SEQUENCE, processing_minutes_for, total_processing_minutes } from "@/lib/activities"
import { DISPLAY_INDEX_OFFSET, ResourceKind } from "@/lib/constants"

import { SectionBlock } from "./section_block"

const ASSUMPTIONS = [
  "Every student follows the same three steps, in the same order.",
  "Each step takes a fixed number of minutes, known before the desk opens.",
  "Students arrive at a fixed interval. The first student arrives at 08:00.",
  "A step uses one officer or one computer and runs to the end. Work is not interrupted.",
  "The officer pool covers the registry check and the timetable. The computer pool covers the Student Portal.",
  "If the officer or the computer is busy, the student waits. The student who has waited longest goes next.",
  "The desk closes at the end of the session. Anyone still there is overtime.",
] as const

export function ModelSection() {
  const officer_minutes = processing_minutes_for(ResourceKind.OFFICER)
  const computer_minutes = processing_minutes_for(ResourceKind.COMPUTER)
  const chain = total_processing_minutes()

  return (
    <SectionBlock
      id="model"
      kicker="The model"
      title="Three steps at the Registry"
      lede="This is course registration week, not the long admissions process. A student checks in with an officer, registers courses on the Student Portal, then collects a timetable."
    >
      <ol className="grid gap-3 lg:grid-cols-3">
        {ACTIVITY_SEQUENCE.map((activity, index) => (
          <li key={activity.activity_id} className="rounded-xl bg-card p-4 ring-1 ring-foreground/10">
            <p className="font-mono text-[0.7rem] tracking-[0.14em] text-primary uppercase">
              Step {index + DISPLAY_INDEX_OFFSET}
            </p>
            <h3 className="font-heading mt-2 text-xl leading-tight">{activity.label}</h3>
            <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{activity.description}</p>
            <p className="mt-4 font-mono text-sm">
              {activity.processing_minutes} min · {activity.resource_kind}
            </p>
          </li>
        ))}
      </ol>
      <div className="mt-4 grid gap-3 sm:grid-cols-3">
        <Load label="Officer minutes per student" value={`${officer_minutes} min`} />
        <Load label="Computer minutes per student" value={`${computer_minutes} min`} />
        <Load label="Full chain, one student alone" value={`${chain} min`} />
      </div>
      <ul className="mt-6 grid gap-2 sm:grid-cols-2">
        {ASSUMPTIONS.map((assumption) => (
          <li key={assumption} className="rounded-lg bg-card/70 px-3 py-2 text-sm leading-relaxed ring-1 ring-foreground/10">
            {assumption}
          </li>
        ))}
      </ul>
    </SectionBlock>
  )
}

function Load({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl bg-secondary px-4 py-3 text-secondary-foreground">
      <p className="text-xs tracking-wide text-secondary-foreground/70">{label}</p>
      <p className="font-heading mt-1 text-2xl">{value}</p>
    </div>
  )
}
