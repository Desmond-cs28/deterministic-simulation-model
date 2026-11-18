/** Named constants shared by the lab and the parity check. */

export const ResourceKind = {
  OFFICER: "officer",
  COMPUTER: "computer",
} as const

export type ResourceKind = (typeof ResourceKind)[keyof typeof ResourceKind]

export const ActivityId = {
  REGISTRY_CHECK: "registry_check",
  PORTAL_REGISTRATION: "portal_registration",
  TIMETABLE_ISSUE: "timetable_issue",
} as const

export type ActivityId = (typeof ActivityId)[keyof typeof ActivityId]

export const ScenarioId = {
  BASELINE: "baseline",
  MORE_OFFICERS: "more_officers",
  MORE_COMPUTERS: "more_computers",
} as const

export type ScenarioId = (typeof ScenarioId)[keyof typeof ScenarioId]

export const EventKind = {
  RESOURCE_RELEASE: 0,
  STUDENT_READY: 1,
} as const

export const DEFAULT_STUDENT_COUNT = 20
export const DEFAULT_INTERARRIVAL_MINUTES = 8
export const DEFAULT_OFFICER_COUNT = 1
export const DEFAULT_COMPUTER_COUNT = 1
export const DEFAULT_WORKING_PERIOD_MINUTES = 240

export const REGISTRY_CHECK_MINUTES = 6
export const PORTAL_REGISTRATION_MINUTES = 12
export const TIMETABLE_ISSUE_MINUTES = 4

export const BASELINE_OFFICER_COUNT = 1
export const BASELINE_COMPUTER_COUNT = 1
export const MORE_OFFICERS_OFFICER_COUNT = 2
export const MORE_OFFICERS_COMPUTER_COUNT = 1
export const MORE_COMPUTERS_OFFICER_COUNT = 1
export const MORE_COMPUTERS_COMPUTER_COUNT = 2

export const SENSITIVITY_MIN_UNITS = 1
export const SENSITIVITY_MAX_UNITS = 6

export const EMPTY_COUNT = 0
export const FIRST_INDEX = 0
export const INDEX_STEP = 1
export const MIN_RESOURCE_UNITS = 1
export const ZERO_MINUTES = 0
export const MINUTES_PER_HOUR = 60
export const HOURS_PER_DAY = 24
export const SHIFT_START_HOUR = 8
export const SHIFT_START_MINUTE = 0
export const PERCENT_SCALE = 100
export const CLOCK_PAD_WIDTH = 2
export const PARITY_ROUND_DIGITS = 6
export const DISPLAY_INDEX_OFFSET = 1
export const CHILD_STRIDE = 2
export const LEFT_CHILD_OFFSET = 1
export const FIRST_RUN_INDEX = 0

export const MAX_STUDENT_COUNT = 120
export const MAX_INTERARRIVAL_MINUTES = 60
export const MAX_RESOURCE_UNITS = 8
export const MAX_SESSION_MINUTES = 720

export const ARRIVAL_DELTA = 1
export const DEPARTURE_DELTA = -1

export const GANTT_PIXELS_PER_MINUTE = 3
export const GANTT_LABEL_WIDTH = 112
export const GANTT_ROW_HEIGHT = 34
export const GANTT_AXIS_HEIGHT = 28
export const GANTT_PADDING_RIGHT = 16

export const ActivityColor: Record<ActivityId, string> = {
  [ActivityId.REGISTRY_CHECK]: "#02553C",
  [ActivityId.PORTAL_REGISTRATION]: "#013326",
  [ActivityId.TIMETABLE_ISSUE]: "#c4a35a",
}

export const INK = "#14241c"
export const TEAL = "#02553C"
export const NAVY = "#013326"
export const RUST = "#3d8f6e"
export const AMBER = "#c4a35a"
export const GRID = "#d5e4db"
export const PAPER = "#ffffff"
export const MUTED = "#3d5348"

export const LINE_COLORS = [TEAL, NAVY, RUST, AMBER] as const

export const YES_LABEL = "Yes"
export const NO_LABEL = "No"

export const RunStatus = {
  READY: "ready",
  RUNNING: "running",
  ERROR: "error",
} as const

export type RunStatus = (typeof RunStatus)[keyof typeof RunStatus]

export const ValidationMessage = {
  STUDENT_COUNT: "Enter a whole number of students from 0 to 120.",
  INTERARRIVAL: "Enter whole minutes between arrivals, from 0 to 60.",
  OFFICERS: "The desk needs between 1 and 8 registry officers.",
  COMPUTERS: "The desk needs between 1 and 8 Student Portal computers.",
  SESSION: "Enter a working period from 0 to 720 minutes.",
} as const

export const LOADING_DELAY_MS = 160
