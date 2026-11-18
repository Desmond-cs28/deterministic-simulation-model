import { ACTIVITY_SEQUENCE, processing_minutes_for, total_processing_minutes } from "./activities"
import {
  ARRIVAL_DELTA,
  DEPARTURE_DELTA,
  DISPLAY_INDEX_OFFSET,
  EMPTY_COUNT,
  FIRST_INDEX,
  INDEX_STEP,
  MINUTES_PER_HOUR,
  ResourceKind,
  ZERO_MINUTES,
} from "./constants"
import type {
  ResourceMetrics,
  SimulationConfig,
  SimulationMetrics,
  SimulationResult,
  StageMetrics,
} from "./types"

export function completion_lower_bound(config: SimulationConfig): number {
  if (config.student_count === EMPTY_COUNT) {
    return ZERO_MINUTES
  }
  const officer_each = processing_minutes_for(ResourceKind.OFFICER)
  const computer_each = processing_minutes_for(ResourceKind.COMPUTER)
  const chain = total_processing_minutes()
  const last_student = config.student_count - INDEX_STEP
  let bound = last_student * config.interarrival_minutes + chain
  let student_cursor = FIRST_INDEX
  while (student_cursor < config.student_count) {
    const remaining = config.student_count - student_cursor
    const release = student_cursor * config.interarrival_minutes
    const officer_bound = release + Math.ceil((remaining * officer_each) / config.officer_count)
    const computer_bound = release + Math.ceil((remaining * computer_each) / config.computer_count)
    if (officer_bound > bound) {
      bound = officer_bound
    }
    if (computer_bound > bound) {
      bound = computer_bound
    }
    student_cursor += INDEX_STEP
  }
  return bound
}

function safe_ratio(numerator: number, denominator: number): number {
  if (denominator === ZERO_MINUTES) {
    return ZERO_MINUTES
  }
  return numerator / denominator
}

function peak_students(result: SimulationResult): number {
  const events: { moment: number; delta: number }[] = []
  for (const student of result.students) {
    events.push({ moment: student.arrival_minutes, delta: ARRIVAL_DELTA })
    events.push({ moment: student.completion_minutes, delta: DEPARTURE_DELTA })
  }
  events.sort((left, right) => {
    if (left.moment !== right.moment) {
      return left.moment - right.moment
    }
    return left.delta - right.delta
  })
  let present = EMPTY_COUNT
  let peak = EMPTY_COUNT
  for (const event of events) {
    present += event.delta
    if (present > peak) {
      peak = present
    }
  }
  return peak
}

function resource_label(resource_kind: ResourceKind, resource_index: number): string {
  const title = resource_kind === ResourceKind.OFFICER ? "Officer" : "Computer"
  return `${title} ${resource_index + DISPLAY_INDEX_OFFSET}`
}

export function measure(result: SimulationResult): SimulationMetrics {
  const config = result.config
  const chain = total_processing_minutes()
  const officer_each = processing_minutes_for(ResourceKind.OFFICER)
  const computer_each = processing_minutes_for(ResourceKind.COMPUTER)
  const students_processed = result.students.length
  const total_processing = students_processed * chain
  const officer_busy = students_processed * officer_each
  const computer_busy = students_processed * computer_each

  let total_waiting = ZERO_MINUTES
  let flow_sum = ZERO_MINUTES
  let max_flow = ZERO_MINUTES
  let finished_within = EMPTY_COUNT
  for (const student of result.students) {
    total_waiting += student.waiting_minutes
    flow_sum += student.flow_minutes
    if (student.flow_minutes > max_flow) {
      max_flow = student.flow_minutes
    }
    if (student.completion_minutes <= config.working_period_minutes) {
      finished_within += INDEX_STEP
    }
  }

  const makespan = result.makespan_minutes
  const lower_bound = completion_lower_bound(config)
  const resource_count = config.officer_count + config.computer_count
  const officer_available = config.officer_count * makespan
  const computer_available = config.computer_count * makespan
  const overall_available = resource_count * makespan
  let overtime = ZERO_MINUTES
  if (makespan > config.working_period_minutes) {
    overtime = makespan - config.working_period_minutes
  }
  const completion_ratio = safe_ratio(finished_within, students_processed)
  const overall_utilisation = safe_ratio(total_processing, overall_available)

  return {
    makespan_minutes: makespan,
    lower_bound_minutes: lower_bound,
    schedule_efficiency: safe_ratio(lower_bound, makespan),
    students_processed,
    students_finished_within_period: finished_within,
    students_unfinished_within_period: students_processed - finished_within,
    overtime_minutes: overtime,
    total_processing_minutes: total_processing,
    total_waiting_minutes: total_waiting,
    average_waiting_minutes: safe_ratio(total_waiting, students_processed),
    average_flow_minutes: safe_ratio(flow_sum, students_processed),
    max_flow_minutes: max_flow,
    average_students_waiting: safe_ratio(total_waiting, makespan),
    peak_students_in_system: peak_students(result),
    service_efficiency: safe_ratio(total_processing, total_processing + total_waiting),
    officer_busy_minutes: officer_busy,
    officer_idle_minutes: officer_available - officer_busy,
    officer_utilisation: safe_ratio(officer_busy, officer_available),
    computer_busy_minutes: computer_busy,
    computer_idle_minutes: computer_available - computer_busy,
    computer_utilisation: safe_ratio(computer_busy, computer_available),
    overall_busy_minutes: total_processing,
    overall_idle_minutes: overall_available - total_processing,
    overall_utilisation,
    resource_count,
    productivity_per_resource_hour: safe_ratio(
      students_processed * MINUTES_PER_HOUR,
      resource_count * makespan,
    ),
    completion_ratio,
    efficiency_score: completion_ratio * overall_utilisation,
    resources: resource_rows(result, makespan),
    stages: stage_rows(result, students_processed),
  }
}

function resource_rows(result: SimulationResult, makespan: number): ResourceMetrics[] {
  const rows: ResourceMetrics[] = []
  const pools: [ResourceKind, number][] = [
    [ResourceKind.OFFICER, result.config.officer_count],
    [ResourceKind.COMPUTER, result.config.computer_count],
  ]
  for (const [resource_kind, unit_count] of pools) {
    let unit_index = FIRST_INDEX
    while (unit_index < unit_count) {
      let busy = ZERO_MINUTES
      for (const assignment of result.assignments) {
        const same_kind = assignment.resource_kind === resource_kind
        const same_unit = assignment.resource_index === unit_index
        if (same_kind && same_unit) {
          busy += assignment.processing_minutes
        }
      }
      rows.push({
        resource_kind,
        resource_index: unit_index,
        resource_label: resource_label(resource_kind, unit_index),
        busy_minutes: busy,
        idle_minutes: makespan - busy,
        utilisation: safe_ratio(busy, makespan),
      })
      unit_index += INDEX_STEP
    }
  }
  return rows
}

function stage_rows(result: SimulationResult, students_processed: number): StageMetrics[] {
  return ACTIVITY_SEQUENCE.map((activity) => {
    let total_wait = ZERO_MINUTES
    let max_wait = ZERO_MINUTES
    for (const assignment of result.assignments) {
      if (assignment.activity_id !== activity.activity_id) {
        continue
      }
      total_wait += assignment.waiting_minutes
      if (assignment.waiting_minutes > max_wait) {
        max_wait = assignment.waiting_minutes
      }
    }
    return {
      activity_id: activity.activity_id,
      label: activity.label,
      resource_kind: activity.resource_kind,
      processing_minutes: activity.processing_minutes,
      average_wait_minutes: safe_ratio(total_wait, students_processed),
      max_wait_minutes: max_wait,
      total_wait_minutes: total_wait,
    }
  })
}
