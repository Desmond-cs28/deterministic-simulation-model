"""Text tables for the command-line report."""

from registration_sim.activities import ACTIVITY_SEQUENCE
from registration_sim.constants import PERCENT_SCALE
from registration_sim.model import ScenarioRun, SimulationMetrics


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    widths = [len(header) for header in headers]
    for row in rows:
        for column, cell in enumerate(row):
            if len(cell) > widths[column]:
                widths[column] = len(cell)

    def format_row(cells: list[str]) -> str:
        padded = [cell.ljust(widths[column]) for column, cell in enumerate(cells)]
        return "  ".join(padded)

    rule = "  ".join("-" * width for width in widths)
    lines = [format_row(headers), rule]
    for row in rows:
        lines.append(format_row(row))
    return "\n".join(lines)


def _pct(ratio: float) -> str:
    return f"{ratio * PERCENT_SCALE:.1f}%"


def _num(value: float) -> str:
    return f"{value:.1f}"


def activity_table() -> str:
    headers = ["Activity", "Resource", "Minutes", "What happens"]
    rows: list[list[str]] = []
    for activity in ACTIVITY_SEQUENCE:
        rows.append(
            [
                activity.label,
                activity.resource_kind.value,
                str(activity.processing_minutes),
                activity.description,
            ]
        )
    return render_table(headers, rows)


def comparison_rows(runs: tuple[ScenarioRun, ...] | list[ScenarioRun]) -> list[list[str]]:
    rows: list[list[str]] = []
    for run in runs:
        metrics = run.metrics
        rows.append(
            [
                run.scenario.short_label,
                str(run.scenario.officer_count),
                str(run.scenario.computer_count),
                str(metrics.makespan_minutes),
                str(metrics.students_finished_within_period),
                str(metrics.students_processed),
                str(metrics.overtime_minutes),
                _pct(metrics.officer_utilisation),
                _pct(metrics.computer_utilisation),
                _pct(metrics.overall_utilisation),
                str(metrics.overall_idle_minutes),
                _num(metrics.average_waiting_minutes),
                _pct(metrics.service_efficiency),
            ]
        )
    return rows


COMPARISON_HEADERS = [
    "Scenario",
    "Officers",
    "Computers",
    "Total time",
    "Finished",
    "Processed",
    "Overtime",
    "Officer use",
    "Computer use",
    "Overall use",
    "Idle min.",
    "Avg wait",
    "System efficiency",
]


def comparison_table(runs: tuple[ScenarioRun, ...] | list[ScenarioRun]) -> str:
    return render_table(COMPARISON_HEADERS, comparison_rows(runs))


def resource_table(metrics: SimulationMetrics) -> str:
    headers = ["Resource", "Busy min.", "Idle min.", "Utilisation"]
    rows = [
        [
            row.resource_label,
            str(row.busy_minutes),
            str(row.idle_minutes),
            _pct(row.utilisation),
        ]
        for row in metrics.resources
    ]
    return render_table(headers, rows)


def stage_table(metrics: SimulationMetrics) -> str:
    headers = ["Activity", "Resource", "Process min.", "Avg wait", "Max wait"]
    rows = [
        [
            stage.label,
            stage.resource_kind.value,
            str(stage.processing_minutes),
            _num(stage.average_wait_minutes),
            str(stage.max_wait_minutes),
        ]
        for stage in metrics.stages
    ]
    return render_table(headers, rows)
