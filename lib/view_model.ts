import { PERCENT_SCALE, SENSITIVITY_MAX_UNITS, SENSITIVITY_MIN_UNITS } from "./constants"
import { best_sensitivity_cell, recommend, run_sensitivity, run_study } from "./experiments"
import { measure } from "./metrics"
import { study_paragraphs } from "./narrative"
import { simulate } from "./engine"
import type { ScenarioRun, SensitivityCell, SimulationConfig, SimulationMetrics, SimulationResult } from "./types"

export type HallModel = {
  result: SimulationResult
  metrics: SimulationMetrics
  study: ScenarioRun[]
  recommended: ScenarioRun
  sensitivity: SensitivityCell[]
  best_cell: SensitivityCell
  paragraphs: string[]
}

export function build_model(config: SimulationConfig): HallModel {
  const result = simulate(config)
  const metrics = measure(result)
  const study = run_study(config)
  const recommended = recommend(study)
  const sensitivity = run_sensitivity(config)
  const best_cell = best_sensitivity_cell(sensitivity)
  const paragraphs = study_paragraphs(study, recommended)
  if (
    best_cell.officer_count !== recommended.scenario.officer_count ||
    best_cell.computer_count !== recommended.scenario.computer_count
  ) {
    paragraphs.push(
      `On the wider grid of ${SENSITIVITY_MIN_UNITS} to ${SENSITIVITY_MAX_UNITS} officers and computers, ${best_cell.officer_count} officers and ${best_cell.computer_count} computers score higher: makespan ${best_cell.makespan_minutes} minutes, ${best_cell.students_finished_within_period} of ${best_cell.student_count} students inside the session, utilisation ${(best_cell.overall_utilisation * PERCENT_SCALE).toFixed(1)}%.`,
    )
  }
  return { result, metrics, study, recommended, sensitivity, best_cell, paragraphs }
}
