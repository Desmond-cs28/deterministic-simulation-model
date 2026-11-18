"""Write the results page the preview opens. The page is produced by this program."""

from html import escape
from pathlib import Path

from registration_sim.activities import ACTIVITY_SEQUENCE
from registration_sim.constants import (
    CLOCK_PAD_WIDTH,
    DISPLAY_INDEX_OFFSET,
    HOURS_PER_DAY,
    MINUTES_PER_HOUR,
    MIN_RESOURCE_UNITS,
    PERCENT_SCALE,
    SHIFT_START_HOUR,
    SHIFT_START_MINUTE,
)
from registration_sim.model import ScenarioRun, SimulationConfig, SimulationMetrics
from registration_sim.narrative import study_paragraphs

REPO_ROOT = Path(__file__).resolve().parent.parent
REPORT_PAGE = REPO_ROOT / "index.html"


def clock_label(minutes_from_open: int) -> str:
    total = SHIFT_START_HOUR * MINUTES_PER_HOUR + SHIFT_START_MINUTE + minutes_from_open
    hour = (total // MINUTES_PER_HOUR) % HOURS_PER_DAY
    minute = total % MINUTES_PER_HOUR
    return f"{hour:0{CLOCK_PAD_WIDTH}d}:{minute:0{CLOCK_PAD_WIDTH}d}"


def _units(count: int, singular: str, plural: str) -> str:
    word = singular if count == MIN_RESOURCE_UNITS else plural
    return f"{count} {word}"


def _pct(ratio: float) -> str:
    return f"{ratio * PERCENT_SCALE:.1f}%"


def _relative_src(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def write_report(
    config: SimulationConfig,
    metrics: SimulationMetrics,
    study: tuple[ScenarioRun, ...] | list[ScenarioRun],
    recommended: ScenarioRun,
    figures: list[Path],
) -> Path:
    paragraphs = study_paragraphs(study, recommended)
    page = _page(config, metrics, study, recommended, paragraphs, figures)
    REPORT_PAGE.write_text(page, encoding="utf-8")
    return REPORT_PAGE


def _page(
    config: SimulationConfig,
    metrics: SimulationMetrics,
    study: tuple[ScenarioRun, ...] | list[ScenarioRun],
    recommended: ScenarioRun,
    paragraphs: tuple[str, ...] | list[str],
    figures: list[Path],
) -> str:
    steps = "\n".join(_step(index, activity.label, activity.resource_kind.value, activity.processing_minutes, activity.description) for index, activity in enumerate(ACTIVITY_SEQUENCE))
    rows = "\n".join(_result_row(run, recommended) for run in study)
    reading = "\n".join(f"<p>{escape(paragraph)}</p>" for paragraph in paragraphs)
    graphs = "\n".join(_graph(path) for path in figures)
    finish = clock_label(metrics.makespan_minutes)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Palm University College registration simulation</title>
  <style>
    :root {{
      --ink: #14241c;
      --green: #02553c;
      --deep: #013326;
      --paper: #f3f6f2;
      --card: #ffffff;
      --line: #c9ddd3;
      --muted: #3d5348;
      --gold: #c4a35a;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font: 16px/1.5 Georgia, "Times New Roman", serif;
    }}
    header {{
      background: var(--deep);
      color: #f4faf6;
      padding: 2.2rem 1.25rem 1.8rem;
    }}
    header p, main p {{ max-width: 44rem; }}
    .kicker {{
      letter-spacing: 0.14em;
      text-transform: uppercase;
      font: 0.72rem/1.4 ui-monospace, monospace;
      color: #d7ebe3;
    }}
    h1 {{ font-weight: 500; font-size: 2.4rem; line-height: 1.1; margin: 0.4rem 0; }}
    main {{ max-width: 68rem; margin: 0 auto; padding: 1.5rem 1.25rem 3rem; }}
    h2 {{ font-weight: 500; font-size: 1.6rem; margin: 2rem 0 0.6rem; }}
    .steps, .stats {{ display: grid; gap: 0.8rem; }}
    .steps {{ grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr)); }}
    .stats {{ grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr)); margin-top: 1rem; }}
    article, .stat {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 0.8rem;
      padding: 0.9rem 1rem;
    }}
    .step-no {{ color: var(--green); font: 0.72rem/1.4 ui-monospace, monospace; letter-spacing: 0.12em; text-transform: uppercase; }}
    .muted {{ color: var(--muted); }}
    table {{ width: 100%; border-collapse: collapse; background: var(--card); font-size: 0.92rem; }}
    th, td {{ text-align: left; padding: 0.55rem 0.6rem; border-bottom: 1px solid var(--line); vertical-align: top; }}
    th {{ font: 0.72rem/1.3 ui-monospace, monospace; letter-spacing: 0.04em; text-transform: uppercase; color: var(--muted); }}
    tr.best {{ background: #d7ebe3; }}
    .wrap {{ overflow-x: auto; border: 1px solid var(--line); border-radius: 0.8rem; }}
    figure {{ margin: 1rem 0; background: var(--card); border: 1px solid var(--line); border-radius: 0.8rem; padding: 0.6rem; }}
    img {{ width: 100%; height: auto; display: block; }}
    figcaption {{ color: var(--muted); font-size: 0.9rem; padding: 0.4rem 0.3rem 0.2rem; }}
  </style>
</head>
<body>
  <header>
    <p class="kicker">Palm University College · Manya Jorpanya</p>
    <h1>Course registration simulation</h1>
    <p>One morning at the Registry. {escape(str(config.student_count))} students arrive every {escape(str(config.interarrival_minutes))} minutes from 08:00. The desk is open for {escape(str(config.working_period_minutes))} minutes. Arrivals and processing times are fixed, so this schedule is the same every time the program runs.</p>
  </header>
  <main>
    <h2>The three steps</h2>
    <div class="steps">
      {steps}
    </div>
    <h2>This morning, with the current desk</h2>
    <p class="muted">{escape(_units(config.officer_count, "officer", "officers"))} and {escape(_units(config.computer_count, "computer", "computers"))}.</p>
    <div class="stats">
      {_stat("Total time", f"{finish} · {metrics.makespan_minutes} min")}
      {_stat("Students processed", str(metrics.students_processed))}
      {_stat("Finished by close", f"{metrics.students_finished_within_period} / {metrics.students_processed}")}
      {_stat("Idle time", f"{metrics.overall_idle_minutes} min")}
      {_stat("Officer use", _pct(metrics.officer_utilisation))}
      {_stat("Computer use", _pct(metrics.computer_utilisation))}
      {_stat("System efficiency", _pct(metrics.service_efficiency))}
    </div>
    <h2>Three resource allocations</h2>
    <p>The same students are registered three times. First the desk as it stands, then one extra officer, then one extra computer.</p>
    <div class="wrap">
      <table>
        <thead>
          <tr>
            <th>Allocation</th>
            <th>Officers</th>
            <th>Computers</th>
            <th>Total time</th>
            <th>Processed</th>
            <th>Finished</th>
            <th>Idle min.</th>
            <th>Officer use</th>
            <th>Computer use</th>
            <th>System efficiency</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </div>
    <h2>Graphs</h2>
    {graphs}
    <h2>What the results mean</h2>
    <p>The most efficient allocation is <strong>{escape(recommended.scenario.name)}</strong>: {escape(_units(recommended.scenario.officer_count, "officer", "officers"))} and {escape(_units(recommended.scenario.computer_count, "computer", "computers"))}.</p>
    {reading}
  </main>
</body>
</html>
"""


def _step(index: int, label: str, resource: str, minutes: int, description: str) -> str:
    number = index + DISPLAY_INDEX_OFFSET
    return (
        "<article>"
        f"<p class=\"step-no\">Step {number}</p>"
        f"<h3>{escape(label)}</h3>"
        f"<p>{escape(description)}</p>"
        f"<p><strong>{minutes} min</strong> · {escape(resource)}</p>"
        "</article>"
    )


def _stat(label: str, value: str) -> str:
    return f"<div class=\"stat\"><p class=\"step-no\">{escape(label)}</p><p><strong>{escape(value)}</strong></p></div>"


def _result_row(run: ScenarioRun, recommended: ScenarioRun) -> str:
    metrics = run.metrics
    marker = " class=\"best\"" if run.scenario.scenario_id == recommended.scenario.scenario_id else ""
    name = escape(run.scenario.name)
    if run.scenario.scenario_id == recommended.scenario.scenario_id:
        name = f"{name} · most efficient"
    finish = clock_label(metrics.makespan_minutes)
    return (
        f"<tr{marker}>"
        f"<td>{name}</td>"
        f"<td>{run.scenario.officer_count}</td>"
        f"<td>{run.scenario.computer_count}</td>"
        f"<td>{finish} ({metrics.makespan_minutes} min)</td>"
        f"<td>{metrics.students_processed}</td>"
        f"<td>{metrics.students_finished_within_period}</td>"
        f"<td>{metrics.overall_idle_minutes}</td>"
        f"<td>{_pct(metrics.officer_utilisation)}</td>"
        f"<td>{_pct(metrics.computer_utilisation)}</td>"
        f"<td>{_pct(metrics.service_efficiency)}</td>"
        "</tr>"
    )


def _graph(path: Path) -> str:
    title = path.stem.replace("_", " ")
    return (
        "<figure>"
        f"<img src=\"{escape(_relative_src(path))}\" alt=\"{escape(title)}\">"
        f"<figcaption>{escape(title)}</figcaption>"
        "</figure>"
    )
