"""Named constants for the registration-centre simulation.

The model compares these names in code so resource kinds, activity ids,
and numeric thresholds stay in one place.
"""

from enum import Enum


class ResourceKind(str, Enum):
    OFFICER = "officer"
    COMPUTER = "computer"


class ActivityId(str, Enum):
    DOCUMENT_VERIFICATION = "document_verification"
    COURSE_ENROLMENT = "course_enrolment"
    FEE_ASSESSMENT = "fee_assessment"
    CARD_ISSUE = "card_issue"


class ScenarioId(str, Enum):
    BASELINE = "baseline"
    MORE_OFFICERS = "more_officers"
    LEAN = "lean"
    MORE_COMPUTERS = "more_computers"
    BALANCED = "balanced"
    EXPANDED = "expanded"


# Cohort that arrives during one morning session at North Hall.
DEFAULT_STUDENT_COUNT = 36
DEFAULT_INTERARRIVAL_MINUTES = 3
DEFAULT_OFFICER_COUNT = 2
DEFAULT_COMPUTER_COUNT = 2
DEFAULT_WORKING_PERIOD_MINUTES = 240

# Fixed processing times, in minutes, for the deterministic model.
DOCUMENT_VERIFICATION_MINUTES = 6
COURSE_ENROLMENT_MINUTES = 10
FEE_ASSESSMENT_MINUTES = 5
CARD_ISSUE_MINUTES = 4

BASELINE_OFFICER_COUNT = 2
BASELINE_COMPUTER_COUNT = 2
MORE_OFFICERS_OFFICER_COUNT = 4
MORE_OFFICERS_COMPUTER_COUNT = 2
LEAN_OFFICER_COUNT = 2
LEAN_COMPUTER_COUNT = 3
MORE_COMPUTERS_OFFICER_COUNT = 2
MORE_COMPUTERS_COMPUTER_COUNT = 4
CLOSE_SCORE_GAP = 0.02
BALANCED_OFFICER_COUNT = 3
BALANCED_COMPUTER_COUNT = 4
EXPANDED_OFFICER_COUNT = 4
EXPANDED_COMPUTER_COUNT = 4

SENSITIVITY_MIN_UNITS = 1
SENSITIVITY_MAX_UNITS = 6

EMPTY_COUNT = 0
FIRST_INDEX = 0
INDEX_STEP = 1
MIN_RESOURCE_UNITS = 1
ZERO_MINUTES = 0
MINUTES_PER_HOUR = 60
HOURS_PER_DAY = 24
SHIFT_START_HOUR = 8
SHIFT_START_MINUTE = 0
FULL_RATIO = 1.0
PERCENT_SCALE = 100
CLOCK_PAD_WIDTH = 2
PARITY_ROUND_DIGITS = 6
DISPLAY_INDEX_OFFSET = 1

FIGURE_MAKESPAN = "makespan_by_scenario.png"
FIGURE_UTILISATION = "utilisation_by_scenario.png"
FIGURE_COMPLETIONS = "students_within_period.png"
FIGURE_SENSITIVITY = "sensitivity_makespan.png"
COMPARISON_CSV = "scenario_comparison.csv"

ARRIVAL_DELTA = 1
DEPARTURE_DELTA = -1


class EventKind(int, Enum):
    """Order at one clock time: free a resource before seating a newly ready student."""

    RESOURCE_RELEASE = 0
    STUDENT_READY = 1
