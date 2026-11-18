"""The three steps of course registration at Palm University College."""

from dataclasses import dataclass

from registration_sim.constants import (
    PORTAL_REGISTRATION_MINUTES,
    REGISTRY_CHECK_MINUTES,
    TIMETABLE_ISSUE_MINUTES,
    ZERO_MINUTES,
    ActivityId,
    ResourceKind,
)


@dataclass(frozen=True)
class ActivitySpec:
    activity_id: ActivityId
    label: str
    short_label: str
    resource_kind: ResourceKind
    processing_minutes: int
    description: str


# Every student walks this sequence. Stages do not overlap for one student.
ACTIVITY_SEQUENCE: tuple[ActivitySpec, ...] = (
    ActivitySpec(
        activity_id=ActivityId.REGISTRY_CHECK,
        label="Registry check",
        short_label="Registry",
        resource_kind=ResourceKind.OFFICER,
        processing_minutes=REGISTRY_CHECK_MINUTES,
        description=(
            "A registry officer checks the student ID and confirms the "
            "programme: Computer Science, Business Information Technology, "
            "or Business Administration."
        ),
    ),
    ActivitySpec(
        activity_id=ActivityId.PORTAL_REGISTRATION,
        label="Student Portal registration",
        short_label="Portal",
        resource_kind=ResourceKind.COMPUTER,
        processing_minutes=PORTAL_REGISTRATION_MINUTES,
        description=(
            "The student registers semester courses on a Student Portal "
            "computer at the registry desk."
        ),
    ),
    ActivitySpec(
        activity_id=ActivityId.TIMETABLE_ISSUE,
        label="Timetable issue",
        short_label="Timetable",
        resource_kind=ResourceKind.OFFICER,
        processing_minutes=TIMETABLE_ISSUE_MINUTES,
        description=(
            "The officer confirms the course list and issues the printed timetable."
        ),
    ),
)


def activity_by_id(activity_id: ActivityId) -> ActivitySpec:
    for activity in ACTIVITY_SEQUENCE:
        if activity.activity_id == activity_id:
            return activity
    raise KeyError(activity_id)


def processing_minutes_for(resource_kind: ResourceKind) -> int:
    total = ZERO_MINUTES
    for activity in ACTIVITY_SEQUENCE:
        if activity.resource_kind == resource_kind:
            total += activity.processing_minutes
    return total


def total_processing_minutes() -> int:
    total = ZERO_MINUTES
    for activity in ACTIVITY_SEQUENCE:
        total += activity.processing_minutes
    return total
