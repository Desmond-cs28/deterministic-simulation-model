"""Plain-language reading of the three Palm registry experiments."""

from registration_sim.constants import (
    EMPTY_COUNT,
    MIN_RESOURCE_UNITS,
    PERCENT_SCALE,
    ZERO_MINUTES,
    ScenarioId,
)
from registration_sim.model import ScenarioRun


def find_run(runs: tuple[ScenarioRun, ...] | list[ScenarioRun], scenario_id: ScenarioId) -> ScenarioRun:
    for run in runs:
        if run.scenario.scenario_id == scenario_id:
            return run
    raise KeyError(scenario_id)


def _count_label(count: int, singular: str, plural: str) -> str:
    word = singular if count == MIN_RESOURCE_UNITS else plural
    return f"{count} {word}"


def _percent(ratio: float) -> str:
    return f"{ratio * PERCENT_SCALE:.1f}%"


def _makespan_change(resource_name: str, from_count: int, to_count: int, before: int, after: int) -> str:
    delta = after - before
    if delta == ZERO_MINUTES:
        return (
            f"Adding a {resource_name} (from {from_count} to {to_count}) "
            f"leaves the finish time at {after} minutes."
        )
    if delta < ZERO_MINUTES:
        saved = -delta
        return (
            f"Adding a {resource_name} (from {from_count} to {to_count}) "
            f"brings the finish time forward by {saved} minutes, from {before} to {after}."
        )
    return (
        f"Adding a {resource_name} (from {from_count} to {to_count}) "
        f"pushes the finish time out by {delta} minutes, from {before} to {after}."
    )


def study_paragraphs(runs: tuple[ScenarioRun, ...] | list[ScenarioRun], recommended: ScenarioRun) -> tuple[str, ...]:
    baseline = find_run(runs, ScenarioId.BASELINE)
    if baseline.result.config.student_count == EMPTY_COUNT:
        return ("No students arrive, so the registry desk has nothing to compare.",)
    more_officers = find_run(runs, ScenarioId.MORE_OFFICERS)
    more_computers = find_run(runs, ScenarioId.MORE_COMPUTERS)
    base = baseline.metrics
    cohort = baseline.result.config.student_count
    session = baseline.result.config.working_period_minutes
    chosen = recommended.metrics
    opening = (
        f"Palm University College registers {cohort} undergraduates on this morning "
        f"of course-registration week. Each student spends "
        f"{base.total_processing_minutes // cohort} minutes at the desk: "
        f"a registry check, course registration on the Student Portal, and a timetable. "
        f"The desk is open for {session} minutes from 08:00. "
        f"With {_count_label(baseline.scenario.officer_count, 'officer', 'officers')} and "
        f"{_count_label(baseline.scenario.computer_count, 'computer', 'computers')} the last student leaves at "
        f"{base.makespan_minutes} minutes, "
        f"{base.students_finished_within_period} of {cohort} finish before the desk closes, "
        f"and overtime is {base.overtime_minutes} minutes."
    )
    bottleneck = (
        f"On the current desk the portal computer is busy for {_percent(base.computer_utilisation)} "
        f"of the morning and the officer is busy for {_percent(base.officer_utilisation)}. "
        f"Students wait {base.average_waiting_minutes:.1f} minutes on average."
    )
    officer_effect = _makespan_change(
        "registry officer",
        baseline.scenario.officer_count,
        more_officers.scenario.officer_count,
        base.makespan_minutes,
        more_officers.metrics.makespan_minutes,
    )
    officer_use = (
        f"Students finished before the desk closes move from {base.students_finished_within_period} "
        f"to {more_officers.metrics.students_finished_within_period}. "
        f"Officer utilisation moves from {_percent(base.officer_utilisation)} "
        f"to {_percent(more_officers.metrics.officer_utilisation)}."
    )
    computer_effect = _makespan_change(
        "portal computer",
        baseline.scenario.computer_count,
        more_computers.scenario.computer_count,
        base.makespan_minutes,
        more_computers.metrics.makespan_minutes,
    )
    computer_use = (
        f"Students finished before the desk closes move from {base.students_finished_within_period} "
        f"to {more_computers.metrics.students_finished_within_period}. "
        f"Average waiting moves from {base.average_waiting_minutes:.1f} minutes "
        f"to {more_computers.metrics.average_waiting_minutes:.1f} minutes."
    )
    recommendation = (
        f"The most efficient allocation is {recommended.scenario.name}: "
        f"{_count_label(recommended.scenario.officer_count, 'officer', 'officers')} and "
        f"{_count_label(recommended.scenario.computer_count, 'computer', 'computers')}. "
        f"It finishes {chosen.students_finished_within_period} of {cohort} students "
        f"before the desk closes, in {chosen.makespan_minutes} minutes, "
        f"with overall utilisation {_percent(chosen.overall_utilisation)} "
        f"and {chosen.overall_idle_minutes} idle resource-minutes."
    )
    return (opening, bottleneck, officer_effect, officer_use, computer_effect, computer_use, recommendation)
