# Exploratory Data Analysis

Research notebook and exported charts for the MSME financial health dataset.

| Item | Path |
|------|------|
| Notebook | [`comprehensive_eda.ipynb`](comprehensive_eda.ipynb) |
| All figures (19) | [`figures/`](figures/README.md) |
| Decision summary | [`decision_parameters_summary.csv`](decision_parameters_summary.csv) |

---

## Findings at a glance

| Finding | Detail |
|---------|--------|
| Strongest categorical predictor | `funeral_insurance` (Cramér's V ≈ 0.55) |
| Top mutual information feature | `funeral_insurance` (MI ≈ 0.22) |
| Class imbalance | ~13:1 max/min class ratio |
| Insurance adoption | Higher current insurance count aligns with Medium/High targets |
| Financial services | More active products (mobile money, cards, loans) correlate with better health |
| Model benchmark (LightGBM OOF) | Accuracy 0.87, F1 macro 0.80, macro ROC-AUC 0.94 |

---

## Selected charts

### Association strength (Cramér's V)

![Top categorical predictors](figures/08_top_categorical_cramers_v_with_target.png)

### Insurance adoption vs target

![Insurance tiers](figures/11_insurance_adoption_tier_vs_target.png)

### Financial services adoption vs target

![Financial services tiers](figures/12_financial_services_adoption_tier_vs_target.png)

### Model evaluation (LightGBM, 5-fold OOF)

![Confusion matrix](figures/17_confusion_matrix_lightgbm_oof.png)

![ROC curves one-vs-rest](figures/18_roc_curves_ovr_lightgbm_oof.png)

---

## Rerun behavior

- Plot cells **skip** generation if the PNG already exists in `figures/`.
- The notebook **displays** cached images inline and in section 21 (figure gallery).
- Delete a specific PNG or `decision_parameters_summary.csv` to force regeneration.

```bash
cd financial-prediction-model
python -m jupyter notebook eda/comprehensive_eda.ipynb
```
