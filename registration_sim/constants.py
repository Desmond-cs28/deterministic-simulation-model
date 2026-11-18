"""Named constants for the registration-centre simulation.

The model compares these names in code so resource kinds, activity ids,
and numeric thresholds stay in one place.
"""

from enum import Enum


class ResourceKind(str, Enum):
    OFFICER = "officer"
    COMPUTER = "computer"


class ActivityId(str, Enum):
    REGISTRY_CHECK = "registry_check"
    PORTAL_REGISTRATION = "portal_registration"
    TIMETABLE_ISSUE = "timetable_issue"


class ScenarioId(str, Enum):
    BASELINE = "baseline"
    MORE_OFFICERS = "more_officers"
    MORE_COMPUTERS = "more_computers"


# One morning of undergraduate course registration at Palm University College.
# The 2026/27 calendar sets course registration for 31 August to 4 September.
# About 100 undergraduates share that week, so one morning is a small fixed group.
DEFAULT_STUDENT_COUNT = 20
DEFAULT_INTERARRIVAL_MINUTES = 8
DEFAULT_OFFICER_COUNT = 1
DEFAULT_COMPUTER_COUNT = 1
DEFAULT_WORKING_PERIOD_MINUTES = 240

# Fixed processing times, in minutes, for the deterministic model.
REGISTRY_CHECK_MINUTES = 6
PORTAL_REGISTRATION_MINUTES = 12
TIMETABLE_ISSUE_MINUTES = 4

BASELINE_OFFICER_COUNT = 1
BASELINE_COMPUTER_COUNT = 1
MORE_OFFICERS_OFFICER_COUNT = 2
MORE_OFFICERS_COMPUTER_COUNT = 1
MORE_COMPUTERS_OFFICER_COUNT = 1
MORE_COMPUTERS_COMPUTER_COUNT = 2

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
