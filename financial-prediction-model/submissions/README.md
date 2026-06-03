# Submissions

Competition-format prediction files (`ID`, `Target`) for the Zindi MSME Financial Health challenge.

| File | Version | Notes |
|------|---------|--------|
| `financial_prediction_v3_submission.csv` | **v3 (current)** | LightGBM + v3 feature engineering |
| `financial_prediction_v2_submission.csv` | v2 | Earlier iteration |
| `financial_prediction_v1_submission.csv` | v1 | Baseline |
| `financial_prediction_v1_1_v1.1d_submission.csv` | v1.1 | Variant run |
| `financial_prediction_v1_2_v1.2a_submission.csv` | v1.2 | Variant run |

---

## Format

```csv
ID,Target
ID_3AU4SV,Low
...
```

`Target` must be one of: `Low`, `Medium`, `High`.

---

## Regenerate v3

```bash
cd financial-prediction-model
python models/financial_prediction_v3.py
```

Writes `submissions/financial_prediction_v3_submission.csv` from `datasets/Test.csv` using the trained model in `models/`.

---

## Model context

v3 predictions are driven by insurance and financial-service signals, country, and formalization features. See [`models/README.md`](../models/README.md) and EDA charts in [`eda/`](../eda/README.md).
