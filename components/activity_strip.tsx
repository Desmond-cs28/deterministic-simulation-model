import { ACTIVITY_SEQUENCE, processing_minutes_for, total_processing_minutes } from "@/lib/activities"
import { DISPLAY_INDEX_OFFSET, ResourceKind } from "@/lib/constants"

import { SectionBlock } from "./section_block"

const ASSUMPTIONS = [
  "Every student follows the same four activities, in the same order.",
  "Processing times are constant and known before the session opens.",
  "Students arrive at a fixed interval. The first student arrives as the hall opens.",
  "An activity seizes one resource unit and runs to completion. Work is not interrupted.",
  "When several units are free, the student takes the lowest-numbered unit.",
  "If every unit of the needed kind is busy, the student waits. The longest-waiting student is seated first.",
  "Officers are one shared pool for document verification and fee assessment. Computers are one shared pool for enrolment and card issue.",
  "A student who finishes an activity joins the next queue at once, so an officer can call the next student while an earlier student is still at a computer.",
  "Forms, chairs, and the network are available whenever an officer or a computer is free.",
  "The session runs from 08:00. Work still open at the close continues, and that extra time is overtime.",
] as const

export function ModelSection() {
  const officer_minutes = processing_minutes_for(ResourceKind.OFFICER)
  const computer_minutes = processing_minutes_for(ResourceKind.COMPUTER)
  const chain = total_processing_minutes()

  return (
    <SectionBlock
      id="model"
      kicker="The model"
      title="Four activities, two scarce pools"
      lede="Each student is a job in a flow shop. The officer work and the computer work are the loads that staffing has to cover."
    >
      <ol className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
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
      <div className="mt-6 rounded-xl bg-card p-5 ring-1 ring-foreground/10">
        <h3 className="font-heading text-xl">Scheduling rule</h3>
        <pre className="mt-3 overflow-x-auto font-mono text-[0.78rem] leading-6 text-foreground/90">
{`arrival(i) = i × interarrival
ready(i, first) = arrival(i)
start(i, s) = max(ready(i, s), free time of the chosen unit)
end(i, s)   = start(i, s) + processing(s)
ready(i, s+1) = end(i, s)
makespan = max over students of end(i, last activity)`}
        </pre>
        <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
          The chosen unit is the lowest-numbered unit of the activity&apos;s resource that is already free.
          A lower bound on the makespan is the later of the last student&apos;s chain and the officer work
          (or computer work) of every arrival suffix, spread across the units of that pool.
        </p>
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
