"""One-off script to generate model and EDA Jupyter notebooks."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODELS = ROOT / "models"
EDA = ROOT / "eda"
FIGURES = EDA / "figures"


def nb(cells):
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "cells": cells,
    }


def md(source):
    return {"cell_type": "markdown", "metadata": {}, "source": source if isinstance(source, list) else [source]}


def code(source):
    lines = source if isinstance(source, list) else source.split("\n")
    lines = [l + "\n" for l in lines]
    if lines:
        lines[-1] = lines[-1].rstrip("\n")
    return {"cell_type": "code", "metadata": {}, "outputs": [], "execution_count": None, "source": lines}


def save(path, cells):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(nb(cells), indent=1), encoding="utf-8")
    print(f"Wrote {path}")


# ---------------------------------------------------------------------------
# Model notebook
# ---------------------------------------------------------------------------
MODEL_CELLS = [
    md(
        """# Financial Health Prediction — Model v3.0

**Competition:** Data.org Financial Health Prediction Challenge  
**Objective:** Predict Financial Health Index (`Low` / `Medium` / `High`) for MSMEs.

This notebook implements the production pipeline: data-driven feature engineering, preprocessing, stratified cross-validated LightGBM training, and submission export.

---"""
    ),
    md(
        """## 1. Configuration and paths

All paths are relative to the `financial-prediction-model` project root. Training and test CSVs live under `datasets/`; artifacts are written to `models/` and `submissions/`."""
    ),
    code(
        """import os
import warnings
import joblib
import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, f1_score, log_loss
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings("ignore")

RANDOM_STATE = 42
N_FOLDS = 5
MODEL_NAME = "financial_prediction_v3"

from pathlib import Path

_cwd = Path.cwd()
if (_cwd / "datasets" / "Train.csv").is_file():
    BASE_PATH = str(_cwd)
elif (_cwd.parent / "datasets" / "Train.csv").is_file():
    BASE_PATH = str(_cwd.parent)
else:
    raise FileNotFoundError(
        "datasets/Train.csv not found. Set working directory to financial-prediction-model or models/."
    )

TRAIN_PATH = os.path.join(BASE_PATH, "datasets", "Train.csv")
TEST_PATH = os.path.join(BASE_PATH, "datasets", "Test.csv")
SUBMISSION_PATH = os.path.join(BASE_PATH, "submissions", f"{MODEL_NAME}_submission.csv")
MODEL_PATH = os.path.join(BASE_PATH, "models", f"{MODEL_NAME}_model.pkl")

TARGET_MAP = {"Low": 0, "Medium": 1, "High": 2}
TARGET_MAP_REVERSE = {0: "Low", 1: "Medium", 2: "High"}
BINARY_MAP = {
    "Yes": 1,
    "No": 0,
    "Have now": 1,
    "Used before": 0.5,
    "Never had": 0,
    "Used to have but don't have now": 0.25,
}

print("BASE_PATH:", BASE_PATH)
print("Train:", TRAIN_PATH)
print("Test:", TEST_PATH)"""
    ),
    md(
        """## 2. Load training and test data

We load labeled training rows and unlabeled test rows, preserve `ID` for submission, and encode the target as integers for multiclass learning."""
    ),
    code(
        """train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

print(f"Train shape: {train_df.shape}")
print(f"Test shape: {test_df.shape}")

train_ids = train_df["ID"].copy()
test_ids = test_df["ID"].copy()
y = train_df["Target"].map(TARGET_MAP)

print("\\nTarget distribution:")
print(train_df["Target"].value_counts())"""
    ),
    md(
        """## 3. Feature engineering (v3)

Engineered features follow EDA findings: funeral insurance and insurance tiers, financial-service adoption, country effects, formalization, risk flags, missingness patterns, attitudes, and numeric ratios/interactions.

`create_v3_features` is imported from `financial_prediction_v3.py` so the notebook and training script share one implementation."""
    ),
    code(
        """import importlib.util

raw_feature_cols = [c for c in train_df.columns if c not in ["ID", "Target"]]
X_train = train_df[raw_feature_cols].copy()
X_test = test_df[raw_feature_cols].copy()
print(f"Original features: {len(raw_feature_cols)}")

_module_path = os.path.join(BASE_PATH, "models", "financial_prediction_v3.py")
_spec = importlib.util.spec_from_file_location("financial_prediction_v3", _module_path)
fpv3 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fpv3)
create_v3_features = fpv3.create_v3_features

engineered_train = create_v3_features(X_train, is_train=True)
engineered_test = create_v3_features(X_test, is_train=False)
engineered_feature_names = engineered_train.columns.tolist()

X_train_combined = pd.concat([X_train, engineered_train], axis=1)
X_test_combined = pd.concat([X_test, engineered_test], axis=1)
print(f"Engineered features: {engineered_train.shape[1]}")
print(f"Combined columns: {X_train_combined.shape[1]}")"""
    ),
    md(
        """## 4. Preprocessing

Numeric medians and categorical modes are fit on training data only. Label encoders are fit on the union of train and test categories to avoid unseen-label errors at inference."""
    ),
    code(
        """all_numeric_cols = X_train_combined.select_dtypes(
    include=["int64", "float64", "int32", "float32"]
).columns.tolist()
all_categorical_cols = X_train_combined.select_dtypes(include=["object"]).columns.tolist()

imputation_values = {}
for col in all_numeric_cols:
    median_val = X_train_combined[col].median()
    imputation_values[col] = median_val
    X_train_combined[col] = X_train_combined[col].fillna(median_val)
    X_test_combined[col] = X_test_combined[col].fillna(median_val)

for col in all_categorical_cols:
    mode_val = (
        X_train_combined[col].mode()[0]
        if len(X_train_combined[col].mode()) > 0
        else "Unknown"
    )
    imputation_values[col] = mode_val
    X_train_combined[col] = X_train_combined[col].fillna(mode_val)
    X_test_combined[col] = X_test_combined[col].fillna(mode_val)

label_encoders = {}
for col in all_categorical_cols:
    le = LabelEncoder()
    combined = pd.concat([X_train_combined[col], X_test_combined[col]], axis=0).astype(str)
    le.fit(combined)
    X_train_combined[col] = le.transform(X_train_combined[col].astype(str))
    X_test_combined[col] = le.transform(X_test_combined[col].astype(str))
    label_encoders[col] = le

feature_cols = X_train_combined.columns.tolist()
print(f"Final feature count: {len(feature_cols)}")"""
    ),
    md(
        """## 5. LightGBM training (stratified K-fold)

Five-fold stratified cross-validation produces out-of-fold probabilities for unbiased metrics. Test predictions are averaged across folds. Early stopping limits overfitting per fold."""
    ),
    code(
        """lgb_params = {
    "objective": "multiclass",
    "num_class": 3,
    "metric": "multi_logloss",
    "boosting_type": "gbdt",
    "n_estimators": 1500,
    "learning_rate": 0.025,
    "num_leaves": 55,
    "max_depth": 8,
    "min_child_samples": 25,
    "subsample": 0.8,
    "subsample_freq": 1,
    "colsample_bytree": 0.7,
    "reg_alpha": 0.15,
    "reg_lambda": 0.15,
    "min_split_gain": 0.005,
    "random_state": RANDOM_STATE,
    "verbose": -1,
    "n_jobs": -1,
}

skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=RANDOM_STATE)
oof_preds = np.zeros((len(X_train_combined), 3))
test_preds = np.zeros((len(X_test_combined), 3))
fold_scores = []
feature_importance_list = []

for fold, (train_idx, val_idx) in enumerate(skf.split(X_train_combined, y), 1):
    X_tr = X_train_combined.iloc[train_idx]
    X_val = X_train_combined.iloc[val_idx]
    y_tr, y_val = y.iloc[train_idx], y.iloc[val_idx]

    model = lgb.LGBMClassifier(**lgb_params)
    model.fit(
        X_tr,
        y_tr,
        eval_set=[(X_val, y_val)],
        callbacks=[lgb.early_stopping(150, verbose=False)],
    )
    feature_importance_list.append(model.feature_importances_)
    val_preds_proba = model.predict_proba(X_val)
    oof_preds[val_idx] = val_preds_proba
    test_preds += model.predict_proba(X_test_combined) / N_FOLDS

    val_preds_class = np.argmax(val_preds_proba, axis=1)
    fold_scores.append(
        {
            "fold": fold,
            "accuracy": accuracy_score(y_val, val_preds_class),
            "f1_macro": f1_score(y_val, val_preds_class, average="macro"),
            "log_loss": log_loss(y_val, val_preds_proba),
        }
    )
    print(f"Fold {fold}: {fold_scores[-1]}")"""
    ),
    md("""## 6. Cross-validation results

Out-of-fold (OOF) metrics summarize expected leaderboard performance without holdout leakage."""),
    code(
        """oof_preds_class = np.argmax(oof_preds, axis=1)
oof_acc = accuracy_score(y, oof_preds_class)
oof_f1 = f1_score(y, oof_preds_class, average="macro")
oof_logloss = log_loss(y, oof_preds)

print(f"OOF Accuracy: {oof_acc:.4f}")
print(f"OOF F1 (macro): {oof_f1:.4f}")
print(f"OOF Log Loss: {oof_logloss:.4f}")
print("\\nClassification report:")
print(classification_report(y, oof_preds_class, target_names=["Low", "Medium", "High"]))"""
    ),
    md("""## 7. Feature importance

Average gain-based importance across folds highlights which raw and engineered columns drive predictions."""),
    code(
        """importance_df = (
    pd.DataFrame(
        {
            "feature": feature_cols,
            "importance": np.mean(feature_importance_list, axis=0),
            "std": np.std(feature_importance_list, axis=0),
        }
    )
    .sort_values("importance", ascending=False)
    .reset_index(drop=True)
)

importance_df["is_engineered"] = importance_df["feature"].isin(engineered_feature_names)
try:
    from IPython.display import display
    display(importance_df.head(30))
except ImportError:
    print(importance_df.head(30).to_string())

top_30 = importance_df.head(30)["feature"].tolist()
print(f"Engineered features in top 30: {sum(f in engineered_feature_names for f in top_30)}")"""
    ),
    md(
        """## 8. Save model and create submission

The full training set is refit for deployment. Artifacts include encoders, imputation values, feature list, and CV metrics."""
    ),
    code(
        """final_model = lgb.LGBMClassifier(**lgb_params)
final_model.fit(X_train_combined, y)

model_artifacts = {
    "model": final_model,
    "label_encoders": label_encoders,
    "feature_cols": feature_cols,
    "imputation_values": imputation_values,
    "target_map": TARGET_MAP,
    "target_map_reverse": TARGET_MAP_REVERSE,
    "cv_metrics": {"accuracy": oof_acc, "f1_macro": oof_f1, "log_loss": oof_logloss},
    "importance_df": importance_df,
}
joblib.dump(model_artifacts, MODEL_PATH)
print("Model saved:", MODEL_PATH)

test_preds_class = np.argmax(test_preds, axis=1)
submission = pd.DataFrame(
    {"ID": test_ids, "Target": [TARGET_MAP_REVERSE[c] for c in test_preds_class]}
)
submission.to_csv(SUBMISSION_PATH, index=False)
print("Submission saved:", SUBMISSION_PATH)
submission.head()"""
    ),
]

save(MODELS / "financial_prediction_v3.ipynb", MODEL_CELLS)

import importlib.util

_eda_spec = importlib.util.spec_from_file_location(
    "build_eda_notebook",
    Path(__file__).parent / "build_eda_notebook.py",
)
_eda_mod = importlib.util.module_from_spec(_eda_spec)
_eda_spec.loader.exec_module(_eda_mod)
FIGURES.mkdir(parents=True, exist_ok=True)
save(EDA / "comprehensive_eda.ipynb", _eda_mod.EDA_CELLS)
(FIGURES / ".gitkeep").touch(exist_ok=True)
