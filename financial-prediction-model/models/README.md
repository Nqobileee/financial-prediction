# Models

Training code and artifacts for financial health classification.

| File | Purpose |
|------|---------|
| `financial_prediction_v3.py` | Full pipeline: load data, engineer features, CV train, save model and submission |
| `financial_prediction_v3.ipynb` | Same workflow with markdown sections for each step |
| `financial_prediction_v3_model.pkl` | Serialized model, encoders, imputation values, feature list, CV metrics |

---

## Algorithm (v3)

| Setting | Value |
|---------|--------|
| Estimator | LightGBM multiclass (`num_class=3`) |
| Validation | Stratified 5-fold CV, early stopping |
| Features | Raw survey columns + v3 engineered features (insurance, funeral cover, financial services, country, formalization, missingness, attitudes, ratios) |

Import feature logic without running training:

```python
import importlib.util
from pathlib import Path

path = Path("models/financial_prediction_v3.py")
spec = importlib.util.spec_from_file_location("fpv3", path)
fpv3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fpv3)

features = fpv3.create_v3_features(train_df[feature_cols])
```

---

## Performance (from EDA OOF benchmark)

Cross-validated LightGBM on the encoded feature matrix (see [`eda/`](../eda/README.md) for full analysis):

| Metric | Value |
|--------|-------|
| Accuracy | 0.874 |
| F1 (macro) | 0.805 |
| Macro ROC-AUC (OVR) | 0.944 |

![OOF confusion matrix](../eda/figures/17_confusion_matrix_lightgbm_oof.png)

---

## Run

```bash
cd financial-prediction-model
python models/financial_prediction_v3.py
```

Outputs:

- `models/financial_prediction_v3_model.pkl`
- `submissions/financial_prediction_v3_submission.csv`
