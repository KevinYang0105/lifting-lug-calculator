"""Streamlit app orchestration."""

import streamlit as st

from lifting_lug_calculator.core import calculate_lug_stresses_from_inputs
from lifting_lug_calculator.ui.display import render_header, render_results, render_validation_errors
from lifting_lug_calculator.ui.inputs import render_sidebar
from lifting_lug_calculator.ui.styles import apply_global_styles


def run_app() -> None:
    st.set_page_config(
        page_title="吊耳计算器 | Lifting Lug Calculator",
        page_icon="🔩",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    apply_global_styles()
    inputs = render_sidebar()
    render_header()
    render_validation_errors(inputs)
    results = calculate_lug_stresses_from_inputs(inputs.to_calculation_inputs()).to_dict()
    render_results(inputs, results)
