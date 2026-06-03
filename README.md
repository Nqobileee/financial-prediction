# FinHealth — Financial Health Prediction for Southern African SMEs

> Machine learning and interactive tooling for classifying MSME financial health (**Low**, **Medium**, **High**) using survey data from Eswatini, Lesotho, Malawi, and Zimbabwe.

---

## Overview

| Area | Purpose | README |
|------|---------|--------|
| [`financial-prediction-model/`](financial-prediction-model/README.md) | EDA, LightGBM training, submissions | ML workspace |
| [`src/`](src/README.md) | Next.js survey UI and demo API | Web app |
| [`CITATIONS.md`](CITATIONS.md) | Data attribution and licensing | — |

**Production classifier:** LightGBM v3 (Python). **Web app:** rule-based demo scorer unless an external ML API is connected.

**Dataset:** 9,618 labeled training rows, 39 features, imbalanced target (~65% Low, ~30% Medium, ~5% High).

---

## Research findings (summary)

Analysis in [`financial-prediction-model/eda/`](financial-prediction-model/eda/README.md) highlights the following.

### Data and target

- **Class imbalance** is severe (~13:1 between the largest and smallest class). Stratified K-fold is used for validation.
- **Geography matters:** Malawi skews Low; Eswatini shows relatively more High outcomes than other countries.
- **Missingness** is structured (often by product/country), not random — missing-count features help the model.

### Strongest signals

| Signal | Evidence |
|--------|----------|
| `funeral_insurance` | Highest Cramér's V (~0.55) and top mutual information |
| Insurance adoption (count) | Clear tiering toward Medium/High as current products increase |
| Financial services (mobile money, cards, loans, etc.) | More active services associate with better health |
| Formalization | Record-keeping and tax compliance support Medium/High |
| Country | Encoded market effects and interactions with insurance |

### Model performance (LightGBM, 5-fold OOF)

| Metric | Value |
|--------|-------|
| Accuracy | 0.874 |
| F1 (macro) | 0.805 |
| Macro ROC-AUC (one-vs-rest) | 0.944 |

Full parameter table: [`decision_parameters_summary.csv`](financial-prediction-model/eda/decision_parameters_summary.csv).

---

### Selected figures

**Target distribution** — majority Low; High is rare (~5%).

![Target distribution](financial-prediction-model/eda/figures/02_target_distribution_counts_and_percent.png)

**Country vs target** — regional mix differs materially.

![Target by country](financial-prediction-model/eda/figures/03_target_distribution_by_country_stacked.png)

**Top categorical predictors** — funeral and insurance-related fields dominate.

![Cramér's V with target](financial-prediction-model/eda/figures/08_top_categorical_cramers_v_with_target.png)

**Insurance adoption tiers** — more current insurance products align with better health bands.

![Insurance adoption](financial-prediction-model/eda/figures/11_insurance_adoption_tier_vs_target.png)

**OOF evaluation** — multiclass separation is strong on cross-validation.

![Confusion matrix](financial-prediction-model/eda/figures/17_confusion_matrix_lightgbm_oof.png)

![ROC curves](financial-prediction-model/eda/figures/18_roc_curves_ovr_lightgbm_oof.png)

All 19 charts: [`financial-prediction-model/eda/figures/`](financial-prediction-model/eda/figures/README.md).

---

## Machine learning

### Models used

| Version | Algorithm | Role |
|---------|-----------|------|
| **v3 (current)** | LightGBM multiclass | Main model — stratified 5-fold CV, data-driven features |
| v2, v1.x | Earlier runs | Archived in [`submissions/`](financial-prediction-model/submissions/README.md) |

| Artifact | Path |
|----------|------|
| Training notebook | [`models/financial_prediction_v3.ipynb`](financial-prediction-model/models/financial_prediction_v3.ipynb) |
| Training script | [`models/financial_prediction_v3.py`](financial-prediction-model/models/financial_prediction_v3.py) |
| Saved model | `financial-prediction-model/models/financial_prediction_v3_model.pkl` |
| Submission | `financial-prediction-model/submissions/financial_prediction_v3_submission.csv` |

### Project layout

```
financial-prediction/
├── financial-prediction-model/
│   ├── datasets/       README + Train/Test CSVs
│   ├── eda/            README + notebook + figures/
│   ├── models/         README + v3 train + .pkl
│   ├── submissions/    README + competition CSVs
│   └── scripts/        README + notebook generators
├── src/                README + Next.js app
└── CITATIONS.md
```

**Python stack:** pandas, NumPy, scikit-learn, LightGBM, matplotlib, seaborn, Jupyter.

---

## Web application

| Item | Detail |
|------|--------|
| Framework | Next.js, React, TypeScript, Tailwind CSS |
| API | `/api/health`, `/api/predict` |

See [`src/README.md`](src/README.md).

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

### ML

```bash
cd financial-prediction-model
pip install pandas numpy scikit-learn lightgbm matplotlib seaborn jupyter joblib scipy

jupyter notebook eda/comprehensive_eda.ipynb
python models/financial_prediction_v3.py
```

---

## Environment and secrets

`.env` files are gitignored. Use `.env.local` for local development; do not commit secrets.

---

## License and citation

Code: **MIT License** where applicable. Data: **Zindi** terms and **CC BY-SA 4.0** — see [`CITATIONS.md`](CITATIONS.md).

```
FinHealth: SME Financial Health Prediction Platform (2026).
Southern African MSME dataset — Eswatini, Zimbabwe, Malawi, Lesotho.
```

---

*Evidence-based financial health classification for Southern African MSMEs.*
