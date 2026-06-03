"""
Financial Health Prediction - Version 3.0 (Data-Driven Feature Engineering)
=============================================================================
Competition: Data.org Financial Health Prediction Challenge
Goal: Predict Financial Health Index (Low/Medium/High) for MSMEs

Version 3.0 Improvements (based on deep data analysis):
- Focus on the strongest predictors identified:
  * funeral_insurance (V=0.55, MI=0.22) - STRONGEST predictor
  * Insurance pattern combinations (V up to 0.62)
  * Financial services adoption tiers (clear progression to High)
- Country-specific feature normalization
- Missing value patterns as predictive features
- Feature interactions between top predictors
- Optimized hyperparameters

Author: Competition Team
Date: February 2026
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
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
MODEL_NAME = 'financial_prediction_v3'

# Paths
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAIN_PATH = os.path.join(BASE_PATH, 'Train.csv')
TEST_PATH = os.path.join(BASE_PATH, 'Test.csv')
SUBMISSION_PATH = os.path.join(BASE_PATH, 'submissions', f'{MODEL_NAME}_submission.csv')
MODEL_PATH = os.path.join(BASE_PATH, 'models', f'{MODEL_NAME}_model.pkl')

# Target mapping
TARGET_MAP = {'Low': 0, 'Medium': 1, 'High': 2}
TARGET_MAP_REVERSE = {0: 'Low', 1: 'Medium', 2: 'High'}

# Binary mapping for categorical features
BINARY_MAP = {'Yes': 1, 'No': 0, 'Have now': 1, 'Used before': 0.5, 'Never had': 0,
              'Used to have but don\'t have now': 0.25}

print("=" * 80)
print("FINANCIAL HEALTH PREDICTION - V3.0 DATA-DRIVEN FEATURES")
print("=" * 80)

# ============================================================
# DATA LOADING
# ============================================================
print("\n[1/7] Loading data...")
train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

print(f"    Train shape: {train_df.shape}")
print(f"    Test shape: {test_df.shape}")

train_ids = train_df['ID'].copy()
test_ids = test_df['ID'].copy()

y = train_df['Target'].map(TARGET_MAP)
print(f"\n    Target distribution:")
print(f"    {train_df['Target'].value_counts().to_dict()}")

# ============================================================
# FEATURE ENGINEERING - V3 (DATA-DRIVEN)
# ============================================================
print("\n[2/7] Feature Engineering (Data-Driven Approach)...")

raw_feature_cols = [col for col in train_df.columns if col not in ['ID', 'Target']]
X_train = train_df[raw_feature_cols].copy()
X_test = test_df[raw_feature_cols].copy()

numeric_cols = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = X_train.select_dtypes(include=['object']).columns.tolist()

print(f"    Original features: {len(raw_feature_cols)}")

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def map_to_binary(series, extended_map=None):
    """Map categorical values to numeric with custom mapping"""
    if extended_map is None:
        extended_map = BINARY_MAP
    
    def mapper(val):
        if pd.isna(val):
            return np.nan
        val_str = str(val)
        for key, value in extended_map.items():
            if key.lower() in val_str.lower():
                return value
        return np.nan
    
    return series.apply(mapper)

def create_v3_features(df, is_train=True, train_stats=None):
    """
    Create features based on deep data analysis findings.
    Focus on strongest predictors and their interactions.
    """
    features = pd.DataFrame(index=df.index)
    
    # =====================================================
    # 1. FUNERAL INSURANCE FEATURES (STRONGEST PREDICTOR)
    # Analysis: V=0.55, MI=0.22, RF importance=0.39
    # =====================================================
    if 'funeral_insurance' in df.columns:
        # Detailed encoding
        funeral_map = {
            'Have now': 3,  # 80% Medium, 20% High
            'Used to have but don\'t have now': 1,  # 60-80% Low
            'Never had': 0,  # 83% Low
            'Don\'t know': 0.5
        }
        features['funeral_insurance_detailed'] = df['funeral_insurance'].apply(
            lambda x: funeral_map.get(str(x).strip() if pd.notna(x) else 'Never had', 0)
        )
        
        # Is current holder (key indicator for Medium/High)
        features['has_funeral_insurance_now'] = df['funeral_insurance'].apply(
            lambda x: 1 if pd.notna(x) and 'have now' in str(x).lower() else 0
        )
        
        # Ever had funeral insurance
        features['ever_had_funeral_insurance'] = df['funeral_insurance'].apply(
            lambda x: 1 if pd.notna(x) and ('have now' in str(x).lower() or 'used to' in str(x).lower()) else 0
        )
    
    # =====================================================
    # 2. INSURANCE ADOPTION FEATURES (TOP PREDICTORS)
    # Analysis: has_insurance V=0.32, medical V=0.26, motor V=0.25
    # =====================================================
    insurance_cols = ['has_insurance', 'motor_vehicle_insurance', 'medical_insurance', 'funeral_insurance']
    insurance_scores = []
    
    for col in insurance_cols:
        if col in df.columns:
            # Binary current holder
            is_current = df[col].apply(
                lambda x: 1 if pd.notna(x) and 'have now' in str(x).lower() else 0
            )
            features[f'{col}_current'] = is_current
            insurance_scores.append(is_current)
            
            # Has or has had
            has_ever = df[col].apply(
                lambda x: 1 if pd.notna(x) and ('have' in str(x).lower() or 'yes' in str(x).lower()) else 0
            )
            features[f'{col}_ever'] = has_ever
    
    # Composite insurance scores
    if insurance_scores:
        features['insurance_current_count'] = pd.concat(insurance_scores, axis=1).sum(axis=1)
        features['insurance_current_any'] = (features['insurance_current_count'] > 0).astype(int)
        
        # Insurance tier (clear progression in analysis)
        # 0 insurance = 89% Low, 4+ = mostly High
        def insurance_tier(count):
            if count == 0:
                return 0  # Very likely Low
            elif count == 1:
                return 1  # Likely Medium
            elif count >= 2:
                return 2  # Likely High
            return 0
        features['insurance_tier'] = features['insurance_current_count'].apply(insurance_tier)
    
    # =====================================================
    # 3. FINANCIAL SERVICES FEATURES (CLEAR PROGRESSION)
    # Analysis: 0 services=75.6% Low, 6 services=100% High
    # =====================================================
    financial_cols = ['has_mobile_money', 'has_credit_card', 'has_loan_account', 
                      'has_internet_banking', 'has_debit_card', 'has_cellphone']
    fin_scores = []
    
    for col in financial_cols:
        if col in df.columns:
            # Current holder
            is_current = df[col].apply(
                lambda x: 1 if pd.notna(x) and ('have now' in str(x).lower() or str(x).lower() == 'yes') else 0
            )
            features[f'{col}_current'] = is_current
            fin_scores.append(is_current)
    
    if fin_scores:
        features['financial_service_count'] = pd.concat(fin_scores, axis=1).sum(axis=1)
        
        # Financial service tier (based on analysis showing clear progression)
        def fin_tier(count):
            if count <= 1:
                return 0  # 69-76% Low
            elif count == 2:
                return 1  # 67% Low
            elif count == 3:
                return 2  # 45% Low, 17% High
            elif count >= 4:
                return 3  # 25% Low, 37% High
            return 0
        features['financial_service_tier'] = features['financial_service_count'].apply(fin_tier)
        
        # Digital banking specifically
        digital_cols = ['has_internet_banking', 'has_mobile_money', 'has_debit_card']
        digital_count = 0
        for col in digital_cols:
            if f'{col}_current' in features.columns:
                digital_count += features[f'{col}_current']
        features['digital_banking_count'] = digital_count
    
    # =====================================================
    # 4. STRONG FEATURE INTERACTIONS (FROM ANALYSIS)
    # Analysis: funeral × loan V=0.62, funeral × credit V=0.59
    # =====================================================
    
    # Funeral insurance × Financial services interaction
    if 'has_funeral_insurance_now' in features.columns and 'financial_service_count' in features.columns:
        features['funeral_finserv_interaction'] = features['has_funeral_insurance_now'] * features['financial_service_count']
    
    # Insurance × Credit card interaction
    if 'has_insurance_current' in features.columns and 'has_credit_card_current' in features.columns:
        features['insurance_credit_interaction'] = features['has_insurance_current'] * features['has_credit_card_current']
    
    # Create combined insurance pattern hash
    insurance_pattern_cols = ['has_insurance', 'motor_vehicle_insurance', 'medical_insurance', 'funeral_insurance']
    pattern_parts = []
    for col in insurance_pattern_cols:
        if col in df.columns:
            pattern_parts.append(df[col].fillna('NA').astype(str).str[:3])
    
    if pattern_parts:
        features['insurance_pattern'] = pattern_parts[0]
        for part in pattern_parts[1:]:
            features['insurance_pattern'] = features['insurance_pattern'] + '_' + part
    
    # =====================================================
    # 5. COUNTRY-SPECIFIC FEATURES (V=0.21)
    # Analysis: Eswatini 11.5% High, Malawi 81% Low
    # =====================================================
    if 'country' in df.columns:
        # Country encoding with target-aligned values
        country_map = {
            'eswatini': 3,   # Highest High rate (11.5%)
            'malawi': 0,     # Highest Low rate (81%)
            'zimbabwe': 1,   # 68.6% Low
            'lesotho': 2     # 60.4% Low, 39.3% Medium, almost no High
        }
        features['country_encoded'] = df['country'].map(country_map).fillna(1)
        
        # Country indicators
        for country in ['eswatini', 'malawi', 'zimbabwe', 'lesotho']:
            features[f'is_{country}'] = (df['country'] == country).astype(int)
        
        # Country × insurance interaction
        if 'insurance_current_count' in features.columns:
            features['country_insurance_interaction'] = features['country_encoded'] * features['insurance_current_count']
    
    # =====================================================
    # 6. BUSINESS FORMALIZATION FEATURES (V=0.22)
    # Analysis: keeps_financial_records V=0.22, compliance V=0.17
    # =====================================================
    formalization_scores = []
    
    if 'keeps_financial_records' in df.columns:
        record_map = {
            'Yes, always': 3,
            'Yes, sometimes': 2,
            'Yes': 2,
            'No': 0
        }
        features['keeps_records_score'] = df['keeps_financial_records'].apply(
            lambda x: record_map.get(str(x).strip() if pd.notna(x) else 'No', 0)
        )
        formalization_scores.append(features['keeps_records_score'] / 3)
    
    if 'compliance_income_tax' in df.columns:
        features['tax_compliant'] = df['compliance_income_tax'].apply(
            lambda x: 1 if pd.notna(x) and str(x).lower() == 'yes' else 0
        )
        formalization_scores.append(features['tax_compliant'])
    
    if 'offers_credit_to_customers' in df.columns:
        features['offers_credit'] = df['offers_credit_to_customers'].apply(
            lambda x: 1 if pd.notna(x) and str(x).lower() == 'yes' else 0
        )
        formalization_scores.append(features['offers_credit'])
    
    if 'marketing_word_of_mouth' in df.columns:
        features['uses_marketing'] = df['marketing_word_of_mouth'].apply(
            lambda x: 1 if pd.notna(x) and str(x).lower() == 'yes' else 0
        )
        formalization_scores.append(features['uses_marketing'])
    
    if formalization_scores:
        features['formalization_score'] = pd.concat(formalization_scores, axis=1).mean(axis=1)
    
    # =====================================================
    # 7. RISK INDICATORS
    # Analysis: current_problem_cash_flow V=0.16, uses_informal_lender V=0.19
    # =====================================================
    risk_scores = []
    
    if 'current_problem_cash_flow' in df.columns:
        features['has_cash_flow_problems'] = df['current_problem_cash_flow'].apply(
            lambda x: 1 if pd.notna(x) and str(x).lower() == 'yes' else 0
        )
        risk_scores.append(features['has_cash_flow_problems'])
    
    if 'problem_sourcing_money' in df.columns:
        features['had_funding_problems'] = df['problem_sourcing_money'].apply(
            lambda x: 1 if pd.notna(x) and str(x).lower() == 'yes' else 0
        )
        risk_scores.append(features['had_funding_problems'])
    
    if 'uses_informal_lender' in df.columns:
        features['uses_informal_lender_flag'] = df['uses_informal_lender'].apply(
            lambda x: 1 if pd.notna(x) and 'have now' in str(x).lower() else 0
        )
        risk_scores.append(features['uses_informal_lender_flag'])
    
    if 'uses_friends_family_savings' in df.columns:
        features['uses_informal_savings'] = df['uses_friends_family_savings'].apply(
            lambda x: 1 if pd.notna(x) and 'have now' in str(x).lower() else 0
        )
    
    if risk_scores:
        features['risk_score'] = pd.concat(risk_scores, axis=1).sum(axis=1)
    
    # =====================================================
    # 8. MISSING VALUE PATTERNS (STRONG SIGNAL)
    # Analysis: Missing patterns have high chi2 with target
    # =====================================================
    
    # Key groups with significant missing-target correlation
    insurance_miss_cols = ['motor_vehicle_insurance', 'medical_insurance', 'funeral_insurance']
    fin_miss_cols = ['has_loan_account', 'has_internet_banking', 'has_debit_card']
    
    features['insurance_missing_count'] = df[insurance_miss_cols].isnull().sum(axis=1) if all(c in df.columns for c in insurance_miss_cols) else 0
    features['financial_missing_count'] = df[fin_miss_cols].isnull().sum(axis=1) if all(c in df.columns for c in fin_miss_cols) else 0
    
    # Total missing count
    features['total_missing_count'] = df[raw_feature_cols].isnull().sum(axis=1)
    features['missing_pct'] = features['total_missing_count'] / len(raw_feature_cols)
    
    # Missing pattern indicator - high missing often correlates with specific countries/targets
    features['high_missing'] = (features['total_missing_count'] > 15).astype(int)
    
    # =====================================================
    # 9. PERCEPTION & ATTITUDE FEATURES
    # Analysis: Multiple perception features have moderate V
    # =====================================================
    
    # Positive attitudes
    positive_attitude_cols = [
        'attitude_stable_business_environment',
        'attitude_satisfied_with_achievement', 
        'attitude_more_successful_next_year'
    ]
    
    positive_scores = []
    attitude_map = {
        'Strongly agree': 5, 'Agree': 4, 'Neutral': 3, 'Disagree': 2, 'Strongly disagree': 1
    }
    
    for col in positive_attitude_cols:
        if col in df.columns:
            scores = df[col].apply(lambda x: attitude_map.get(str(x).strip() if pd.notna(x) else 'Neutral', 3))
            positive_scores.append(scores)
    
    if positive_scores:
        features['positive_attitude_score'] = pd.concat(positive_scores, axis=1).mean(axis=1)
    
    # Negative/worried attitudes
    if 'attitude_worried_shutdown' in df.columns:
        features['worried_shutdown_score'] = df['attitude_worried_shutdown'].apply(
            lambda x: attitude_map.get(str(x).strip() if pd.notna(x) else 'Neutral', 3)
        )
    
    # Insurance perception (can't afford, doesn't cover losses)
    perception_cols = [
        'perception_cannot_afford_insurance',
        'perception_insurance_doesnt_cover_losses',
        'perception_insurance_companies_dont_insure_businesses_like_yours'
    ]
    
    negative_perception_scores = []
    for col in perception_cols:
        if col in df.columns:
            # Higher score = more negative perception
            scores = df[col].apply(lambda x: attitude_map.get(str(x).strip() if pd.notna(x) else 'Neutral', 3))
            negative_perception_scores.append(scores)
    
    if negative_perception_scores:
        features['negative_insurance_perception'] = pd.concat(negative_perception_scores, axis=1).mean(axis=1)
    
    # Insurance importance perception
    if 'perception_insurance_important' in df.columns:
        features['insurance_important_score'] = df['perception_insurance_important'].apply(
            lambda x: attitude_map.get(str(x).strip() if pd.notna(x) else 'Neutral', 3)
        )
    
    # Net attitude
    if 'positive_attitude_score' in features.columns and 'worried_shutdown_score' in features.columns:
        features['net_attitude'] = features['positive_attitude_score'] - features['worried_shutdown_score']
    
    # =====================================================
    # 10. NUMERIC FEATURE ENGINEERING
    # Analysis: Low direct correlation, but interactions important
    # =====================================================
    
    # Log transformations (highly skewed data)
    for col in ['personal_income', 'business_expenses', 'business_turnover']:
        if col in df.columns:
            features[f'log_{col}'] = np.log1p(df[col].fillna(0).clip(lower=0))
    
    # Financial ratios
    if 'business_turnover' in df.columns and 'business_expenses' in df.columns:
        turnover = df['business_turnover'].fillna(0).clip(lower=0)
        expenses = df['business_expenses'].fillna(0).clip(lower=0)
        
        # Profit margin
        features['profit_margin'] = (turnover - expenses) / (turnover + 1)
        features['profit_margin'] = features['profit_margin'].clip(-10, 10)
        
        # Is profitable
        features['is_profitable'] = (turnover > expenses).astype(int)
        
        # Expense ratio
        features['expense_ratio'] = expenses / (turnover + 1)
        features['expense_ratio'] = features['expense_ratio'].clip(0, 10)
    
    # Business age features
    if 'business_age_years' in df.columns:
        features['business_age_years_filled'] = df['business_age_years'].fillna(df['business_age_years'].median())
        
        if 'business_age_months' in df.columns:
            features['total_business_months'] = df['business_age_years'] * 12 + df['business_age_months'].fillna(0)
        
        # Business maturity tier
        def maturity_tier(years):
            if pd.isna(years):
                return 1
            elif years < 2:
                return 0  # Startup
            elif years < 5:
                return 1  # Young
            elif years < 10:
                return 2  # Established
            else:
                return 3  # Mature
        features['business_maturity'] = df['business_age_years'].apply(maturity_tier)
    
    # Owner age features
    if 'owner_age' in df.columns:
        features['owner_age_filled'] = df['owner_age'].fillna(df['owner_age'].median())
        features['owner_age_squared'] = features['owner_age_filled'] ** 2
        
        # Age category
        def age_category(age):
            if pd.isna(age):
                return 2
            elif age < 30:
                return 0
            elif age < 45:
                return 1
            elif age < 55:
                return 2
            else:
                return 3
        features['owner_age_category'] = df['owner_age'].apply(age_category)
        
        # Started business at age (proxy for experience)
        if 'business_age_years' in df.columns:
            features['started_at_age'] = df['owner_age'] - df['business_age_years']
            features['started_at_age'] = features['started_at_age'].clip(lower=15)
    
    # Owner demographics
    if 'owner_sex' in df.columns:
        features['is_female_owner'] = (df['owner_sex'] == 'Female').astype(int)
    
    # =====================================================
    # 11. COVID IMPACT
    # Analysis: covid_essential_service V=0.14
    # =====================================================
    if 'covid_essential_service' in df.columns:
        features['was_essential_service'] = df['covid_essential_service'].apply(
            lambda x: 1 if pd.notna(x) and str(x).lower() == 'yes' else 0
        )
    
    # =====================================================
    # 12. COMPOSITE/INTERACTION FEATURES
    # =====================================================
    
    # Combined financial health indicator
    composite_parts = []
    if 'insurance_current_count' in features.columns:
        composite_parts.append(features['insurance_current_count'] * 0.4)
    if 'financial_service_count' in features.columns:
        composite_parts.append(features['financial_service_count'] * 0.3)
    if 'formalization_score' in features.columns:
        composite_parts.append(features['formalization_score'] * 3 * 0.3)
    
    if composite_parts:
        features['financial_health_composite'] = pd.concat(composite_parts, axis=1).sum(axis=1)
    
    # Insurance × Formalization
    if 'insurance_current_count' in features.columns and 'formalization_score' in features.columns:
        features['insurance_formalization_interaction'] = features['insurance_current_count'] * features['formalization_score']
    
    # Country-adjusted features
    if 'country_encoded' in features.columns:
        if 'log_business_turnover' in features.columns:
            features['country_turnover_interaction'] = features['country_encoded'] * features['log_business_turnover']
    
    return features

# ============================================================
# APPLY FEATURE ENGINEERING
# ============================================================
print("    Creating v3 features...")
engineered_train = create_v3_features(X_train, is_train=True)
engineered_test = create_v3_features(X_test, is_train=False)

print(f"    Engineered features: {engineered_train.shape[1]}")

# Combine with original features
X_train_combined = pd.concat([X_train, engineered_train], axis=1)
X_test_combined = pd.concat([X_test, engineered_test], axis=1)

# ============================================================
# PREPROCESSING
# ============================================================
print("\n[3/7] Preprocessing...")

all_numeric_cols = X_train_combined.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns.tolist()
all_categorical_cols = X_train_combined.select_dtypes(include=['object']).columns.tolist()

print(f"    Total numeric: {len(all_numeric_cols)}")
print(f"    Total categorical: {len(all_categorical_cols)}")

# Impute missing values
imputation_values = {}
for col in all_numeric_cols:
    median_val = X_train_combined[col].median()
    imputation_values[col] = median_val
    X_train_combined[col] = X_train_combined[col].fillna(median_val)
    X_test_combined[col] = X_test_combined[col].fillna(median_val)

for col in all_categorical_cols:
    mode_val = X_train_combined[col].mode()[0] if len(X_train_combined[col].mode()) > 0 else 'Unknown'
    imputation_values[col] = mode_val
    X_train_combined[col] = X_train_combined[col].fillna(mode_val)
    X_test_combined[col] = X_test_combined[col].fillna(mode_val)

# Encode categoricals
label_encoders = {}
for col in all_categorical_cols:
    le = LabelEncoder()
    combined = pd.concat([X_train_combined[col], X_test_combined[col]], axis=0).astype(str)
    le.fit(combined)
    X_train_combined[col] = le.transform(X_train_combined[col].astype(str))
    X_test_combined[col] = le.transform(X_test_combined[col].astype(str))
    label_encoders[col] = le

feature_cols = X_train_combined.columns.tolist()
print(f"    Final feature count: {len(feature_cols)}")

# ============================================================
# MODEL TRAINING
# ============================================================
print("\n[4/7] Training LightGBM with optimized parameters...")

# Optimized parameters based on v2 results and data characteristics
lgb_params = {
    'objective': 'multiclass',
    'num_class': 3,
    'metric': 'multi_logloss',
    'boosting_type': 'gbdt',
    'n_estimators': 1500,
    'learning_rate': 0.025,
    'num_leaves': 55,
    'max_depth': 8,
    'min_child_samples': 25,
    'subsample': 0.8,
    'subsample_freq': 1,
    'colsample_bytree': 0.7,
    'reg_alpha': 0.15,
    'reg_lambda': 0.15,
    'min_split_gain': 0.005,
    'random_state': RANDOM_STATE,
    'verbose': -1,
    'n_jobs': -1
}

skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=RANDOM_STATE)

oof_preds = np.zeros((len(X_train_combined), 3))
test_preds = np.zeros((len(X_test_combined), 3))
fold_scores = []
feature_importance_list = []

for fold, (train_idx, val_idx) in enumerate(skf.split(X_train_combined, y), 1):
    print(f"\n    Fold {fold}/{N_FOLDS}...")
    
    X_tr = X_train_combined.iloc[train_idx]
    X_val = X_train_combined.iloc[val_idx]
    y_tr, y_val = y.iloc[train_idx], y.iloc[val_idx]
    
    model = lgb.LGBMClassifier(**lgb_params)
    model.fit(
        X_tr, y_tr,
        eval_set=[(X_val, y_val)],
        callbacks=[lgb.early_stopping(150, verbose=False)]
    )
    
    feature_importance_list.append(model.feature_importances_)
    
    val_preds_proba = model.predict_proba(X_val)
    oof_preds[val_idx] = val_preds_proba
    test_preds += model.predict_proba(X_test_combined) / N_FOLDS
    
    val_preds_class = np.argmax(val_preds_proba, axis=1)
    acc = accuracy_score(y_val, val_preds_class)
    f1 = f1_score(y_val, val_preds_class, average='macro')
    logloss = log_loss(y_val, val_preds_proba)
    
    fold_scores.append({'fold': fold, 'accuracy': acc, 'f1_macro': f1, 'log_loss': logloss})
    print(f"        Accuracy: {acc:.4f} | F1 Macro: {f1:.4f} | Log Loss: {logloss:.4f}")

# ============================================================
# RESULTS
# ============================================================
print("\n" + "=" * 80)
print("CROSS-VALIDATION RESULTS")
print("=" * 80)

oof_preds_class = np.argmax(oof_preds, axis=1)
oof_acc = accuracy_score(y, oof_preds_class)
oof_f1 = f1_score(y, oof_preds_class, average='macro')
oof_logloss = log_loss(y, oof_preds)

print(f"\nOverall OOF Metrics:")
print(f"    Accuracy:   {oof_acc:.4f}")
print(f"    F1 Macro:   {oof_f1:.4f}")
print(f"    Log Loss:   {oof_logloss:.4f}")

fold_df = pd.DataFrame(fold_scores)
print(f"\nPer-Fold Summary:")
print(f"    Accuracy:   {fold_df['accuracy'].mean():.4f} (+/- {fold_df['accuracy'].std():.4f})")
print(f"    F1 Macro:   {fold_df['f1_macro'].mean():.4f} (+/- {fold_df['f1_macro'].std():.4f})")
print(f"    Log Loss:   {fold_df['log_loss'].mean():.4f} (+/- {fold_df['log_loss'].std():.4f})")

print(f"\nClassification Report (OOF):")
print(classification_report(y, oof_preds_class, target_names=['Low', 'Medium', 'High']))

# ============================================================
# FEATURE IMPORTANCE
# ============================================================
print("\n" + "=" * 80)
print("TOP 30 FEATURE IMPORTANCE")
print("=" * 80)

avg_importance = np.mean(feature_importance_list, axis=0)
importance_df = pd.DataFrame({
    'feature': feature_cols,
    'importance': avg_importance,
    'std': np.std(feature_importance_list, axis=0)
}).sort_values('importance', ascending=False)

# Mark engineered features
engineered_feature_names = engineered_train.columns.tolist()

print("\n")
for i, row in importance_df.head(30).iterrows():
    is_new = "NEW" if row['feature'] in engineered_feature_names else ""
    print(f"    {row['feature']:55s}: {row['importance']:>7.0f} (+/- {row['std']:>5.0f}) {is_new}")

# Count engineered features in top 30
top_30_features = importance_df.head(30)['feature'].tolist()
engineered_in_top_30 = sum(1 for f in top_30_features if f in engineered_feature_names)
print(f"\n    Engineered features in top 30: {engineered_in_top_30}")

# ============================================================
# SAVE MODEL
# ============================================================
print("\n[5/7] Saving model...")

final_model = lgb.LGBMClassifier(**lgb_params)
final_model.fit(X_train_combined, y)

model_artifacts = {
    'model': final_model,
    'label_encoders': label_encoders,
    'feature_cols': feature_cols,
    'imputation_values': imputation_values,
    'target_map': TARGET_MAP,
    'target_map_reverse': TARGET_MAP_REVERSE,
    'cv_metrics': {
        'accuracy': oof_acc,
        'f1_macro': oof_f1,
        'log_loss': oof_logloss
    },
    'importance_df': importance_df
}

joblib.dump(model_artifacts, MODEL_PATH)
print(f"    Model saved to: {MODEL_PATH}")

# ============================================================
# CREATE SUBMISSION
# ============================================================
print("\n[6/7] Creating submission...")

test_preds_class = np.argmax(test_preds, axis=1)
test_preds_labels = [TARGET_MAP_REVERSE[c] for c in test_preds_class]

submission = pd.DataFrame({
    'ID': test_ids,
    'Target': test_preds_labels
})

submission.to_csv(SUBMISSION_PATH, index=False)
print(f"    Submission saved to: {SUBMISSION_PATH}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 80)
print("V3.0 DATA-DRIVEN MODEL COMPLETE")
print("=" * 80)
print(f"""
Model: LightGBM (multi-class) with optimized parameters
Original Features: {len(raw_feature_cols)}
Engineered Features: {len(engineered_feature_names)}
Total Features: {len(feature_cols)}
CV Strategy: {N_FOLDS}-fold Stratified

Results:
  - Accuracy:  {oof_acc:.4f}
  - F1 Macro:  {oof_f1:.4f}
  - Log Loss:  {oof_logloss:.4f}

Key Feature Engineering (Data-Driven):
  1. Funeral insurance detailed encoding (STRONGEST predictor, V=0.55)
  2. Insurance current holder indicators & tier system
  3. Financial services count & tier (0 svc=76% Low, 6=100% High)
  4. Strong feature interactions (funeral×loan V=0.62)
  5. Country-specific encoding (Eswatini=11.5% High)
  6. Missing value patterns (significant chi2 with target)
  7. Formalization score (records + tax compliance)
  8. Risk indicators (cash flow, informal lending)
  9. Attitude composite scores
  10. Financial ratios with log transforms

Files saved:
  - Model: {MODEL_PATH}
  - Submission: {SUBMISSION_PATH}
""")
