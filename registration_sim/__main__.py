"""Command-line report for the registration-centre simulation.

Examples
--------
python registration.py
python registration.py --students 20 --officers 1 --computers 2
"""

import argparse
import csv
from pathlib import Path

from registration_sim.activities import processing_minutes_for, total_processing_minutes
from registration_sim.charts import save_study_charts
from registration_sim.constants import (
    COMPARISON_CSV,
    DEFAULT_COMPUTER_COUNT,
    DEFAULT_FIGURE_DIRECTORY,
    DEFAULT_INTERARRIVAL_MINUTES,
    DEFAULT_OFFICER_COUNT,
    DEFAULT_STUDENT_COUNT,
    DEFAULT_WORKING_PERIOD_MINUTES,
    MIN_RESOURCE_UNITS,
    PERCENT_SCALE,
    ResourceKind,
)
from registration_sim.engine import simulate
from registration_sim.experiments import recommend, run_study
from registration_sim.metrics import measure
from registration_sim.model import SimulationConfig
from registration_sim.narrative import study_paragraphs
from registration_sim.report_page import write_report
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
        description="Deterministic simulation of course registration at Palm University College.",
    )
    parser.add_argument("--students", type=int, default=DEFAULT_STUDENT_COUNT)
    parser.add_argument("--interarrival", type=int, default=DEFAULT_INTERARRIVAL_MINUTES)
    parser.add_argument("--officers", type=int, default=DEFAULT_OFFICER_COUNT)
    parser.add_argument("--computers", type=int, default=DEFAULT_COMPUTER_COUNT)
    parser.add_argument("--session", type=int, default=DEFAULT_WORKING_PERIOD_MINUTES)
    parser.add_argument(
        "--charts",
        type=Path,
        default=Path(DEFAULT_FIGURE_DIRECTORY),
        help="Directory for the PNG graphs and the comparison table.",
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


def write_csv(path: Path, runs: tuple) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(COMPARISON_HEADERS)
        writer.writerows(comparison_rows(runs))


def _unit_label(count: int, singular: str, plural: str) -> str:
    word = singular if count == MIN_RESOURCE_UNITS else plural
    return f"{count} {word}"


def main() -> None:
    args = build_parser().parse_args()
    config = config_from_args(args)
    single = simulate(config)
    single_metrics = measure(single)
    study = run_study(config)
    recommended = recommend(study)

    officer_work = processing_minutes_for(ResourceKind.OFFICER)
    computer_work = processing_minutes_for(ResourceKind.COMPUTER)
    print("Palm University College — deterministic course-registration simulation")
    print(
        f"Each student: {total_processing_minutes()} minutes "
        f"({officer_work} with an officer, {computer_work} on a computer)."
    )
    print()
    print("Resources and processing times")
    print(activity_table())
    print()
    print(
        f"Simulation: {config.student_count} students, "
        f"every {config.interarrival_minutes} min, "
        f"{_unit_label(config.officer_count, 'officer', 'officers')}, "
        f"{_unit_label(config.computer_count, 'computer', 'computers')}, "
        f"session {config.working_period_minutes} min."
    )
    print(f"Total time: {single_metrics.makespan_minutes} min")
    print(f"Students processed: {single_metrics.students_processed}")
    print(
        f"Finished in the working period: {single_metrics.students_finished_within_period}"
        f" / {single_metrics.students_processed}"
    )
    print(f"Overtime: {single_metrics.overtime_minutes} min")
    print(f"Idle time: {single_metrics.overall_idle_minutes} resource-minutes")
    print(
        "System efficiency: "
        f"{single_metrics.service_efficiency * PERCENT_SCALE:.1f}% "
        "(time being served, out of time at the desk)"
    )
    print()
    print("Resource utilisation")
    print(resource_table(single_metrics))
    print()
    print("Waiting at each activity")
    print(stage_table(single_metrics))
    print()
    print("Experiments: current desk, one more officer, one more computer")
    print(comparison_table(study))
    print()
    print(f"Most efficient allocation: {recommended.scenario.name}")
    print(
        f"{_unit_label(recommended.scenario.officer_count, 'officer', 'officers')}, "
        f"{_unit_label(recommended.scenario.computer_count, 'computer', 'computers')}."
    )
    print()
    for paragraph in study_paragraphs(study, recommended):
        print(paragraph)
        print()

    figures = save_study_charts(study, args.charts)
    csv_path = args.charts / COMPARISON_CSV
    write_csv(csv_path, study)
    page = write_report(config, single_metrics, study, recommended, figures)
    for figure in figures:
        print(f"Wrote {figure}")
    print(f"Wrote {csv_path}")
    print(f"Wrote {page}")


if __name__ == "__main__":
    main()
