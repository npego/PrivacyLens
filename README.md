# PrivacyLens — GDPR Article 13 Completeness Checker

A web-based tool that automatically checks whether a privacy policy covers the mandatory disclosure requirements of **GDPR Article 13**. Built as a final project for AI for Business (BUSS305).

---

## What it does

PrivacyLens takes any privacy policy as input (pasted text, PDF, TXT, or HTML) and produces a structured completeness report:

- A **compliance score** showing how many of the 6 mandatory Article 13 requirements are covered
- A **colour-coded breakdown** of each requirement (Covered / Minimal / Missing)
- A **segment-by-segment classification** showing which parts of the policy address each legal obligation
- A **multi-policy comparison** mode for up to 3 policies side by side

> ⚠️ This tool checks whether topics are **mentioned**, not whether disclosures are legally adequate. It is a completeness checker, not a compliance certifier.

---

## Requirements

- Python 3.9 or higher
- No GPU required

---

## Installation

```bash
git clone https://github.com/npego/PrivacyLens.git
cd PrivacyLens
pip install -r requirements.txt
```

---

## Running the app

```bash
cd app
streamlit run app.py
```

Then open your browser at **http://localhost:8501**

---

## Project structure

```
PrivacyLens/
├── app/
│   ├── app.py              # Entry point, tab routing
│   ├── config.py           # GDPR requirements mapping, shared CSS
│   ├── model.py            # Model loading, classification, scoring
│   ├── text_processing.py  # Text ingestion, HTML cleaning, segmentation
│   ├── html_builders.py    # All HTML rendering components
│   └── ui_components.py    # Streamlit-specific rendering logic
├── models/
│   └── privacy_policy_classifier_model_a_v2_grid.joblib  # Trained model
└── requirements.txt
```

---

## Model

The classifier is a **TF-IDF + Logistic Regression** pipeline trained on the [OPP-115 corpus](https://usableprivacy.org/data) (115 privacy policies, 3,768 segments, 10 categories). It achieves **Macro-F1 = 0.6865** on a held-out test set of 23 policies.

---

## GDPR Article 13 requirements checked

| Requirement | Type |
|---|---|
| Purposes of data processing | Mandatory |
| Third-party sharing & recipients | Mandatory |
| Data retention period | Mandatory |
| Data security measures | Mandatory |
| Right to access, rectification & erasure | Mandatory |
| Right to object & withdraw consent | Mandatory |
| Notification of policy changes | Recommended |
| Special categories & specific audiences | Recommended |
| Do Not Track & online tracking | Recommended |

---

## Author

Natalia Pego Martínez — AI for Business, BUSS305