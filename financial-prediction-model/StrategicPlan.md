# Data.org Financial Health Prediction Challenge - Strategic Improvement Plan

## Overview

This document outlines a systematic approach to improve the model from baseline to winning solution. Each version includes multiple trials and experiments to identify the best combinations.

**Competition Goal**: Predict the Financial Health Index (Low/Medium/High) of MSMEs across Southern Africa (Zimbabwe, Malawi, Eswatini, Lesotho)  
**Target Variable**: `Target` - Categorical (Low, Medium, High)  
**Evaluation Metric**: Multi-class Classification (likely Log Loss or F1-Score)  
**Strategy**: Incremental improvements with rigorous experimentation  

---

## Key Data Categories

| Category | Features |
|----------|----------|
| **Demographics** | country, owner_age, owner_sex |
| **Business Profile** | business_age_years, business_age_months, business_turnover, business_expenses |
| **Financial Access** | has_mobile_money, has_credit_card, has_debit_card, has_loan_account, has_internet_banking |
| **Insurance** | has_insurance, motor_vehicle_insurance, medical_insurance, funeral_insurance |
| **Attitudes** | attitude_stable_business_environment, attitude_worried_shutdown, attitude_satisfied_with_achievement, attitude_more_successful_next_year |
| **Perceptions** | perception_insurance_important, perception_cannot_afford_insurance, perception_insurance_doesnt_cover_losses |
| **Business Operations** | keeps_financial_records, offers_credit_to_customers, marketing_word_of_mouth, covid_essential_service |
| **Risk Factors** | current_problem_cash_flow, problem_sourcing_money, future_risk_theft_stock |

---

## Version Roadmap

| Version | Focus Area | Expected Score Improvement |
|---------|------------|---------------------------|
| V1 | Baseline Model | ~0.65-0.70 |
| V2 | Feature Engineering | +0.03-0.05 |
| V3 | Model Optimization | +0.02-0.04 |
| V4 | Advanced Encoding & Missing Values | +0.01-0.03 |
| V5 | Ensemble Methods | +0.02-0.03 |
| V6 | Fine-tuning & Class Imbalance | +0.01-0.02 |
| **Final** | **Winning Solution** | **~0.78-0.85** |

---

## Version 1: Baseline Model

### Goal
Establish a working pipeline with minimal preprocessing to understand the problem and set performance benchmarks.

---

### V1.0 - Absolute Baseline

**What to implement:**
```python
# Features: Only original columns (no engineering)
features = ['country', 'owner_age', 'owner_sex', 'business_age_years', 
            'business_turnover', 'business_expenses', 'personal_income',
            'has_mobile_money', 'has_insurance', 'keeps_financial_records']

# Model: Default LightGBM for multi-class
model = lgb.LGBMClassifier(
    objective='multiclass',
    num_class=3,
    random_state=42
)

# Validation: 5-fold stratified
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Target encoding: Map Low=0, Medium=1, High=2
target_map = {'Low': 0, 'Medium': 1, 'High': 2}
```

**Expected Results:**
- Accuracy: ~0.55-0.60
- Macro F1: ~0.45-0.50

**Log this as your absolute baseline - all improvements measured against this.**

---

### V1.1 - Handle Missing Values

**Trial A: Simple imputation**
```python
# Numeric columns: fill with median
numeric_cols = ['owner_age', 'personal_income', 'business_expenses', 
                'business_turnover', 'business_age_years', 'business_age_months']
for col in numeric_cols:
    df[col].fillna(df[col].median(), inplace=True)

# Categorical columns: fill with mode or 'Unknown'
cat_cols = ['country', 'owner_sex', 'has_mobile_money', 'has_insurance']
for col in cat_cols:
    df[col].fillna('Unknown', inplace=True)
```

**Trial B: Create missing indicator features**
```python
for col in ['personal_income', 'business_turnover', 'business_expenses']:
    df[f'{col}_missing'] = df[col].isna().astype(int)
```

**Trial C: Group-based imputation**
```python
# Fill missing income by country median
df['personal_income'] = df.groupby('country')['personal_income'].transform(
    lambda x: x.fillna(x.median())
)
```

**Combinations to test:**
| Trial | Imputation Method | Test Impact |
|-------|-------------------|-------------|
| V1.1a | Global median/mode | Baseline |
| V1.1b | V1.1a + missing indicators | Capture missingness signal |
| V1.1c | Country-based imputation | Regional differences |
| V1.1d | V1.1c + missing indicators | Combined approach |

---

### V1.2 - Simple Categorical Encoding

**Trial A: Label Encoding**
```python
from sklearn.preprocessing import LabelEncoder
for col in cat_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
```

**Trial B: Frequency Encoding**
```python
for col in cat_cols:
    freq = df[col].value_counts(normalize=True)
    df[f'{col}_freq'] = df[col].map(freq)
```

**Trial C: Binary columns already numeric-like**
```python
# Many columns have values like 'Yes', 'No', 'Have now', 'Never had', etc.
binary_map = {
    'Yes': 1, 'No': 0, 
    'Have now': 2, 'Used to have but don't have now': 1, 'Never had': 0,
    'Male': 1, 'Female': 0
}
```

**Combinations to test:**
| Trial | Encoding Method | Columns Applied |
|-------|-----------------|-----------------|
| V1.2a | Label Encoding | All categoricals |
| V1.2b | Ordinal mapping | Binary/ordinal columns |
| V1.2c | Label + Frequency | All + frequency features |

---

### V1.3 - Basic Attitude/Perception Cleaning

**Trial A: Standardize attitude responses**
```python
attitude_cols = ['attitude_stable_business_environment', 'attitude_worried_shutdown',
                 'attitude_satisfied_with_achievement', 'attitude_more_successful_next_year']

# Map to numeric
attitude_map = {'Yes': 1, 'No': 0, "Don't know or N/A": -1, '': -1}
for col in attitude_cols:
    df[col] = df[col].map(attitude_map).fillna(-1)
```

**Trial B: Create attitude score**
```python
# Positive attitudes sum
positive_attitudes = ['attitude_stable_business_environment', 
                      'attitude_satisfied_with_achievement',
                      'attitude_more_successful_next_year']
df['positive_attitude_score'] = df[positive_attitudes].sum(axis=1)
```

---

### V1 Summary Checkpoint

**Expected V1 Final Performance:**
- Accuracy: ~0.60-0.65
- Macro F1: ~0.50-0.55
- Log Loss: ~0.85-0.95

---

## Version 2: Feature Engineering Deep Dive

### Goal
Systematically engineer features from each data dimension to capture predictive patterns.

---

### V2.1 - Financial Ratio Features

**Trial A: Basic business metrics**
```python
# Profit margin proxy
df['profit_margin'] = (df['business_turnover'] - df['business_expenses']) / df['business_turnover'].clip(lower=1)

# Expense ratio
df['expense_ratio'] = df['business_expenses'] / df['business_turnover'].clip(lower=1)

# Personal income to business ratio
df['personal_to_business_ratio'] = df['personal_income'] / df['business_turnover'].clip(lower=1)
```

**Trial B: Business scale indicators**
```python
# Log transformations for skewed values
df['log_turnover'] = np.log1p(df['business_turnover'])
df['log_expenses'] = np.log1p(df['business_expenses'])
df['log_income'] = np.log1p(df['personal_income'])

# Business size category
df['business_size'] = pd.cut(df['business_turnover'], 
                              bins=[0, 10000, 50000, 200000, float('inf')],
                              labels=['micro', 'small', 'medium', 'large'])
```

**Trial C: Financial health indicators**
```python
# Is profitable?
df['is_profitable'] = (df['business_turnover'] > df['business_expenses']).astype(int)

# High expense warning
df['high_expense_ratio'] = (df['expense_ratio'] > 0.8).astype(int)

# Income diversification (personal vs business)
df['income_diversified'] = (df['personal_income'] > df['business_turnover'] * 0.5).astype(int)
```

**Combinations to test:**
| Trial | Financial Features | Focus |
|-------|-------------------|-------|
| V2.1a | Basic ratios | Core metrics |
| V2.1b | V2.1a + log transforms | Handle skewness |
| V2.1c | V2.1b + binary indicators | Clear signals |
| V2.1d | V2.1c + size categories | Segment effects |

---

### V2.2 - Business Experience Features

**Trial A: Total business age**
```python
df['total_business_months'] = (df['business_age_years'] * 12) + df['business_age_months'].fillna(0)
df['business_maturity'] = pd.cut(df['total_business_months'], 
                                  bins=[0, 12, 36, 60, 120, float('inf')],
                                  labels=['startup', 'young', 'established', 'mature', 'veteran'])
```

**Trial B: Experience-turnover interactions**
```python
# Turnover per year of operation
df['turnover_per_year'] = df['business_turnover'] / df['business_age_years'].clip(lower=1)

# Growth proxy
df['monthly_turnover'] = df['business_turnover'] / (df['total_business_months'].clip(lower=1))
```

**Trial C: Owner age interactions**
```python
# Age at business start
df['age_at_start'] = df['owner_age'] - df['business_age_years']

# Experience ratio
df['experience_ratio'] = df['business_age_years'] / df['owner_age'].clip(lower=1)

# Owner maturity category
df['owner_maturity'] = pd.cut(df['owner_age'], 
                               bins=[0, 25, 35, 45, 55, float('inf')],
                               labels=['young', 'early_career', 'mid_career', 'experienced', 'senior'])
```

---

### V2.3 - Financial Access Score

**Trial A: Create composite access scores**
```python
# Banking access features
banking_cols = ['has_mobile_money', 'has_credit_card', 'has_debit_card', 
                'has_loan_account', 'has_internet_banking']

# Convert to binary (1 if 'Have now', else 0)
for col in banking_cols:
    df[f'{col}_binary'] = (df[col] == 'Have now').astype(int)

df['banking_access_score'] = df[[f'{col}_binary' for col in banking_cols]].sum(axis=1)
```

**Trial B: Insurance coverage score**
```python
insurance_cols = ['has_insurance', 'motor_vehicle_insurance', 
                  'medical_insurance', 'funeral_insurance']

for col in insurance_cols:
    df[f'{col}_binary'] = df[col].isin(['Have now', 'Yes']).astype(int)

df['insurance_score'] = df[[f'{col}_binary' for col in insurance_cols]].sum(axis=1)
```

**Trial C: Total financial inclusion score**
```python
df['financial_inclusion_score'] = df['banking_access_score'] + df['insurance_score']

# Normalize to 0-1
df['financial_inclusion_normalized'] = df['financial_inclusion_score'] / df['financial_inclusion_score'].max()
```

---

### V2.4 - Attitude & Perception Engineering

**Trial A: Positive/Negative attitude balance**
```python
positive_cols = ['attitude_stable_business_environment', 
                 'attitude_satisfied_with_achievement',
                 'attitude_more_successful_next_year']

negative_cols = ['attitude_worried_shutdown', 'current_problem_cash_flow',
                 'problem_sourcing_money']

df['positive_attitude_count'] = sum((df[col] == 'Yes').astype(int) for col in positive_cols)
df['negative_attitude_count'] = sum((df[col] == 'Yes').astype(int) for col in negative_cols)
df['attitude_balance'] = df['positive_attitude_count'] - df['negative_attitude_count']
```

**Trial B: Insurance perception score**
```python
# Negative perceptions about insurance
perception_negative = ['perception_insurance_doesnt_cover_losses',
                       'perception_cannot_afford_insurance',
                       'perception_insurance_companies_dont_insure_businesses_like_yours']

df['insurance_perception_barriers'] = sum((df[col] == 'Yes').astype(int) for col in perception_negative)

# Positive perception
df['insurance_perceived_important'] = (df['perception_insurance_important'] == 'Yes').astype(int)

# Net insurance perception
df['insurance_perception_net'] = df['insurance_perceived_important'] - df['insurance_perception_barriers']
```

**Trial C: Risk awareness features**
```python
df['aware_of_theft_risk'] = (df['future_risk_theft_stock'] == 'Yes').astype(int)

# Risk-mitigation ratio
df['has_insurance_for_risk'] = (df['has_insurance'] == 'Yes') & (df['aware_of_theft_risk'] == 1)
df['risk_mitigation_aligned'] = df['has_insurance_for_risk'].astype(int)
```

---

### V2.5 - Business Operations Features

**Trial A: Business formality score**
```python
formality_indicators = [
    ('keeps_financial_records', 'Yes, always'),
    ('compliance_income_tax', 'Yes'),
    ('has_insurance', 'Yes'),
    ('covid_essential_service', 'Yes')
]

df['formality_score'] = sum((df[col] == val).astype(int) for col, val in formality_indicators)
```

**Trial B: Customer/Market engagement**
```python
df['offers_credit'] = (df['offers_credit_to_customers'].str.contains('Yes', na=False)).astype(int)
df['uses_word_of_mouth'] = (df['marketing_word_of_mouth'] == 'Yes').astype(int)
```

**Trial C: Informal finance usage**
```python
df['uses_informal_finance'] = (
    (df['uses_friends_family_savings'] == 'Have now') | 
    (df['uses_informal_lender'] == 'Have now')
).astype(int)

# Formal vs informal preference
df['formal_finance_preference'] = df['banking_access_score'] - df['uses_informal_finance']
```

---

### V2.6 - Country-Specific Features

**Trial A: Country one-hot encoding**
```python
country_dummies = pd.get_dummies(df['country'], prefix='country')
df = pd.concat([df, country_dummies], axis=1)
```

**Trial B: Country-level aggregates**
```python
# Average turnover by country
df['country_avg_turnover'] = df.groupby('country')['business_turnover'].transform('mean')
df['turnover_vs_country'] = df['business_turnover'] / df['country_avg_turnover'].clip(lower=1)

# Country insurance penetration
df['country_insurance_rate'] = df.groupby('country')['has_insurance'].transform(
    lambda x: (x == 'Yes').mean()
)
```

**Trial C: Country-business size interactions**
```python
df['country_size'] = df['country'] + '_' + df['business_size'].astype(str)
```

---

### V2 Summary Checkpoint

**Feature Selection Strategy:**
After all V2 experiments, analyze feature importance:

```python
importance_df = pd.DataFrame({
    'feature': feature_cols,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

# Keep top N features or those above threshold
top_features = importance_df[importance_df['importance'] > 0.005]['feature'].tolist()
```

**Expected V2 Final Performance:**
- Accuracy: ~0.65-0.70
- Macro F1: ~0.55-0.62
- Log Loss: ~0.75-0.85

---

## Version 3: Model Optimization

### Goal
Optimize model architecture, hyperparameters, and training process for multi-class classification.

---

### V3.1 - Algorithm Comparison

**Trial A: LightGBM (Default)**
```python
lgb_model = lgb.LGBMClassifier(
    objective='multiclass',
    num_class=3,
    n_estimators=1000,
    learning_rate=0.05,
    num_leaves=31,
    random_state=42
)
```

**Trial B: XGBoost**
```python
xgb_model = xgb.XGBClassifier(
    objective='multi:softprob',
    num_class=3,
    n_estimators=1000,
    learning_rate=0.05,
    max_depth=6,
    tree_method='hist',
    random_state=42
)
```

**Trial C: CatBoost**
```python
cat_model = CatBoostClassifier(
    loss_function='MultiClass',
    iterations=1000,
    learning_rate=0.05,
    depth=6,
    cat_features=categorical_columns,
    random_state=42,
    verbose=False
)
```

**Trial D: Random Forest**
```python
rf_model = RandomForestClassifier(
    n_estimators=500,
    max_depth=15,
    min_samples_leaf=10,
    random_state=42,
    n_jobs=-1
)
```

**Comparison Table:**
| Model | Accuracy | Macro F1 | Log Loss | Training Time |
|-------|----------|----------|----------|---------------|
| LightGBM | | | | |
| XGBoost | | | | |
| CatBoost | | | | |
| RandomForest | | | | |

**Decision**: Identify top 2-3 models for ensembling later

---

### V3.2 - LightGBM Hyperparameter Tuning

**Full Hyperparameter Search with Optuna:**
```python
def objective(trial):
    params = {
        'objective': 'multiclass',
        'num_class': 3,
        'metric': 'multi_logloss',
        'verbosity': -1,
        'boosting_type': 'gbdt',
        'random_state': 42,
        
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.15, log=True),
        'n_estimators': trial.suggest_int('n_estimators', 300, 2000),
        'num_leaves': trial.suggest_int('num_leaves', 20, 100),
        'max_depth': trial.suggest_int('max_depth', 4, 12),
        'min_child_samples': trial.suggest_int('min_child_samples', 5, 100),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'reg_alpha': trial.suggest_float('reg_alpha', 1e-4, 10.0, log=True),
        'reg_lambda': trial.suggest_float('reg_lambda', 1e-4, 10.0, log=True),
    }
    
    cv_scores = cross_val_score(lgb.LGBMClassifier(**params), X, y, 
                                 cv=5, scoring='f1_macro')
    return cv_scores.mean()

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)
```

---

### V3.3 - Class Imbalance Handling

**Trial A: Class weights**
```python
from sklearn.utils.class_weight import compute_class_weight

class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
weight_dict = dict(zip(np.unique(y_train), class_weights))

# LightGBM
params['class_weight'] = weight_dict
```

**Trial B: SMOTE for multi-class**
```python
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42, sampling_strategy='auto')
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
```

**Trial C: Custom sampling strategy**
```python
# Focus on minority class (e.g., if 'High' is rare)
sampling_strategy = {0: 5000, 1: 5000, 2: 5000}  # Equalize classes
```

**Comparison Table:**
| Method | Accuracy | Macro F1 | Notes |
|--------|----------|----------|-------|
| No weighting | | | |
| Class weights | | | |
| SMOTE | | | |
| Custom sampling | | | |

---

### V3 Summary Checkpoint

**Best Configuration Per Model:**
- LightGBM: [Document best params]
- XGBoost: [Document best params]
- CatBoost: [Document best params]

**Expected V3 Final Performance:**
- Accuracy: ~0.70-0.75
- Macro F1: ~0.60-0.68
- Log Loss: ~0.65-0.75

---

## Version 4: Advanced Encoding & Missing Value Strategies

### Goal
Apply sophisticated encoding strategies to extract maximum signal from categorical features.

---

### V4.1 - Target Encoding (Multi-Class)

**Trial A: Mean target encoding per class**
```python
def target_encode_multiclass_oof(train, test, col, target, n_splits=5):
    """OOF target encoding for multi-class - creates one feature per class"""
    from sklearn.model_selection import StratifiedKFold
    
    classes = sorted(train[target].unique())
    kf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    
    for cls in classes:
        train[f'{col}_te_class_{cls}'] = np.nan
        
        for train_idx, val_idx in kf.split(train, train[target]):
            # Calculate mean for this class from training fold
            class_rate = train.iloc[train_idx].groupby(col)[target].apply(
                lambda x: (x == cls).mean()
            )
            train.iloc[val_idx, train.columns.get_loc(f'{col}_te_class_{cls}')] = \
                train.iloc[val_idx][col].map(class_rate)
        
        # Fill NaN with global rate
        global_rate = (train[target] == cls).mean()
        train[f'{col}_te_class_{cls}'].fillna(global_rate, inplace=True)
        
        # For test, use all training data
        full_rate = train.groupby(col)[target].apply(lambda x: (x == cls).mean())
        test[f'{col}_te_class_{cls}'] = test[col].map(full_rate)
        test[f'{col}_te_class_{cls}'].fillna(global_rate, inplace=True)
    
    return train, test
```

**Columns to target encode:**
```python
te_columns = ['country', 'owner_sex', 'business_size', 'owner_maturity']
```

---

### V4.2 - Ordinal Encoding Strategy

**Trial A: Ordered categorical encoding**
```python
# Many features have inherent order
ordinal_mappings = {
    'has_mobile_money': {'Never had': 0, 'Used to have but don't have now': 1, 'Have now': 2},
    'has_credit_card': {'Never had': 0, 'Used to have but don't have now': 1, 'Have now': 2},
    'keeps_financial_records': {'No': 0, 'Yes, sometimes': 1, 'Yes, always': 2},
    'offers_credit_to_customers': {'No': 0, 'Yes, sometimes': 1, 'Yes, always': 2}
}

for col, mapping in ordinal_mappings.items():
    df[f'{col}_ordinal'] = df[col].map(mapping).fillna(-1)
```

---

### V4.3 - Missing Value Deep Dive

**Trial A: Missing pattern analysis**
```python
# Create missing pattern features
missing_patterns = df[['personal_income', 'business_turnover', 'business_expenses']].isna()
df['financial_data_missing_count'] = missing_patterns.sum(axis=1)
df['all_financial_missing'] = (df['financial_data_missing_count'] == 3).astype(int)
```

**Trial B: Predictive imputation**
```python
from sklearn.impute import KNNImputer

# Use KNN to impute missing financial values
imputer = KNNImputer(n_neighbors=5)
financial_cols = ['personal_income', 'business_turnover', 'business_expenses']
df[financial_cols] = imputer.fit_transform(df[financial_cols])
```

---

### V4 Summary Checkpoint

**Best Encoding Strategy:**
- Use OOF target encoding for: [list columns]
- Use ordinal encoding for: [list columns]
- Use frequency encoding for: [list columns]

**Expected V4 Final Performance:**
- Accuracy: ~0.72-0.77
- Macro F1: ~0.65-0.72
- Log Loss: ~0.60-0.70

---

## Version 5: Ensemble Methods

### Goal
Combine multiple models to improve robustness and performance.

---

### V5.1 - Simple Averaging Ensemble

**Trial A: Equal-weight averaging**
```python
# Predictions from different models (probability for each class)
pred_lgb = lgb_model.predict_proba(X_test)  # Shape: (n_samples, 3)
pred_xgb = xgb_model.predict_proba(X_test)
pred_cat = cat_model.predict_proba(X_test)

# Simple average
ensemble_proba = (pred_lgb + pred_xgb + pred_cat) / 3
ensemble_pred = np.argmax(ensemble_proba, axis=1)
```

---

### V5.2 - Weighted Averaging

**Trial A: CV-based weights**
```python
cv_f1_lgb = 0.68
cv_f1_xgb = 0.66
cv_f1_cat = 0.69

total = cv_f1_lgb + cv_f1_xgb + cv_f1_cat
weights = [cv_f1_lgb/total, cv_f1_xgb/total, cv_f1_cat/total]

ensemble_proba = weights[0]*pred_lgb + weights[1]*pred_xgb + weights[2]*pred_cat
```

**Trial B: Optimize weights with scipy**
```python
from scipy.optimize import minimize

def objective(weights):
    pred = weights[0]*oof_lgb + weights[1]*oof_xgb + weights[2]*oof_cat
    pred_classes = np.argmax(pred, axis=1)
    return -f1_score(y_train, pred_classes, average='macro')

constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
bounds = [(0, 1) for _ in range(3)]

result = minimize(objective, x0=[0.33, 0.33, 0.34], bounds=bounds, constraints=constraints)
```

---

### V5.3 - Multi-Seed Ensembling

**Trial A: Same model, different seeds**
```python
seeds = [42, 123, 456, 789, 2024]
predictions = []

for seed in seeds:
    model = lgb.LGBMClassifier(**params, random_state=seed)
    model.fit(X_train, y_train)
    pred = model.predict_proba(X_test)
    predictions.append(pred)

# Average across seeds
ensemble_proba = np.mean(predictions, axis=0)
```

---

### V5.4 - Stacking Ensemble

**Trial A: Level 1: OOF predictions as features**
```python
# Generate OOF predictions for each model
# OOF predictions have shape (n_train, 3) for 3 classes

# Create Level 2 data (9 features: 3 classes × 3 models)
X_level2_train = np.hstack([oof_lgb, oof_xgb, oof_cat])
X_level2_test = np.hstack([test_lgb, test_xgb, test_cat])
```

**Trial B: Level 2 meta-learners**
```python
# Option 1: Logistic Regression
meta_lr = LogisticRegression(multi_class='multinomial', max_iter=1000)
meta_lr.fit(X_level2_train, y_train)

# Option 2: LightGBM (light)
meta_lgb = lgb.LGBMClassifier(n_estimators=100, num_leaves=8, objective='multiclass')
```

---

### V5 Summary Checkpoint

**Best Ensemble Configuration:**
- Models included: [list]
- Weights: [list]
- Stacking meta-learner: [specify]

**Expected V5 Final Performance:**
- Accuracy: ~0.75-0.80
- Macro F1: ~0.70-0.75
- Log Loss: ~0.55-0.65

---

## Version 6: Final Optimization and Polish

### Goal
Fine-tune final predictions with post-processing and edge case handling.

---

### V6.1 - Post-Processing

**Trial A: Calibration**
```python
from sklearn.calibration import CalibratedClassifierCV

calibrated_model = CalibratedClassifierCV(model, method='isotonic', cv=5)
calibrated_model.fit(X_train, y_train)
```

**Trial B: Temperature scaling**
```python
# Soften or sharpen probability distributions
def temperature_scale(proba, T=1.0):
    proba_scaled = np.power(proba, 1/T)
    return proba_scaled / proba_scaled.sum(axis=1, keepdims=True)
```

**Trial C: Threshold optimization**
```python
# Optimize decision thresholds per class
from sklearn.metrics import f1_score

def find_optimal_thresholds(proba, y_true):
    # Grid search for best thresholds
    pass
```

---

### V6.2 - Pseudo-Labeling

**Trial A: High-confidence pseudo-labels**
```python
def add_pseudo_labels(X_train, y_train, X_test, model, confidence_threshold=0.9):
    test_proba = model.predict_proba(X_test)
    max_proba = test_proba.max(axis=1)
    confident_mask = max_proba >= confidence_threshold
    
    pseudo_labels = test_proba.argmax(axis=1)
    
    X_augmented = pd.concat([X_train, X_test[confident_mask]])
    y_augmented = pd.concat([y_train, pd.Series(pseudo_labels[confident_mask])])
    
    return X_augmented, y_augmented
```

---

### V6.3 - Feature Selection Refinement

**Trial A: Remove low-importance features**
```python
importance_threshold = 0.001
important_features = [f for f, imp in zip(feature_cols, model.feature_importances_) 
                      if imp >= importance_threshold]
```

**Trial B: Recursive feature elimination**
```python
from sklearn.feature_selection import RFECV

rfecv = RFECV(estimator=lgb.LGBMClassifier(**params), 
              step=10, cv=5, scoring='f1_macro', min_features_to_select=30)
rfecv.fit(X_train, y_train)
```

---

### V6.4 - Cross-Validation Refinement

**Trial A: Increase folds**
```python
# Standard: 5-fold
# Try: 7-fold, 10-fold for more stability
```

**Trial B: Repeated cross-validation**
```python
from sklearn.model_selection import RepeatedStratifiedKFold

rskf = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=42)
```

---

### V6.5 - Final Submission Strategy

**Strategy A: Single best model**
- Use model with highest CV score

**Strategy B: Ensemble final**
- Use best ensemble configuration

**Strategy C: Multiple submissions**
```python
# Submission 1: Best CV score model
# Submission 2: Best ensemble
# Submission 3: Conservative (calibrated) model
# Track which performs best on leaderboard
```

---

## Experiment Tracking Template

Use this template to track all experiments:

```markdown
### Experiment: [VERSION]-[TRIAL]
**Date**: YYYY-MM-DD
**Description**: [What you tested]

**Configuration**:
- Features: [Count and key features]
- Model: [Algorithm and key params]
- CV: [Strategy]

**Results**:
| Metric | Score |
|--------|-------|
| Accuracy | |
| Macro F1 | |
| Log Loss | |

**Observations**:
- [Key findings]

**Decision**: 
- [ ] Keep this approach
- [ ] Discard
- [ ] Combine with other approach
```

---

## Final Checklist

### Before Each Submission
- [ ] Cross-validation scores are stable
- [ ] No data leakage in feature engineering
- [ ] Target encoding uses OOF method
- [ ] Class predictions map correctly: 0→Low, 1→Medium, 2→High
- [ ] All test IDs included
- [ ] Submission format matches SampleSubmission.csv

### Code Quality
- [ ] Random seeds fixed for reproducibility
- [ ] Feature engineering applied identically to train/test
- [ ] Memory-efficient for large ensembles

### Documentation
- [ ] All experiments logged
- [ ] Best parameters documented
- [ ] Feature importance analyzed
- [ ] Ensemble weights recorded

---

## Expected Final Performance

After completing all versions:

| Metric | V1 Baseline | V6 Final | Improvement |
|--------|-------------|----------|-------------|
| Accuracy | 0.58 | 0.78+ | +0.20 |
| Macro F1 | 0.48 | 0.73+ | +0.25 |
| Log Loss | 0.90 | 0.55 | -0.35 |

---

## Quick Reference: What to Try When Stuck

### Score not improving?
1. Add more target encoding features
2. Try different aggregation levels by country
3. Increase ensemble diversity
4. Check for data leakage

### Overfitting (train >> validation)?
1. Increase regularization (reg_alpha, reg_lambda)
2. Reduce num_leaves / max_depth
3. Increase min_child_samples
4. Remove low-importance features
5. Use stronger class weights

### Validation unstable across folds?
1. Increase number of folds
2. Use repeated CV
3. Check for data leakage
4. Ensure stratification is working

### Poor minority class performance?
1. Use class weights
2. Try SMOTE oversampling
3. Adjust decision thresholds
4. Focus features on minority class signals

---

**Document Version**: 1.0  
**Created**: February 10, 2026  
**Competition**: Data.org Financial Health Prediction Challenge
