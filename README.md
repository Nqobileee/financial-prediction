# FinHealth — Financial Health Prediction for Southern African SMEs

> Machine learning and interactive tooling for classifying MSME financial health (**Low**, **Medium**, **High**) using survey data from Eswatini, Lesotho, Malawi, and Zimbabwe.

---

## Overview

This repository combines two parts:

| Area | Purpose |
|------|---------|
| **`financial-prediction-model/`** | Training pipeline, EDA, competition submissions |
| **Root (`src/`)** | Next.js web app with survey UI and a demo prediction API |

The **production classifier** is **LightGBM v3** (Python). The **web app** uses a separate rule-based scorer for demos when the ML API is not wired in.

**Dataset:** 9,618 labeled training rows, 39 features, imbalanced target (~65% Low, ~30% Medium, ~5% High). See [`CITATIONS.md`](CITATIONS.md) for data attribution and licensing.

---

## Machine learning

### Models used

| Version | Algorithm | Role |
|---------|-----------|------|
| **v3 (current)** | LightGBM multiclass | Main model — stratified 5-fold CV, data-driven feature engineering |
| v2 | Earlier iteration | Archived submission in `submissions/` |
| v1 / v1.1 / v1.2 | Earlier iterations | Archived submissions in `submissions/` |

**v3 highlights**

- **Target:** Financial Health Index → `Low` / `Medium` / `High`
- **Features:** Raw survey fields plus engineered signals (insurance tiers, funeral insurance encoding, financial-service adoption, country effects, formalization, missingness patterns, attitudes, numeric ratios)
- **Validation:** Stratified K-fold (5), early stopping per fold
- **Artifacts:** `models/financial_prediction_v3_model.pkl`, `submissions/financial_prediction_v3_submission.csv`

**Reported EDA / CV benchmarks** (from latest EDA run; see `eda/decision_parameters_summary.csv`):

| Metric | Value |
|--------|-------|
| OOF accuracy (LightGBM) | 0.874 |
| OOF F1 (macro) | 0.805 |
| Macro ROC-AUC (one-vs-rest) | 0.944 |
| Strongest categorical signal | `funeral_insurance` (Cramér's V ≈ 0.55) |

---

### Exploratory data analysis (EDA)

| Item | Location |
|------|----------|
| Notebook | [`financial-prediction-model/eda/comprehensive_eda.ipynb`](financial-prediction-model/eda/comprehensive_eda.ipynb) |
| Figures (19 charts) | [`financial-prediction-model/eda/figures/`](financial-prediction-model/eda/figures/) |
| Findings summary | [`financial-prediction-model/eda/decision_parameters_summary.csv`](financial-prediction-model/eda/decision_parameters_summary.csv) |

The EDA notebook covers missingness, target balance, numeric and categorical associations (chi-square, Cramér's V, mutual information), insurance and financial-service tiers, engineered-feature analysis, Random Forest and LightGBM importance, confusion matrix, and ROC curves.

**Rerun behavior:** Skips plotting when a figure PNG already exists; displays cached images inline and in the figure gallery. Delete a PNG (or `decision_parameters_summary.csv`) to regenerate it.

---

### Model training notebook

| Item | Location |
|------|----------|
| Notebook | [`financial-prediction-model/models/financial_prediction_v3.ipynb`](financial-prediction-model/models/financial_prediction_v3.ipynb) |
| Script (same logic) | [`financial-prediction-model/models/financial_prediction_v3.py`](financial-prediction-model/models/financial_prediction_v3.py) |

Run the notebook or script from `financial-prediction-model/` so paths resolve to `datasets/`, `models/`, and `submissions/`.

---

### ML project layout

```
financial-prediction-model/
├── datasets/          Train.csv, Test.csv, VariableDefinitions.csv
├── eda/               comprehensive_eda.ipynb, figures/, decision_parameters_summary.csv
├── models/            v3 notebook, script, saved .pkl
├── submissions/       v1–v3 competition CSVs
└── scripts/           Notebook generators (optional maintenance)
```

**Python stack:** pandas, NumPy, scikit-learn, LightGBM, matplotlib, seaborn, Jupyter.

---

## Web application

| Item | Detail |
|------|--------|
| Framework | Next.js (App Router), React, TypeScript |
| Styling | Tailwind CSS |
| API | `/api/health`, `/api/predict` (demo heuristic scorer) |

The UI supports survey-style input and results views. Connect `NEXT_PUBLIC_API_URL` via a local `.env` file if you add an external ML backend (env files are gitignored; use `.env.example` as a template if you add one).

---

## Getting started

### Web app

```bash
git clone <repository-url>
cd financial-prediction
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

### ML notebooks

```bash
cd financial-prediction-model
pip install pandas numpy scikit-learn lightgbm matplotlib seaborn jupyter joblib scipy

# EDA (generates figures/ and decision_parameters_summary.csv)
python -m jupyter notebook eda/comprehensive_eda.ipynb

# Train v3 and write model + submission
python models/financial_prediction_v3.py
# or open models/financial_prediction_v3.ipynb
```

---

## Environment and secrets

All `.env` files are ignored by git (see [`.gitignore`](.gitignore)). Do not commit API keys or production URLs. Copy variables from your team template into `.env.local` for local development.

---

## License and citation

Project code is open source under the **MIT License** unless noted otherwise. Training data usage follows **Zindi** competition terms and **CC BY-SA 4.0** — see [`CITATIONS.md`](CITATIONS.md).

**Suggested citation**

```
FinHealth: SME Financial Health Prediction Platform (2026).
Southern African MSME dataset — Eswatini, Zimbabwe, Malawi, Lesotho.
```

---

*Evidence-based financial health classification for Southern African MSMEs.*
