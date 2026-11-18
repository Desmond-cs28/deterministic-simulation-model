import { recommend, run_study } from "./experiments"
import { measure } from "./metrics"
import { study_paragraphs } from "./narrative"
import { simulate } from "./engine"
import type { ScenarioRun, SimulationConfig, SimulationMetrics, SimulationResult } from "./types"

export type HallModel = {
  result: SimulationResult
  metrics: SimulationMetrics
  study: ScenarioRun[]
  recommended: ScenarioRun
  paragraphs: string[]
}

export function build_model(config: SimulationConfig): HallModel {
  const result = simulate(config)
  const metrics = measure(result)
  const study = run_study(config)
  const recommended = recommend(study)
  const paragraphs = study_paragraphs(study, recommended)
  return { result, metrics, study, recommended, paragraphs }
}
