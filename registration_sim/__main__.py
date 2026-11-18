"""Command-line report for the registration-centre simulation.

Examples
--------
python -m registration_sim
python -m registration_sim --students 40 --officers 3 --computers 4
python -m registration_sim --charts output/figures
"""

import argparse
import csv
import json
from pathlib import Path

from registration_sim.activities import processing_minutes_for, total_processing_minutes
from registration_sim.charts import save_study_charts
from registration_sim.constants import (
    COMPARISON_CSV,
    DEFAULT_COMPUTER_COUNT,
    DEFAULT_INTERARRIVAL_MINUTES,
    DEFAULT_OFFICER_COUNT,
    DEFAULT_STUDENT_COUNT,
    DEFAULT_WORKING_PERIOD_MINUTES,
    ResourceKind,
)
from registration_sim.engine import simulate
from registration_sim.experiments import (
    default_config,
    recommend,
    run_sensitivity,
    run_study,
)
from registration_sim.metrics import measure
from registration_sim.model import SimulationConfig
from registration_sim.narrative import study_paragraphs
from registration_sim.serialize import run_payload
from registration_sim.tables import (
    COMPARISON_HEADERS,
    activity_table,
    comparison_rows,
    comparison_table,
    resource_table,
    stage_table,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Deterministic simulation of North Hall student registration.",
    )
    parser.add_argument("--students", type=int, default=DEFAULT_STUDENT_COUNT)
    parser.add_argument("--interarrival", type=int, default=DEFAULT_INTERARRIVAL_MINUTES)
    parser.add_argument("--officers", type=int, default=DEFAULT_OFFICER_COUNT)
    parser.add_argument("--computers", type=int, default=DEFAULT_COMPUTER_COUNT)
    parser.add_argument("--session", type=int, default=DEFAULT_WORKING_PERIOD_MINUTES)
    parser.add_argument(
        "--charts",
        type=Path,
        default=None,
        help="Directory for PNG figures and the comparison CSV.",
    )
    parser.add_argument(
        "--export-parity",
        type=Path,
        default=None,
        help="Write a JSON fixture the web lab uses to check its engine.",
    )
    return parser


def config_from_args(args: argparse.Namespace) -> SimulationConfig:
    return SimulationConfig(
        student_count=args.students,
        interarrival_minutes=args.interarrival,
        officer_count=args.officers,
        computer_count=args.computers,
        working_period_minutes=args.session,
    )


def export_parity(path: Path) -> None:
    """Small hand cases plus the default study, including the full trace."""
    cases = [
        SimulationConfig(1, 0, 1, 1, 240),
        SimulationConfig(2, 0, 1, 1, 240),
        SimulationConfig(3, 100, 1, 1, 240),
        default_config(),
    ]
    payloads: list[dict[str, object]] = []
    for config in cases:
        result = simulate(config)
        from registration_sim.experiments import Scenario
        from registration_sim.constants import ScenarioId

        scenario = Scenario(
            scenario_id=ScenarioId.BASELINE,
            name="parity",
            short_label="parity",
            summary="parity",
            officer_count=config.officer_count,
            computer_count=config.computer_count,
        )
        from registration_sim.model import ScenarioRun

        run = ScenarioRun(scenario=scenario, result=result, metrics=measure(result))
        payloads.append(run_payload(run, include_assignments=True))

    study = run_study(default_config())
    for run in study:
        payloads.append(run_payload(run, include_assignments=True))

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payloads, indent=2), encoding="utf-8")


def write_csv(path: Path, runs: tuple) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(COMPARISON_HEADERS)
        writer.writerows(comparison_rows(runs))


def main() -> None:
    args = build_parser().parse_args()
    if args.export_parity is not None:
        export_parity(args.export_parity)
        print(f"Wrote {args.export_parity}")
        return

    config = config_from_args(args)
    single = simulate(config)
    single_metrics = measure(single)
    study = run_study(config)
    recommended = recommend(study)

    officer_work = processing_minutes_for(ResourceKind.OFFICER)
    computer_work = processing_minutes_for(ResourceKind.COMPUTER)
    print("North Hall registration — deterministic simulation")
    print(
        f"Each student: {total_processing_minutes()} minutes "
        f"({officer_work} with an officer, {computer_work} on a computer)."
    )
    print()
    print("Activities")
    print(activity_table())
    print()
    print(
        f"Single run: {config.student_count} students, "
        f"every {config.interarrival_minutes} min, "
        f"{config.officer_count} officers, {config.computer_count} computers, "
        f"session {config.working_period_minutes} min."
    )
    print(f"Makespan: {single_metrics.makespan_minutes} min")
    print(
        f"Finished in session: {single_metrics.students_finished_within_period}"
        f" / {single_metrics.students_processed}"
    )
    print(f"Overtime: {single_metrics.overtime_minutes} min")
    print(f"Total waiting: {single_metrics.total_waiting_minutes} min")
    print(f"Idle resource-minutes: {single_metrics.overall_idle_minutes}")
    print()
    print("Resources")
    print(resource_table(single_metrics))
    print()
    print("Stages")
    print(stage_table(single_metrics))
    print()
    print("Resource-allocation experiments")
    print(comparison_table(study))
    print()
    print(f"Recommended allocation: {recommended.scenario.name}")
    print()
    for paragraph in study_paragraphs(study, recommended):
        print(paragraph)
        print()

    if args.charts is not None:
        sensitivity = run_sensitivity(config)
        figures = save_study_charts(study, sensitivity, args.charts)
        csv_path = args.charts / COMPARISON_CSV
        write_csv(csv_path, study)
        for figure in figures:
            print(f"Wrote {figure}")
        print(f"Wrote {csv_path}")


if __name__ == "__main__":
    main()
