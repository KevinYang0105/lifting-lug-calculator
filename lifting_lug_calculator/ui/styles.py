"""Shared Streamlit styles."""

import streamlit as st


def apply_global_styles() -> None:
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(135deg, #0f1117 0%, #1a1d27 50%, #0f1117 100%); color: #e8eaf0; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #161b2e 0%, #1e2235 100%); border-right: 1px solid rgba(99, 179, 237, 0.15); }
.main-title { font-size: 2rem; font-weight: 700; background: linear-gradient(90deg, #63b3ed, #76e4f7, #9f7aea); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 0.25rem; }
.subtitle { color: #718096; font-size: 0.9rem; margin-bottom: 2rem; font-weight: 400; letter-spacing: 0.05em; }
.status-card { background: rgba(26, 32, 55, 0.8); border: 1px solid rgba(99, 179, 237, 0.1); border-radius: 12px; padding: 1.2rem 1.4rem; margin-bottom: 0.75rem; backdrop-filter: blur(10px); transition: all 0.2s ease; }
.status-card:hover { border-color: rgba(99, 179, 237, 0.3); transform: translateY(-1px); }
.status-pass { border-left: 4px solid #48bb78; background: rgba(72, 187, 120, 0.05); }
.status-fail { border-left: 4px solid #fc8181; background: rgba(252, 129, 129, 0.05); }
.stress-name { font-size: 0.85rem; color: #a0aec0; font-weight: 500; letter-spacing: 0.03em; margin-bottom: 0.5rem; }
.stress-values { display: flex; align-items: center; gap: 1rem; }
.stress-actual { font-size: 1.6rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; color: #e2e8f0; }
.stress-allowable { font-size: 0.8rem; color: #718096; }
.status-badge-pass { background: rgba(72, 187, 120, 0.15); color: #68d391; border: 1px solid rgba(72, 187, 120, 0.3); border-radius: 20px; padding: 0.2rem 0.8rem; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.05em; }
.status-badge-fail { background: rgba(252, 129, 129, 0.15); color: #fc8181; border: 1px solid rgba(252, 129, 129, 0.3); border-radius: 20px; padding: 0.2rem 0.8rem; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.05em; }
.section-divider { border: none; border-top: 1px solid rgba(99, 179, 237, 0.1); margin: 1.5rem 0; }
div[data-testid="stWidgetLabel"] p, div[data-testid="stWidgetLabel"] label, label span, .stCheckbox p { color: #f7fafc !important; font-weight: 500 !important; }
[data-testid="stMetric"] { background: rgba(26,32,55,0.5); border-radius: 8px; padding: 0.5rem; }
[data-testid="stMetricLabel"] p { color: #f7fafc !important; font-weight: 500 !important; }
[data-testid="stMetricLabel"] svg { fill: #f7fafc !important; color: #f7fafc !important; }
[data-testid="stMetricValue"] div { color: #ffffff !important; font-weight: 700 !important; }
div.stButton > button { background: linear-gradient(135deg, #3182ce, #2b6cb0); color: white; border: none; border-radius: 8px; padding: 0.5rem 1.5rem; font-weight: 600; width: 100%; transition: all 0.2s; }
div.stButton > button:hover { background: linear-gradient(135deg, #4299e1, #3182ce); transform: translateY(-1px); box-shadow: 0 4px 15px rgba(49,130,206,0.4); }
.sidebar-section-title { font-size: 0.7rem; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: #4299e1; margin: 1.2rem 0 0.5rem 0; }
[data-testid="stDownloadButton"] button { background: linear-gradient(135deg, #e0f2fe, #7dd3fc) !important; color: #0c4a6e !important; font-weight: 800 !important; font-size: 1rem !important; border: 2px solid #38bdf8 !important; border-radius: 8px !important; box-shadow: 0 4px 10px rgba(56, 189, 248, 0.4) !important; transition: all 0.2s ease !important; }
[data-testid="stDownloadButton"] button:hover { background: linear-gradient(135deg, #bae6fd, #38bdf8) !important; transform: translateY(-2px) !important; box-shadow: 0 6px 15px rgba(56, 189, 248, 0.6) !important; }
[data-testid="stExpander"] summary { background: linear-gradient(135deg, #e0f2fe, #7dd3fc) !important; border-radius: 8px !important; border: 1px solid #38bdf8 !important; padding: 0.5rem 1rem !important; margin-bottom: 0.5rem !important; }
[data-testid="stExpander"] summary p { color: #0c4a6e !important; font-weight: 800 !important; font-size: 1.05rem !important; }
[data-testid="stExpander"] summary svg { color: #0c4a6e !important; fill: #0c4a6e !important; }
</style>
""",
        unsafe_allow_html=True,
    )
