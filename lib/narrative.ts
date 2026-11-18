import {
  CLOSE_SCORE_GAP,
  EMPTY_COUNT,
  FIRST_INDEX,
  INDEX_STEP,
  PERCENT_SCALE,
  ScenarioId,
  ZERO_MINUTES,
} from "./constants"
import { recommendation_key } from "./experiments"
import type { ScenarioRun } from "./types"

export function find_run(runs: ScenarioRun[], scenario_id: ScenarioId): ScenarioRun {
  for (const run of runs) {
    if (run.scenario.scenario_id === scenario_id) {
      return run
    }
  }
  throw new Error(`Missing scenario ${scenario_id}`)
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
    return (
      `Raising the number of ${resource_name} from ${from_count} to ${to_count} ` +
      `leaves the makespan at ${after} minutes.`
    )
  }
  if (delta < ZERO_MINUTES) {
    const saved = -delta
    return (
      `Raising the number of ${resource_name} from ${from_count} to ${to_count} ` +
      `shortens the makespan by ${saved} minutes, from ${before} to ${after}.`
    )
  }
  return (
    `Raising the number of ${resource_name} from ${from_count} to ${to_count} ` +
    `lengthens the makespan by ${delta} minutes, from ${before} to ${after}.`
  )
}

function bottleneck_sentence(run: ScenarioRun): string {
  const metrics = run.metrics
  const officer_text = percent(metrics.officer_utilisation)
  const computer_text = percent(metrics.computer_utilisation)
  if (metrics.computer_utilisation > metrics.officer_utilisation) {
    return (
      `In the baseline hall the scarce resource is the computer pool, ` +
      `busy for ${computer_text} of the makespan, while officers sit at ${officer_text}.`
    )
  }
  if (metrics.officer_utilisation > metrics.computer_utilisation) {
    return (
      `In the baseline hall the scarce resource is the officer pool, ` +
      `busy for ${officer_text} of the makespan, while computers sit at ${computer_text}.`
    )
  }
  return `In the baseline hall, officers and computers are equally busy at ${officer_text} utilisation.`
}

function runner_up_paragraph(runs: ScenarioRun[], recommended: ScenarioRun): string {
  const ordered = [...runs].sort((left, right) => {
    const left_key = recommendation_key(left)
    const right_key = recommendation_key(right)
    let cursor = FIRST_INDEX
    while (cursor < left_key.length) {
      if (left_key[cursor] !== right_key[cursor]) {
        return right_key[cursor] - left_key[cursor]
      }
      cursor += INDEX_STEP
    }
    return FIRST_INDEX
  })
  if (ordered.length <= INDEX_STEP) {
    return "This study has a single allocation to compare."
  }
  const runner = ordered[FIRST_INDEX + INDEX_STEP]
  const gap = Math.abs(recommended.metrics.efficiency_score - runner.metrics.efficiency_score)
  if (gap > CLOSE_SCORE_GAP) {
    return (
      `The next allocation on the efficiency score is ${runner.scenario.name} ` +
      `at ${runner.metrics.efficiency_score.toFixed(3)}.`
    )
  }
  return (
    `${runner.scenario.name} sits close on the efficiency score ` +
    `(${runner.metrics.efficiency_score.toFixed(3)} against ${recommended.metrics.efficiency_score.toFixed(3)}). ` +
    `It staffs ${runner.scenario.officer_count} officers and ${runner.scenario.computer_count} computers, ` +
    `finishes at ${runner.metrics.makespan_minutes} minutes, and holds average waiting to ` +
    `${runner.metrics.average_waiting_minutes.toFixed(1)} minutes, compared with ` +
    `${recommended.metrics.average_waiting_minutes.toFixed(1)} minutes under ${recommended.scenario.name}. ` +
    `The leaner mix is the one to staff when officer-time and computer-time are the budget. ` +
    `The nearby mix is the one to staff when shorter queues matter as well.`
  )
}

export function study_paragraphs(runs: ScenarioRun[], recommended: ScenarioRun): string[] {
  const baseline = find_run(runs, ScenarioId.BASELINE)
  if (baseline.result.config.student_count === EMPTY_COUNT) {
    return ["The cohort is empty, so the hall has no registration work to compare."]
  }
  const more_officers = find_run(runs, ScenarioId.MORE_OFFICERS)
  const lean = find_run(runs, ScenarioId.LEAN)
  const more_computers = find_run(runs, ScenarioId.MORE_COMPUTERS)
  const base_metrics = baseline.metrics
  const cohort = baseline.result.config.student_count
  const session = baseline.result.config.working_period_minutes
  const chain = Math.floor(base_metrics.total_processing_minutes / cohort)
  const recommended_metrics = recommended.metrics

  return [
    `The hall registers a fixed cohort of ${cohort} students. ` +
      `Each student needs ${chain} minutes of processing, split across shared officers and shared computers. ` +
      `The session lasts ${session} minutes. ` +
      `With the baseline allocation the last student finishes at ${base_metrics.makespan_minutes} minutes, ` +
      `${base_metrics.students_finished_within_period} of ${cohort} students finish inside the session, ` +
      `and overtime is ${base_metrics.overtime_minutes} minutes.`,
    bottleneck_sentence(baseline),
    makespan_change(
      "registration officers",
      baseline.scenario.officer_count,
      more_officers.scenario.officer_count,
      base_metrics.makespan_minutes,
      more_officers.metrics.makespan_minutes,
    ),
    `Students finished inside the session move from ${base_metrics.students_finished_within_period} to ` +
      `${more_officers.metrics.students_finished_within_period} when only the officer pool grows. ` +
      `Officer utilisation moves from ${percent(base_metrics.officer_utilisation)} ` +
      `to ${percent(more_officers.metrics.officer_utilisation)}, and computer utilisation moves from ` +
      `${percent(base_metrics.computer_utilisation)} to ${percent(more_officers.metrics.computer_utilisation)}.`,
    makespan_change(
      "registration computers",
      baseline.scenario.computer_count,
      lean.scenario.computer_count,
      base_metrics.makespan_minutes,
      lean.metrics.makespan_minutes,
    ),
    `Students finished inside the session move from ${base_metrics.students_finished_within_period} to ` +
      `${lean.metrics.students_finished_within_period} when the computer pool grows from ` +
      `${baseline.scenario.computer_count} to ${lean.scenario.computer_count}. ` +
      `Average waiting time moves from ${base_metrics.average_waiting_minutes.toFixed(1)} minutes ` +
      `to ${lean.metrics.average_waiting_minutes.toFixed(1)} minutes.`,
    makespan_change(
      "registration computers",
      lean.scenario.computer_count,
      more_computers.scenario.computer_count,
      lean.metrics.makespan_minutes,
      more_computers.metrics.makespan_minutes,
    ),
    runner_up_paragraph(runs, recommended),
    `The most efficient allocation in this study is ${recommended.scenario.name} ` +
      `(${recommended.scenario.officer_count} officers and ${recommended.scenario.computer_count} computers). ` +
      `It finishes ${recommended_metrics.students_finished_within_period} of ${cohort} students inside the session, ` +
      `with a makespan of ${recommended_metrics.makespan_minutes} minutes, overall resource utilisation of ` +
      `${percent(recommended_metrics.overall_utilisation)}, and ${recommended_metrics.overall_idle_minutes} idle resource-minutes. ` +
      `The efficiency score, completion ratio times overall utilisation, is ${recommended_metrics.efficiency_score.toFixed(3)}. ` +
      `Schedule efficiency against the lower bound is ${percent(recommended_metrics.schedule_efficiency)}.`,
    "The ranking finishes the largest number of students before the session closes, then keeps the highest overall utilisation, so a larger pool is chosen only when the extra officers or computers still earn their time. Service efficiency is processing time divided by processing plus waiting. It rises when queues shrink, and it can look strong for a generously staffed hall whose resources then spend more of the makespan idle.",
  ]
}
