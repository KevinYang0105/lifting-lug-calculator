"""Stress calculation logic."""

import math

from lifting_lug_calculator.core.constants import ALLOWABLE_RULES
from lifting_lug_calculator.core.models import (
    AreaResults,
    CalculationInputs,
    CalculationMetrics,
    CalculationResult,
    MetricResult,
)


def _build_metric(value: float, allowable: float) -> MetricResult:
    return MetricResult(value=value, allowable=allowable, passed=value <= allowable)


def calculate_lug_stresses_from_inputs(inputs: CalculationInputs) -> CalculationResult:
    """Calculate lifting lug stresses from typed inputs."""
    theta_rad = math.radians(inputs.theta_deg)
    p_design = (inputs.fv * 1000 * inputs.kd) / math.sin(theta_rad)

    t_eff = inputs.t + 2 * inputs.t_p
    if inputs.r <= inputs.d / 2 or t_eff <= 0 or inputs.dp <= 0 or inputs.w <= 0 or inputs.hf <= 0:
        raise ValueError("几何尺寸输入错误（如 R 必须大于 d/2，厚度/直径不能为 0）")
    if inputs.dp > inputs.d:
        raise ValueError("销轴直径 dp 不能大于孔径 d。")

    net_area = 2 * t_eff * (inputs.r - inputs.d / 2)
    shear_area = 2 * t_eff * (inputs.r - inputs.d / 2)
    bearing_area = t_eff * inputs.dp
    weld_throat = 0.707 * inputs.hf
    weld_area = weld_throat * 2 * inputs.w

    areas = AreaResults(
        net_area=net_area,
        shear_area=shear_area,
        bearing_area=bearing_area,
        weld_throat=weld_throat,
        weld_area=weld_area,
    )
    metrics = CalculationMetrics(
        tensile=_build_metric(
            p_design / net_area,
            ALLOWABLE_RULES["tensile"]["compute"](inputs.fy, inputs.fu, inputs.ns),
        ),
        tear_out=_build_metric(
            p_design / shear_area,
            ALLOWABLE_RULES["tear_out"]["compute"](inputs.fy, inputs.fu, inputs.ns),
        ),
        bearing=_build_metric(
            p_design / bearing_area,
            ALLOWABLE_RULES["bearing"]["compute"](inputs.fy, inputs.fu, inputs.ns),
        ),
        weld=_build_metric(
            p_design / weld_area,
            ALLOWABLE_RULES["weld"]["compute"](inputs.fy, inputs.fu, inputs.ns),
        ),
    )
    return CalculationResult(p_design=p_design, t_eff=t_eff, areas=areas, metrics=metrics)


def calculate_lug_stresses(**kwargs) -> dict:
    """Backward-compatible dict API used by tests and UI."""
    try:
        inputs = CalculationInputs(**kwargs)
        return calculate_lug_stresses_from_inputs(inputs).to_dict()
    except Exception as exc:
        return {"error": f"{exc}"}
