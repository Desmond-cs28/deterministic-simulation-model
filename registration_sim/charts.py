"""Static figures for the written report."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from registration_sim.constants import (
    FIGURE_COMPLETIONS,
    FIGURE_MAKESPAN,
    FIGURE_UTILISATION,
    PERCENT_SCALE,
)
from registration_sim.model import ScenarioRun

INK = "#14241c"
TEAL = "#02553C"
NAVY = "#013326"
RUST = "#3d8f6e"
PAPER = "#ffffff"
GRID = "#d5e4db"
AMBER = "#c4a35a"


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
    axis.set_ylabel("Minutes from 08:00")
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


def save_study_charts(
    study: tuple[ScenarioRun, ...] | list[ScenarioRun],
    output_dir: Path,
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    session_minutes = study[0].result.config.working_period_minutes
    targets = [
        output_dir / FIGURE_MAKESPAN,
        output_dir / FIGURE_UTILISATION,
        output_dir / FIGURE_COMPLETIONS,
    ]
    save_makespan_chart(study, session_minutes, targets[0])
    save_utilisation_chart(study, targets[1])
    save_completion_chart(study, targets[2])
    return targets
