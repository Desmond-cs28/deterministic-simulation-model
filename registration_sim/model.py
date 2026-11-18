"""Data exchanged by the engine, the metrics, and the report."""

from dataclasses import dataclass

from registration_sim.constants import ActivityId, ResourceKind, ScenarioId


@dataclass(frozen=True)
class SimulationConfig:
    student_count: int
    interarrival_minutes: int
    officer_count: int
    computer_count: int
    working_period_minutes: int


@dataclass(frozen=True)
class StageAssignment:
    student_index: int
    activity_id: ActivityId
    resource_kind: ResourceKind
    resource_index: int
    ready_minutes: int
    start_minutes: int
    end_minutes: int

    @property
    def waiting_minutes(self) -> int:
        return self.start_minutes - self.ready_minutes

    @property
    def processing_minutes(self) -> int:
        return self.end_minutes - self.start_minutes


@dataclass(frozen=True)
class StudentRecord:
    student_index: int
    arrival_minutes: int
    completion_minutes: int
    waiting_minutes: int
    flow_minutes: int
    stages: tuple[StageAssignment, ...]


@dataclass(frozen=True)
class SimulationResult:
    config: SimulationConfig
    students: tuple[StudentRecord, ...]
    assignments: tuple[StageAssignment, ...]
    makespan_minutes: int


@dataclass(frozen=True)
class ResourceMetrics:
    resource_kind: ResourceKind
    resource_index: int
    resource_label: str
    busy_minutes: int
    idle_minutes: int
    utilisation: float


@dataclass(frozen=True)
class StageMetrics:
    activity_id: ActivityId
    label: str
    resource_kind: ResourceKind
    processing_minutes: int
    average_wait_minutes: float
    max_wait_minutes: int
    total_wait_minutes: int


@dataclass(frozen=True)
class SimulationMetrics:
    makespan_minutes: int
    lower_bound_minutes: int
    schedule_efficiency: float
    students_processed: int
    students_finished_within_period: int
    students_unfinished_within_period: int
    overtime_minutes: int
    total_processing_minutes: int
    total_waiting_minutes: int
    average_waiting_minutes: float
    average_flow_minutes: float
    max_flow_minutes: int
    average_students_waiting: float
    peak_students_in_system: int
    service_efficiency: float
    officer_busy_minutes: int
    officer_idle_minutes: int
    officer_utilisation: float
    computer_busy_minutes: int
    computer_idle_minutes: int
    computer_utilisation: float
    overall_busy_minutes: int
    overall_idle_minutes: int
    overall_utilisation: float
    resource_count: int
    productivity_per_resource_hour: float
    completion_ratio: float
    efficiency_score: float
    resources: tuple[ResourceMetrics, ...]
    stages: tuple[StageMetrics, ...]


@dataclass(frozen=True)
class Scenario:
    scenario_id: ScenarioId
    name: str
    short_label: str
    summary: str
    officer_count: int
    computer_count: int


@dataclass(frozen=True)
class ScenarioRun:
    scenario: Scenario
    result: SimulationResult
    metrics: SimulationMetrics
