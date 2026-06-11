# app.py — entry point

import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import streamlit as st
import streamlit.components.v1 as components

from config import SHARED_CSS, STREAMLIT_CSS, GDPR_REQUIREMENTS
from model import load_model, classify_policy, compute_compliance, compliance_score
from html_builders import (
    build_compliance_html,
    build_category_bars_html,
    build_stats_html,
    build_comparison_table_html,
    build_comparison_bars_html,
    build_score_overview_html,
)
from ui_components import get_text_from_input, render_segments_section

st.set_page_config(
    page_title="PrivacyLens — GDPR Article 13 Completeness Checker",
    page_icon="🇪🇺",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(STREAMLIT_CSS, unsafe_allow_html=True)

MODEL = load_model()

# ── EU top bar — full width ───────────────────────────────────────────────────
components.html(SHARED_CSS + """
<div style="background:#003399;padding:0.55rem 3rem;display:flex;align-items:center;gap:1rem;width:100%">
    <span style="font-size:1rem;letter-spacing:3px;color:#FFCC00">★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★ ★</span>
    <span style="color:rgba(255,255,255,0.8);font-size:0.75rem;font-weight:400;
                 letter-spacing:0.06em;text-transform:uppercase">
        GDPR Article 13 Completeness Checker &nbsp;·&nbsp;
        General Data Protection Regulation (EU) 2016/679
    </span>
</div>
""", height=52, scrolling=False)

# ── Hero — full width ─────────────────────────────────────────────────────────
components.html(SHARED_CSS + """
<div style="background:linear-gradient(135deg,#003399 0%,#0052cc 60%,#0066ff 100%);
            padding:3rem 3rem 2.5rem;position:relative;overflow:hidden;width:100%">
    <div style="position:absolute;right:-60px;top:-60px;width:300px;height:300px;
                background:rgba(255,204,0,0.08);border-radius:50%"></div>
    <div style="position:absolute;right:80px;bottom:-80px;width:200px;height:200px;
                background:rgba(255,204,0,0.05);border-radius:50%"></div>
    <div style="position:relative;z-index:1">
        <div style="display:inline-flex;align-items:center;gap:0.4rem;
                    background:rgba(255,204,0,0.15);border:1px solid rgba(255,204,0,0.3);
                    color:#FFCC00;padding:0.25rem 0.75rem;border-radius:20px;
                    font-size:0.75rem;font-weight:600;letter-spacing:0.05em;
                    text-transform:uppercase;margin-bottom:1rem">
            🇪🇺 &nbsp; GDPR Article 13
        </div>
        <h1 style="font-size:2.6rem;font-weight:700;color:#ffffff;
                   letter-spacing:-0.02em;margin-bottom:0.4rem">
            Privacy<span style="color:#FFCC00">Lens</span>
        </h1>
        <p style="color:rgba(255,255,255,0.75);font-size:1rem;font-weight:300;max-width:900px">
            Upload a privacy policy and instantly verify its completeness against GDPR Article 13 — the regulation that defines what every privacy policy must disclose. Compare up to three policies side by side.
        </p>
    </div>
</div>
""", height=210, scrolling=False)

if MODEL is None:
    st.error("⚠️ Model not found. Make sure the .joblib file exists in the models/ folder.")
    st.stop()

# ── Build requirements panel HTML ─────────────────────────────────────────────
def build_requirements_panel_html() -> str:
    mandatory = [r for r in GDPR_REQUIREMENTS if r["required"]]
    recommended = [r for r in GDPR_REQUIREMENTS if not r["required"]]

    rows_mandatory = ""
    for req in mandatory:
        rows_mandatory += f"""
        <div style="display:flex;align-items:center;gap:0.6rem;
                    padding:0.45rem 0;border-bottom:1px solid #e8ecf4">
            <div style="width:7px;height:7px;border-radius:50%;
                        background:#003399;flex-shrink:0"></div>
            <div style="font-size:0.82rem;color:#1a2340;font-weight:500">
                {req['name']}</div>
        </div>"""

    rows_recommended = ""
    for req in recommended:
        rows_recommended += f"""
        <div style="display:flex;align-items:center;gap:0.6rem;
                    padding:0.45rem 0;border-bottom:1px solid #e8ecf4;opacity:0.7">
            <div style="width:7px;height:7px;border-radius:50%;
                        background:#d0d7e3;flex-shrink:0"></div>
            <div style="font-size:0.82rem;color:#1a2340;font-weight:500">
                {req['name']}</div>
        </div>"""

    return SHARED_CSS + f"""
    <div style="background:#f0f4ff;border:1px solid #c0cef5;border-left:4px solid #003399;
                border-radius:10px;padding:1.25rem 1.5rem">
        <div style="font-weight:700;color:#003399;font-size:0.88rem;
                    margin-bottom:0.75rem;text-transform:uppercase;
                    letter-spacing:0.05em">What this tool checks</div>

        <div style="font-size:0.7rem;font-weight:700;color:#003399;
                    text-transform:uppercase;letter-spacing:0.08em;
                    margin-bottom:0.4rem">
            ● Mandatory — Art. 13 GDPR</div>
        {rows_mandatory}

        <div style="font-size:0.7rem;font-weight:700;color:#6b7a99;
                    text-transform:uppercase;letter-spacing:0.08em;
                    margin-top:0.75rem;margin-bottom:0.4rem">
            ○ Recommended</div>
        {rows_recommended}

        <div style="margin-top:0.9rem;padding-top:0.75rem;
                    border-top:1px solid #c0cef5;font-size:0.75rem;color:#6b7a99;
                    line-height:1.5">
            The tool checks whether each topic is <em>mentioned</em> in the policy,
            not whether it is legally sufficient.
        </div>
    </div>"""

tab1, tab2 = st.tabs(["📋  Analyze a Policy", "⚖️  Compare Policies"])

# ── TAB 1 ─────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    col_input, col_info = st.columns([3, 1], gap="large")

    with col_input:
        text = get_text_from_input("single")

    with col_info:
        n_req = len(GDPR_REQUIREMENTS)
        components.html(
            build_requirements_panel_html(),
            height=n_req * 46 + 180,
            scrolling=False,
        )

    if text:
        if st.button("🔍  Analyze Policy", key="btn_single"):
            with st.spinner("Segmenting and classifying…"):
                df = classify_policy(text, MODEL)
            if df.empty:
                st.warning("No segments could be extracted. Please check the input text.")
            else:
                comp = compute_compliance(df)
                found, total, pct = compliance_score(comp)
                st.markdown("<hr class='divider'>", unsafe_allow_html=True)
                col_left, col_right = st.columns([1, 1], gap="large")
                with col_left:
                    components.html(
                        build_compliance_html(comp),
                        height=len(GDPR_REQUIREMENTS) * 52 + 220,
                        scrolling=False,
                    )
                with col_right:
                    st.markdown("**Category distribution**")
                    max_c = int(df["Category"].value_counts().max())
                    components.html(
                        build_category_bars_html(df, max_c),
                        height=df["Category"].nunique() * 52 + 30,
                        scrolling=False,
                    )
                    components.html(build_stats_html(df, pct), height=110, scrolling=False)
                st.markdown("<hr class='divider'>", unsafe_allow_html=True)
                st.markdown("**Classified segments**")
                render_segments_section(df)

# ── TAB 2 ─────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    n_policies = st.radio(
        "Number of policies to compare", [2, 3],
        horizontal=True, key="n_pol",
    )
    policy_names, policy_texts = [], []
    cols = st.columns(n_policies, gap="large")
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"**Policy {i+1}**")
            name = st.text_input("Policy name", value=f"Policy {i+1}", key=f"name_{i}")
            text_i = get_text_from_input(f"comp_{i}")
            policy_names.append(name)
            policy_texts.append(text_i)

    if all(t is not None for t in policy_texts):
        if st.button("⚖️  Compare Policies", key="btn_compare"):
            with st.spinner("Analyzing all policies…"):
                all_dfs = [classify_policy(t, MODEL) for t in policy_texts]
                all_compliance = [compute_compliance(df) for df in all_dfs]
                all_scores = [compliance_score(c) for c in all_compliance]

            st.markdown("<hr class='divider'>", unsafe_allow_html=True)

            st.markdown("**Compliance score overview**")
            components.html(
                build_score_overview_html(all_scores, policy_names, n_policies),
                height=170, scrolling=False,
            )
            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("**Requirement comparison**")
            components.html(
                build_comparison_table_html(all_compliance, policy_names, n_policies),
                height=len(GDPR_REQUIREMENTS) * 58 + 60, scrolling=False,
            )
            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown("**Segments per category**")
            all_cats_count = len(
                set(cat for df in all_dfs for cat in df["Category"].unique())
            )
            components.html(
                build_comparison_bars_html(all_dfs, policy_names, n_policies),
                height=all_cats_count * (n_policies * 28 + 30) + 40,
                scrolling=False,
            )

            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("**Individual policy details**")
            for i in range(n_policies):
                with st.expander(f"📄 {policy_names[i]} — full breakdown"):
                    components.html(
                        build_compliance_html(all_compliance[i]),
                        height=len(GDPR_REQUIREMENTS) * 52 + 220,
                        scrolling=False,
                    )
                    st.markdown("**Classified segments**")
                    render_segments_section(all_dfs[i])