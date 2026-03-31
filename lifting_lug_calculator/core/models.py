"""Typed data models used across the app."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class CalculationInputs:
    fv: float
    kd: float
    theta_deg: float
    t: float
    t_p: float
    d: float
    dp: float
    r: float
    w: float
    hf: float
    fy: float
    fu: float
    ns: float


@dataclass(frozen=True)
class AreaResults:
    net_area: float
    shear_area: float
    bearing_area: float
    weld_throat: float
    weld_area: float


@dataclass(frozen=True)
class MetricResult:
    value: float
    allowable: float
    passed: bool


@dataclass(frozen=True)
class CalculationMetrics:
    tensile: MetricResult
    tear_out: MetricResult
    bearing: MetricResult
    weld: MetricResult


@dataclass(frozen=True)
class CalculationResult:
    p_design: float
    t_eff: float
    areas: AreaResults
    metrics: CalculationMetrics

    def to_dict(self) -> dict:
        return asdict(self)
