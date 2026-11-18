import {
  EMPTY_COUNT,
  MAX_INTERARRIVAL_MINUTES,
  MAX_RESOURCE_UNITS,
  MAX_SESSION_MINUTES,
  MAX_STUDENT_COUNT,
  MIN_RESOURCE_UNITS,
  ValidationMessage,
  ZERO_MINUTES,
} from "./constants"
import type { SimulationConfig } from "./types"

export type DraftText = {
  student_count: string
  interarrival_minutes: string
  officer_count: string
  computer_count: string
  working_period_minutes: string
}

export type ParseResult =
  | { ok: true; config: SimulationConfig }
  | { ok: false; message: string }

const WHOLE_NUMBER = /^\d+$/

export function draft_from_config(config: SimulationConfig): DraftText {
  return {
    student_count: String(config.student_count),
    interarrival_minutes: String(config.interarrival_minutes),
    officer_count: String(config.officer_count),
    computer_count: String(config.computer_count),
    working_period_minutes: String(config.working_period_minutes),
  }
}

function parse_whole(text: string): number | null {
  const trimmed = text.trim()
  if (!WHOLE_NUMBER.test(trimmed)) {
    return null
  }
  return Number(trimmed)
}

function in_range(value: number | null, low: number, high: number): value is number {
  return value !== null && value >= low && value <= high
}

export function parse_draft(draft: DraftText): ParseResult {
  const student_count = parse_whole(draft.student_count)
  const interarrival_minutes = parse_whole(draft.interarrival_minutes)
  const officer_count = parse_whole(draft.officer_count)
  const computer_count = parse_whole(draft.computer_count)
  const working_period_minutes = parse_whole(draft.working_period_minutes)

  if (!in_range(student_count, EMPTY_COUNT, MAX_STUDENT_COUNT)) {
    return { ok: false, message: ValidationMessage.STUDENT_COUNT }
  }
  if (!in_range(interarrival_minutes, ZERO_MINUTES, MAX_INTERARRIVAL_MINUTES)) {
    return { ok: false, message: ValidationMessage.INTERARRIVAL }
  }
  if (!in_range(officer_count, MIN_RESOURCE_UNITS, MAX_RESOURCE_UNITS)) {
    return { ok: false, message: ValidationMessage.OFFICERS }
  }
  if (!in_range(computer_count, MIN_RESOURCE_UNITS, MAX_RESOURCE_UNITS)) {
    return { ok: false, message: ValidationMessage.COMPUTERS }
  }
  if (!in_range(working_period_minutes, ZERO_MINUTES, MAX_SESSION_MINUTES)) {
    return { ok: false, message: ValidationMessage.SESSION }
  }

  return {
    ok: true,
    config: {
      student_count,
      interarrival_minutes,
      officer_count,
      computer_count,
      working_period_minutes,
    },
  }
}
