"""Plain-language reading of a completed resource study."""

from registration_sim.constants import (
    CLOSE_SCORE_GAP,
    EMPTY_COUNT,
    FIRST_INDEX,
    INDEX_STEP,
    PERCENT_SCALE,
    ZERO_MINUTES,
    ScenarioId,
)
from registration_sim.experiments import recommendation_key
from registration_sim.model import ScenarioRun


def find_run(runs: tuple[ScenarioRun, ...] | list[ScenarioRun], scenario_id: ScenarioId) -> ScenarioRun:
    for run in runs:
        if run.scenario.scenario_id == scenario_id:
            return run
    raise KeyError(scenario_id)


def _percent(ratio: float) -> str:
    return f"{ratio * PERCENT_SCALE:.1f}%"


def _makespan_change(resource_name: str, from_count: int, to_count: int, before: int, after: int) -> str:
    delta = after - before
    if delta == ZERO_MINUTES:
        return (
            f"Raising the number of {resource_name} from {from_count} to {to_count} "
            f"leaves the makespan at {after} minutes."
        )
    if delta < ZERO_MINUTES:
        saved = -delta
        return (
            f"Raising the number of {resource_name} from {from_count} to {to_count} "
            f"shortens the makespan by {saved} minutes, from {before} to {after}."
        )
    return (
        f"Raising the number of {resource_name} from {from_count} to {to_count} "
        f"lengthens the makespan by {delta} minutes, from {before} to {after}."
    )


def _bottleneck_sentence(run: ScenarioRun) -> str:
    metrics = run.metrics
    officer_text = _percent(metrics.officer_utilisation)
    computer_text = _percent(metrics.computer_utilisation)
    if metrics.computer_utilisation > metrics.officer_utilisation:
        scarce = "computer"
        busy = computer_text
        slack = officer_text
        slack_name = "officers"
    elif metrics.officer_utilisation > metrics.computer_utilisation:
        scarce = "officer"
        busy = officer_text
        slack = computer_text
        slack_name = "computers"
    else:
        return (
            f"In the baseline hall, officers and computers are equally busy "
            f"at {officer_text} utilisation."
        )
    return (
        f"In the baseline hall the scarce resource is the {scarce} pool, "
        f"busy for {busy} of the makespan, while {slack_name} sit at {slack}."
    )


def study_paragraphs(runs: tuple[ScenarioRun, ...] | list[ScenarioRun], recommended: ScenarioRun) -> tuple[str, ...]:
    baseline = find_run(runs, ScenarioId.BASELINE)
    if baseline.result.config.student_count == EMPTY_COUNT:
        return (
            "The cohort is empty, so the hall has no registration work to compare.",
        )
    more_officers = find_run(runs, ScenarioId.MORE_OFFICERS)
    lean = find_run(runs, ScenarioId.LEAN)
    more_computers = find_run(runs, ScenarioId.MORE_COMPUTERS)
    base_metrics = baseline.metrics
    cohort = baseline.result.config.student_count
    session = baseline.result.config.working_period_minutes
    recommended_metrics = recommended.metrics

    opening = (
        f"The hall registers a fixed cohort of {cohort} students. "
        f"Each student needs {base_metrics.total_processing_minutes // cohort} minutes of "
        f"processing, split across shared officers and shared computers. "
        f"The session lasts {session} minutes. "
        f"With the baseline allocation the last student finishes at "
        f"{base_metrics.makespan_minutes} minutes, "
        f"{base_metrics.students_finished_within_period} of {cohort} students finish "
        f"inside the session, and overtime is {base_metrics.overtime_minutes} minutes."
    )
    officer_effect = _makespan_change(
        "registration officers",
        baseline.scenario.officer_count,
        more_officers.scenario.officer_count,
        base_metrics.makespan_minutes,
        more_officers.metrics.makespan_minutes,
    )
    officer_service = (
        f"Students finished inside the session move from "
        f"{base_metrics.students_finished_within_period} to "
        f"{more_officers.metrics.students_finished_within_period} "
        f"when only the officer pool grows. "
        f"Officer utilisation moves from {_percent(base_metrics.officer_utilisation)} "
        f"to {_percent(more_officers.metrics.officer_utilisation)}, and computer "
        f"utilisation moves from {_percent(base_metrics.computer_utilisation)} "
        f"to {_percent(more_officers.metrics.computer_utilisation)}."
    )
    computer_effect = _makespan_change(
        "registration computers",
        baseline.scenario.computer_count,
        lean.scenario.computer_count,
        base_metrics.makespan_minutes,
        lean.metrics.makespan_minutes,
    )
    computer_service = (
        f"Students finished inside the session move from "
        f"{base_metrics.students_finished_within_period} to "
        f"{lean.metrics.students_finished_within_period} "
        f"when the computer pool grows from {baseline.scenario.computer_count} "
        f"to {lean.scenario.computer_count}. "
        f"Average waiting time moves from {base_metrics.average_waiting_minutes:.1f} "
        f"minutes to {lean.metrics.average_waiting_minutes:.1f} minutes."
    )
    further_computers = _makespan_change(
        "registration computers",
        lean.scenario.computer_count,
        more_computers.scenario.computer_count,
        lean.metrics.makespan_minutes,
        more_computers.metrics.makespan_minutes,
    )
    recommendation = (
        f"The most efficient allocation in this study is {recommended.scenario.name} "
        f"({recommended.scenario.officer_count} officers and "
        f"{recommended.scenario.computer_count} computers). "
        f"It finishes {recommended_metrics.students_finished_within_period} of {cohort} "
        f"students inside the session, with a makespan of "
        f"{recommended_metrics.makespan_minutes} minutes, overall resource utilisation "
        f"of {_percent(recommended_metrics.overall_utilisation)}, and "
        f"{recommended_metrics.overall_idle_minutes} idle resource-minutes. "
        f"The efficiency score, completion ratio times overall utilisation, is "
        f"{recommended_metrics.efficiency_score:.3f}. "
        f"Schedule efficiency against the lower bound is "
        f"{_percent(recommended_metrics.schedule_efficiency)}."
    )
    rule = (
        "The ranking finishes the largest number of students before the session "
        "closes, then keeps the highest overall utilisation, so a larger pool is "
        "chosen only when the extra officers or computers still earn their time. "
        "Service efficiency is processing time divided by processing plus waiting. "
        "It rises when queues shrink, and it can look strong for a generously "
        "staffed hall whose resources then spend more of the makespan idle."
    )
    return (
        opening,
        _bottleneck_sentence(baseline),
        officer_effect,
        officer_service,
        computer_effect,
        computer_service,
        further_computers,
        _runner_up_paragraph(runs, recommended),
        recommendation,
        rule,
    )


def _runner_up_paragraph(runs: tuple[ScenarioRun, ...] | list[ScenarioRun], recommended: ScenarioRun) -> str:
    ordered = sorted(runs, key=recommendation_key, reverse=True)
    if len(ordered) <= INDEX_STEP:
        return "This study has a single allocation to compare."
    runner = ordered[FIRST_INDEX + INDEX_STEP]
    gap = abs(recommended.metrics.efficiency_score - runner.metrics.efficiency_score)
    if gap > CLOSE_SCORE_GAP:
        return (
            f"The next allocation on the efficiency score is {runner.scenario.name} "
            f"at {runner.metrics.efficiency_score:.3f}."
        )
    return (
        f"{runner.scenario.name} sits close on the efficiency score "
        f"({runner.metrics.efficiency_score:.3f} against {recommended.metrics.efficiency_score:.3f}). "
        f"It staffs {runner.scenario.officer_count} officers and {runner.scenario.computer_count} computers, "
        f"finishes at {runner.metrics.makespan_minutes} minutes, and holds average waiting to "
        f"{runner.metrics.average_waiting_minutes:.1f} minutes, compared with "
        f"{recommended.metrics.average_waiting_minutes:.1f} minutes under {recommended.scenario.name}. "
        f"The leaner mix is the one to staff when officer-time and computer-time are the budget. "
        f"The nearby mix is the one to staff when shorter queues matter as well."
    )
