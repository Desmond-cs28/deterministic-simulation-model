/** Named constants shared by the lab and the parity check. */

export const ResourceKind = {
  OFFICER: "officer",
  COMPUTER: "computer",
} as const

export type ResourceKind = (typeof ResourceKind)[keyof typeof ResourceKind]

export const ActivityId = {
  DOCUMENT_VERIFICATION: "document_verification",
  COURSE_ENROLMENT: "course_enrolment",
  FEE_ASSESSMENT: "fee_assessment",
  CARD_ISSUE: "card_issue",
} as const

export type ActivityId = (typeof ActivityId)[keyof typeof ActivityId]

export const ScenarioId = {
  BASELINE: "baseline",
  MORE_OFFICERS: "more_officers",
  LEAN: "lean",
  MORE_COMPUTERS: "more_computers",
  BALANCED: "balanced",
  EXPANDED: "expanded",
} as const

export type ScenarioId = (typeof ScenarioId)[keyof typeof ScenarioId]

export const EventKind = {
  RESOURCE_RELEASE: 0,
  STUDENT_READY: 1,
} as const

export const DEFAULT_STUDENT_COUNT = 36
export const DEFAULT_INTERARRIVAL_MINUTES = 3
export const DEFAULT_OFFICER_COUNT = 2
export const DEFAULT_COMPUTER_COUNT = 2
export const DEFAULT_WORKING_PERIOD_MINUTES = 240

export const DOCUMENT_VERIFICATION_MINUTES = 6
export const COURSE_ENROLMENT_MINUTES = 10
export const FEE_ASSESSMENT_MINUTES = 5
export const CARD_ISSUE_MINUTES = 4

export const BASELINE_OFFICER_COUNT = 2
export const BASELINE_COMPUTER_COUNT = 2
export const MORE_OFFICERS_OFFICER_COUNT = 4
export const MORE_OFFICERS_COMPUTER_COUNT = 2
export const LEAN_OFFICER_COUNT = 2
export const LEAN_COMPUTER_COUNT = 3
export const MORE_COMPUTERS_OFFICER_COUNT = 2
export const MORE_COMPUTERS_COMPUTER_COUNT = 4
export const CLOSE_SCORE_GAP = 0.02
export const BALANCED_OFFICER_COUNT = 3
export const BALANCED_COMPUTER_COUNT = 4
export const EXPANDED_OFFICER_COUNT = 4
export const EXPANDED_COMPUTER_COUNT = 4

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
  [ActivityId.DOCUMENT_VERIFICATION]: "#0e6b62",
  [ActivityId.COURSE_ENROLMENT]: "#243044",
  [ActivityId.FEE_ASSESSMENT]: "#b4492a",
  [ActivityId.CARD_ISSUE]: "#c4922a",
}

export const INK = "#1c1915"
export const TEAL = "#0e6b62"
export const NAVY = "#243044"
export const RUST = "#b4492a"
export const AMBER = "#c4922a"
export const GRID = "#e4dccf"
export const PAPER = "#fbf7ef"
export const MUTED = "#5e574c"

export const LINE_COLORS = [TEAL, NAVY, RUST, AMBER, "#6b4c9a", "#3d6b4f"] as const

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
  OFFICERS: "The hall needs between 1 and 8 registration officers.",
  COMPUTERS: "The hall needs between 1 and 8 registration computers.",
  SESSION: "Enter a working period from 0 to 720 minutes.",
} as const

export const LOADING_DELAY_MS = 160
