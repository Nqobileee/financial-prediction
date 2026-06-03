# pylint: skip-file
"""EDA notebook cell definitions (imported by build_notebooks.py)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EDA = ROOT / "eda"


def md(s):
    return {"cell_type": "markdown", "metadata": {}, "source": s if isinstance(s, list) else [s]}


def code(s):
    lines = s if isinstance(s, list) else s.split("\n")
    lines = [l + "\n" for l in lines]
    if lines:
        lines[-1] = lines[-1].rstrip("\n")
    return {"cell_type": "code", "metadata": {}, "outputs": [], "execution_count": None, "source": lines}


EDA_CELLS = [
    md(
        """# Financial Health Prediction — Exploratory Data Analysis

Comprehensive research notebook for the MSME Financial Health dataset. All figures are saved under `eda/figures/` with descriptive filenames for reports and presentations.

**Contents:** data quality, target balance, univariate and bivariate analysis, association tests (chi-square, Cramér's V, mutual information), engineered features, baseline models, ROC-AUC (one-vs-rest), confusion matrices, and feature importance.

---"""
    ),
    md(
        """## 1. Environment, paths, and plotting defaults

Charts are saved under `eda/figures/` only when missing. Existing PNGs are reused (not deleted). Each chart is shown inline in the notebook and listed again in the figure gallery at the end."""
    ),
    code(
        """%matplotlib inline
import os
import warnings
from pathlib import Path

import joblib
import lightgbm as lgb
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from scipy.stats import chi2_contingency
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import mutual_info_classif
from sklearn.metrics import (
    accuracy_score,
    auc,
    roc_curve,
    classification_report,
    confusion_matrix,
    f1_score,
    log_loss,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.preprocessing import LabelEncoder, label_binarize

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["figure.dpi"] = 120
plt.rcParams["savefig.dpi"] = 150
plt.rcParams["font.size"] = 10

# Resolve project root (notebook may run from eda/ or project root)
BASE_PATH = Path.cwd()
for candidate in [BASE_PATH, BASE_PATH.parent, BASE_PATH / ".."]:
    p = candidate.resolve()
    if (p / "datasets" / "Train.csv").is_file():
        BASE_PATH = p
        break
else:
    raise FileNotFoundError(
        "Could not find datasets/Train.csv. Run from financial-prediction-model/ or eda/."
    )

DATASETS = BASE_PATH / "datasets"
FIGURES = (BASE_PATH / "eda" / "figures").resolve()
FINDINGS_PATH = (BASE_PATH / "eda" / "decision_parameters_summary.csv").resolve()
VAR_DEF_PATH = DATASETS / "VariableDefinitions.csv"
TRAIN_PATH = DATASETS / "Train.csv"
TEST_PATH = DATASETS / "Test.csv"

TARGET_MAP = {"Low": 0, "Medium": 1, "High": 2}
CLASS_NAMES = ["Low", "Medium", "High"]
RANDOM_STATE = 42

EXPECTED_FIGURES = (
    "01_missing_value_pattern_sample500.png",
    "02_target_distribution_counts_and_percent.png",
    "03_target_distribution_by_country_stacked.png",
    "04_numeric_feature_distributions_histograms.png",
    "05_numeric_boxplots_by_target.png",
    "06_numeric_correlation_with_target.png",
    "07_numeric_correlation_heatmap.png",
    "08_top_categorical_cramers_v_with_target.png",
    "09_mutual_information_top25.png",
    "10_top_categorical_target_composition_stacked.png",
    "11_insurance_adoption_tier_vs_target.png",
    "12_financial_services_adoption_tier_vs_target.png",
    "13_engineered_features_correlation_heatmap.png",
    "14_engineered_features_boxplots_by_target.png",
    "15_random_forest_feature_importance_top30.png",
    "16_engineered_features_rf_importance_top15.png",
    "17_confusion_matrix_lightgbm_oof.png",
    "18_roc_curves_ovr_lightgbm_oof.png",
    "19_lightgbm_feature_importance_top30.png",
)


FIGURES.mkdir(parents=True, exist_ok=True)


def figure_exists(name):
    path = FIGURES / name
    return path.is_file() and path.stat().st_size > 0


def show_figure(name):
    \"\"\"Display a saved figure in the notebook.\"\"\"
    from IPython.display import Image, display

    path = FIGURES / name
    if not path.is_file():
        print(f"Not found (run plot cell first): {name}")
        return
    display(Image(filename=str(path)))


def save_figure(name, tight=True):
    \"\"\"Save the current plot if missing, then display it (never deletes existing files).\"\"\"
    if name not in EXPECTED_FIGURES:
        raise ValueError(f"Unexpected figure name: {name}")
    path = FIGURES / name
    if figure_exists(name):
        plt.close("all")
        print(f"Using cached figure: {name}")
    else:
        if tight:
            plt.tight_layout()
        plt.savefig(path, bbox_inches="tight")
        plt.close("all")
        print(f"Saved: {name}")
    show_figure(name)


cached_figs = sum(figure_exists(n) for n in EXPECTED_FIGURES)
print("BASE_PATH:", BASE_PATH)
print("Figures directory:", FIGURES)
print(f"Cached figures on disk: {cached_figs}/{len(EXPECTED_FIGURES)}")"""
    ),
    md("""## 2. Load data and variable dictionary"""),
    code(
        """train = pd.read_csv(TRAIN_PATH)
test = pd.read_csv(TEST_PATH)
var_defs = pd.read_csv(VAR_DEF_PATH)

print("Train:", train.shape, "| Test:", test.shape)
print("\\nTarget distribution (%):")
print((train["Target"].value_counts(normalize=True) * 100).round(2))

display(var_defs.head(10))"""
    ),
    md("""## 3. Data overview and quality"""),
    code(
        """overview = pd.DataFrame({
    "dtype": train.dtypes,
    "missing_count": train.isnull().sum(),
    "missing_pct": (train.isnull().sum() / len(train) * 100).round(2),
    "n_unique": train.nunique(),
})
overview = overview.sort_values("missing_pct", ascending=False)
display(overview.head(20))

# Missingness heatmap (sample of rows for readability)
if not figure_exists("01_missing_value_pattern_sample500.png"):
    sample_idx = np.random.RandomState(RANDOM_STATE).choice(
        len(train), size=min(500, len(train)), replace=False
    )
    miss_matrix = train.iloc[sample_idx].isnull().astype(int)
    plt.figure(figsize=(14, 8))
    sns.heatmap(
        miss_matrix,
        cbar=True,
        cmap="viridis",
        yticklabels=False,
        xticklabels=miss_matrix.columns,
    )
    plt.title("Missing Value Patterns (500-row sample)")
    plt.xticks(rotation=90)
save_figure("01_missing_value_pattern_sample500.png")"""
    ),
    md("""## 4. Target distribution and class imbalance"""),
    code(
        """target_counts = train["Target"].value_counts().reindex(CLASS_NAMES)
target_pct = (target_counts / len(train) * 100).round(2)

if not figure_exists("02_target_distribution_counts_and_percent.png"):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    sns.barplot(x=target_counts.index, y=target_counts.values, ax=axes[0], palette="Blues_d")
    axes[0].set_title("Target Counts")
    axes[0].set_ylabel("Count")
    sns.barplot(x=target_pct.index, y=target_pct.values, ax=axes[1], palette="Greens_d")
    axes[1].set_title("Target Proportions (%)")
    axes[1].set_ylabel("Percent")
save_figure("02_target_distribution_counts_and_percent.png")

imbalance_ratio = target_counts.max() / target_counts.min()
print(f"Imbalance ratio (max/min): {imbalance_ratio:.2f}")"""
    ),
    md("""## 5. Geographic segmentation (country)"""),
    code(
        """country_target = pd.crosstab(train["country"], train["Target"], normalize="index") * 100

if not figure_exists("03_target_distribution_by_country_stacked.png"):
    plt.figure(figsize=(10, 6))
    country_target[CLASS_NAMES].plot(kind="bar", stacked=True, colormap="Set2")
    plt.ylabel("Percent within country")
    plt.title("Target Mix by Country")
    plt.legend(title="Target", bbox_to_anchor=(1.02, 1))
    plt.xticks(rotation=0)
save_figure("03_target_distribution_by_country_stacked.png")

chi2, p, _, _ = chi2_contingency(pd.crosstab(train["country"], train["Target"]))
print(f"Country vs Target chi2 p-value: {p:.2e}")"""
    ),
    md("""## 6. Numeric features — distributions and target separation"""),
    code(
        """numeric_cols = train.select_dtypes(include=[np.number]).columns.tolist()
numeric_cols = [c for c in numeric_cols if c not in ["ID"]]
print("Numeric columns:", numeric_cols)

# Distribution grid
n_num = len(numeric_cols)
ncols = 3
nrows = int(np.ceil(n_num / ncols))

if not figure_exists("04_numeric_feature_distributions_histograms.png"):
    fig, axes = plt.subplots(nrows, ncols, figsize=(14, 4 * nrows))
    axes = axes.flatten()
    for i, col in enumerate(numeric_cols):
        sns.histplot(train[col].dropna(), kde=True, ax=axes[i], color="steelblue")
        axes[i].set_title(col)
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)
    plt.suptitle("Numeric Feature Distributions", y=1.02)
save_figure("04_numeric_feature_distributions_histograms.png")

# Boxplots by target
if not figure_exists("05_numeric_boxplots_by_target.png"):
    fig, axes = plt.subplots(nrows, ncols, figsize=(14, 4 * nrows))
    axes = axes.flatten()
    for i, col in enumerate(numeric_cols):
        sns.boxplot(data=train, x="Target", y=col, order=CLASS_NAMES, ax=axes[i])
        axes[i].set_title(col)
        axes[i].tick_params(axis="x", rotation=30)
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)
    plt.suptitle("Numeric Features by Target", y=1.02)
save_figure("05_numeric_boxplots_by_target.png")"""
    ),
    md("""## 7. Numeric correlation with target and heatmap"""),
    code(
        """train_num = train.copy()
train_num["target_encoded"] = train_num["Target"].map(TARGET_MAP)

corr_with_target = (
    train_num[numeric_cols + ["target_encoded"]]
    .corr()["target_encoded"]
    .drop("target_encoded")
    .sort_values(key=abs, ascending=False)
)

if not figure_exists("06_numeric_correlation_with_target.png"):
    plt.figure(figsize=(8, 5))
    corr_with_target.plot(kind="barh", color="teal")
    plt.title("Pearson Correlation with Encoded Target")
    plt.xlabel("Correlation")
save_figure("06_numeric_correlation_with_target.png")

if not figure_exists("07_numeric_correlation_heatmap.png"):
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        train_num[numeric_cols].corr(),
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        square=True,
    )
    plt.title("Numeric Feature Correlation Matrix")
save_figure("07_numeric_correlation_heatmap.png")"""
    ),
    md("""## 8. Categorical association — Cramér's V and chi-square"""),
    code(
        """def cramers_v(x, y):
    confusion = pd.crosstab(x, y)
    chi2 = chi2_contingency(confusion)[0]
    n = confusion.sum().sum()
    r, k = confusion.shape
    return np.sqrt(chi2 / (n * (min(r, k) - 1)))


cat_cols = [c for c in train.columns if c not in ["ID", "Target"] and train[c].dtype == "object"]

assoc_rows = []
for col in cat_cols:
    sub = train[[col, "Target"]].dropna()
    if sub[col].nunique() < 2:
        continue
    ct = pd.crosstab(sub[col], sub["Target"])
    chi2, p, _, _ = chi2_contingency(ct)
    assoc_rows.append(
        {
            "feature": col,
            "cramers_v": cramers_v(sub[col], sub["Target"]),
            "chi2_pvalue": p,
            "n_categories": sub[col].nunique(),
        }
    )

assoc_df = pd.DataFrame(assoc_rows).sort_values("cramers_v", ascending=False)
display(assoc_df.head(15))

if not figure_exists("08_top_categorical_cramers_v_with_target.png"):
    plt.figure(figsize=(10, 8))
    top_assoc = assoc_df.head(20)
    sns.barplot(data=top_assoc, y="feature", x="cramers_v", palette="magma")
    plt.title("Top 20 Categorical Features by Cramér's V with Target")
save_figure("08_top_categorical_cramers_v_with_target.png")"""
    ),
    md("""## 9. Mutual information scores"""),
    code(
        """# Encode categoricals for MI
mi_df = train.drop(columns=["ID"]).copy()
mi_df["target_encoded"] = mi_df["Target"].map(TARGET_MAP)
for col in mi_df.select_dtypes(include="object").columns:
    if col != "Target":
        mi_df[col] = LabelEncoder().fit_transform(mi_df[col].astype(str))

mi_df = mi_df.fillna(-1)
X_mi = mi_df.drop(columns=["Target", "target_encoded"])
y_mi = mi_df["target_encoded"]

mi_scores = mutual_info_classif(X_mi, y_mi, random_state=RANDOM_STATE, discrete_features="auto")
mi_result = (
    pd.DataFrame({"feature": X_mi.columns, "mutual_information": mi_scores})
    .sort_values("mutual_information", ascending=False)
)
display(mi_result.head(20))

if not figure_exists("09_mutual_information_top25.png"):
    plt.figure(figsize=(10, 8))
    sns.barplot(
        data=mi_result.head(25),
        y="feature",
        x="mutual_information",
        palette="viridis",
    )
    plt.title("Top 25 Features by Mutual Information")
save_figure("09_mutual_information_top25.png")"""
    ),
    md("""## 10. Top categorical features vs target"""),
    code(
        """top_cat = assoc_df.head(6)["feature"].tolist()

if not figure_exists("10_top_categorical_target_composition_stacked.png"):
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    for ax, col in zip(axes, top_cat):
        ct_pct = pd.crosstab(train[col], train["Target"], normalize="index")[CLASS_NAMES] * 100
        ct_pct.plot(kind="bar", stacked=True, ax=ax, colormap="Pastel1")
        ax.set_title(col)
        ax.set_ylabel("% within category")
        ax.tick_params(axis="x", rotation=45)
    plt.suptitle("Target Composition for Top Categorical Predictors", y=1.02)
save_figure("10_top_categorical_target_composition_stacked.png")"""
    ),
    md("""## 11. Insurance and financial services — decision tiers"""),
    code(
        """def is_current_holder(val):
    if pd.isna(val):
        return 0
    s = str(val).lower()
    return int("have now" in s or s == "yes")


insurance_cols = [
    "has_insurance",
    "motor_vehicle_insurance",
    "medical_insurance",
    "funeral_insurance",
]
fin_cols = [
    "has_mobile_money",
    "has_credit_card",
    "has_loan_account",
    "has_internet_banking",
    "has_debit_card",
    "has_cellphone",
]

eda = train.copy()
eda["insurance_count"] = sum(eda[c].apply(is_current_holder) for c in insurance_cols)
eda["financial_service_count"] = sum(eda[c].apply(is_current_holder) for c in fin_cols)

for count_col, title_prefix in [
    ("insurance_count", "Insurance"),
    ("financial_service_count", "Financial services"),
]:
    fname = (
        "11_insurance_adoption_tier_vs_target.png"
        if "insurance" in count_col
        else "12_financial_services_adoption_tier_vs_target.png"
    )
    if not figure_exists(fname):
        tier_target = pd.crosstab(eda[count_col], eda["Target"], normalize="index")[CLASS_NAMES] * 100
        plt.figure(figsize=(9, 5))
        tier_target.plot(kind="bar", stacked=True, colormap="Set3")
        plt.title(f"{title_prefix} adoption count vs target (%)")
        plt.xlabel(f"{title_prefix} count (current)")
        plt.ylabel("Percent")
        plt.legend(title="Target", bbox_to_anchor=(1.02, 1))
    save_figure(fname)"""
    ),
    md("""## 12. Feature engineering (v3) — preview and engineered-target analysis"""),
    code(
        '''# Reuse same engineering logic as production model (abbreviated for EDA)
raw_cols = [c for c in train.columns if c not in ["ID", "Target"]]


def create_v3_features_eda(df):
    f = pd.DataFrame(index=df.index)
    if "funeral_insurance" in df.columns:
        funeral_map = {"Have now": 3, "Used to have but don't have now": 1, "Never had": 0, "Don't know": 0.5}
        f["funeral_insurance_detailed"] = df["funeral_insurance"].apply(
            lambda x: funeral_map.get(str(x).strip() if pd.notna(x) else "Never had", 0)
        )
        f["has_funeral_insurance_now"] = df["funeral_insurance"].apply(
            lambda x: 1 if pd.notna(x) and "have now" in str(x).lower() else 0
        )
    ins_cols = ["has_insurance", "motor_vehicle_insurance", "medical_insurance", "funeral_insurance"]
    scores = []
    for col in ins_cols:
        if col in df.columns:
            cur = df[col].apply(lambda x: 1 if pd.notna(x) and "have now" in str(x).lower() else 0)
            f[f"{col}_current"] = cur
            scores.append(cur)
    if scores:
        f["insurance_current_count"] = pd.concat(scores, axis=1).sum(axis=1)
    fin_cols = [
        "has_mobile_money",
        "has_credit_card",
        "has_loan_account",
        "has_internet_banking",
        "has_debit_card",
        "has_cellphone",
    ]
    fscores = []
    for col in fin_cols:
        if col in df.columns:
            cur = df[col].apply(
                lambda x: 1 if pd.notna(x) and ("have now" in str(x).lower() or str(x).lower() == "yes") else 0
            )
            f[f"{col}_current"] = cur
            fscores.append(cur)
    if fscores:
        f["financial_service_count"] = pd.concat(fscores, axis=1).sum(axis=1)
    if "country" in df.columns:
        f["country_encoded"] = df["country"].map({"eswatini": 3, "malawi": 0, "zimbabwe": 1, "lesotho": 2}).fillna(1)
    if "keeps_financial_records" in df.columns:
        rm = {"Yes, always": 3, "Yes, sometimes": 2, "Yes": 2, "No": 0}
        f["keeps_records_score"] = df["keeps_financial_records"].apply(
            lambda x: rm.get(str(x).strip() if pd.notna(x) else "No", 0)
        )
        f["formalization_score"] = f["keeps_records_score"] / 3
    for col in ["personal_income", "business_expenses", "business_turnover"]:
        if col in df.columns:
            f[f"log_{col}"] = np.log1p(df[col].fillna(0).clip(lower=0))
    parts = []
    if "insurance_current_count" in f.columns:
        parts.append(f["insurance_current_count"] * 0.4)
    if "financial_service_count" in f.columns:
        parts.append(f["financial_service_count"] * 0.3)
    if "formalization_score" in f.columns:
        parts.append(f["formalization_score"] * 3 * 0.3)
    if parts:
        f["financial_health_composite"] = pd.concat(parts, axis=1).sum(axis=1)
    return f


eng = create_v3_features_eda(train[raw_cols])
print("Engineered feature count:", eng.shape[1])
display(eng.describe().T.head(15))

# Correlation among key engineered features
key_eng = [
    c
    for c in [
        "funeral_insurance_detailed",
        "insurance_current_count",
        "financial_service_count",
        "financial_health_composite",
        "formalization_score",
        "country_encoded",
    ]
    if c in eng.columns
]
if key_eng and not figure_exists("13_engineered_features_correlation_heatmap.png"):
    eng_plot = eng[key_eng].copy()
    eng_plot["target"] = train["Target"].map(TARGET_MAP)
    plt.figure(figsize=(8, 6))
    sns.heatmap(eng_plot.corr(), annot=True, fmt=".2f", cmap="RdBu_r", center=0)
    plt.title("Engineered Feature Correlation Matrix")
if key_eng:
    save_figure("13_engineered_features_correlation_heatmap.png")'''
    ),
    md("""## 13. Engineered features vs target"""),
    code(
        """plot_eng = [c for c in eng.columns if eng[c].nunique() <= 20][:6]

if not figure_exists("14_engineered_features_boxplots_by_target.png"):
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    axes = axes.flatten()
    for ax, col in zip(axes, plot_eng):
        sns.boxplot(
            data=pd.concat([eng[[col]], train["Target"]], axis=1),
            x="Target",
            y=col,
            order=CLASS_NAMES,
            ax=ax,
        )
        ax.set_title(col)
    plt.suptitle("Engineered Features by Target", y=1.02)
save_figure("14_engineered_features_boxplots_by_target.png")"""
    ),
    md("""## 14. Preprocessing matrix for modeling benchmarks"""),
    code(
        """X_raw = train[raw_cols].copy()
X_eng = pd.concat([X_raw, eng], axis=1)

# Simple encoding for tree models
X_model = X_eng.copy()
for col in X_model.select_dtypes(include="object").columns:
    X_model[col] = LabelEncoder().fit_transform(X_model[col].astype(str))
X_model = X_model.fillna(-1)

y = train["Target"].map(TARGET_MAP)
print("Modeling matrix shape:", X_model.shape)"""
    ),
    md("""## 15. Random Forest — baseline feature importance"""),
    code(
        """rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=12,
    class_weight="balanced",
    random_state=RANDOM_STATE,
    n_jobs=-1,
)
rf.fit(X_model, y)

rf_imp = (
    pd.DataFrame({"feature": X_model.columns, "importance": rf.feature_importances_})
    .sort_values("importance", ascending=False)
)
display(rf_imp.head(25))

if not figure_exists("15_random_forest_feature_importance_top30.png"):
    plt.figure(figsize=(10, 8))
    sns.barplot(data=rf_imp.head(30), y="feature", x="importance", palette="crest")
    plt.title("Random Forest Feature Importance (Top 30)")
save_figure("15_random_forest_feature_importance_top30.png")

rf_imp["is_engineered"] = rf_imp["feature"].isin(eng.columns)
eng_top = rf_imp[rf_imp["is_engineered"]].head(15)
if not figure_exists("16_engineered_features_rf_importance_top15.png"):
    plt.figure(figsize=(9, 5))
    sns.barplot(data=eng_top, y="feature", x="importance", palette="flare")
    plt.title("Engineered Features — RF Importance")
save_figure("16_engineered_features_rf_importance_top15.png")"""
    ),
    md("""## 16. LightGBM cross-validated performance"""),
    code(
        """lgb_params = {
    "objective": "multiclass",
    "num_class": 3,
    "learning_rate": 0.05,
    "n_estimators": 400,
    "num_leaves": 31,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "random_state": RANDOM_STATE,
    "verbose": -1,
}

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
oof_proba = np.zeros((len(X_model), 3))

for tr_idx, va_idx in skf.split(X_model, y):
    clf = lgb.LGBMClassifier(**lgb_params)
    clf.fit(X_model.iloc[tr_idx], y.iloc[tr_idx])
    oof_proba[va_idx] = clf.predict_proba(X_model.iloc[va_idx])

oof_pred = np.argmax(oof_proba, axis=1)
print("OOF Accuracy:", round(accuracy_score(y, oof_pred), 4))
print("OOF F1 macro:", round(f1_score(y, oof_pred, average="macro"), 4))
print("OOF Log loss:", round(log_loss(y, oof_proba), 4))
print(classification_report(y, oof_pred, target_names=CLASS_NAMES))"""
    ),
    md("""## 17. Confusion matrix (OOF)"""),
    code(
        """cm = confusion_matrix(y, oof_pred)

if not figure_exists("17_confusion_matrix_lightgbm_oof.png"):
    plt.figure(figsize=(7, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=CLASS_NAMES,
        yticklabels=CLASS_NAMES,
    )
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix — LightGBM OOF")
save_figure("17_confusion_matrix_lightgbm_oof.png")"""
    ),
    md("""## 18. ROC curves and AUC (one-vs-rest)"""),
    code(
        """y_bin = label_binarize(y, classes=[0, 1, 2])

if not figure_exists("18_roc_curves_ovr_lightgbm_oof.png"):
    fig, ax = plt.subplots(figsize=(8, 7))
    auc_scores = {}
    for i, cls in enumerate(CLASS_NAMES):
        fpr, tpr, _ = roc_curve(y_bin[:, i], oof_proba[:, i])
        auc_scores[cls] = auc(fpr, tpr)
        ax.plot(fpr, tpr, label=f"{cls} (AUC={auc_scores[cls]:.3f})")
    ax.plot([0, 1], [0, 1], "k--", alpha=0.4, label="Chance")
    ax.set_title("ROC Curves — One-vs-Rest (OOF LightGBM)")
    ax.legend(loc="lower right")
save_figure("18_roc_curves_ovr_lightgbm_oof.png")

auc_scores = {}
for i, cls in enumerate(CLASS_NAMES):
    auc_scores[cls] = roc_auc_score(y_bin[:, i], oof_proba[:, i])

macro_auc = roc_auc_score(y_bin, oof_proba, multi_class="ovr", average="macro")
weighted_auc = roc_auc_score(y_bin, oof_proba, multi_class="ovr", average="weighted")
print("Per-class AUC:", {k: round(v, 4) for k, v in auc_scores.items()})
print(f"Macro OVR AUC: {macro_auc:.4f} | Weighted OVR AUC: {weighted_auc:.4f}")"""
    ),
    md("""## 19. LightGBM feature importance (gain)"""),
    code(
        """final_lgb = lgb.LGBMClassifier(**lgb_params)
final_lgb.fit(X_model, y)

lgb_imp = (
    pd.DataFrame({"feature": X_model.columns, "importance": final_lgb.feature_importances_})
    .sort_values("importance", ascending=False)
)
display(lgb_imp.head(25))

if not figure_exists("19_lightgbm_feature_importance_top30.png"):
    plt.figure(figsize=(10, 8))
    sns.barplot(data=lgb_imp.head(30), y="feature", x="importance", palette="cubehelix")
    plt.title("LightGBM Feature Importance (Top 30)")
save_figure("19_lightgbm_feature_importance_top30.png")"""
    ),
    md("""## 20. Decision parameters summary"""),
    code(
        """if FINDINGS_PATH.exists():
    decision_summary = pd.read_csv(FINDINGS_PATH)
    print(f"Using cached findings: {FINDINGS_PATH.name}")
else:
    decision_summary = pd.DataFrame(
        [
            {
                "parameter": "Strongest categorical signal",
                "value": assoc_df.iloc[0]["feature"] if len(assoc_df) else "N/A",
                "metric": f"Cramér's V = {assoc_df.iloc[0]['cramers_v']:.3f}" if len(assoc_df) else "",
            },
            {
                "parameter": "Top MI feature",
                "value": mi_result.iloc[0]["feature"],
                "metric": f"MI = {mi_result.iloc[0]['mutual_information']:.4f}",
            },
            {
                "parameter": "Class imbalance ratio",
                "value": f"{imbalance_ratio:.2f}",
                "metric": "max class / min class count",
            },
            {
                "parameter": "OOF Accuracy (LGBM)",
                "value": f"{accuracy_score(y, oof_pred):.4f}",
                "metric": "5-fold stratified CV",
            },
            {
                "parameter": "OOF F1 macro",
                "value": f"{f1_score(y, oof_pred, average='macro'):.4f}",
                "metric": "primary ranking metric candidate",
            },
            {
                "parameter": "Macro ROC-AUC (OVR)",
                "value": f"{macro_auc:.4f}",
                "metric": "one-vs-rest on OOF probabilities",
            },
            {
                "parameter": "Recommended stratification",
                "value": "StratifiedKFold on Target",
                "metric": "handles 65/30/5% class mix",
            },
            {
                "parameter": "Key engineered blocks",
                "value": "insurance tiers, financial services, funeral insurance, country, formalization",
                "metric": "see model v3 notebook",
            },
        ]
    )
    decision_summary.to_csv(FINDINGS_PATH, index=False, mode="w")
    print(f"Saved findings: {FINDINGS_PATH.name}")

display(decision_summary)

saved = {p.name for p in FIGURES.glob("*.png")}
missing = [n for n in EXPECTED_FIGURES if n not in saved]
print(f"\\nFigures on disk: {len(saved)}/{len(EXPECTED_FIGURES)}")
if missing:
    print("  Still need to generate:", ", ".join(missing))"""
    ),
]

FIGURE_TITLES = {
    "01_missing_value_pattern_sample500.png": "Missing value pattern",
    "02_target_distribution_counts_and_percent.png": "Target distribution",
    "03_target_distribution_by_country_stacked.png": "Target by country",
    "04_numeric_feature_distributions_histograms.png": "Numeric distributions",
    "05_numeric_boxplots_by_target.png": "Numeric features by target",
    "06_numeric_correlation_with_target.png": "Correlation with target",
    "07_numeric_correlation_heatmap.png": "Numeric correlation heatmap",
    "08_top_categorical_cramers_v_with_target.png": "Cramér's V (top categoricals)",
    "09_mutual_information_top25.png": "Mutual information",
    "10_top_categorical_target_composition_stacked.png": "Top categoricals vs target",
    "11_insurance_adoption_tier_vs_target.png": "Insurance adoption tiers",
    "12_financial_services_adoption_tier_vs_target.png": "Financial services tiers",
    "13_engineered_features_correlation_heatmap.png": "Engineered feature correlations",
    "14_engineered_features_boxplots_by_target.png": "Engineered features by target",
    "15_random_forest_feature_importance_top30.png": "Random Forest importance",
    "16_engineered_features_rf_importance_top15.png": "Engineered RF importance",
    "17_confusion_matrix_lightgbm_oof.png": "Confusion matrix (LightGBM OOF)",
    "18_roc_curves_ovr_lightgbm_oof.png": "ROC curves (one-vs-rest)",
    "19_lightgbm_feature_importance_top30.png": "LightGBM importance",
}

_gallery_md = """## 21. Figure gallery

Static previews from `figures/`. These render in the notebook when the PNG files exist (no need to re-plot).

"""
for _name in FIGURE_TITLES:
    _title = FIGURE_TITLES.get(_name, _name)
    _gallery_md += f"### {_title}\n\n![](figures/{_name})\n\n"

EDA_CELLS.append(md(_gallery_md))
