"""Sidebar input collection."""

from dataclasses import dataclass

import streamlit as st

from lifting_lug_calculator.core import MATERIAL_DB, CalculationInputs
from lifting_lug_calculator.reporting import ReportParams


@dataclass(frozen=True)
class SidebarInputs:
    material: str
    fy: float
    fu: float
    ns: float
    fv_ton: float
    kd: float
    theta: int
    t: float
    tp: float
    d: float
    dp: float
    r: float
    h: float
    hf: float
    w: float
    use_custom_w: bool

    @property
    def fv(self) -> float:
        return self.fv_ton * 9.81

    def to_calculation_inputs(self) -> CalculationInputs:
        return CalculationInputs(
            fv=self.fv,
            kd=self.kd,
            theta_deg=self.theta,
            t=self.t,
            t_p=self.tp,
            d=self.d,
            dp=self.dp,
            r=self.r,
            w=self.w,
            hf=self.hf,
            fy=self.fy,
            fu=self.fu,
            ns=self.ns,
        )

    def to_report_params(self) -> ReportParams:
        return ReportParams(
            fv_ton=self.fv_ton,
            fv=self.fv,
            kd=self.kd,
            theta=self.theta,
            t=self.t,
            tp=self.tp,
            d=self.d,
            dp=self.dp,
            r=self.r,
            h=self.h,
            w=self.w,
            hf=self.hf,
            fy=self.fy,
            fu=self.fu,
            ns=self.ns,
        )


def render_sidebar() -> SidebarInputs:
    with st.sidebar:
        st.markdown('<p class="main-title" style="font-size:1.3rem;">🔩 吊耳计算器</p>', unsafe_allow_html=True)
        st.markdown('<p style="color:#718096; font-size:0.78rem;">Lifting Lug Stress Calculator</p>', unsafe_allow_html=True)
        st.divider()

        st.markdown('<p class="sidebar-section-title">📦 材质参数</p>', unsafe_allow_html=True)
        material = st.selectbox("材质选择", list(MATERIAL_DB.keys()), index=0)
        if material == "自定义":
            fy = st.number_input("材料屈服强度 Fy (MPa)", min_value=100.0, max_value=1000.0, value=355.0, step=5.0)
            fu = st.number_input("材料抗拉强度 Fu (MPa)", min_value=100.0, max_value=1200.0, value=470.0, step=5.0)
        else:
            fy = float(st.number_input("材料屈服强度 Fy (MPa)", value=float(MATERIAL_DB[material]["fy"]), step=5.0))
            fu = float(st.number_input("材料抗拉强度 Fu (MPa)", value=float(MATERIAL_DB[material]["fu"]), step=5.0))

        ns = st.number_input("结构安全系数 Ns", min_value=1.0, max_value=10.0, value=3.0, step=0.1, help="默认取 3.0，大型起重设备常用安全系数")
        st.divider()

        st.markdown('<p class="sidebar-section-title">⚡ 工况载荷</p>', unsafe_allow_html=True)
        fv_ton = st.number_input("单只吊耳受力 Fv (t)", min_value=0.01, max_value=5000.0, value=10.0, step=1.0, help='输入质量单位"吨"，系统自动换算为 kN（1t ≈ 9.81 kN）')
        fv = fv_ton * 9.81
        st.markdown(f'<p style="color:#63b3ed; font-size:0.8rem; margin-top:-0.5rem;">≈ <b>{fv:.2f} kN</b></p>', unsafe_allow_html=True)
        kd = st.number_input("动载系数 Kd", min_value=1.0, max_value=3.0, value=1.25, step=0.05, help="静载取 1.0，动载通常取 1.25")
        theta = st.slider("吊索与水平面夹角 θ (°)", min_value=10, max_value=90, value=60, step=1, help="夹角越大，垂直分力越大，通常60°~90°")
        st.divider()

        st.markdown('<p class="sidebar-section-title">📐 吊耳几何尺寸 (mm)</p>', unsafe_allow_html=True)
        t = st.number_input("吊耳主板厚度 t (mm)", min_value=1.0, max_value=200.0, value=20.0, step=1.0)
        tp = st.number_input("单侧加强板厚度 tp (mm)", min_value=0.0, max_value=100.0, value=0.0, step=1.0, help="无加强板时取 0。有效厚度 t_eff = t + 2×tp")
        if tp > 0:
            st.info(f"有效厚度 t_eff = {t} + 2×{tp} = **{t + 2 * tp:.0f} mm**")
        d = st.number_input("销轴孔孔径 d (mm)", min_value=1.0, max_value=500.0, value=52.0, step=1.0)
        dp = st.number_input("销轴直径 dp (mm)", min_value=1.0, max_value=500.0, value=50.0, step=1.0, help="销轴直径，通常略小于孔径")
        r = st.number_input("孔心至边缘距离 R (mm)", min_value=1.0, max_value=1000.0, value=80.0, step=1.0)
        h = st.number_input("圆心到底边距离 H (mm)", min_value=1.0, max_value=2000.0, value=80.0, step=1.0, help="用于控制吊耳正视图与侧视图的竖向投影基准")
        hf = st.number_input("焊缝焊脚尺寸 hf (mm)", min_value=1.0, max_value=50.0, value=12.0, step=1.0)
        if h <= d / 2:
            st.warning("当前 H 不大于 d/2，示意图中销轴孔可能会接近或穿过底边；该提示不影响当前强度校核。")

        use_custom_w = st.checkbox("自定义吊耳根部宽度 W", value=False, help="不勾选则默认取 W = 2R（半圆头吊耳）")
        if use_custom_w:
            input_w = st.number_input("吊耳根部宽度 W (mm)", min_value=1.0, max_value=2000.0, value=float(2 * r), step=1.0)
            w = max(input_w, 2 * r)
            if input_w < 2 * r:
                st.warning(f"自定义 W 不得小于 2R，已按最小合法值 **{w:.0f} mm** 自动修正。")
        else:
            w = 2 * r
            st.info(f"W = 2R = **{w:.0f} mm**")

        st.divider()
        st.markdown('<p style="color:#f7fafc; font-size:0.85rem; font-weight:500;">💡 公式参考：通用工程力学校验方法</p>', unsafe_allow_html=True)

    return SidebarInputs(
        material=material,
        fy=fy,
        fu=fu,
        ns=ns,
        fv_ton=fv_ton,
        kd=kd,
        theta=theta,
        t=t,
        tp=tp,
        d=d,
        dp=dp,
        r=r,
        h=h,
        hf=hf,
        w=w,
        use_custom_w=use_custom_w,
    )
