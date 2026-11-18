"""Discrete-event engine for a deterministic registration hall.

Students arrive on a fixed interval and walk the registry activities in order.
Each activity seizes the lowest-numbered free unit of its resource and
holds that unit, without interruption, for a known processing time.

A student who finishes one activity becomes ready for the next at once,
so later students can use an officer while an earlier student is on a
computer. When several students are waiting, the one who has waited
longest starts first.
"""

import heapq
from collections import deque

from registration_sim.activities import ACTIVITY_SEQUENCE
from registration_sim.constants import (
    EMPTY_COUNT,
    FIRST_INDEX,
    INDEX_STEP,
    MIN_RESOURCE_UNITS,
    ZERO_MINUTES,
    EventKind,
    ResourceKind,
)
from registration_sim.model import (
    SimulationConfig,
    SimulationResult,
    StageAssignment,
    StudentRecord,
)


class ConfigurationError(ValueError):
    """The hall cannot be scheduled with the supplied counts."""


def validate_config(config: SimulationConfig) -> None:
    if config.student_count < EMPTY_COUNT:
        raise ConfigurationError("Student count cannot be negative.")
    if config.interarrival_minutes < ZERO_MINUTES:
        raise ConfigurationError("Interarrival time cannot be negative.")
    if config.officer_count < MIN_RESOURCE_UNITS:
        raise ConfigurationError("The desk needs at least one registry officer.")
    if config.computer_count < MIN_RESOURCE_UNITS:
        raise ConfigurationError("The desk needs at least one Student Portal computer.")
    if config.working_period_minutes < ZERO_MINUTES:
        raise ConfigurationError("The working period cannot be negative.")


def select_available_unit(free_at: list[int], now: int) -> int | None:
    """Lowest-numbered unit that is already free at `now`."""
    selected_index: int | None = None
    unit_index = FIRST_INDEX
    pool_size = len(free_at)
    while unit_index < pool_size:
        if free_at[unit_index] <= now and selected_index is None:
            selected_index = unit_index
        unit_index += INDEX_STEP
    return selected_index


def simulate(config: SimulationConfig) -> SimulationResult:
    validate_config(config)
    free_at: dict[ResourceKind, list[int]] = {
        ResourceKind.OFFICER: [ZERO_MINUTES] * config.officer_count,
        ResourceKind.COMPUTER: [ZERO_MINUTES] * config.computer_count,
    }
    waiting: dict[ResourceKind, deque[int]] = {
        ResourceKind.OFFICER: deque(),
        ResourceKind.COMPUTER: deque(),
    }
    stage_index = [FIRST_INDEX] * config.student_count
    ready_at = [ZERO_MINUTES] * config.student_count
    completion_at = [ZERO_MINUTES] * config.student_count
    assignments: list[StageAssignment] = []
    events: list[tuple[int, int, int, int, str]] = []
    sequence = FIRST_INDEX

    def push(moment: int, kind: EventKind, student_index: int, resource_kind: str) -> None:
        nonlocal sequence
        heapq.heappush(events, (moment, int(kind), student_index, sequence, resource_kind))
        sequence += INDEX_STEP

    def begin_stage(student_index: int, unit_index: int, start_minutes: int) -> None:
        activity = ACTIVITY_SEQUENCE[stage_index[student_index]]
        end_minutes = start_minutes + activity.processing_minutes
        free_at[activity.resource_kind][unit_index] = end_minutes
        assignments.append(
            StageAssignment(
                student_index=student_index,
                activity_id=activity.activity_id,
                resource_kind=activity.resource_kind,
                resource_index=unit_index,
                ready_minutes=ready_at[student_index],
                start_minutes=start_minutes,
                end_minutes=end_minutes,
            )
        )
        stage_index[student_index] += INDEX_STEP
        if stage_index[student_index] < len(ACTIVITY_SEQUENCE):
            push(end_minutes, EventKind.STUDENT_READY, student_index, "")
        else:
            completion_at[student_index] = end_minutes
        push(end_minutes, EventKind.RESOURCE_RELEASE, student_index, activity.resource_kind.value)

    def start_or_queue(student_index: int, moment: int) -> None:
        ready_at[student_index] = moment
        activity = ACTIVITY_SEQUENCE[stage_index[student_index]]
        unit_index = select_available_unit(free_at[activity.resource_kind], moment)
        if unit_index is None:
            waiting[activity.resource_kind].append(student_index)
            return
        begin_stage(student_index, unit_index, moment)

    def serve_queue(resource_kind: ResourceKind, moment: int) -> None:
        queue = waiting[resource_kind]
        if len(queue) == EMPTY_COUNT:
            return
        student_index = queue.popleft()
        unit_index = select_available_unit(free_at[resource_kind], moment)
        if unit_index is None:
            queue.appendleft(student_index)
            return
        begin_stage(student_index, unit_index, moment)

    for student_index in range(config.student_count):
        push(
            student_index * config.interarrival_minutes,
            EventKind.STUDENT_READY,
            student_index,
            "",
        )

    while len(events) > EMPTY_COUNT:
        moment, kind_value, student_index, _sequence, resource_value = heapq.heappop(events)
        if kind_value == int(EventKind.RESOURCE_RELEASE):
            serve_queue(ResourceKind(resource_value), moment)
        else:
            start_or_queue(student_index, moment)

    students = _student_records(config, assignments, completion_at)
    makespan_minutes = ZERO_MINUTES
    for student in students:
        if student.completion_minutes > makespan_minutes:
            makespan_minutes = student.completion_minutes
    return SimulationResult(
        config=config,
        students=tuple(students),
        assignments=tuple(assignments),
        makespan_minutes=makespan_minutes,
    )


def _student_records(
    config: SimulationConfig,
    assignments: list[StageAssignment],
    completion_at: list[int],
) -> list[StudentRecord]:
    grouped: list[list[StageAssignment]] = [[] for _student in range(config.student_count)]
    for assignment in assignments:
        grouped[assignment.student_index].append(assignment)

    students: list[StudentRecord] = []
    for student_index, stages in enumerate(grouped):
        arrival_minutes = student_index * config.interarrival_minutes
        waiting_minutes = ZERO_MINUTES
        for stage in stages:
            waiting_minutes += stage.waiting_minutes
        completion_minutes = completion_at[student_index]
        students.append(
            StudentRecord(
                student_index=student_index,
                arrival_minutes=arrival_minutes,
                completion_minutes=completion_minutes,
                waiting_minutes=waiting_minutes,
                flow_minutes=completion_minutes - arrival_minutes,
                stages=tuple(stages),
            )
        )
    return students
