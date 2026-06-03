# EDA Figures

Numbered PNG exports from [`comprehensive_eda.ipynb`](../comprehensive_eda.ipynb). Parent overview: [`eda/README.md`](../README.md).

**Reruns:** Existing files are reused (not deleted). Remove a file to regenerate that chart only.

---

## Index

| File | Description |
|------|-------------|
| `01_missing_value_pattern_sample500.png` | Missingness heatmap (500-row sample) |
| `02_target_distribution_counts_and_percent.png` | Class counts and proportions |
| `03_target_distribution_by_country_stacked.png` | Target mix by country |
| `04_numeric_feature_distributions_histograms.png` | Numeric histograms |
| `05_numeric_boxplots_by_target.png` | Numeric features vs target |
| `06_numeric_correlation_with_target.png` | Correlation with target |
| `07_numeric_correlation_heatmap.png` | Numeric correlation matrix |
| `08_top_categorical_cramers_v_with_target.png` | Top Cramér's V scores |
| `09_mutual_information_top25.png` | Mutual information ranking |
| `10_top_categorical_target_composition_stacked.png` | Top categoricals vs target |
| `11_insurance_adoption_tier_vs_target.png` | Insurance count tiers |
| `12_financial_services_adoption_tier_vs_target.png` | Financial services tiers |
| `13_engineered_features_correlation_heatmap.png` | Engineered feature correlations |
| `14_engineered_features_boxplots_by_target.png` | Engineered features vs target |
| `15_random_forest_feature_importance_top30.png` | Random Forest importance |
| `16_engineered_features_rf_importance_top15.png` | Engineered RF importance |
| `17_confusion_matrix_lightgbm_oof.png` | OOF confusion matrix |
| `18_roc_curves_ovr_lightgbm_oof.png` | One-vs-rest ROC curves |
| `19_lightgbm_feature_importance_top30.png` | LightGBM gain importance |

---

## Highlighted in READMEs

| Chart | Used in |
|-------|---------|
| 02, 03 | Root README, `datasets/README.md` |
| 08, 11, 12, 17, 18 | Root README, `eda/README.md` |
| 19 | `financial-prediction-model/README.md` |
| 17 | `models/README.md` |

`decision_parameters_summary.csv` lives in [`eda/`](../decision_parameters_summary.csv).
