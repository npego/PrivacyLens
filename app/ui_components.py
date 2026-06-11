# ui_components.py — reusable Streamlit widgets

import re
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

from text_processing import clean_html, extract_text_from_file
from html_builders import build_segments_table_html


def get_text_from_input(prefix: str):
    input_mode = st.radio(
        "Input method",
        ["📋 Paste text", "📄 Upload file (PDF, TXT, HTML, CSV)"],
        horizontal=True,
        key=f"mode_{prefix}",
    )
    text = None
    if input_mode == "📋 Paste text":
        raw = st.text_area(
            "Paste the privacy policy text here", height=200, key=f"ta_{prefix}",
            placeholder="Paste plain text or raw HTML — HTML tags will be stripped automatically."
        )
        if raw.strip():
            if re.search(r"<[a-zA-Z][\s\S]*?>", raw):
                text = clean_html(raw)
                st.caption("🧹 HTML detected and cleaned automatically.")
            else:
                text = raw.strip()
    else:
        f = st.file_uploader(
            "Upload file", type=["pdf", "txt", "html", "htm", "csv"],
            key=f"file_{prefix}", help="Supported: PDF, TXT, HTML, HTM, CSV"
        )
        if f:
            ext = f.name.lower().split(".")[-1]
            text = extract_text_from_file(f)
            if not text or not text.strip():
                st.error("Could not extract text from this file." + (" It may be a scanned PDF." if ext == "pdf" else ""))
                text = None
            elif ext in ("html", "htm"):
                st.caption("🧹 HTML tags stripped automatically.")
    return text


def render_segments_section(df: pd.DataFrame) -> None:
    st.markdown("**Filter by category**")
    all_cats = sorted(df["Category"].unique().tolist())
    selected = st.multiselect("", all_cats, default=all_cats, key=f"filter_{id(df)}")
    filtered = df[df["Category"].isin(selected)] if selected else df
    table_html = build_segments_table_html(df, selected)
    row_height = min(len(filtered) * 50 + 80, 450)
    components.html(table_html, height=row_height, scrolling=False)
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("⬇ Download CSV", csv, "predictions.csv", "text/csv", key=f"dl_{id(df)}")