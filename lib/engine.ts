/**
 * Discrete-event engine. Event order matches the Python program:
 * at one clock time a freed resource seats the longest-waiting student
 * before a newly ready student is allowed to take a unit.
 */

import { ACTIVITY_SEQUENCE } from "./activities"
import {
  CHILD_STRIDE,
  EMPTY_COUNT,
  EventKind,
  FIRST_INDEX,
  INDEX_STEP,
  LEFT_CHILD_OFFSET,
  MIN_RESOURCE_UNITS,
  ResourceKind,
  ZERO_MINUTES,
} from "./constants"
import type {
  SimulationConfig,
  SimulationResult,
  StageAssignment,
  StudentRecord,
} from "./types"

type HeapEvent = {
  moment: number
  kind: number
  student_index: number
  sequence: number
  resource_kind: string
}

export class ConfigurationError extends Error {}

export function validate_config(config: SimulationConfig): void {
  if (config.student_count < EMPTY_COUNT) {
    throw new ConfigurationError("Student count cannot be negative.")
  }
  if (config.interarrival_minutes < ZERO_MINUTES) {
    throw new ConfigurationError("Interarrival time cannot be negative.")
  }
  if (config.officer_count < MIN_RESOURCE_UNITS) {
    throw new ConfigurationError("The hall needs at least one registration officer.")
  }
  if (config.computer_count < MIN_RESOURCE_UNITS) {
    throw new ConfigurationError("The hall needs at least one registration computer.")
  }
  if (config.working_period_minutes < ZERO_MINUTES) {
    throw new ConfigurationError("The working period cannot be negative.")
  }
}

function event_before(left: HeapEvent, right: HeapEvent): boolean {
  if (left.moment !== right.moment) {
    return left.moment < right.moment
  }
  if (left.kind !== right.kind) {
    return left.kind < right.kind
  }
  if (left.student_index !== right.student_index) {
    return left.student_index < right.student_index
  }
  return left.sequence < right.sequence
}

function heap_push(heap: HeapEvent[], event: HeapEvent): void {
  heap.push(event)
  let index = heap.length - INDEX_STEP
  while (index > FIRST_INDEX) {
    const parent = Math.floor((index - INDEX_STEP) / CHILD_STRIDE)
    if (!event_before(heap[index], heap[parent])) {
      return
    }
    const swap = heap[parent]
    heap[parent] = heap[index]
    heap[index] = swap
    index = parent
  }
}

function heap_pop(heap: HeapEvent[]): HeapEvent {
  const top = heap[FIRST_INDEX]
  const last = heap.pop()
  if (heap.length === EMPTY_COUNT || last === undefined) {
    return top
  }
  heap[FIRST_INDEX] = last
  let index = FIRST_INDEX
  while (index >= FIRST_INDEX) {
    const left = index * CHILD_STRIDE + LEFT_CHILD_OFFSET
    const right = left + INDEX_STEP
    let smallest = index
    if (left < heap.length && event_before(heap[left], heap[smallest])) {
      smallest = left
    }
    if (right < heap.length && event_before(heap[right], heap[smallest])) {
      smallest = right
    }
    if (smallest === index) {
      return top
    }
    const swap = heap[smallest]
    heap[smallest] = heap[index]
    heap[index] = swap
    index = smallest
  }
  return top
}

export function select_available_unit(free_at: number[], now: number): number | null {
  let unit_index = FIRST_INDEX
  const pool_size = free_at.length
  while (unit_index < pool_size) {
    if (free_at[unit_index] <= now) {
      return unit_index
    }
    unit_index += INDEX_STEP
  }
  return null
}

export function simulate(config: SimulationConfig): SimulationResult {
  validate_config(config)
  const free_at: Record<ResourceKind, number[]> = {
    [ResourceKind.OFFICER]: Array(config.officer_count).fill(ZERO_MINUTES),
    [ResourceKind.COMPUTER]: Array(config.computer_count).fill(ZERO_MINUTES),
  }
  const waiting: Record<ResourceKind, number[]> = {
    [ResourceKind.OFFICER]: [],
    [ResourceKind.COMPUTER]: [],
  }
  const stage_index = Array(config.student_count).fill(FIRST_INDEX)
  const ready_at = Array(config.student_count).fill(ZERO_MINUTES)
  const completion_at = Array(config.student_count).fill(ZERO_MINUTES)
  const assignments: StageAssignment[] = []
  const events: HeapEvent[] = []
  let sequence = FIRST_INDEX

  function push(moment: number, kind: number, student_index: number, resource_kind: string): void {
    heap_push(events, { moment, kind, student_index, sequence, resource_kind })
    sequence += INDEX_STEP
  }

  function begin_stage(student_index: number, unit_index: number, start_minutes: number): void {
    const activity = ACTIVITY_SEQUENCE[stage_index[student_index]]
    const end_minutes = start_minutes + activity.processing_minutes
    free_at[activity.resource_kind][unit_index] = end_minutes
    assignments.push({
      student_index,
      activity_id: activity.activity_id,
      resource_kind: activity.resource_kind,
      resource_index: unit_index,
      ready_minutes: ready_at[student_index],
      start_minutes,
      end_minutes,
      waiting_minutes: start_minutes - ready_at[student_index],
      processing_minutes: activity.processing_minutes,
    })
    stage_index[student_index] += INDEX_STEP
    if (stage_index[student_index] < ACTIVITY_SEQUENCE.length) {
      push(end_minutes, EventKind.STUDENT_READY, student_index, "")
    } else {
      completion_at[student_index] = end_minutes
    }
    push(end_minutes, EventKind.RESOURCE_RELEASE, student_index, activity.resource_kind)
  }

  function start_or_queue(student_index: number, moment: number): void {
    ready_at[student_index] = moment
    const activity = ACTIVITY_SEQUENCE[stage_index[student_index]]
    const unit_index = select_available_unit(free_at[activity.resource_kind], moment)
    if (unit_index === null) {
      waiting[activity.resource_kind].push(student_index)
      return
    }
    begin_stage(student_index, unit_index, moment)
  }

  function serve_queue(resource_kind: ResourceKind, moment: number): void {
    const queue = waiting[resource_kind]
    if (queue.length === EMPTY_COUNT) {
      return
    }
    const student_index = queue.shift()
    if (student_index === undefined) {
      return
    }
    const unit_index = select_available_unit(free_at[resource_kind], moment)
    if (unit_index === null) {
      queue.unshift(student_index)
      return
    }
    begin_stage(student_index, unit_index, moment)
  }

  for (let student_index = FIRST_INDEX; student_index < config.student_count; student_index += INDEX_STEP) {
    push(student_index * config.interarrival_minutes, EventKind.STUDENT_READY, student_index, "")
  }

  while (events.length > EMPTY_COUNT) {
    const event = heap_pop(events)
    if (event.kind === EventKind.RESOURCE_RELEASE) {
      serve_queue(event.resource_kind as ResourceKind, event.moment)
    } else {
      start_or_queue(event.student_index, event.moment)
    }
  }

  const students = student_records(config, assignments, completion_at)
  let makespan_minutes = ZERO_MINUTES
  for (const student of students) {
    if (student.completion_minutes > makespan_minutes) {
      makespan_minutes = student.completion_minutes
    }
  }
  return { config, students, assignments, makespan_minutes }
}

function student_records(
  config: SimulationConfig,
  assignments: StageAssignment[],
  completion_at: number[],
): StudentRecord[] {
  const grouped: StageAssignment[][] = Array.from({ length: config.student_count }, () => [])
  for (const assignment of assignments) {
    grouped[assignment.student_index].push(assignment)
  }
  return grouped.map((stages, student_index) => {
    const arrival_minutes = student_index * config.interarrival_minutes
    let waiting_minutes = ZERO_MINUTES
    for (const stage of stages) {
      waiting_minutes += stage.waiting_minutes
    }
    const completion_minutes = completion_at[student_index]
    return {
      student_index,
      arrival_minutes,
      completion_minutes,
      waiting_minutes,
      flow_minutes: completion_minutes - arrival_minutes,
      stages,
    }
  })
}
