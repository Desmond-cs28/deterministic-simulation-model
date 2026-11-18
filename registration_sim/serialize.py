"""JSON payloads shared with the web lab's parity check."""

from registration_sim.model import ScenarioRun, SimulationMetrics, SimulationResult


def assignment_payload(result: SimulationResult) -> list[dict[str, int | str]]:
    rows: list[dict[str, int | str]] = []
    for stage in result.assignments:
        rows.append(
            {
                "student_index": stage.student_index,
                "activity_id": stage.activity_id.value,
                "resource_kind": stage.resource_kind.value,
                "resource_index": stage.resource_index,
                "ready_minutes": stage.ready_minutes,
                "start_minutes": stage.start_minutes,
                "end_minutes": stage.end_minutes,
            }
        )
    return rows


def metrics_payload(metrics: SimulationMetrics) -> dict[str, float | int]:
    return {
        "makespan_minutes": metrics.makespan_minutes,
        "lower_bound_minutes": metrics.lower_bound_minutes,
        "students_processed": metrics.students_processed,
        "students_finished_within_period": metrics.students_finished_within_period,
        "overtime_minutes": metrics.overtime_minutes,
        "total_processing_minutes": metrics.total_processing_minutes,
        "total_waiting_minutes": metrics.total_waiting_minutes,
        "average_waiting_minutes": metrics.average_waiting_minutes,
        "average_flow_minutes": metrics.average_flow_minutes,
        "max_flow_minutes": metrics.max_flow_minutes,
        "peak_students_in_system": metrics.peak_students_in_system,
        "officer_busy_minutes": metrics.officer_busy_minutes,
        "officer_idle_minutes": metrics.officer_idle_minutes,
        "computer_busy_minutes": metrics.computer_busy_minutes,
        "computer_idle_minutes": metrics.computer_idle_minutes,
        "overall_idle_minutes": metrics.overall_idle_minutes,
        "overall_busy_minutes": metrics.overall_busy_minutes,
        "resource_count": metrics.resource_count,
        "officer_utilisation": metrics.officer_utilisation,
        "computer_utilisation": metrics.computer_utilisation,
        "overall_utilisation": metrics.overall_utilisation,
        "service_efficiency": metrics.service_efficiency,
        "schedule_efficiency": metrics.schedule_efficiency,
        "completion_ratio": metrics.completion_ratio,
        "efficiency_score": metrics.efficiency_score,
        "productivity_per_resource_hour": metrics.productivity_per_resource_hour,
        "average_students_waiting": metrics.average_students_waiting,
    }


def run_payload(run: ScenarioRun, include_assignments: bool) -> dict[str, object]:
    config = run.result.config
    payload: dict[str, object] = {
        "scenario_id": run.scenario.scenario_id.value,
        "name": run.scenario.name,
        "officer_count": config.officer_count,
        "computer_count": config.computer_count,
        "student_count": config.student_count,
        "interarrival_minutes": config.interarrival_minutes,
        "working_period_minutes": config.working_period_minutes,
        "metrics": metrics_payload(run.metrics),
    }
    if include_assignments:
        payload["assignments"] = assignment_payload(run.result)
    return payload
