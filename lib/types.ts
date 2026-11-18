import type { ActivityId, ResourceKind, ScenarioId } from "./constants"

export type SimulationConfig = {
  student_count: number
  interarrival_minutes: number
  officer_count: number
  computer_count: number
  working_period_minutes: number
}

export type StageAssignment = {
  student_index: number
  activity_id: ActivityId
  resource_kind: ResourceKind
  resource_index: number
  ready_minutes: number
  start_minutes: number
  end_minutes: number
  waiting_minutes: number
  processing_minutes: number
}

export type StudentRecord = {
  student_index: number
  arrival_minutes: number
  completion_minutes: number
  waiting_minutes: number
  flow_minutes: number
  stages: StageAssignment[]
}

export type SimulationResult = {
  config: SimulationConfig
  students: StudentRecord[]
  assignments: StageAssignment[]
  makespan_minutes: number
}

export type ResourceMetrics = {
  resource_kind: ResourceKind
  resource_index: number
  resource_label: string
  busy_minutes: number
  idle_minutes: number
  utilisation: number
}

export type StageMetrics = {
  activity_id: ActivityId
  label: string
  resource_kind: ResourceKind
  processing_minutes: number
  average_wait_minutes: number
  max_wait_minutes: number
  total_wait_minutes: number
}

export type SimulationMetrics = {
  makespan_minutes: number
  lower_bound_minutes: number
  schedule_efficiency: number
  students_processed: number
  students_finished_within_period: number
  students_unfinished_within_period: number
  overtime_minutes: number
  total_processing_minutes: number
  total_waiting_minutes: number
  average_waiting_minutes: number
  average_flow_minutes: number
  max_flow_minutes: number
  average_students_waiting: number
  peak_students_in_system: number
  service_efficiency: number
  officer_busy_minutes: number
  officer_idle_minutes: number
  officer_utilisation: number
  computer_busy_minutes: number
  computer_idle_minutes: number
  computer_utilisation: number
  overall_busy_minutes: number
  overall_idle_minutes: number
  overall_utilisation: number
  resource_count: number
  productivity_per_resource_hour: number
  completion_ratio: number
  efficiency_score: number
  resources: ResourceMetrics[]
  stages: StageMetrics[]
}

export type Scenario = {
  scenario_id: ScenarioId
  name: string
  short_label: string
  summary: string
  officer_count: number
  computer_count: number
}

export type ScenarioRun = {
  scenario: Scenario
  result: SimulationResult
  metrics: SimulationMetrics
}

export type SensitivityCell = {
  officer_count: number
  computer_count: number
  makespan_minutes: number
  students_finished_within_period: number
  student_count: number
  overall_utilisation: number
  overtime_minutes: number
}

export type ActivitySpec = {
  activity_id: ActivityId
  label: string
  short_label: string
  resource_kind: ResourceKind
  processing_minutes: number
  description: string
}
