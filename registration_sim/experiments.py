"""The resource-allocation experiments required by the project."""

from dataclasses import replace

from registration_sim.constants import (
    BASELINE_COMPUTER_COUNT,
    BASELINE_OFFICER_COUNT,
    DEFAULT_COMPUTER_COUNT,
    DEFAULT_INTERARRIVAL_MINUTES,
    DEFAULT_OFFICER_COUNT,
    DEFAULT_STUDENT_COUNT,
    DEFAULT_WORKING_PERIOD_MINUTES,
    INDEX_STEP,
    MORE_COMPUTERS_COMPUTER_COUNT,
    MORE_COMPUTERS_OFFICER_COUNT,
    MORE_OFFICERS_COMPUTER_COUNT,
    MORE_OFFICERS_OFFICER_COUNT,
    PARITY_ROUND_DIGITS,
    SENSITIVITY_MAX_UNITS,
    SENSITIVITY_MIN_UNITS,
    ScenarioId,
)
from registration_sim.engine import simulate
from registration_sim.metrics import measure
from registration_sim.model import Scenario, ScenarioRun, SimulationConfig


def default_config() -> SimulationConfig:
    return SimulationConfig(
        student_count=DEFAULT_STUDENT_COUNT,
        interarrival_minutes=DEFAULT_INTERARRIVAL_MINUTES,
        officer_count=DEFAULT_OFFICER_COUNT,
        computer_count=DEFAULT_COMPUTER_COUNT,
        working_period_minutes=DEFAULT_WORKING_PERIOD_MINUTES,
    )


def study_scenarios() -> tuple[Scenario, ...]:
    """Three allocations for one morning at the Palm registry desk.

    The current desk, a second officer, and a second portal computer.
    """
    return (
        Scenario(
            scenario_id=ScenarioId.BASELINE,
            name="Current desk",
            short_label="Desk 1+1",
            summary="One registry officer and one Student Portal computer.",
            officer_count=BASELINE_OFFICER_COUNT,
            computer_count=BASELINE_COMPUTER_COUNT,
        ),
        Scenario(
            scenario_id=ScenarioId.MORE_OFFICERS,
            name="Second officer",
            short_label="Officers 2+1",
            summary="Two registry officers, still with one portal computer.",
            officer_count=MORE_OFFICERS_OFFICER_COUNT,
            computer_count=MORE_OFFICERS_COMPUTER_COUNT,
        ),
        Scenario(
            scenario_id=ScenarioId.MORE_COMPUTERS,
            name="Second computer",
            short_label="Computers 1+2",
            summary="One registry officer, with a second Student Portal computer.",
            officer_count=MORE_COMPUTERS_OFFICER_COUNT,
            computer_count=MORE_COMPUTERS_COMPUTER_COUNT,
        ),
    )


def config_for_scenario(base: SimulationConfig, scenario: Scenario) -> SimulationConfig:
    return replace(
        base,
        officer_count=scenario.officer_count,
        computer_count=scenario.computer_count,
    )


def run_scenario(base: SimulationConfig, scenario: Scenario) -> ScenarioRun:
    result = simulate(config_for_scenario(base, scenario))
    return ScenarioRun(scenario=scenario, result=result, metrics=measure(result))


def run_study(base: SimulationConfig | None = None) -> tuple[ScenarioRun, ...]:
    config = default_config() if base is None else base
    return tuple(run_scenario(config, scenario) for scenario in study_scenarios())


def recommendation_key(run: ScenarioRun) -> tuple[float, float, int, int]:
    """Rank allocations for a fixed morning session.

    Finish as many students as possible before the session closes.
    Among those service levels, prefer the allocation that keeps
    resources busy (less officer-time and computer-time per cohort).
    Equal utilisation then prefers the smaller pool, then the shorter day.
    """
    metrics = run.metrics
    return (
        float(metrics.students_finished_within_period),
        round(metrics.overall_utilisation, PARITY_ROUND_DIGITS),
        -metrics.resource_count,
        -metrics.makespan_minutes,
    )


def recommend(runs: tuple[ScenarioRun, ...] | list[ScenarioRun]) -> ScenarioRun:
    ordered = sorted(runs, key=recommendation_key, reverse=True)
    return ordered[FIRST_RUN_INDEX]


FIRST_RUN_INDEX = 0


def sensitivity_levels() -> range:
    return range(SENSITIVITY_MIN_UNITS, SENSITIVITY_MAX_UNITS + INDEX_STEP)


def run_sensitivity(base: SimulationConfig) -> tuple[ScenarioRun, ...]:
    """One run for every officer/computer pair in the study range."""
    runs: list[ScenarioRun] = []
    for officer_count in sensitivity_levels():
        for computer_count in sensitivity_levels():
            scenario = Scenario(
                scenario_id=ScenarioId.BASELINE,
                name=f"{officer_count} officers, {computer_count} computers",
                short_label=f"{officer_count}+{computer_count}",
                summary="Sensitivity cell",
                officer_count=officer_count,
                computer_count=computer_count,
            )
            runs.append(run_scenario(base, scenario))
    return tuple(runs)
