"""Static figures for the written report."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from registration_sim.constants import (
    FIGURE_COMPLETIONS,
    FIGURE_MAKESPAN,
    FIGURE_SENSITIVITY,
    FIGURE_UTILISATION,
    PERCENT_SCALE,
    SENSITIVITY_MIN_UNITS,
)
from registration_sim.model import ScenarioRun

INK = "#1c1915"
TEAL = "#0e6b62"
NAVY = "#243044"
RUST = "#b4492a"
PAPER = "#fbf7ef"
GRID = "#e4dccf"
AMBER = "#c4922a"
BAND = "#efe6d6"
LINE_COLORS = (TEAL, NAVY, RUST, AMBER, "#6b4c9a", "#3d6b4f")


def _style_axis(axis: plt.Axes) -> None:
    axis.set_facecolor(PAPER)
    axis.tick_params(colors=INK, labelsize=9)
    axis.grid(axis="y", color=GRID, linewidth=0.8)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    for spine in axis.spines.values():
        spine.set_color(GRID)
    axis.title.set_color(INK)
    axis.xaxis.label.set_color(INK)
    axis.yaxis.label.set_color(INK)


def _new_figure() -> tuple[plt.Figure, plt.Axes]:
    figure, axis = plt.subplots(figsize=(9.2, 5.1), dpi=140)
    figure.patch.set_facecolor(PAPER)
    _style_axis(axis)
    return figure, axis


def _labels(runs: list[ScenarioRun] | tuple[ScenarioRun, ...]) -> list[str]:
    return [run.scenario.short_label.replace(" ", "\n") for run in runs]


def save_makespan_chart(
    runs: tuple[ScenarioRun, ...] | list[ScenarioRun],
    session_minutes: int,
    path: Path,
) -> None:
    figure, axis = _new_figure()
    labels = _labels(runs)
    values = [run.metrics.makespan_minutes for run in runs]
    positions = list(range(len(values)))
    axis.bar(positions, values, color=TEAL, width=0.72)
    axis.axhline(session_minutes, color=RUST, linewidth=1.4, linestyle="--")
    axis.set_xticks(positions, labels)
    axis.set_ylabel("Minutes from hall opening")
    axis.set_title("Makespan against the morning session")
    axis.legend(
        handles=[
            plt.Line2D([0], [0], color=RUST, linestyle="--", label=f"Session close ({session_minutes} min)")
        ],
        frameon=False,
    )
    figure.tight_layout()
    figure.savefig(path)
    plt.close(figure)


def save_utilisation_chart(runs: tuple[ScenarioRun, ...] | list[ScenarioRun], path: Path) -> None:
    figure, axis = _new_figure()
    labels = _labels(runs)
    positions = list(range(len(runs)))
    width = 0.36
    officer = [run.metrics.officer_utilisation * PERCENT_SCALE for run in runs]
    computer = [run.metrics.computer_utilisation * PERCENT_SCALE for run in runs]
    officer_positions = [position - width / 2 for position in positions]
    computer_positions = [position + width / 2 for position in positions]
    axis.bar(officer_positions, officer, width=width, color=NAVY, label="Officers")
    axis.bar(computer_positions, computer, width=width, color=TEAL, label="Computers")
    axis.set_xticks(positions, labels)
    axis.set_ylabel("Utilisation (%)")
    axis.set_ylim(0, 100)
    axis.set_title("Resource utilisation by allocation")
    axis.legend(frameon=False)
    figure.tight_layout()
    figure.savefig(path)
    plt.close(figure)


def save_completion_chart(runs: tuple[ScenarioRun, ...] | list[ScenarioRun], path: Path) -> None:
    figure, axis = _new_figure()
    labels = _labels(runs)
    values = [run.metrics.students_finished_within_period for run in runs]
    cohort = runs[0].result.config.student_count
    positions = list(range(len(values)))
    axis.bar(positions, values, color=AMBER, width=0.72)
    axis.axhline(cohort, color=NAVY, linewidth=1.4, linestyle="--")
    axis.set_xticks(positions, labels)
    axis.set_ylabel("Students")
    axis.set_title("Students who finish before the session closes")
    axis.legend(
        handles=[plt.Line2D([0], [0], color=NAVY, linestyle="--", label=f"Full cohort ({cohort})")],
        frameon=False,
    )
    figure.tight_layout()
    figure.savefig(path)
    plt.close(figure)


def save_sensitivity_chart(runs: tuple[ScenarioRun, ...] | list[ScenarioRun], path: Path) -> None:
    figure, axis = _new_figure()
    by_computers: dict[int, list[ScenarioRun]] = {}
    for run in runs:
        count = run.scenario.computer_count
        by_computers.setdefault(count, []).append(run)
    for offset, computer_count in enumerate(sorted(by_computers)):
        series = sorted(by_computers[computer_count], key=lambda run: run.scenario.officer_count)
        axis.plot(
            [run.scenario.officer_count for run in series],
            [run.metrics.makespan_minutes for run in series],
            color=LINE_COLORS[offset % len(LINE_COLORS)],
            marker="o",
            linewidth=1.8,
            label=(
                f"{computer_count} computer"
                if computer_count == SENSITIVITY_MIN_UNITS
                else f"{computer_count} computers"
            ),
        )
    axis.set_xlabel("Registration officers")
    axis.set_ylabel("Makespan (minutes)")
    axis.set_title("Makespan as officers and computers increase")
    axis.set_xticks(list(range(SENSITIVITY_MIN_UNITS, max(by_computers) + 1)))
    axis.legend(
        frameon=False,
        ncol=3,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.18),
    )
    figure.tight_layout()
    figure.subplots_adjust(bottom=0.22)
    figure.savefig(path)
    plt.close(figure)


def save_study_charts(
    study: tuple[ScenarioRun, ...] | list[ScenarioRun],
    sensitivity: tuple[ScenarioRun, ...] | list[ScenarioRun],
    output_dir: Path,
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    session_minutes = study[0].result.config.working_period_minutes
    targets = [
        output_dir / FIGURE_MAKESPAN,
        output_dir / FIGURE_UTILISATION,
        output_dir / FIGURE_COMPLETIONS,
        output_dir / FIGURE_SENSITIVITY,
    ]
    save_makespan_chart(study, session_minutes, targets[0])
    save_utilisation_chart(study, targets[1])
    save_completion_chart(study, targets[2])
    save_sensitivity_chart(sensitivity, targets[3])
    return targets
