"""Deterministic simulation of a university registration centre."""

from registration_sim.engine import ConfigurationError, simulate
from registration_sim.metrics import measure
from registration_sim.model import SimulationConfig, SimulationMetrics, SimulationResult

__all__ = [
    "ConfigurationError",
    "SimulationConfig",
    "SimulationMetrics",
    "SimulationResult",
    "measure",
    "simulate",
]
