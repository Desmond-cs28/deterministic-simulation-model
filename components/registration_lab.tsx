"use client"

import { useMemo, useRef, useState } from "react"

import { EMPTY_COUNT, LOADING_DELAY_MS, RunStatus } from "@/lib/constants"
import { draft_from_config, parse_draft, type DraftText } from "@/lib/draft"
import { default_config } from "@/lib/experiments"
import { build_model } from "@/lib/view_model"
import type { Scenario } from "@/lib/types"

import { ModelSection } from "./activity_strip"
import { DetailTables } from "./detail_tables"
import { ExperimentPanel } from "./experiment_panel"
import { Glossary } from "./glossary"
import { Interpretation } from "./interpretation"
import { KpiGrid } from "./kpi_grid"
import { LabControls } from "./lab_controls"
import { Masthead } from "./masthead"
import { ResourceGantt } from "./resource_gantt"
import { SectionBlock } from "./section_block"
import { SensitivityPanel } from "./sensitivity_panel"

const LAB_ANCHOR = "lab"

export function RegistrationLab() {
  const initial = default_config()
  const [draft, set_draft] = useState(() => draft_from_config(initial))
  const [applied, set_applied] = useState(initial)
  const [status, set_status] = useState<RunStatus>(RunStatus.READY)
  const [error_message, set_error_message] = useState("")
  const timer_ref = useRef<number | null>(null)
  const model = useMemo(() => build_model(applied), [applied])
  const cohort_empty = applied.student_count === EMPTY_COUNT
  const running = status === RunStatus.RUNNING

  function commit(next_draft: DraftText) {
    const parsed = parse_draft(next_draft)
    if (!parsed.ok) {
      set_status(RunStatus.ERROR)
      set_error_message(parsed.message)
      return
    }
    if (timer_ref.current !== null) {
      window.clearTimeout(timer_ref.current)
    }
    set_status(RunStatus.RUNNING)
    set_error_message("")
    timer_ref.current = window.setTimeout(() => {
      set_applied(parsed.config)
      set_status(RunStatus.READY)
      timer_ref.current = null
    }, LOADING_DELAY_MS)
  }

  function apply_counts(officer_count: number, computer_count: number) {
    const next_draft = {
      ...draft,
      officer_count: String(officer_count),
      computer_count: String(computer_count),
    }
    set_draft(next_draft)
    commit(next_draft)
    document.getElementById(LAB_ANCHOR)?.scrollIntoView({ behavior: "smooth", block: "start" })
  }

  function on_scenario(scenario: Scenario) {
    apply_counts(scenario.officer_count, scenario.computer_count)
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      <Masthead />
      <main className="mx-auto flex max-w-6xl flex-col gap-16 px-4 py-10 sm:px-6 sm:py-14">
        <ModelSection />
        <SectionBlock
          id={LAB_ANCHOR}
          kicker="A single run"
          title="Schedule this morning"
          lede="Change the cohort or the staffing, then run the hall. The timeline, the resource table, and the student list all describe that one schedule."
        >
          <div className="grid items-start gap-4 lg:grid-cols-[minmax(0,0.92fr)_minmax(0,1.08fr)]">
            <LabControls
              draft={draft}
              applied={applied}
              status={status}
              on_change={(field, value) => set_draft((current) => ({ ...current, [field]: value }))}
              on_run={() => commit(draft)}
              on_scenario={on_scenario}
            />
            <div aria-busy={running} className={running ? "opacity-60" : undefined}>
              {status === RunStatus.ERROR ? (
                <p role="alert" className="mb-3 rounded-lg border border-destructive/40 bg-destructive/10 px-3 py-2 text-sm text-destructive">
                  {error_message} The schedule on screen is still the previous valid run.
                </p>
              ) : null}
              {running ? (
                <p className="mb-3 font-mono text-xs tracking-[0.14em] text-primary uppercase">Scheduling the hall…</p>
              ) : null}
              {cohort_empty ? <EmptyHall /> : <KpiGrid metrics={model.metrics} />}
            </div>
          </div>
          {cohort_empty ? null : (
            <div className="mt-4 flex flex-col gap-4">
              <ResourceGantt result={model.result} />
              <DetailTables result={model.result} metrics={model.metrics} />
            </div>
          )}
        </SectionBlock>
        <ExperimentPanel
          runs={model.study}
          recommended_id={model.recommended.scenario.scenario_id}
          session_minutes={applied.working_period_minutes}
          on_open={(run) => on_scenario(run.scenario)}
        />
        <SensitivityPanel
          cells={model.sensitivity}
          session_minutes={applied.working_period_minutes}
          applied_officers={applied.officer_count}
          applied_computers={applied.computer_count}
          best_officers={model.best_cell.officer_count}
          best_computers={model.best_cell.computer_count}
          on_select={apply_counts}
        />
        <Interpretation paragraphs={model.paragraphs} recommended={model.recommended} />
        <Glossary />
      </main>
      <footer className="border-t border-foreground/10 px-4 py-8 text-sm text-muted-foreground sm:px-6">
        <div className="mx-auto flex max-w-6xl flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <p>North Hall registration model. Same inputs, same schedule.</p>
          <p className="font-mono text-xs">python -m registration_sim</p>
        </div>
      </footer>
    </div>
  )
}

function EmptyHall() {
  return (
    <div className="flex h-full min-h-48 flex-col justify-center rounded-xl border border-dashed border-foreground/20 bg-card px-5 py-8">
      <h3 className="font-heading text-2xl">The cohort is empty</h3>
      <p className="mt-2 max-w-md text-sm leading-relaxed text-muted-foreground">
        Set the student count to at least one and run the simulation. With nobody to register, makespan, waiting, and utilisation are all zero.
      </p>
    </div>
  )
}
