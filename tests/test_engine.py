"""Hand-checked cases and structural properties of the deterministic model."""

from registration_sim.activities import processing_minutes_for, total_processing_minutes
from registration_sim.constants import (
    CARD_ISSUE_MINUTES,
    COURSE_ENROLMENT_MINUTES,
    DOCUMENT_VERIFICATION_MINUTES,
    EMPTY_COUNT,
    FEE_ASSESSMENT_MINUTES,
    FIRST_INDEX,
    FULL_RATIO,
    ZERO_MINUTES,
    ActivityId,
    ResourceKind,
    ScenarioId,
)
from registration_sim.engine import ConfigurationError, simulate
from registration_sim.experiments import default_config, recommend, run_study
from registration_sim.metrics import completion_lower_bound, measure
from registration_sim.model import SimulationConfig

ONE_STUDENT = 1
TWO_STUDENTS = 2
THREE_STUDENTS = 3
ONE_UNIT = 1
OPEN_ARRIVAL = 0
WIDE_GAP_MINUTES = 100
SESSION_MINUTES = 240
HAND_MAKESPAN_TWO = 35
HAND_WAIT_FIRST = 5
HAND_WAIT_SECOND = 10
HAND_OFFICER_BUSY = 22
HAND_COMPUTER_BUSY = 28
HAND_LOWER_BOUND = 28
CHAIN_MINUTES = (
    DOCUMENT_VERIFICATION_MINUTES
    + COURSE_ENROLMENT_MINUTES
    + FEE_ASSESSMENT_MINUTES
    + CARD_ISSUE_MINUTES
)


def _config(students: int, interarrival: int, officers: int, computers: int) -> SimulationConfig:
    return SimulationConfig(
        student_count=students,
        interarrival_minutes=interarrival,
        officer_count=officers,
        computer_count=computers,
        working_period_minutes=SESSION_MINUTES,
    )


def test_single_student_has_no_wait_and_known_finish() -> None:
    result = simulate(_config(ONE_STUDENT, OPEN_ARRIVAL, ONE_UNIT, ONE_UNIT))
    student = result.students[FIRST_INDEX]
    assert result.makespan_minutes == CHAIN_MINUTES
    assert student.waiting_minutes == ZERO_MINUTES
    assert student.completion_minutes == CHAIN_MINUTES
    ends = [stage.end_minutes for stage in student.stages]
    assert ends == [
        DOCUMENT_VERIFICATION_MINUTES,
        DOCUMENT_VERIFICATION_MINUTES + COURSE_ENROLMENT_MINUTES,
        DOCUMENT_VERIFICATION_MINUTES + COURSE_ENROLMENT_MINUTES + FEE_ASSESSMENT_MINUTES,
        CHAIN_MINUTES,
    ]
    assert [stage.activity_id for stage in student.stages] == [
        ActivityId.DOCUMENT_VERIFICATION,
        ActivityId.COURSE_ENROLMENT,
        ActivityId.FEE_ASSESSMENT,
        ActivityId.CARD_ISSUE,
    ]


def test_two_students_one_unit_each_match_the_hand_schedule() -> None:
    result = simulate(_config(TWO_STUDENTS, OPEN_ARRIVAL, ONE_UNIT, ONE_UNIT))
    metrics = measure(result)
    first, second = result.students
    assert result.makespan_minutes == HAND_MAKESPAN_TWO
    assert first.waiting_minutes == HAND_WAIT_FIRST
    assert second.waiting_minutes == HAND_WAIT_SECOND
    assert [stage.start_minutes for stage in first.stages] == [0, 6, 16, 26]
    assert [stage.start_minutes for stage in second.stages] == [6, 16, 26, 31]
    assert metrics.officer_busy_minutes == HAND_OFFICER_BUSY
    assert metrics.computer_busy_minutes == HAND_COMPUTER_BUSY
    assert metrics.officer_idle_minutes == HAND_MAKESPAN_TWO - HAND_OFFICER_BUSY
    assert metrics.computer_idle_minutes == HAND_MAKESPAN_TWO - HAND_COMPUTER_BUSY
    assert metrics.lower_bound_minutes == HAND_LOWER_BOUND
    assert metrics.students_processed == TWO_STUDENTS


def test_wide_arrival_gap_removes_waiting() -> None:
    result = simulate(_config(THREE_STUDENTS, WIDE_GAP_MINUTES, ONE_UNIT, ONE_UNIT))
    last_arrival = (THREE_STUDENTS - 1) * WIDE_GAP_MINUTES
    assert result.makespan_minutes == last_arrival + CHAIN_MINUTES
    for student in result.students:
        assert student.waiting_minutes == ZERO_MINUTES
        assert student.flow_minutes == CHAIN_MINUTES


def test_busy_time_depends_only_on_the_cohort() -> None:
    sparse = measure(simulate(_config(THREE_STUDENTS, WIDE_GAP_MINUTES, 4, 5)))
    tight = measure(simulate(_config(THREE_STUDENTS, OPEN_ARRIVAL, ONE_UNIT, ONE_UNIT)))
    expected_officer = THREE_STUDENTS * processing_minutes_for(ResourceKind.OFFICER)
    expected_computer = THREE_STUDENTS * processing_minutes_for(ResourceKind.COMPUTER)
    expected_total = THREE_STUDENTS * total_processing_minutes()
    assert sparse.officer_busy_minutes == expected_officer
    assert tight.officer_busy_minutes == expected_officer
    assert sparse.computer_busy_minutes == expected_computer
    assert tight.overall_busy_minutes == expected_total
    assert sparse.total_processing_minutes == expected_total


def test_extra_resources_never_lengthen_the_makespan() -> None:
    base = simulate(_config(12, 2, 2, 2)).makespan_minutes
    more_officers = simulate(_config(12, 2, 4, 2)).makespan_minutes
    more_computers = simulate(_config(12, 2, 2, 4)).makespan_minutes
    both = simulate(_config(12, 2, 4, 4)).makespan_minutes
    assert more_officers <= base
    assert more_computers <= base
    assert both <= more_officers
    assert both <= more_computers


def test_lower_bound_never_exceeds_makespan() -> None:
    students = 8
    while students <= 12:
        officers = 1
        while officers <= 4:
            computers = 1
            while computers <= 4:
                config = _config(students, 3, officers, computers)
                result = simulate(config)
                assert completion_lower_bound(config) <= result.makespan_minutes
                metrics = measure(result)
                assert metrics.officer_idle_minutes >= ZERO_MINUTES
                assert metrics.computer_idle_minutes >= ZERO_MINUTES
                assert metrics.overall_utilisation <= FULL_RATIO
                computers += 1
            officers += 1
        students += 2


def test_repeat_runs_match() -> None:
    config = default_config()
    first = simulate(config)
    second = simulate(config)
    assert first.assignments == second.assignments
    assert measure(first) == measure(second)


def test_empty_cohort_is_a_zero_schedule() -> None:
    result = simulate(_config(EMPTY_COUNT, 3, 2, 2))
    metrics = measure(result)
    assert result.makespan_minutes == ZERO_MINUTES
    assert metrics.students_processed == EMPTY_COUNT
    assert metrics.overall_utilisation == float(ZERO_MINUTES)
    assert metrics.efficiency_score == float(ZERO_MINUTES)


def test_missing_resource_is_rejected() -> None:
    try:
        simulate(_config(4, 3, EMPTY_COUNT, 2))
    except ConfigurationError:
        rejected = True
    else:
        rejected = False
    assert rejected


def test_default_study_finds_the_lean_mix_most_efficient() -> None:
    runs = run_study()
    chosen = recommend(runs)
    by_id = {run.scenario.scenario_id: run for run in runs}
    baseline = by_id[ScenarioId.BASELINE]
    more_officers = by_id[ScenarioId.MORE_OFFICERS]
    lean = by_id[ScenarioId.LEAN]
    more_computers = by_id[ScenarioId.MORE_COMPUTERS]
    balanced = by_id[ScenarioId.BALANCED]
    expanded = by_id[ScenarioId.EXPANDED]
    assert chosen.scenario.scenario_id == ScenarioId.LEAN
    assert more_officers.metrics.makespan_minutes == baseline.metrics.makespan_minutes
    assert lean.metrics.makespan_minutes < baseline.metrics.makespan_minutes
    assert more_computers.metrics.makespan_minutes == lean.metrics.makespan_minutes
    assert lean.metrics.students_finished_within_period == lean.metrics.students_processed
    assert balanced.metrics.students_finished_within_period == balanced.metrics.students_processed
    assert lean.metrics.efficiency_score > balanced.metrics.efficiency_score
    assert balanced.metrics.makespan_minutes < lean.metrics.makespan_minutes
    assert expanded.metrics.average_waiting_minutes < balanced.metrics.average_waiting_minutes


def test_default_study_recommends_a_member_and_ranks_by_the_rule() -> None:
    runs = run_study()
    chosen = recommend(runs)
    ids = {run.scenario.scenario_id for run in runs}
    assert chosen.scenario.scenario_id in ids
    assert ScenarioId.BASELINE in ids
    assert ScenarioId.MORE_OFFICERS in ids
    assert ScenarioId.MORE_COMPUTERS in ids
    for run in runs:
        if run.scenario.scenario_id == chosen.scenario.scenario_id:
            continue
        assert _rank(chosen) >= _rank(run)


def _rank(run):
    from registration_sim.experiments import recommendation_key

    return recommendation_key(run)


def test_tie_break_keeps_the_lowest_resource_index() -> None:
    result = simulate(_config(ONE_STUDENT, OPEN_ARRIVAL, 3, 3))
    for stage in result.students[FIRST_INDEX].stages:
        assert stage.resource_index == FIRST_INDEX
