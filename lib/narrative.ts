import { EMPTY_COUNT, MIN_RESOURCE_UNITS, PERCENT_SCALE, ScenarioId, ZERO_MINUTES } from "./constants"
import type { ScenarioRun } from "./types"

export function find_run(runs: ScenarioRun[], scenario_id: ScenarioId): ScenarioRun {
  for (const run of runs) {
    if (run.scenario.scenario_id === scenario_id) {
      return run
    }
  }
  throw new Error(`Missing scenario ${scenario_id}`)
}

function count_label(count: number, singular: string, plural: string): string {
  const word = count === MIN_RESOURCE_UNITS ? singular : plural
  return `${count} ${word}`
}

function percent(ratio: number): string {
  return `${(ratio * PERCENT_SCALE).toFixed(1)}%`
}

function makespan_change(
  resource_name: string,
  from_count: number,
  to_count: number,
  before: number,
  after: number,
): string {
  const delta = after - before
  if (delta === ZERO_MINUTES) {
    return `Adding a ${resource_name} (from ${from_count} to ${to_count}) leaves the finish time at ${after} minutes.`
  }
  if (delta < ZERO_MINUTES) {
    return (
      `Adding a ${resource_name} (from ${from_count} to ${to_count}) ` +
      `brings the finish time forward by ${-delta} minutes, from ${before} to ${after}.`
    )
  }
  return (
    `Adding a ${resource_name} (from ${from_count} to ${to_count}) ` +
    `pushes the finish time out by ${delta} minutes, from ${before} to ${after}.`
  )
}

export function study_paragraphs(runs: ScenarioRun[], recommended: ScenarioRun): string[] {
  const baseline = find_run(runs, ScenarioId.BASELINE)
  if (baseline.result.config.student_count === EMPTY_COUNT) {
    return ["No students arrive, so the registry desk has nothing to compare."]
  }
  const more_officers = find_run(runs, ScenarioId.MORE_OFFICERS)
  const more_computers = find_run(runs, ScenarioId.MORE_COMPUTERS)
  const base = baseline.metrics
  const cohort = baseline.result.config.student_count
  const session = baseline.result.config.working_period_minutes
  const chosen = recommended.metrics
  const chain = base.total_processing_minutes / cohort
  return [
    `Palm University College registers ${cohort} undergraduates on this morning of course-registration week. Each student spends ${chain} minutes at the desk: a registry check, course registration on the Student Portal, and a timetable. The desk is open for ${session} minutes from 08:00. With ${count_label(baseline.scenario.officer_count, "officer", "officers")} and ${count_label(baseline.scenario.computer_count, "computer", "computers")} the last student leaves at ${base.makespan_minutes} minutes, ${base.students_finished_within_period} of ${cohort} finish before the desk closes, and overtime is ${base.overtime_minutes} minutes.`,
    `On the current desk the portal computer is busy for ${percent(base.computer_utilisation)} of the morning and the officer is busy for ${percent(base.officer_utilisation)}. Students wait ${base.average_waiting_minutes.toFixed(1)} minutes on average.`,
    makespan_change(
      "registry officer",
      baseline.scenario.officer_count,
      more_officers.scenario.officer_count,
      base.makespan_minutes,
      more_officers.metrics.makespan_minutes,
    ),
    `Students finished before the desk closes move from ${base.students_finished_within_period} to ${more_officers.metrics.students_finished_within_period}. Officer utilisation moves from ${percent(base.officer_utilisation)} to ${percent(more_officers.metrics.officer_utilisation)}.`,
    makespan_change(
      "portal computer",
      baseline.scenario.computer_count,
      more_computers.scenario.computer_count,
      base.makespan_minutes,
      more_computers.metrics.makespan_minutes,
    ),
    `Students finished before the desk closes move from ${base.students_finished_within_period} to ${more_computers.metrics.students_finished_within_period}. Average waiting moves from ${base.average_waiting_minutes.toFixed(1)} minutes to ${more_computers.metrics.average_waiting_minutes.toFixed(1)} minutes.`,
    `The most efficient allocation is ${recommended.scenario.name}: ${count_label(recommended.scenario.officer_count, "officer", "officers")} and ${count_label(recommended.scenario.computer_count, "computer", "computers")}. It finishes ${chosen.students_finished_within_period} of ${cohort} students before the desk closes, in ${chosen.makespan_minutes} minutes, with overall utilisation ${percent(chosen.overall_utilisation)} and ${chosen.overall_idle_minutes} idle resource-minutes.`,
  ]
}
