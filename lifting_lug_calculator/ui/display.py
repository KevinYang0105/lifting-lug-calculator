"""Main content rendering."""

import math

import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt

from lifting_lug_calculator.core import ALLOWABLE_RULES
from lifting_lug_calculator.reporting import generate_word_report
from lifting_lug_calculator.ui.inputs import SidebarInputs
from lifting_lug_calculator.visualization import draw_lug_diagram


def render_header() -> None:
    st.markdown('<h1 class="main-title">🔩 吊耳应力校验计算书</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">LIFTING LUG STRESS VERIFICATION REPORT</p>', unsafe_allow_html=True)


def render_validation_errors(inputs: SidebarInputs) -> None:
    if inputs.dp > inputs.d:
        st.error("❌ 销轴直径 dp 不能大于孔径 d，请修正输入参数。")
        st.stop()


def render_results(inputs: SidebarInputs, results: dict) -> None:
    checks = [results["metrics"][name]["passed"] for name in ("tensile", "tear_out", "bearing", "weld")]
    if all(checks):
        st.success("✅ **综合校验：全部通过 PASS** — 该吊耳设计满足所有受力校验要求。")
    else:
        fail_count = sum(1 for item in checks if not item)
        st.error(f"🚨 **综合校验：存在风险 FAIL** — 共 {fail_count} 项指标超出许用应力，请修改参数！")

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    _render_diagram_and_summary(inputs, results)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    _render_indicator_cards(results)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    _render_report_section(inputs, results, checks)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align:center; color:#4a5568; font-size:0.75rem;">'
        '吊耳计算器 v1.1 &nbsp;|&nbsp; 支持加强板有效厚度 &nbsp;|&nbsp; 仅供工程参考，最终设计须经专业工程师审核'
        '</p>',
        unsafe_allow_html=True,
    )


def _render_diagram_and_summary(inputs: SidebarInputs, results: dict) -> None:
    col_diagram, col_metrics = st.columns([2, 1])
    with col_diagram:
        st.markdown(
            '<div style="background:rgba(26,32,55,0.6); border:1px solid rgba(99,179,237,0.15); '
            'border-radius:12px; padding:0.8rem; text-align:center;">'
            '<p style="color:#63b3ed; font-size:0.85rem; font-weight:600; margin-bottom:0.3rem;">'
            '📐 吊耳几何示意图</p>'
            '<p style="color:#718096; font-size:0.7rem; margin-bottom:0;">'
            '图示随左侧参数实时更新</p></div>',
            unsafe_allow_html=True,
        )
        try:
            fig = draw_lug_diagram(inputs.w, inputs.r, inputs.h, inputs.d, inputs.t, inputs.tp, inputs.theta)
            st.pyplot(fig, width="stretch")
            plt.close(fig)
        except Exception as exc:
            st.error(f"预览图生成失败: {exc}")

    with col_metrics:
        st.metric("设计拉力 P", f"{results['p_design'] / 1000:.2f} kN", help="已含动载系数 Kd 和角度修正")
        st.metric("动载系数 Kd", f"{inputs.kd}")
        st.metric("吊索角度 θ", f"{inputs.theta}°")
        st.metric("安全系数 Ns", f"{inputs.ns}")
        if inputs.tp > 0:
            st.metric("有效厚度 t_eff", f"{results['t_eff']:.0f} mm", help=f"t + 2×tp = {inputs.t} + 2×{inputs.tp}")


def _render_indicator_cards(results: dict) -> None:
    st.subheader("📊 应力校验结果")
    indicators = [
        {"name": "① 销轴孔净截面拉应力", "symbol": "σ_t", "actual": results["metrics"]["tensile"]["value"], "allowable": results["metrics"]["tensile"]["allowable"], "unit": "MPa", "pass": results["metrics"]["tensile"]["passed"]},
        {"name": "② 孔端面双面剪切撕裂应力", "symbol": "τ_v", "actual": results["metrics"]["tear_out"]["value"], "allowable": results["metrics"]["tear_out"]["allowable"], "unit": "MPa", "pass": results["metrics"]["tear_out"]["passed"]},
        {"name": "③ 销轴孔承压应力", "symbol": "σ_b", "actual": results["metrics"]["bearing"]["value"], "allowable": results["metrics"]["bearing"]["allowable"], "unit": "MPa", "pass": results["metrics"]["bearing"]["passed"]},
        {"name": "④ 底部焊缝综合剪应力", "symbol": "τ_weld", "actual": results["metrics"]["weld"]["value"], "allowable": results["metrics"]["weld"]["allowable"], "unit": "MPa", "pass": results["metrics"]["weld"]["passed"]},
    ]

    cols = st.columns(2)
    for index, indicator in enumerate(indicators):
        pct = (indicator["actual"] / indicator["allowable"]) * 100
        badge = '<span class="status-badge-pass">✓ PASS</span>' if indicator["pass"] else '<span class="status-badge-fail">✗ FAIL</span>'
        card_class = "status-pass" if indicator["pass"] else "status-fail"
        bar_color = "#48bb78" if indicator["pass"] else "#fc8181"
        bar_pct = min(pct, 100)
        html = f"""
        <div class="status-card {card_class}">
            <div class="stress-name">{indicator['name']} &nbsp; {badge}</div>
            <div class="stress-values">
                <span class="stress-actual">{indicator['actual']:.2f}</span>
                <span class="stress-allowable">/ {indicator['allowable']:.2f} {indicator['unit']}<br>({indicator['symbol']})</span>
            </div>
            <div style="margin-top:0.6rem;">
                <div style="background:rgba(255,255,255,0.05); border-radius:4px; height:6px; overflow:hidden;">
                    <div style="background:{bar_color}; width:{bar_pct:.1f}%; height:100%; border-radius:4px; transition:width 0.5s;"></div>
                </div>
                <div style="font-size:0.72rem; color:#718096; margin-top:0.25rem;">利用率 {pct:.1f}%</div>
            </div>
        </div>
        """
        with cols[index % 2]:
            st.markdown(html, unsafe_allow_html=True)


def _render_report_section(inputs: SidebarInputs, results: dict, checks: list[bool]) -> None:
    st.markdown("---")
    col_title, col_btn = st.columns([0.8, 0.2])
    with col_title:
        st.subheader("📋 详细计算书")
    with col_btn:
        word_file = generate_word_report(inputs.to_report_params(), results)
        st.download_button(
            label="📥 导出 Word 报告",
            data=word_file,
            file_name="吊耳校验计算书_Lifting_Lug_Report.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            help="点击下载详细计算书至本地。由于网页应用特性，会调用浏览器的「另存为」对话框让您选择保存位置。",
        )

    with st.expander("展开查看完整计算过程（可截图存档）", expanded=True):
        st.markdown(_build_report_markdown(inputs, results, checks))
        st.markdown("---")
        df = pd.DataFrame(_build_summary_data(results, checks))
        st.markdown("#### 七、汇总表")
        st.dataframe(df, width="stretch", hide_index=True)


def _build_report_markdown(inputs: SidebarInputs, results: dict, checks: list[bool]) -> str:
    extra_note = ""
    if inputs.tp > 0:
        extra_note = (
            f"\n> **注：** 有效厚度 $t_{{eff}} = t + 2 \\times t_p = {inputs.t} + 2 \\times {inputs.tp} = {results['t_eff']:.0f}$ mm。"
            "应力计算（指标一~三）采用有效厚度，焊缝应力（指标四）仅通过主板传递。\n"
        )

    return f"""
#### 一、基本参数
| 参数 | 符号 | 数值 | 单位 |
|------|------|------|------|
| 单只吊耳受力 | $F_v$ | {inputs.fv_ton} t（{inputs.fv:.2f} kN） | — |
| 动载系数 | $K_d$ | {inputs.kd} | — |
| 吊索夹角 | $θ$ | {inputs.theta} | ° |
| 材料屈服强度 | $F_y$ | {inputs.fy} | MPa |
| 材料抗拉强度 | $F_u$ | {inputs.fu} | MPa |
| 结构安全系数 | $N_s$ | {inputs.ns} | — |
| 吊耳主板厚 | $t$ | {inputs.t} | mm |
| 单侧加强板厚 | $t_p$ | {inputs.tp} | mm |
| **有效厚度** | $t_{{eff}}$ | **{results['t_eff']:.0f}** | mm |
| 销轴孔孔径 | $d$ | {inputs.d} | mm |
| 销轴直径 | $d_p$ | {inputs.dp} | mm |
| 孔心至边缘距离 | $R$ | {inputs.r} | mm |
| 圆心到底边距离 | $H$ | {inputs.h} | mm |
| 角焊缝焊脚 | $h_f$ | {inputs.hf} | mm |
| 吊耳根部宽度 | $W$ | {inputs.w:.1f} | mm |
{extra_note}
---
#### 二、设计拉力换算

$$P = \\frac{{F_v \\times 1000 \\times K_d}}{{\\sin\\theta}} = \\frac{{{inputs.fv} \\times 1000 \\times {inputs.kd}}}{{\\sin({inputs.theta}°)}} = \\frac{{{inputs.fv * 1000 * inputs.kd:,.0f}}}{{{math.sin(math.radians(inputs.theta)):.4f}}} = \\mathbf{{{results['p_design']:,.0f} \\ \\text{{N}}}} = \\mathbf{{{results['p_design'] / 1000:.2f} \\ \\text{{kN}}}}$$

---
#### 三、指标一：销轴孔净截面拉应力 $\\sigma_t$

许用拉应力：${ALLOWABLE_RULES['tensile']['label']} = \\dfrac{{{inputs.fy}}}{{{inputs.ns}}} = {results['metrics']['tensile']['allowable']:.2f} \\ \\text{{MPa}}$

净截面面积：$A_{{net}} = 2 \\times t_{{eff}} \\times (R - d/2) = 2 \\times {results['t_eff']:.0f} \\times ({inputs.r} - {inputs.d}/2) = {results['areas']['net_area']:.2f} \\ \\text{{mm}}^2$

$$\\sigma_t = \\frac{{P}}{{A_{{net}}}} = \\frac{{{results['p_design']:,.0f}}}{{{results['areas']['net_area']:.2f}}} = \\mathbf{{{results['metrics']['tensile']['value']:.2f} \\ \\text{{MPa}}}}$$

校验：$\\sigma_t = {results['metrics']['tensile']['value']:.2f} \\ \\text{{MPa}} \\ {"\\le" if checks[0] else ">"} \\ [\\sigma_t] = {results['metrics']['tensile']['allowable']:.2f} \\ \\text{{MPa}}$ → {"**✅ 通过**" if checks[0] else "**❌ 不满足**"}

---
#### 四、指标二：孔端面双面剪切撕裂应力 $\\tau_v$

许用剪切应力：${ALLOWABLE_RULES['tear_out']['label']} = \\dfrac{{0.58 \\times {inputs.fy}}}{{{inputs.ns}}} = {results['metrics']['tear_out']['allowable']:.2f} \\ \\text{{MPa}}$

双面剪切面积：$A_{{shear}} = 2 \\times t_{{eff}} \\times (R - d/2) = 2 \\times {results['t_eff']:.0f} \\times ({inputs.r} - {inputs.d}/2) = {results['areas']['shear_area']:.2f} \\ \\text{{mm}}^2$

$$\\tau_v = \\frac{{P}}{{A_{{shear}}}} = \\frac{{{results['p_design']:,.0f}}}{{{results['areas']['shear_area']:.2f}}} = \\mathbf{{{results['metrics']['tear_out']['value']:.2f} \\ \\text{{MPa}}}}$$

校验：$\\tau_v = {results['metrics']['tear_out']['value']:.2f} \\ \\text{{MPa}} \\ {"\\le" if checks[1] else ">"} \\ [\\tau_v] = {results['metrics']['tear_out']['allowable']:.2f} \\ \\text{{MPa}}$ → {"**✅ 通过**" if checks[1] else "**❌ 不满足**"}

---
#### 五、指标三：销轴孔局部承压应力 $\\sigma_b$

许用承压应力：${ALLOWABLE_RULES['bearing']['label']} = \\dfrac{{1.25 \\times {inputs.fy}}}{{{inputs.ns}}} = {results['metrics']['bearing']['allowable']:.2f} \\ \\text{{MPa}}$

承压接触面积：$A_{{bearing}} = t_{{eff}} \\times d_p = {results['t_eff']:.0f} \\times {inputs.dp} = {results['areas']['bearing_area']:.2f} \\ \\text{{mm}}^2$

$$\\sigma_b = \\frac{{P}}{{A_{{bearing}}}} = \\frac{{{results['p_design']:,.0f}}}{{{results['areas']['bearing_area']:.2f}}} = \\mathbf{{{results['metrics']['bearing']['value']:.2f} \\ \\text{{MPa}}}}$$

校验：$\\sigma_b = {results['metrics']['bearing']['value']:.2f} \\ \\text{{MPa}} \\ {"\\le" if checks[2] else ">"} \\ [\\sigma_b] = {results['metrics']['bearing']['allowable']:.2f} \\ \\text{{MPa}}$ → {"**✅ 通过**" if checks[2] else "**❌ 不满足**"}

---
#### 六、指标四：底部焊缝综合剪应力 $\\tau_{{weld}}$

许用焊缝应力：${ALLOWABLE_RULES['weld']['label']} = 0.3 \\times {inputs.fu} = {results['metrics']['weld']['allowable']:.2f} \\ \\text{{MPa}}$

焊喉有效厚度：$a = 0.707 \\times h_f = 0.707 \\times {inputs.hf} = {results['areas']['weld_throat']:.3f} \\ \\text{{mm}}$

有效焊缝面积：$A_{{weld}} = 0.707 \\times h_f \\times 2W = {results['areas']['weld_throat']:.3f} \\times 2 \\times {inputs.w:.1f} = {results['areas']['weld_area']:.2f} \\ \\text{{mm}}^2$

$$\\tau_{{weld}} = \\frac{{P}}{{0.707 \\times h_f \\times 2W}} = \\frac{{{results['p_design']:,.0f}}}{{{results['areas']['weld_area']:.2f}}} = \\mathbf{{{results['metrics']['weld']['value']:.2f} \\ \\text{{MPa}}}}$$

校验：$\\tau_{{weld}} = {results['metrics']['weld']['value']:.2f} \\ \\text{{MPa}} \\ {"\\le" if checks[3] else ">"} \\ [\\tau_{{weld}}] = {results['metrics']['weld']['allowable']:.2f} \\ \\text{{MPa}}$ → {"**✅ 通过**" if checks[3] else "**❌ 不满足**"}
"""


def _build_summary_data(results: dict, checks: list[bool]) -> dict:
    return {
        "校验项目": ["① 拉应力 σ_t", "② 撕裂应力 τ_v", "③ 承压应力 σ_b", "④ 焊缝应力 τ_weld"],
        "实际值 (MPa)": [
            f"{results['metrics']['tensile']['value']:.2f}",
            f"{results['metrics']['tear_out']['value']:.2f}",
            f"{results['metrics']['bearing']['value']:.2f}",
            f"{results['metrics']['weld']['value']:.2f}",
        ],
        "许用值 (MPa)": [
            f"{results['metrics']['tensile']['allowable']:.2f}",
            f"{results['metrics']['tear_out']['allowable']:.2f}",
            f"{results['metrics']['bearing']['allowable']:.2f}",
            f"{results['metrics']['weld']['allowable']:.2f}",
        ],
        "利用率 (%)": [
            f"{results['metrics']['tensile']['value'] / results['metrics']['tensile']['allowable'] * 100:.1f}%",
            f"{results['metrics']['tear_out']['value'] / results['metrics']['tear_out']['allowable'] * 100:.1f}%",
            f"{results['metrics']['bearing']['value'] / results['metrics']['bearing']['allowable'] * 100:.1f}%",
            f"{results['metrics']['weld']['value'] / results['metrics']['weld']['allowable'] * 100:.1f}%",
        ],
        "结论": [
            "✅ 通过" if checks[0] else "❌ 不满足",
            "✅ 通过" if checks[1] else "❌ 不满足",
            "✅ 通过" if checks[2] else "❌ 不满足",
            "✅ 通过" if checks[3] else "❌ 不满足",
        ],
    }
