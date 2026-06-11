# html_builders.py — HTML string builders rendered via components.html()

import pandas as pd
from config import SHARED_CSS, GDPR_REQUIREMENTS, CATEGORY_COLORS, POLICY_BAR_COLORS
from model import compliance_score


def _score_colors(pct: int) -> tuple:
    if pct >= 70:
        return "#1a7f37", "#e0f0e8", "#f0faf3"
    elif pct >= 40:
        return "#9a6700", "#fdf3d0", "#fffbeb"
    return "#cf222e", "#fde8e8", "#fff5f5"


def build_compliance_html(comp: dict) -> str:
    found, total, pct = compliance_score(comp)
    ring_color, ring_bg, inner_bg = _score_colors(pct)
    verdict = "Compliant" if pct >= 70 else "Partially compliant" if pct >= 40 else "Non-compliant"
    conic = f"conic-gradient({ring_color} {pct*3.6}deg, {ring_bg} 0)"

    html = SHARED_CSS + f"""
    <div class="score-container">
        <div class="score-ring" style="background:{conic}">
            <div style="width:80px;height:80px;background:{inner_bg};border-radius:50%;
                        display:flex;align-items:center;justify-content:center;
                        font-size:1.4rem;font-weight:700;color:{ring_color}">{pct}%</div>
        </div>
        <div>
            <div style="font-size:1.3rem;font-weight:700;color:#1a2340;margin-bottom:0.3rem">
                {found}/{total} mandatory requirements covered</div>
            <div style="color:#6b7a99;font-size:0.88rem;margin-bottom:0.5rem">GDPR Article 13 compliance assessment</div>
            <span style="background:{ring_color}1a;color:{ring_color};border:1px solid {ring_color}44;
                         padding:0.2rem 0.7rem;border-radius:20px;font-size:0.78rem;font-weight:700">{verdict}</span>
        </div>
    </div>
    <div class="section-title">Mandatory requirements (Art. 13)</div>"""

    for req_id, req in comp.items():
        if not req["required"]:
            continue
        s = req["status"]
        row_cls = "req-found" if s == "found" else "req-partial" if s == "partial" else "req-missing"
        dot_cls = "dot-green" if s == "found" else "dot-yellow" if s == "partial" else "dot-red"
        sc = "#1a7f37" if s == "found" else "#9a6700" if s == "partial" else "#cf222e"
        st_txt = "✓ Covered" if s == "found" else "⚠ Minimal" if s == "partial" else "✗ Missing"
        ct = f"{req['count']} segments" if req["count"] > 0 else "—"
        html += f'<div class="req-row {row_cls}"><div class="req-dot {dot_cls}"></div><div class="req-name">{req["name"]}</div><div class="req-art">{req["article"]}</div><div class="req-count">{ct}</div><span style="color:{sc};font-weight:700;font-size:0.82rem">{st_txt}</span></div>'

    html += '<div class="section-title" style="margin-top:1.25rem">Recommended provisions</div>'
    for req_id, req in comp.items():
        if req["required"]:
            continue
        s = req["status"]
        row_cls = "req-found" if s == "found" else "req-partial" if s == "partial" else "req-missing"
        dot_cls = "dot-green" if s == "found" else "dot-yellow" if s == "partial" else "dot-red"
        ct = f"{req['count']} segments" if req["count"] > 0 else "—"
        html += f'<div class="req-row {row_cls}" style="opacity:0.8"><div class="req-dot {dot_cls}"></div><div class="req-name">{req["name"]}</div><div class="req-art">{req["article"]}</div><div class="req-count">{ct}</div></div>'
    return html


def build_category_bars_html(df: pd.DataFrame, max_count: int) -> str:
    cat_counts = df["Category"].value_counts().reset_index()
    cat_counts.columns = ["Category", "Count"]
    bars = ""
    for _, row in cat_counts.iterrows():
        pct_bar = row["Count"] / max_count * 100 if max_count > 0 else 0
        color = CATEGORY_COLORS.get(row["Category"], "#6b7a99")
        bars += f'<div style="margin-bottom:0.65rem"><div style="display:flex;justify-content:space-between;font-size:0.82rem;margin-bottom:4px"><span style="color:#1a2340;font-weight:500">{row["Category"]}</span><span style="color:#6b7a99;font-family:monospace">{row["Count"]}</span></div><div style="background:#e8ecf4;border-radius:4px;height:7px"><div style="width:{pct_bar:.1f}%;height:7px;border-radius:4px;background:{color}"></div></div></div>'
    return SHARED_CSS + f'<div>{bars}</div>'


def build_stats_html(df: pd.DataFrame, pct: int) -> str:
    color_stat, _, _ = _score_colors(pct)
    return SHARED_CSS + f'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;text-align:center;background:#f5f7fa;border:1px solid #d0d7e3;border-radius:10px;padding:1.25rem"><div><div style="font-size:2rem;font-weight:700;color:#003399">{len(df)}</div><div style="color:#6b7a99;font-size:0.78rem">Segments</div></div><div><div style="font-size:2rem;font-weight:700;color:#003399">{df["Category"].nunique()}</div><div style="color:#6b7a99;font-size:0.78rem">Categories</div></div><div><div style="font-size:2rem;font-weight:700;color:{color_stat}">{pct}%</div><div style="color:#6b7a99;font-size:0.78rem">Compliance</div></div></div>'


def build_segments_table_html(df: pd.DataFrame, selected_cats: list) -> str:
    filtered = df[df["Category"].isin(selected_cats)] if selected_cats else df
    rows = ""
    for _, row in filtered.iterrows():
        cat = row["Category"]
        color = CATEGORY_COLORS.get(cat, "#6b7a99")
        snippet = row["Segment"][:220] + ("…" if len(row["Segment"]) > 220 else "")
        snippet = snippet.replace("<", "&lt;").replace(">", "&gt;")
        rows += f'<tr><td style="padding:0.6rem 1rem;color:#1a2340;font-size:0.84rem;border-bottom:1px solid #d0d7e3;max-width:600px;vertical-align:top">{snippet}</td><td style="padding:0.6rem 1rem;border-bottom:1px solid #d0d7e3;white-space:nowrap;vertical-align:top"><span class="badge" style="background:{color}15;color:{color};border:1px solid {color}33">{cat}</span></td></tr>'
    return SHARED_CSS + f'<div style="max-height:400px;overflow-y:auto;border:1px solid #d0d7e3;border-radius:10px"><table style="width:100%;border-collapse:collapse"><thead><tr style="background:#003399;position:sticky;top:0"><th style="padding:0.75rem 1rem;text-align:left;color:rgba(255,255,255,0.85);font-size:0.72rem;text-transform:uppercase;letter-spacing:0.07em">Segment text</th><th style="padding:0.75rem 1rem;text-align:left;color:rgba(255,255,255,0.85);font-size:0.72rem;text-transform:uppercase;letter-spacing:0.07em">Category</th></tr></thead><tbody>{rows}</tbody></table></div>'


def build_comparison_table_html(all_compliance: list, policy_names: list, n: int) -> str:
    grid_cols = "2fr " + " ".join(["1fr"] * n)
    header_cells = "".join(f'<div style="text-align:center">{policy_names[i]}</div>' for i in range(n))
    rows = ""
    for req in GDPR_REQUIREMENTS:
        req_id = req["id"]
        badge = '<span style="font-size:0.68rem;color:#cf222e;margin-left:6px;font-weight:700">REQUIRED</span>' if req["required"] else ""
        cells = ""
        for i in range(n):
            status = all_compliance[i][req_id]["status"]
            count = all_compliance[i][req_id]["count"]
            icon = "✓" if status == "found" else "⚠" if status == "partial" else "✗"
            color = "#1a7f37" if status == "found" else "#9a6700" if status == "partial" else "#cf222e"
            count_str = str(count) if count else ""
            cells += f'<div style="text-align:center;color:{color};font-weight:700;font-size:1rem">{icon}<span style="color:#6b7a99;font-size:0.72rem;font-family:monospace;margin-left:4px">{count_str}</span></div>'
        rows += f'<div class="comp-row" style="grid-template-columns:{grid_cols}"><div style="color:#1a2340;font-size:0.85rem">{req["name"]}{badge}<div style="color:#6b7a99;font-size:0.72rem;font-family:monospace">{req["article"]}</div></div>{cells}</div>'
    return SHARED_CSS + f'<div class="comp-header" style="grid-template-columns:{grid_cols}"><div>Requirement</div>{header_cells}</div>{rows}'


def build_comparison_bars_html(all_dfs: list, policy_names: list, n: int) -> str:
    all_cats = sorted(set(cat for df in all_dfs for cat in df["Category"].unique()))
    max_any = max((df["Category"].value_counts().max() for df in all_dfs if not df.empty), default=1)
    html = SHARED_CSS
    for cat in all_cats:
        color_cat = CATEGORY_COLORS.get(cat, "#6b7a99")
        html += f'<div style="margin-bottom:1.1rem"><div style="font-size:0.82rem;font-weight:700;color:{color_cat};margin-bottom:6px">{cat}</div>'
        for i in range(n):
            cnt = int(all_dfs[i]["Category"].value_counts().get(cat, 0))
            bar_pct = cnt / max_any * 100 if max_any > 0 else 0
            pcol = POLICY_BAR_COLORS[i % len(POLICY_BAR_COLORS)]
            html += f'<div style="display:flex;align-items:center;gap:10px;font-size:0.8rem;margin-bottom:5px"><span style="color:#6b7a99;width:90px;flex-shrink:0;font-weight:600">{policy_names[i]}</span><div style="flex:1;background:#e8ecf4;border-radius:3px;height:6px"><div style="width:{bar_pct:.1f}%;height:6px;border-radius:3px;background:{pcol}"></div></div><span style="color:#6b7a99;font-family:monospace;width:24px;text-align:right">{cnt}</span></div>'
        html += '</div>'
    return html


def build_score_overview_html(all_scores: list, policy_names: list, n: int) -> str:
    cols_html = ""
    for i in range(n):
        found, total, pct = all_scores[i]
        color, _, _ = _score_colors(pct)
        verdict = "Compliant" if pct >= 70 else "Partial" if pct >= 40 else "Non-compliant"
        top_color = POLICY_BAR_COLORS[i % len(POLICY_BAR_COLORS)]
        cols_html += f'<div style="background:#f5f7fa;border:1px solid #d0d7e3;border-top:4px solid {top_color};border-radius:10px;padding:1.25rem;text-align:center"><div style="font-size:0.88rem;font-weight:700;color:#6b7a99;margin-bottom:0.5rem">{policy_names[i]}</div><div style="font-size:3rem;font-weight:700;color:{color}">{pct}%</div><div style="color:#6b7a99;font-size:0.82rem;margin-bottom:0.4rem">{found}/{total} mandatory</div><span style="background:{color}1a;color:{color};border:1px solid {color}33;padding:0.15rem 0.6rem;border-radius:20px;font-size:0.75rem;font-weight:700">{verdict}</span></div>'
    grid = " ".join(["1fr"] * n)
    return SHARED_CSS + f'<div style="display:grid;grid-template-columns:{grid};gap:1rem">{cols_html}</div>'