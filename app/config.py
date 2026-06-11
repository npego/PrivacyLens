# config.py — constants, colors, CSS

GDPR_REQUIREMENTS = [
    {"id": "collection_purposes", "name": "Purposes of data processing", "article": "Art. 13(1)(c)", "categories": ["First Party Collection/Use"], "required": True},
    {"id": "third_parties", "name": "Third party sharing & recipients", "article": "Art. 13(1)(e)", "categories": ["Third Party Sharing/Collection"], "required": True},
    {"id": "retention", "name": "Data retention period", "article": "Art. 13(2)(a)", "categories": ["Data Retention"], "required": True},
    {"id": "security", "name": "Data security measures", "article": "Art. 13 / Art. 32", "categories": ["Data Security"], "required": True},
    {"id": "user_rights", "name": "Right to access, rectification & erasure", "article": "Art. 13(2)(b)", "categories": ["User Access, Edit and Deletion"], "required": True},
    {"id": "user_choice", "name": "Right to object & withdraw consent", "article": "Art. 13(2)(c)(d)", "categories": ["User Choice/Control"], "required": True},
    {"id": "policy_changes", "name": "Notification of policy changes", "article": "Art. 13 / best practice", "categories": ["Policy Change"], "required": False},
    {"id": "specific_audiences", "name": "Special categories & specific audiences", "article": "Art. 13 / Art. 9", "categories": ["International and Specific Audiences"], "required": False},
    {"id": "do_not_track", "name": "Do Not Track & online tracking", "article": "Art. 13 / ePrivacy", "categories": ["Do Not Track"], "required": False},
]

CATEGORY_COLORS = {
    "First Party Collection/Use":            "#0052cc",
    "Third Party Sharing/Collection":        "#6435c9",
    "User Choice/Control":                   "#e07b00",
    "User Access, Edit and Deletion":        "#1a7f37",
    "Data Retention":                        "#9a6700",
    "Data Security":                         "#0e7c61",
    "Policy Change":                         "#0066aa",
    "Do Not Track":                          "#b85c00",
    "International and Specific Audiences":  "#c0392b",
    "Other":                                 "#6b7a99",
}

POLICY_BAR_COLORS = ["#003399", "#0e7c61", "#9a6700"]

SHARED_CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;600;700&family=Source+Code+Pro:wght@400;500&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Source Sans 3', sans-serif; background: transparent; color: #1a2340; }
.section-title { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #003399; border-bottom: 2px solid #FFCC00; display: inline-block; padding-bottom: 2px; margin-bottom: 0.75rem; }
.card { background: #f5f7fa; border: 1px solid #d0d7e3; border-radius: 10px; padding: 1.25rem; margin-bottom: 1rem; }
.card-blue { background: #f0f4ff; border: 1px solid #c0cef5; border-left: 4px solid #003399; border-radius: 10px; padding: 1.25rem 1.5rem; margin-bottom: 1rem; }
.badge { display: inline-block; padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.72rem; font-weight: 600; white-space: nowrap; }
.req-row { display: flex; align-items: center; gap: 0.75rem; padding: 0.6rem 1rem; border-radius: 8px; margin-bottom: 0.4rem; font-size: 0.88rem; }
.req-found   { background: #f0faf3; border: 1px solid #c6e8ce; }
.req-partial { background: #fffbeb; border: 1px solid #f5e09a; }
.req-missing { background: #fff5f5; border: 1px solid #fac5c5; }
.req-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.dot-green  { background: #1a7f37; }
.dot-yellow { background: #9a6700; }
.dot-red    { background: #cf222e; }
.req-name  { flex: 1; color: #1a2340; font-weight: 600; }
.req-art   { color: #6b7a99; font-size: 0.72rem; font-weight: 600; font-family: 'Source Code Pro', monospace; }
.req-count { color: #6b7a99; font-family: 'Source Code Pro', monospace; font-size: 0.78rem; }
.score-container { display: flex; align-items: center; gap: 2rem; padding: 1.5rem; background: #f5f7fa; border: 1px solid #d0d7e3; border-radius: 10px; margin-bottom: 1rem; }
.score-ring { width: 100px; height: 100px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.6rem; font-weight: 700; flex-shrink: 0; }
.comp-header { display: grid; gap: 1rem; padding: 0.75rem 1rem; background: #003399; border-radius: 8px 8px 0 0; font-weight: 600; font-size: 0.8rem; color: rgba(255,255,255,0.85); text-transform: uppercase; letter-spacing: 0.05em; }
.comp-row { display: grid; gap: 1rem; padding: 0.6rem 1rem; border-bottom: 1px solid #d0d7e3; font-size: 0.85rem; align-items: center; }
.comp-row:hover { background: #f5f7fa; }
</style>"""

STREAMLIT_CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; background-color: #ffffff; color: #1a2340; }
.stApp { background-color: #ffffff; }
#MainMenu, footer, header { visibility: hidden; }

/* Full width with no side padding so top bar and hero reach the edges */
.block-container { padding: 0 0 3rem !important; max-width: 100% !important; }

/* Inner content padding — applied manually in tabs */
.content-pad { padding: 0 3rem; }

/* Tabs — bigger and more spaced */
.stTabs { padding: 0 3rem; margin-top: 1.5rem; }
.stTabs [data-baseweb="tab-list"] {
    background: #f5f7fa;
    border-radius: 12px;
    padding: 6px;
    gap: 16px;
    border: 1px solid #d0d7e3;
    width: fit-content;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #6b7a99;
    font-weight: 600;
    font-size: 1rem !important;
    padding: 0.65rem 2.5rem !important;
    min-width: 200px;
    text-align: center;
}
.stTabs [aria-selected="true"] { background: #003399 !important; color: white !important; }

/* Tab content padding */
.stTabs [data-baseweb="tab-panel"] { padding: 0 3rem; }

/* Inputs */
.stFileUploader > div { background: #f5f7fa !important; border: 1px dashed #d0d7e3 !important; border-radius: 10px !important; }
.stTextArea textarea { background: #f5f7fa !important; border: 1px solid #d0d7e3 !important; color: #1a2340 !important; font-size: 0.85rem !important; }
.stButton button { background: #003399 !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important; padding: 0.5rem 2rem !important; }
.stButton button:hover { opacity: 0.85 !important; }
.stDownloadButton button { background: #f5f7fa !important; color: #003399 !important; border: 1px solid #d0d7e3 !important; border-radius: 8px !important; font-weight: 600 !important; }
.divider { border: none; border-top: 1px solid #d0d7e3; margin: 1.5rem 0; }
</style>"""