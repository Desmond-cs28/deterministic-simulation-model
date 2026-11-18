import {
  CLOCK_PAD_WIDTH,
  DISPLAY_INDEX_OFFSET,
  HOURS_PER_DAY,
  MINUTES_PER_HOUR,
  PERCENT_SCALE,
  SHIFT_START_HOUR,
  SHIFT_START_MINUTE,
} from "./constants"

export function format_percent(ratio: number): string {
  return `${(ratio * PERCENT_SCALE).toFixed(1)}%`
}

export function format_one_decimal(value: number): string {
  return value.toFixed(1)
}

export function format_score(value: number): string {
  return value.toFixed(3)
}

export function format_clock(minutes_from_open: number): string {
  const total = SHIFT_START_HOUR * MINUTES_PER_HOUR + SHIFT_START_MINUTE + minutes_from_open
  const wrapped = ((total % (HOURS_PER_DAY * MINUTES_PER_HOUR)) + HOURS_PER_DAY * MINUTES_PER_HOUR) %
    (HOURS_PER_DAY * MINUTES_PER_HOUR)
  const hour = Math.floor(wrapped / MINUTES_PER_HOUR)
  const minute = wrapped % MINUTES_PER_HOUR
  return `${String(hour).padStart(CLOCK_PAD_WIDTH, "0")}:${String(minute).padStart(CLOCK_PAD_WIDTH, "0")}`
}

export function student_label(student_index: number): string {
  return `Student ${student_index + DISPLAY_INDEX_OFFSET}`
}

export function format_count(finished: number, total: number): string {
  return `${finished} / ${total}`
}
