"""Performance measures for one completed registration run."""

from math import ceil

from registration_sim.activities import (
    ACTIVITY_SEQUENCE,
    processing_minutes_for,
    total_processing_minutes,
)
from registration_sim.constants import (
    ARRIVAL_DELTA,
    DEPARTURE_DELTA,
    DISPLAY_INDEX_OFFSET,
    EMPTY_COUNT,
    FIRST_INDEX,
    FULL_RATIO,
    INDEX_STEP,
    MINUTES_PER_HOUR,
    ZERO_MINUTES,
    ResourceKind,
)
from registration_sim.model import (
    ResourceMetrics,
    SimulationConfig,
    SimulationMetrics,
    SimulationResult,
    StageMetrics,
)


def completion_lower_bound(config: SimulationConfig) -> int:
    """A relaxation bound on the time needed to finish the cohort.

    The bound keeps three facts that any feasible schedule must respect:
    the last student still needs a full pass through the activities, and
    the officer work (and, separately, the computer work) of every suffix
    of the arrival list cannot start before that suffix arrives.
    """
    if config.student_count == EMPTY_COUNT:
        return ZERO_MINUTES

    officer_each = processing_minutes_for(ResourceKind.OFFICER)
    computer_each = processing_minutes_for(ResourceKind.COMPUTER)
    chain = total_processing_minutes()
    last_student = config.student_count - INDEX_STEP
    bound = last_student * config.interarrival_minutes + chain

    student_cursor = FIRST_INDEX
    while student_cursor < config.student_count:
        remaining = config.student_count - student_cursor
        release = student_cursor * config.interarrival_minutes
        officer_bound = release + ceil(remaining * officer_each / config.officer_count)
        computer_bound = release + ceil(
            remaining * computer_each / config.computer_count
        )
        if officer_bound > bound:
            bound = officer_bound
        if computer_bound > bound:
            bound = computer_bound
        student_cursor += INDEX_STEP
    return bound


def _safe_ratio(numerator: float, denominator: float) -> float:
    if denominator == ZERO_MINUTES:
        return float(ZERO_MINUTES)
    return numerator / denominator


def _peak_students(result: SimulationResult) -> int:
    events: list[tuple[int, int]] = []
    for student in result.students:
        events.append((student.arrival_minutes, ARRIVAL_DELTA))
        events.append((student.completion_minutes, DEPARTURE_DELTA))
    events.sort()
    present = EMPTY_COUNT
    peak = EMPTY_COUNT
    for _moment, delta in events:
        present += delta
        if present > peak:
            peak = present
    return peak


def _resource_label(resource_kind: ResourceKind, resource_index: int) -> str:
    if resource_kind == ResourceKind.OFFICER:
        title = "Officer"
    else:
        title = "Computer"
    unit_number = resource_index + DISPLAY_INDEX_OFFSET
    return f"{title} {unit_number}"


def measure(result: SimulationResult) -> SimulationMetrics:
    config = result.config
    chain = total_processing_minutes()
    officer_each = processing_minutes_for(ResourceKind.OFFICER)
    computer_each = processing_minutes_for(ResourceKind.COMPUTER)
    students_processed = len(result.students)
    total_processing = students_processed * chain
    officer_busy = students_processed * officer_each
    computer_busy = students_processed * computer_each

    total_waiting = ZERO_MINUTES
    max_flow = ZERO_MINUTES
    finished_within = EMPTY_COUNT
    for student in result.students:
        total_waiting += student.waiting_minutes
        if student.flow_minutes > max_flow:
            max_flow = student.flow_minutes
        if student.completion_minutes <= config.working_period_minutes:
            finished_within += INDEX_STEP

    makespan = result.makespan_minutes
    lower_bound = completion_lower_bound(config)
    resource_count = config.officer_count + config.computer_count
    officer_available = config.officer_count * makespan
    computer_available = config.computer_count * makespan
    overall_available = resource_count * makespan
    officer_idle = officer_available - officer_busy
    computer_idle = computer_available - computer_busy
    overall_idle = overall_available - total_processing
    overtime = ZERO_MINUTES
    if makespan > config.working_period_minutes:
        overtime = makespan - config.working_period_minutes

    unfinished = students_processed - finished_within
    completion_ratio = _safe_ratio(finished_within, students_processed)
    overall_utilisation = _safe_ratio(total_processing, overall_available)
    productivity = _safe_ratio(
        students_processed * MINUTES_PER_HOUR,
        resource_count * makespan,
    )

    resources = _resource_rows(result, makespan)
    stages = _stage_rows(result, students_processed)

    return SimulationMetrics(
        makespan_minutes=makespan,
        lower_bound_minutes=lower_bound,
        schedule_efficiency=_safe_ratio(lower_bound, makespan),
        students_processed=students_processed,
        students_finished_within_period=finished_within,
        students_unfinished_within_period=unfinished,
        overtime_minutes=overtime,
        total_processing_minutes=total_processing,
        total_waiting_minutes=total_waiting,
        average_waiting_minutes=_safe_ratio(total_waiting, students_processed),
        average_flow_minutes=_safe_ratio(
            sum(student.flow_minutes for student in result.students),
            students_processed,
        ),
        max_flow_minutes=max_flow,
        average_students_waiting=_safe_ratio(total_waiting, makespan),
        peak_students_in_system=_peak_students(result),
        service_efficiency=_safe_ratio(total_processing, total_processing + total_waiting),
        officer_busy_minutes=officer_busy,
        officer_idle_minutes=officer_idle,
        officer_utilisation=_safe_ratio(officer_busy, officer_available),
        computer_busy_minutes=computer_busy,
        computer_idle_minutes=computer_idle,
        computer_utilisation=_safe_ratio(computer_busy, computer_available),
        overall_busy_minutes=total_processing,
        overall_idle_minutes=overall_idle,
        overall_utilisation=overall_utilisation,
        resource_count=resource_count,
        productivity_per_resource_hour=productivity,
        completion_ratio=completion_ratio,
        efficiency_score=completion_ratio * overall_utilisation,
        resources=tuple(resources),
        stages=tuple(stages),
    )


def _resource_rows(result: SimulationResult, makespan: int) -> list[ResourceMetrics]:
    config = result.config
    rows: list[ResourceMetrics] = []
    for resource_kind, unit_count in (
        (ResourceKind.OFFICER, config.officer_count),
        (ResourceKind.COMPUTER, config.computer_count),
    ):
        unit_index = FIRST_INDEX
        while unit_index < unit_count:
            busy = ZERO_MINUTES
            for assignment in result.assignments:
                same_kind = assignment.resource_kind == resource_kind
                same_unit = assignment.resource_index == unit_index
                if same_kind and same_unit:
                    busy += assignment.processing_minutes
            idle = makespan - busy
            rows.append(
                ResourceMetrics(
                    resource_kind=resource_kind,
                    resource_index=unit_index,
                    resource_label=_resource_label(resource_kind, unit_index),
                    busy_minutes=busy,
                    idle_minutes=idle,
                    utilisation=_safe_ratio(busy, makespan),
                )
            )
            unit_index += INDEX_STEP
    return rows


def _stage_rows(result: SimulationResult, students_processed: int) -> list[StageMetrics]:
    rows: list[StageMetrics] = []
    for activity in ACTIVITY_SEQUENCE:
        total_wait = ZERO_MINUTES
        max_wait = ZERO_MINUTES
        for assignment in result.assignments:
            if assignment.activity_id != activity.activity_id:
                continue
            wait = assignment.waiting_minutes
            total_wait += wait
            if wait > max_wait:
                max_wait = wait
        rows.append(
            StageMetrics(
                activity_id=activity.activity_id,
                label=activity.label,
                resource_kind=activity.resource_kind,
                processing_minutes=activity.processing_minutes,
                average_wait_minutes=_safe_ratio(total_wait, students_processed),
                max_wait_minutes=max_wait,
                total_wait_minutes=total_wait,
            )
        )
    return rows


def full_ratio() -> float:
    """Exposed so callers can name a completed ratio without a literal."""
    return FULL_RATIO
