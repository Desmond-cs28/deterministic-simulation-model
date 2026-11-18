"""Registration activities and the resource each one seizes."""

from dataclasses import dataclass

from registration_sim.constants import (
    CARD_ISSUE_MINUTES,
    COURSE_ENROLMENT_MINUTES,
    DOCUMENT_VERIFICATION_MINUTES,
    FEE_ASSESSMENT_MINUTES,
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
        activity_id=ActivityId.DOCUMENT_VERIFICATION,
        label="Document verification",
        short_label="Documents",
        resource_kind=ResourceKind.OFFICER,
        processing_minutes=DOCUMENT_VERIFICATION_MINUTES,
        description=(
            "An officer checks the admission letter, identity document, "
            "and prerequisite record."
        ),
    ),
    ActivitySpec(
        activity_id=ActivityId.COURSE_ENROLMENT,
        label="Course enrolment",
        short_label="Enrolment",
        resource_kind=ResourceKind.COMPUTER,
        processing_minutes=COURSE_ENROLMENT_MINUTES,
        description=(
            "The student enters course selections on a registration computer "
            "and writes them to the student information system."
        ),
    ),
    ActivitySpec(
        activity_id=ActivityId.FEE_ASSESSMENT,
        label="Fee assessment",
        short_label="Fees",
        resource_kind=ResourceKind.OFFICER,
        processing_minutes=FEE_ASSESSMENT_MINUTES,
        description=(
            "An officer calculates tuition, applies a recorded waiver or "
            "scholarship, and confirms the payment entry."
        ),
    ),
    ActivitySpec(
        activity_id=ActivityId.CARD_ISSUE,
        label="Card and timetable",
        short_label="Card",
        resource_kind=ResourceKind.COMPUTER,
        processing_minutes=CARD_ISSUE_MINUTES,
        description=(
            "A registration computer prints the timetable and encodes the "
            "student card."
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
