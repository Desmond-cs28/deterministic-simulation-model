"use client"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { RunStatus } from "@/lib/constants"
import type { DraftText } from "@/lib/draft"
import { study_scenarios } from "@/lib/experiments"
import type { Scenario, SimulationConfig } from "@/lib/types"

type LabControlsProps = {
  draft: DraftText
  applied: SimulationConfig
  status: RunStatus
  on_change: (field: keyof DraftText, value: string) => void
  on_run: () => void
  on_scenario: (scenario: Scenario) => void
}

export function LabControls({ draft, applied, status, on_change, on_run, on_scenario }: LabControlsProps) {
  const running = status === RunStatus.RUNNING
  const scenarios = study_scenarios()

  return (
    <form
      className="rounded-xl bg-card p-4 ring-1 ring-foreground/10 sm:p-5"
      onSubmit={(event) => {
        event.preventDefault()
        on_run()
      }}
    >
      <h3 className="font-heading text-2xl">Staff the hall</h3>
      <p className="mt-1 text-sm leading-relaxed text-muted-foreground">
        The single run below uses these counts. The experiment table keeps the same cohort and session, and swaps only the officer and computer pools.
      </p>
      <div className="mt-4 grid gap-3 sm:grid-cols-2">
        <Field
          id="student_count"
          label="Students in the cohort"
          hint="Use 0 to see the empty hall."
          value={draft.student_count}
          on_change={(value) => on_change("student_count", value)}
        />
        <Field
          id="interarrival_minutes"
          label="Minutes between arrivals"
          hint="0 means everyone is at the door at 08:00."
          value={draft.interarrival_minutes}
          on_change={(value) => on_change("interarrival_minutes", value)}
        />
        <Field
          id="officer_count"
          label="Registration officers"
          hint="Shared by documents and fees."
          value={draft.officer_count}
          on_change={(value) => on_change("officer_count", value)}
        />
        <Field
          id="computer_count"
          label="Registration computers"
          hint="Shared by enrolment and card issue."
          value={draft.computer_count}
          on_change={(value) => on_change("computer_count", value)}
        />
        <Field
          id="working_period_minutes"
          label="Session length (minutes)"
          hint="Work past this point is overtime."
          value={draft.working_period_minutes}
          on_change={(value) => on_change("working_period_minutes", value)}
        />
      </div>
      <Button type="submit" className="mt-4 h-10 cursor-pointer px-4" disabled={running}>
        {running ? "Scheduling the hall…" : "Run simulation"}
      </Button>
      <div className="mt-5">
        <p className="text-xs tracking-wide text-muted-foreground uppercase">Load a study allocation</p>
        <div className="mt-2 flex flex-wrap gap-2">
          {scenarios.map((scenario) => {
            const active =
              applied.officer_count === scenario.officer_count &&
              applied.computer_count === scenario.computer_count
            return (
              <Button
                key={scenario.scenario_id}
                type="button"
                variant={active ? "default" : "outline"}
                className="h-9 cursor-pointer"
                aria-pressed={active}
                onClick={() => on_scenario(scenario)}
              >
                {scenario.short_label}
              </Button>
            )
          })}
        </div>
      </div>
    </form>
  )
}

function Field({
  id,
  label,
  hint,
  value,
  on_change,
}: {
  id: string
  label: string
  hint: string
  value: string
  on_change: (value: string) => void
}) {
  return (
    <div className="grid gap-1.5">
      <Label htmlFor={id}>{label}</Label>
      <Input
        id={id}
        inputMode="numeric"
        value={value}
        onChange={(event) => on_change(event.target.value)}
        className="h-10 bg-background"
      />
      <p className="text-xs leading-relaxed text-muted-foreground">{hint}</p>
    </div>
  )
}
