import {
  BALANCED_COMPUTER_COUNT,
  BALANCED_OFFICER_COUNT,
  BASELINE_COMPUTER_COUNT,
  BASELINE_OFFICER_COUNT,
  DEFAULT_COMPUTER_COUNT,
  DEFAULT_INTERARRIVAL_MINUTES,
  DEFAULT_OFFICER_COUNT,
  DEFAULT_STUDENT_COUNT,
  DEFAULT_WORKING_PERIOD_MINUTES,
  EXPANDED_COMPUTER_COUNT,
  EXPANDED_OFFICER_COUNT,
  FIRST_INDEX,
  LEAN_COMPUTER_COUNT,
  LEAN_OFFICER_COUNT,
  FIRST_RUN_INDEX,
  INDEX_STEP,
  MORE_COMPUTERS_COMPUTER_COUNT,
  MORE_COMPUTERS_OFFICER_COUNT,
  MORE_OFFICERS_COMPUTER_COUNT,
  MORE_OFFICERS_OFFICER_COUNT,
  PARITY_ROUND_DIGITS,
  SENSITIVITY_MAX_UNITS,
  SENSITIVITY_MIN_UNITS,
  ScenarioId,
} from "./constants"
import { simulate } from "./engine"
import { measure } from "./metrics"
import type { Scenario, ScenarioRun, SensitivityCell, SimulationConfig } from "./types"

export function default_config(): SimulationConfig {
  return {
    student_count: DEFAULT_STUDENT_COUNT,
    interarrival_minutes: DEFAULT_INTERARRIVAL_MINUTES,
    officer_count: DEFAULT_OFFICER_COUNT,
    computer_count: DEFAULT_COMPUTER_COUNT,
    working_period_minutes: DEFAULT_WORKING_PERIOD_MINUTES,
  }
}

export function study_scenarios(): Scenario[] {
  return [
    {
      scenario_id: ScenarioId.BASELINE,
      name: "Baseline hall",
      short_label: "Baseline 2+2",
      summary: "Two officers and two computers, the current North Hall staffing.",
      officer_count: BASELINE_OFFICER_COUNT,
      computer_count: BASELINE_COMPUTER_COUNT,
    },
    {
      scenario_id: ScenarioId.MORE_OFFICERS,
      name: "Extra officers",
      short_label: "Officers 4+2",
      summary: "Four officers, still with two computers.",
      officer_count: MORE_OFFICERS_OFFICER_COUNT,
      computer_count: MORE_OFFICERS_COMPUTER_COUNT,
    },
    {
      scenario_id: ScenarioId.LEAN,
      name: "Lean computer step",
      short_label: "Lean 2+3",
      summary: "Two officers and three computers, one extra terminal on the baseline hall.",
      officer_count: LEAN_OFFICER_COUNT,
      computer_count: LEAN_COMPUTER_COUNT,
    },
    {
      scenario_id: ScenarioId.MORE_COMPUTERS,
      name: "Extra computers",
      short_label: "Computers 2+4",
      summary: "Two officers, with the computer pool raised to four.",
      officer_count: MORE_COMPUTERS_OFFICER_COUNT,
      computer_count: MORE_COMPUTERS_COMPUTER_COUNT,
    },
    {
      scenario_id: ScenarioId.BALANCED,
      name: "Work-balanced mix",
      short_label: "Balanced 3+4",
      summary: "Three officers and four computers, close to the 11:14 work ratio.",
      officer_count: BALANCED_OFFICER_COUNT,
      computer_count: BALANCED_COMPUTER_COUNT,
    },
    {
      scenario_id: ScenarioId.EXPANDED,
      name: "Both pools doubled",
      short_label: "Doubled 4+4",
      summary: "Four officers and four computers.",
      officer_count: EXPANDED_OFFICER_COUNT,
      computer_count: EXPANDED_COMPUTER_COUNT,
    },
  ]
}

export function run_scenario(base: SimulationConfig, scenario: Scenario): ScenarioRun {
  const result = simulate({
    ...base,
    officer_count: scenario.officer_count,
    computer_count: scenario.computer_count,
  })
  return { scenario, result, metrics: measure(result) }
}

export function run_study(base: SimulationConfig): ScenarioRun[] {
  return study_scenarios().map((scenario) => run_scenario(base, scenario))
}

export function recommendation_key(run: ScenarioRun): [number, number, number, number] {
  const metrics = run.metrics
  return [
    metrics.students_finished_within_period,
    round_digits(metrics.overall_utilisation, PARITY_ROUND_DIGITS),
    -metrics.resource_count,
    -metrics.makespan_minutes,
  ]
}

export function recommend(runs: ScenarioRun[]): ScenarioRun {
  const ordered = [...runs].sort((left, right) => compare_keys(recommendation_key(right), recommendation_key(left)))
  return ordered[FIRST_RUN_INDEX]
}

export function best_sensitivity_cell(cells: SensitivityCell[]): SensitivityCell {
  const ordered = [...cells].sort((left, right) => compare_keys(cell_key(right), cell_key(left)))
  return ordered[FIRST_RUN_INDEX]
}

function cell_key(cell: SensitivityCell): [number, number, number, number] {
  return [
    cell.students_finished_within_period,
    round_digits(cell.overall_utilisation, PARITY_ROUND_DIGITS),
    -(cell.officer_count + cell.computer_count),
    -cell.makespan_minutes,
  ]
}

function compare_keys(left: [number, number, number, number], right: [number, number, number, number]): number {
  let cursor = FIRST_INDEX
  while (cursor < left.length) {
    if (left[cursor] !== right[cursor]) {
      return left[cursor] - right[cursor]
    }
    cursor += INDEX_STEP
  }
  return FIRST_INDEX
}

function round_digits(value: number, digits: number): number {
  const scale = 10 ** digits
  return Math.round(value * scale) / scale
}

export function run_sensitivity(base: SimulationConfig): SensitivityCell[] {
  const cells: SensitivityCell[] = []
  let officer_count = SENSITIVITY_MIN_UNITS
  while (officer_count <= SENSITIVITY_MAX_UNITS) {
    let computer_count = SENSITIVITY_MIN_UNITS
    while (computer_count <= SENSITIVITY_MAX_UNITS) {
      const result = simulate({ ...base, officer_count, computer_count })
      const metrics = measure(result)
      cells.push({
        officer_count,
        computer_count,
        makespan_minutes: metrics.makespan_minutes,
        students_finished_within_period: metrics.students_finished_within_period,
        student_count: base.student_count,
        overall_utilisation: metrics.overall_utilisation,
        overtime_minutes: metrics.overtime_minutes,
      })
      computer_count += INDEX_STEP
    }
    officer_count += INDEX_STEP
  }
  return cells
}
