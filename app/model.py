# model.py — model loading, classification, GDPR compliance scoring

import joblib
import pandas as pd
import streamlit as st
from pathlib import Path

from text_processing import segment_text
from config import GDPR_REQUIREMENTS


@st.cache_resource
def load_model():
    model_path = (
        Path(__file__).parent.parent
        / "models"
        / "privacy_policy_classifier_model_a_v2_grid.joblib"
    )
    if not model_path.exists():
        return None
    return joblib.load(model_path)


def classify_policy(text: str, model) -> pd.DataFrame:
    segments = segment_text(text)
    if not segments:
        return pd.DataFrame()
    predictions = model.predict(segments)
    return pd.DataFrame({"Segment": segments, "Category": predictions})


def compute_compliance(df: pd.DataFrame) -> dict:
    if df.empty:
        return {}
    counts = df["Category"].value_counts().to_dict()
    result = {}
    for req in GDPR_REQUIREMENTS:
        total = sum(counts.get(cat, 0) for cat in req["categories"])
        status = "missing" if total == 0 else "partial" if total == 1 else "found"
        result[req["id"]] = {**req, "count": total, "status": status}
    return result


def compliance_score(comp: dict) -> tuple:
    required = [v for v in comp.values() if v["required"]]
    found = sum(1 for v in required if v["status"] in ("found", "partial"))
    pct = round(found / len(required) * 100) if required else 0
    return found, len(required), pct