"""
Financial Health Prediction - Version 1.0 (Baseline Model)
============================================================
Competition: Data.org Financial Health Prediction Challenge
Goal: Predict Financial Health Index (Low/Medium/High) for MSMEs

This baseline model implements:
- Simple missing value imputation (median for numeric, mode for categorical)
- Label encoding for categorical features
- LightGBM multi-class classifier with default parameters
- 5-fold stratified cross-validation

Author: Competition Team
Date: February 2026
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score, log_loss, classification_report
import lightgbm as lgb
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# CONFIGURATION
# ============================================================
RANDOM_STATE = 42
N_FOLDS = 5
MODEL_NAME = 'financial_prediction_v1'

# Paths
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAIN_PATH = os.path.join(BASE_PATH, 'Train.csv')
TEST_PATH = os.path.join(BASE_PATH, 'Test.csv')
SUBMISSION_PATH = os.path.join(BASE_PATH, 'submissions', f'{MODEL_NAME}_submission.csv')
MODEL_PATH = os.path.join(BASE_PATH, 'models', f'{MODEL_NAME}_model.pkl')

# Target mapping
TARGET_MAP = {'Low': 0, 'Medium': 1, 'High': 2}
TARGET_MAP_REVERSE = {0: 'Low', 1: 'Medium', 2: 'High'}

# ============================================================
# DATA LOADING
# ============================================================
print("=" * 60)
print("FINANCIAL HEALTH PREDICTION - V1.0 BASELINE")
print("=" * 60)

print("\n[1/6] Loading data...")
train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

print(f"    Train shape: {train_df.shape}")
print(f"    Test shape: {test_df.shape}")

# Store IDs for submission
train_ids = train_df['ID'].copy()
test_ids = test_df['ID'].copy()

# Encode target
y = train_df['Target'].map(TARGET_MAP)
print(f"\n    Target distribution:")
print(f"    {train_df['Target'].value_counts().to_dict()}")

# ============================================================
# FEATURE ENGINEERING (V1 - MINIMAL)
# ============================================================
print("\n[2/6] Preprocessing features...")

# Drop ID and Target from features
feature_cols = [col for col in train_df.columns if col not in ['ID', 'Target']]

X_train = train_df[feature_cols].copy()
X_test = test_df[feature_cols].copy()

# Identify column types
numeric_cols = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = X_train.select_dtypes(include=['object']).columns.tolist()

print(f"    Numeric features: {len(numeric_cols)}")
print(f"    Categorical features: {len(categorical_cols)}")

# ============================================================
# MISSING VALUE IMPUTATION
# ============================================================
print("\n[3/6] Handling missing values...")

# Numeric: fill with median
for col in numeric_cols:
    median_val = X_train[col].median()
    X_train[col] = X_train[col].fillna(median_val)
    X_test[col] = X_test[col].fillna(median_val)

# Categorical: fill with mode (most frequent)
for col in categorical_cols:
    mode_val = X_train[col].mode()[0] if len(X_train[col].mode()) > 0 else 'Unknown'
    X_train[col] = X_train[col].fillna(mode_val)
    X_test[col] = X_test[col].fillna(mode_val)

print(f"    Missing values handled")

# ============================================================
# CATEGORICAL ENCODING (Label Encoding)
# ============================================================
print("\n[4/6] Encoding categorical features...")

label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    # Fit on combined train+test to handle unseen categories
    combined = pd.concat([X_train[col], X_test[col]], axis=0).astype(str)
    le.fit(combined)
    X_train[col] = le.transform(X_train[col].astype(str))
    X_test[col] = le.transform(X_test[col].astype(str))
    label_encoders[col] = le

print(f"    Encoded {len(categorical_cols)} categorical features")

# ============================================================
# MODEL TRAINING WITH CROSS-VALIDATION
# ============================================================
print("\n[5/6] Training LightGBM model with 5-fold CV...")

# LightGBM parameters (baseline - mostly defaults)
lgb_params = {
    'objective': 'multiclass',
    'num_class': 3,
    'metric': 'multi_logloss',
    'boosting_type': 'gbdt',
    'n_estimators': 500,
    'learning_rate': 0.05,
    'num_leaves': 31,
    'max_depth': -1,
    'min_child_samples': 20,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'random_state': RANDOM_STATE,
    'verbose': -1,
    'n_jobs': -1
}

# Stratified K-Fold
skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=RANDOM_STATE)

# Store OOF predictions and test predictions
oof_preds = np.zeros((len(X_train), 3))
test_preds = np.zeros((len(X_test), 3))

# Store metrics per fold
fold_scores = []

for fold, (train_idx, val_idx) in enumerate(skf.split(X_train, y), 1):
    print(f"\n    Fold {fold}/{N_FOLDS}...")
    
    # Split data
    X_tr, X_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
    y_tr, y_val = y.iloc[train_idx], y.iloc[val_idx]
    
    # Train model
    model = lgb.LGBMClassifier(**lgb_params)
    model.fit(
        X_tr, y_tr,
        eval_set=[(X_val, y_val)],
        callbacks=[lgb.early_stopping(50, verbose=False)]
    )
    
    # Predict on validation
    val_preds_proba = model.predict_proba(X_val)
    oof_preds[val_idx] = val_preds_proba
    
    # Predict on test (accumulate)
    test_preds += model.predict_proba(X_test) / N_FOLDS
    
    # Calculate metrics
    val_preds_class = np.argmax(val_preds_proba, axis=1)
    acc = accuracy_score(y_val, val_preds_class)
    f1 = f1_score(y_val, val_preds_class, average='macro')
    logloss = log_loss(y_val, val_preds_proba)
    
    fold_scores.append({'fold': fold, 'accuracy': acc, 'f1_macro': f1, 'log_loss': logloss})
    print(f"        Accuracy: {acc:.4f} | F1 Macro: {f1:.4f} | Log Loss: {logloss:.4f}")

# ============================================================
# OVERALL CV RESULTS
# ============================================================
print("\n" + "=" * 60)
print("CROSS-VALIDATION RESULTS")
print("=" * 60)

# OOF metrics
oof_preds_class = np.argmax(oof_preds, axis=1)
oof_acc = accuracy_score(y, oof_preds_class)
oof_f1 = f1_score(y, oof_preds_class, average='macro')
oof_logloss = log_loss(y, oof_preds)

print(f"\nOverall OOF Metrics:")
print(f"    Accuracy:   {oof_acc:.4f}")
print(f"    F1 Macro:   {oof_f1:.4f}")
print(f"    Log Loss:   {oof_logloss:.4f}")

# Per-fold summary
fold_df = pd.DataFrame(fold_scores)
print(f"\nPer-Fold Summary:")
print(f"    Accuracy:   {fold_df['accuracy'].mean():.4f} (+/- {fold_df['accuracy'].std():.4f})")
print(f"    F1 Macro:   {fold_df['f1_macro'].mean():.4f} (+/- {fold_df['f1_macro'].std():.4f})")
print(f"    Log Loss:   {fold_df['log_loss'].mean():.4f} (+/- {fold_df['log_loss'].std():.4f})")

# Classification report
print(f"\nClassification Report (OOF):")
print(classification_report(y, oof_preds_class, target_names=['Low', 'Medium', 'High']))

# ============================================================
# SAVE MODEL
# ============================================================
print("\n[6/6] Saving model and predictions...")

# Train final model on all data
final_model = lgb.LGBMClassifier(**lgb_params)
final_model.fit(X_train, y)

# Save model and encoders
model_artifacts = {
    'model': final_model,
    'label_encoders': label_encoders,
    'feature_cols': feature_cols,
    'numeric_cols': numeric_cols,
    'categorical_cols': categorical_cols,
    'target_map': TARGET_MAP,
    'target_map_reverse': TARGET_MAP_REVERSE,
    'cv_metrics': {
        'accuracy': oof_acc,
        'f1_macro': oof_f1,
        'log_loss': oof_logloss
    }
}

joblib.dump(model_artifacts, MODEL_PATH)
print(f"    Model saved to: {MODEL_PATH}")

# ============================================================
# CREATE SUBMISSION
# ============================================================

# Get class predictions from averaged test probabilities
test_preds_class = np.argmax(test_preds, axis=1)
test_preds_labels = [TARGET_MAP_REVERSE[c] for c in test_preds_class]

# Create submission DataFrame
submission = pd.DataFrame({
    'ID': test_ids,
    'Target': test_preds_labels
})

# Save submission
submission.to_csv(SUBMISSION_PATH, index=False)
print(f"    Submission saved to: {SUBMISSION_PATH}")

# ============================================================
# FEATURE IMPORTANCE
# ============================================================
print("\n" + "=" * 60)
print("TOP 15 FEATURE IMPORTANCE")
print("=" * 60)

importance_df = pd.DataFrame({
    'feature': feature_cols,
    'importance': final_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n")
for i, row in importance_df.head(15).iterrows():
    print(f"    {row['feature']:45s} : {row['importance']:>6.0f}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("V1.0 BASELINE COMPLETE")
print("=" * 60)
print(f"""
Model: LightGBM (multi-class)
Features: {len(feature_cols)} ({len(numeric_cols)} numeric, {len(categorical_cols)} categorical)
CV Strategy: {N_FOLDS}-fold Stratified
Encoding: Label Encoding

Results:
  - Accuracy:  {oof_acc:.4f}
  - F1 Macro:  {oof_f1:.4f}
  - Log Loss:  {oof_logloss:.4f}

Files saved:
  - Model: {MODEL_PATH}
  - Submission: {SUBMISSION_PATH}
""")
