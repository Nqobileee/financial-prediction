"""
Financial Health Prediction - Version 2.0 (Advanced Feature Engineering)
==========================================================================
Competition: Data.org Financial Health Prediction Challenge
Goal: Predict Financial Health Index (Low/Medium/High) for MSMEs

Version 2.0 Improvements:
- Comprehensive feature engineering with domain knowledge
- Feature correlation analysis and visualization
- Multiple encoding strategies (Target encoding, Frequency encoding)
- Feature interaction terms
- Robust missing value imputation
- Optimized LightGBM with better hyperparameters
- Feature importance and SHAP analysis

Author: Competition Team
Date: February 2026
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, f1_score, log_loss, classification_report
import lightgbm as lgb
import joblib
import os
import warnings
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
warnings.filterwarnings('ignore')

# ============================================================
# CONFIGURATION
# ============================================================
RANDOM_STATE = 42
N_FOLDS = 5
MODEL_NAME = 'financial_prediction_v2'
GENERATE_PLOTS = True  # Set to False to skip visualization

# Paths
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAIN_PATH = os.path.join(BASE_PATH, 'Train.csv')
TEST_PATH = os.path.join(BASE_PATH, 'Test.csv')
SUBMISSION_PATH = os.path.join(BASE_PATH, 'submissions', f'{MODEL_NAME}_submission.csv')
MODEL_PATH = os.path.join(BASE_PATH, 'models', f'{MODEL_NAME}_model.pkl')
PLOTS_PATH = os.path.join(BASE_PATH, 'models', 'v2_plots')

# Create plots directory
if GENERATE_PLOTS:
    os.makedirs(PLOTS_PATH, exist_ok=True)

# Target mapping
TARGET_MAP = {'Low': 0, 'Medium': 1, 'High': 2}
TARGET_MAP_REVERSE = {0: 'Low', 1: 'Medium', 2: 'High'}

# ============================================================
# DATA LOADING
# ============================================================
print("=" * 70)
print("FINANCIAL HEALTH PREDICTION - V2.0 ADVANCED FEATURE ENGINEERING")
print("=" * 70)

print("\n[1/8] Loading data...")
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
# EXPLORATORY DATA ANALYSIS & CORRELATION ANALYSIS
# ============================================================
print("\n[2/8] Exploratory Data Analysis & Correlation Analysis...")

# Drop ID and Target from features
raw_feature_cols = [col for col in train_df.columns if col not in ['ID', 'Target']]
X_train_raw = train_df[raw_feature_cols].copy()
X_test_raw = test_df[raw_feature_cols].copy()

# Identify column types
numeric_cols = X_train_raw.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = X_train_raw.select_dtypes(include=['object']).columns.tolist()

print(f"    Original Numeric features: {len(numeric_cols)}")
print(f"    Original Categorical features: {len(categorical_cols)}")

# Missing value analysis
missing_df = pd.DataFrame({
    'column': raw_feature_cols,
    'missing_train': [X_train_raw[col].isnull().sum() for col in raw_feature_cols],
    'missing_pct_train': [X_train_raw[col].isnull().mean() * 100 for col in raw_feature_cols],
    'missing_test': [X_test_raw[col].isnull().sum() for col in raw_feature_cols],
    'missing_pct_test': [X_test_raw[col].isnull().mean() * 100 for col in raw_feature_cols]
}).sort_values('missing_pct_train', ascending=False)

print("\n    Top 10 features by missing %:")
for i, row in missing_df.head(10).iterrows():
    print(f"        {row['column']:55s}: {row['missing_pct_train']:.1f}%")

# ============================================================
# CORRELATION ANALYSIS FOR NUMERIC FEATURES
# ============================================================
print("\n[3/8] Correlation Analysis...")

# Create a temporary dataframe with numeric features and target for correlation
corr_df = X_train_raw[numeric_cols].copy()
corr_df['Target'] = y

# Calculate correlations with target
correlations = {}
for col in numeric_cols:
    # Remove NaN rows for correlation calculation
    temp_df = corr_df[[col, 'Target']].dropna()
    if len(temp_df) > 100:
        corr, p_value = stats.spearmanr(temp_df[col], temp_df['Target'])
        correlations[col] = {'correlation': corr, 'p_value': p_value, 'n_samples': len(temp_df)}

corr_results_df = pd.DataFrame(correlations).T
corr_results_df = corr_results_df.sort_values('correlation', key=abs, ascending=False)

print("\n    Numeric Feature Correlations with Target (Spearman):")
for col, row in corr_results_df.iterrows():
    strength = "STRONG" if abs(row['correlation']) > 0.2 else "MEDIUM" if abs(row['correlation']) > 0.1 else "weak"
    print(f"        {col:35s}: r={row['correlation']:+.4f} (p={row['p_value']:.4e}) [{strength}]")

# ============================================================
# CATEGORICAL FEATURE ANALYSIS
# ============================================================
print("\n[4/8] Categorical Feature Analysis...")

# Analyze relationship between categorical features and target
cat_target_analysis = {}
for col in categorical_cols:
    temp_df = train_df[[col, 'Target']].dropna()
    if len(temp_df) > 100:
        # Chi-square test
        contingency = pd.crosstab(temp_df[col], temp_df['Target'])
        if contingency.shape[0] > 1 and contingency.shape[1] > 1:
            chi2, p_value, dof, expected = stats.chi2_contingency(contingency)
            # Cramér's V for effect size
            n = contingency.sum().sum()
            min_dim = min(contingency.shape) - 1
            cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0
            cat_target_analysis[col] = {
                'chi2': chi2, 
                'p_value': p_value, 
                'cramers_v': cramers_v,
                'n_categories': contingency.shape[0]
            }

cat_results_df = pd.DataFrame(cat_target_analysis).T
cat_results_df = cat_results_df.sort_values('cramers_v', ascending=False)

print("\n    Categorical Feature Associations with Target (Cramer's V):")
for col, row in cat_results_df.head(20).iterrows():
    strength = "STRONG" if row['cramers_v'] > 0.2 else "MEDIUM" if row['cramers_v'] > 0.1 else "weak"
    print(f"        {col:60s}: V={row['cramers_v']:.4f} (χ²={row['chi2']:.1f}, p={row['p_value']:.4e}) [{strength}]")

# ============================================================
# VISUALIZATION
# ============================================================
if GENERATE_PLOTS:
    print("\n[5/8] Generating Visualizations...")
    
    # 1. Numeric feature distributions by target
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, col in enumerate(numeric_cols):
        ax = axes[i]
        for target_val in ['Low', 'Medium', 'High']:
            data = train_df[train_df['Target'] == target_val][col].dropna()
            if len(data) > 0:
                ax.hist(data, bins=50, alpha=0.5, label=target_val, density=True)
        ax.set_title(f'{col}')
        ax.set_xlabel(col)
        ax.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_PATH, 'numeric_distributions_by_target.png'), dpi=150)
    plt.close()
    print(f"    Saved: numeric_distributions_by_target.png")
    
    # 2. Correlation heatmap of numeric features
    fig, ax = plt.subplots(figsize=(10, 8))
    numeric_corr = X_train_raw[numeric_cols].corr()
    sns.heatmap(numeric_corr, annot=True, cmap='coolwarm', center=0, fmt='.2f', ax=ax)
    plt.title('Numeric Feature Correlations')
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_PATH, 'numeric_correlation_heatmap.png'), dpi=150)
    plt.close()
    print(f"    Saved: numeric_correlation_heatmap.png")
    
    # 3. Top categorical features by target
    top_cat_cols = cat_results_df.head(6).index.tolist()
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    
    for i, col in enumerate(top_cat_cols):
        ax = axes[i]
        cross_tab = pd.crosstab(train_df[col], train_df['Target'], normalize='index') * 100
        cross_tab[['Low', 'Medium', 'High']].plot(kind='bar', ax=ax, stacked=True)
        ax.set_title(f'{col[:40]}...' if len(col) > 40 else col)
        ax.set_xlabel('')
        ax.tick_params(axis='x', rotation=45)
        ax.legend(title='Target')
        ax.set_ylabel('Percentage')
    
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_PATH, 'top_categorical_by_target.png'), dpi=150)
    plt.close()
    print(f"    Saved: top_categorical_by_target.png")
    
    # 4. Box plots for numeric features by target
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for i, col in enumerate(numeric_cols):
        ax = axes[i]
        data_to_plot = []
        labels = []
        for target_val in ['Low', 'Medium', 'High']:
            data = train_df[train_df['Target'] == target_val][col].dropna()
            if len(data) > 0:
                # Log transform for skewed data
                data_log = np.log1p(data[data > 0]) if data.min() >= 0 else data
                data_to_plot.append(data_log)
                labels.append(target_val)
        
        if data_to_plot:
            bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True)
            colors = ['lightblue', 'lightgreen', 'lightsalmon']
            for patch, color in zip(bp['boxes'], colors):
                patch.set_facecolor(color)
        ax.set_title(f'{col} (log scale)')
        ax.set_xlabel('Target')
    
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_PATH, 'numeric_boxplots_by_target.png'), dpi=150)
    plt.close()
    print(f"    Saved: numeric_boxplots_by_target.png")
    
    # 5. Missing value pattern
    fig, ax = plt.subplots(figsize=(14, 8))
    missing_matrix = X_train_raw.isnull().astype(int)
    # Sample for visualization
    sample_idx = np.random.choice(len(missing_matrix), min(500, len(missing_matrix)), replace=False)
    sns.heatmap(missing_matrix.iloc[sample_idx], cbar=True, yticklabels=False, ax=ax, cmap='YlOrRd')
    ax.set_title('Missing Value Pattern (Sample)')
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_PATH, 'missing_value_pattern.png'), dpi=150)
    plt.close()
    print(f"    Saved: missing_value_pattern.png")

else:
    print("\n[5/8] Skipping visualizations (GENERATE_PLOTS=False)")

# ============================================================
# ADVANCED FEATURE ENGINEERING
# ============================================================
print("\n[6/8] Advanced Feature Engineering...")

# Work with copies
X_train = X_train_raw.copy()
X_test = X_test_raw.copy()

# --- Feature Engineering Functions ---

def create_financial_features(df):
    """Create financial ratio and derived features"""
    features = pd.DataFrame(index=df.index)
    
    # 1. Financial Ratios
    # Profit margin proxy (turnover - expenses) / turnover
    features['profit_margin'] = (df['business_turnover'] - df['business_expenses']) / (df['business_turnover'] + 1)
    features['profit_margin'] = features['profit_margin'].replace([np.inf, -np.inf], 0)
    
    # Monthly turnover estimate (assuming annual turnover)
    features['monthly_turnover'] = df['business_turnover'] / 12
    
    # Monthly profit estimate
    features['monthly_profit'] = (df['business_turnover'] - df['business_expenses']) / 12
    features['monthly_profit'] = features['monthly_profit'].replace([np.inf, -np.inf], 0)
    
    # Expense to turnover ratio
    features['expense_turnover_ratio'] = df['business_expenses'] / (df['business_turnover'] + 1)
    features['expense_turnover_ratio'] = features['expense_turnover_ratio'].replace([np.inf, -np.inf], 0)
    
    # Personal income to business turnover ratio
    features['personal_business_ratio'] = df['personal_income'] / (df['business_turnover'] + 1)
    features['personal_business_ratio'] = features['personal_business_ratio'].replace([np.inf, -np.inf], 0)
    
    # 2. Business Maturity Features
    # Total business age in months
    features['total_business_age_months'] = df['business_age_years'] * 12 + df['business_age_months'].fillna(0)
    
    # Business maturity category
    def categorize_maturity(months):
        if pd.isna(months):
            return np.nan
        elif months <= 12:
            return 0  # Startup
        elif months <= 36:
            return 1  # Early stage
        elif months <= 60:
            return 2  # Growth
        elif months <= 120:
            return 3  # Established
        else:
            return 4  # Mature
    
    features['business_maturity'] = features['total_business_age_months'].apply(categorize_maturity)
    
    # 3. Scale indicators
    # Log transformations for highly skewed features
    features['log_turnover'] = np.log1p(df['business_turnover'].fillna(0).clip(lower=0))
    features['log_expenses'] = np.log1p(df['business_expenses'].fillna(0).clip(lower=0))
    features['log_personal_income'] = np.log1p(df['personal_income'].fillna(0).clip(lower=0))
    
    # 4. Turnover per year of business
    features['turnover_per_year'] = df['business_turnover'] / (df['business_age_years'] + 1)
    features['turnover_per_year'] = features['turnover_per_year'].replace([np.inf, -np.inf], 0)
    
    # 5. Owner age related features
    features['owner_age_squared'] = df['owner_age'] ** 2
    
    # Owner experience proxy (age - assumed start age)
    features['owner_experience'] = df['owner_age'] - 22  # Assuming business start typically after education
    features['owner_experience'] = features['owner_experience'].clip(lower=0)
    
    # Age category
    def categorize_age(age):
        if pd.isna(age):
            return np.nan
        elif age < 25:
            return 0  # Young
        elif age < 35:
            return 1  # Early career
        elif age < 45:
            return 2  # Mid career
        elif age < 55:
            return 3  # Experienced
        else:
            return 4  # Senior
    
    features['owner_age_category'] = df['owner_age'].apply(categorize_age)
    
    return features

def create_attitude_score(df):
    """Create composite attitude/perception scores"""
    features = pd.DataFrame(index=df.index)
    
    # Positive attitudes (higher = better)
    positive_cols = [
        'attitude_stable_business_environment',
        'attitude_satisfied_with_achievement',
        'attitude_more_successful_next_year'
    ]
    
    # Negative attitudes (higher = worse)
    negative_cols = [
        'attitude_worried_shutdown',
        'perception_insurance_doesnt_cover_losses',
        'perception_cannot_afford_insurance',
        'perception_insurance_companies_dont_insure_businesses_like_yours'
    ]
    
    # Map categorical responses to numeric scores
    attitude_map = {
        'Strongly agree': 5, 'Agree': 4, 'Neutral': 3, 'Disagree': 2, 'Strongly disagree': 1,
        'Yes': 1, 'No': 0
    }
    
    # Calculate positive attitude score
    positive_scores = []
    for col in positive_cols:
        if col in df.columns:
            scores = df[col].map(attitude_map)
            positive_scores.append(scores)
    
    if positive_scores:
        features['positive_attitude_score'] = pd.concat(positive_scores, axis=1).mean(axis=1)
    
    # Calculate negative attitude score (inverted so higher = more negative)
    negative_scores = []
    for col in negative_cols:
        if col in df.columns:
            scores = df[col].map(attitude_map)
            negative_scores.append(scores)
    
    if negative_scores:
        features['negative_attitude_score'] = pd.concat(negative_scores, axis=1).mean(axis=1)
    
    # Net attitude score
    if 'positive_attitude_score' in features.columns and 'negative_attitude_score' in features.columns:
        features['net_attitude_score'] = features['positive_attitude_score'] - features['negative_attitude_score']
    
    return features

def create_insurance_adoption_score(df):
    """Create insurance adoption and risk management scores"""
    features = pd.DataFrame(index=df.index)
    
    insurance_cols = [
        'has_insurance',
        'motor_vehicle_insurance',
        'medical_insurance',
        'funeral_insurance'
    ]
    
    # Map to binary
    binary_map = {'Yes': 1, 'No': 0, 'Have now': 1, 'Used before': 0.5, 'Never had': 0}
    
    insurance_scores = []
    for col in insurance_cols:
        if col in df.columns:
            scores = df[col].map(binary_map)
            insurance_scores.append(scores)
            # Individual indicator
            features[f'{col}_binary'] = scores
    
    if insurance_scores:
        features['insurance_adoption_score'] = pd.concat(insurance_scores, axis=1).sum(axis=1)
        features['insurance_count'] = pd.concat(insurance_scores, axis=1).notna().sum(axis=1) - \
                                       pd.concat(insurance_scores, axis=1).isna().sum(axis=1)
    
    return features

def create_financial_services_score(df):
    """Create financial services adoption score"""
    features = pd.DataFrame(index=df.index)
    
    financial_service_cols = [
        'has_mobile_money',
        'has_credit_card',
        'has_loan_account',
        'has_internet_banking',
        'has_debit_card',
        'has_cellphone'
    ]
    
    binary_map = {'Yes': 1, 'No': 0, 'Have now': 1, 'Used before': 0.5, 'Never had': 0}
    
    financial_scores = []
    for col in financial_service_cols:
        if col in df.columns:
            scores = df[col].map(binary_map)
            financial_scores.append(scores)
            features[f'{col}_binary'] = scores
    
    if financial_scores:
        features['financial_services_score'] = pd.concat(financial_scores, axis=1).sum(axis=1)
        features['digital_banking_score'] = 0
        if 'has_internet_banking' in df.columns:
            features['digital_banking_score'] += df['has_internet_banking'].map(binary_map).fillna(0)
        if 'has_mobile_money' in df.columns:
            features['digital_banking_score'] += df['has_mobile_money'].map(binary_map).fillna(0)
    
    return features

def create_business_practices_score(df):
    """Create business practices/formalization score"""
    features = pd.DataFrame(index=df.index)
    
    binary_map = {'Yes': 1, 'No': 0, 'Have now': 1, 'Used before': 0.5, 'Never had': 0}
    
    # Good practices indicators
    good_practices = []
    
    if 'keeps_financial_records' in df.columns:
        scores = df['keeps_financial_records'].map(binary_map)
        good_practices.append(scores)
        features['keeps_records_binary'] = scores
    
    if 'compliance_income_tax' in df.columns:
        scores = df['compliance_income_tax'].map(binary_map)
        good_practices.append(scores)
        features['tax_compliant_binary'] = scores
    
    if 'offers_credit_to_customers' in df.columns:
        scores = df['offers_credit_to_customers'].map(binary_map)
        good_practices.append(scores)
        features['offers_credit_binary'] = scores
    
    if 'marketing_word_of_mouth' in df.columns:
        scores = df['marketing_word_of_mouth'].map(binary_map)
        good_practices.append(scores)
        features['uses_marketing_binary'] = scores
    
    if good_practices:
        features['business_practices_score'] = pd.concat(good_practices, axis=1).sum(axis=1)
    
    return features

def create_risk_indicators(df):
    """Create risk indicator features"""
    features = pd.DataFrame(index=df.index)
    
    binary_map = {'Yes': 1, 'No': 0, 'Have now': 1, 'Used before': 0.5, 'Never had': 0}
    
    # Risk factors
    risk_indicators = []
    
    if 'current_problem_cash_flow' in df.columns:
        scores = df['current_problem_cash_flow'].map(binary_map)
        risk_indicators.append(scores)
        features['has_cash_flow_problems'] = scores
    
    if 'problem_sourcing_money' in df.columns:
        scores = df['problem_sourcing_money'].map(binary_map)
        risk_indicators.append(scores)
        features['had_funding_problems'] = scores
    
    if 'future_risk_theft_stock' in df.columns:
        scores = df['future_risk_theft_stock'].map(binary_map)
        risk_indicators.append(scores)
        features['expects_theft_risk'] = scores
    
    if 'uses_informal_lender' in df.columns:
        scores = df['uses_informal_lender'].map(binary_map)
        risk_indicators.append(scores)
        features['uses_informal_lending'] = scores
    
    if risk_indicators:
        features['risk_score'] = pd.concat(risk_indicators, axis=1).sum(axis=1)
    
    return features

def create_country_features(df, train_stats=None):
    """Create country-specific features with target encoding"""
    features = pd.DataFrame(index=df.index)
    
    if 'country' in df.columns:
        # Country indicator (one-hot)
        for country in df['country'].unique():
            features[f'is_{country}'] = (df['country'] == country).astype(int)
    
    return features, train_stats

def create_interaction_features(df, feature_df):
    """Create feature interactions"""
    features = pd.DataFrame(index=df.index)
    
    # Business scale × maturity interaction
    if 'log_turnover' in feature_df.columns and 'total_business_age_months' in feature_df.columns:
        features['scale_maturity_interaction'] = feature_df['log_turnover'] * feature_df['total_business_age_months']
    
    # Owner age × business age interaction
    if 'owner_age' in df.columns and 'business_age_years' in df.columns:
        features['owner_business_age_ratio'] = df['owner_age'] / (df['business_age_years'] + 1)
        features['started_business_at_age'] = df['owner_age'] - df['business_age_years']
    
    # Financial services × business scale
    if 'financial_services_score' in feature_df.columns and 'log_turnover' in feature_df.columns:
        features['finserv_scale_interaction'] = feature_df['financial_services_score'] * feature_df['log_turnover']
    
    return features

def create_missing_indicator_features(df):
    """Create features that indicate missing value patterns"""
    features = pd.DataFrame(index=df.index)
    
    # Total missing count
    features['total_missing_count'] = df.isnull().sum(axis=1)
    features['total_missing_pct'] = df.isnull().mean(axis=1)
    
    # Missing in key financial columns
    financial_cols = ['personal_income', 'business_expenses', 'business_turnover']
    features['missing_financial_count'] = df[financial_cols].isnull().sum(axis=1)
    
    # Missing in attitude columns
    attitude_cols = [col for col in df.columns if 'attitude' in col.lower()]
    if attitude_cols:
        features['missing_attitude_count'] = df[attitude_cols].isnull().sum(axis=1)
    
    # Missing in insurance columns
    insurance_cols = [col for col in df.columns if 'insurance' in col.lower()]
    if insurance_cols:
        features['missing_insurance_count'] = df[insurance_cols].isnull().sum(axis=1)
    
    return features

# --- Apply Feature Engineering ---
print("    Creating financial features...")
fin_features_train = create_financial_features(X_train)
fin_features_test = create_financial_features(X_test)

print("    Creating attitude scores...")
att_features_train = create_attitude_score(X_train)
att_features_test = create_attitude_score(X_test)

print("    Creating insurance adoption scores...")
ins_features_train = create_insurance_adoption_score(X_train)
ins_features_test = create_insurance_adoption_score(X_test)

print("    Creating financial services scores...")
fs_features_train = create_financial_services_score(X_train)
fs_features_test = create_financial_services_score(X_test)

print("    Creating business practices scores...")
bp_features_train = create_business_practices_score(X_train)
bp_features_test = create_business_practices_score(X_test)

print("    Creating risk indicators...")
risk_features_train = create_risk_indicators(X_train)
risk_features_test = create_risk_indicators(X_test)

print("    Creating country features...")
country_features_train, _ = create_country_features(X_train)
country_features_test, _ = create_country_features(X_test)

print("    Creating missing indicator features...")
missing_features_train = create_missing_indicator_features(X_train)
missing_features_test = create_missing_indicator_features(X_test)

# Combine all engineered features
all_engineered_train = pd.concat([
    fin_features_train, att_features_train, ins_features_train, 
    fs_features_train, bp_features_train, risk_features_train,
    country_features_train, missing_features_train
], axis=1)

all_engineered_test = pd.concat([
    fin_features_test, att_features_test, ins_features_test,
    fs_features_test, bp_features_test, risk_features_test,
    country_features_test, missing_features_test
], axis=1)

# Create interaction features using engineered features
print("    Creating interaction features...")
interaction_train = create_interaction_features(X_train, all_engineered_train)
interaction_test = create_interaction_features(X_test, all_engineered_test)

all_engineered_train = pd.concat([all_engineered_train, interaction_train], axis=1)
all_engineered_test = pd.concat([all_engineered_test, interaction_test], axis=1)

print(f"    Total engineered features: {all_engineered_train.shape[1]}")

# ============================================================
# COMBINE WITH ORIGINAL FEATURES
# ============================================================
X_train_combined = pd.concat([X_train, all_engineered_train], axis=1)
X_test_combined = pd.concat([X_test, all_engineered_test], axis=1)

# ============================================================
# MISSING VALUE IMPUTATION (Advanced)
# ============================================================
print("\n[7/8] Advanced Missing Value Imputation...")

# Separate numeric and categorical
all_numeric_cols = X_train_combined.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns.tolist()
all_categorical_cols = X_train_combined.select_dtypes(include=['object']).columns.tolist()

print(f"    Total numeric features: {len(all_numeric_cols)}")
print(f"    Total categorical features: {len(all_categorical_cols)}")

# Store imputation values
imputation_values = {}

# Numeric: fill with median
for col in all_numeric_cols:
    median_val = X_train_combined[col].median()
    imputation_values[col] = median_val
    X_train_combined[col] = X_train_combined[col].fillna(median_val)
    X_test_combined[col] = X_test_combined[col].fillna(median_val)

# Categorical: fill with mode
for col in all_categorical_cols:
    mode_val = X_train_combined[col].mode()[0] if len(X_train_combined[col].mode()) > 0 else 'Unknown'
    imputation_values[col] = mode_val
    X_train_combined[col] = X_train_combined[col].fillna(mode_val)
    X_test_combined[col] = X_test_combined[col].fillna(mode_val)

# ============================================================
# ENCODING (Target Encoding + Label Encoding)
# ============================================================
print("\n    Encoding categorical features...")

# Target encoding for high-cardinality categoricals
def target_encode(train_series, test_series, target, smoothing=10):
    """Target encoding with smoothing"""
    global_mean = target.mean()
    
    # Calculate category statistics
    cat_stats = train_series.groupby(train_series).agg(['count', lambda x: target.loc[x.index].mean()])
    cat_stats.columns = ['count', 'mean']
    
    # Smoothing
    smooth = (cat_stats['count'] * cat_stats['mean'] + smoothing * global_mean) / (cat_stats['count'] + smoothing)
    
    train_encoded = train_series.map(smooth).fillna(global_mean)
    test_encoded = test_series.map(smooth).fillna(global_mean)
    
    return train_encoded, test_encoded

# Apply target encoding to some categorical columns
target_encode_cols = ['country']
label_encoders = {}

for col in all_categorical_cols:
    if col in target_encode_cols:
        # Target encoding
        X_train_combined[f'{col}_target_enc'], X_test_combined[f'{col}_target_enc'] = target_encode(
            X_train_combined[col], X_test_combined[col], y
        )
    
    # Label encoding for all categoricals
    le = LabelEncoder()
    combined = pd.concat([X_train_combined[col], X_test_combined[col]], axis=0).astype(str)
    le.fit(combined)
    X_train_combined[col] = le.transform(X_train_combined[col].astype(str))
    X_test_combined[col] = le.transform(X_test_combined[col].astype(str))
    label_encoders[col] = le

print(f"    Encoded {len(all_categorical_cols)} categorical features")

# Final feature list
feature_cols = X_train_combined.columns.tolist()
print(f"\n    Final feature count: {len(feature_cols)}")

# ============================================================
# CORRELATION ANALYSIS OF NEW FEATURES
# ============================================================
if GENERATE_PLOTS:
    print("\n    Analyzing engineered feature correlations...")
    
    # Select top engineered features by correlation with target
    new_feature_cols = [col for col in feature_cols if col not in raw_feature_cols]
    
    new_correlations = {}
    for col in new_feature_cols[:30]:  # Analyze first 30 engineered features
        temp_df = pd.DataFrame({'feature': X_train_combined[col], 'target': y}).dropna()
        if len(temp_df) > 100:
            corr, p_value = stats.spearmanr(temp_df['feature'], temp_df['target'])
            new_correlations[col] = {'correlation': corr, 'p_value': p_value}
    
    if new_correlations:
        new_corr_df = pd.DataFrame(new_correlations).T.sort_values('correlation', key=abs, ascending=False)
        
        print("\n    Top Engineered Feature Correlations with Target:")
        for col, row in new_corr_df.head(15).iterrows():
            print(f"        {col:45s}: r={row['correlation']:+.4f}")
        
        # Plot top engineered features correlation
        fig, ax = plt.subplots(figsize=(12, 8))
        top_new_features = new_corr_df.head(15).index.tolist()
        correlations_plot = [new_corr_df.loc[f, 'correlation'] for f in top_new_features]
        colors = ['green' if c > 0 else 'red' for c in correlations_plot]
        
        bars = ax.barh(range(len(top_new_features)), correlations_plot, color=colors, alpha=0.7)
        ax.set_yticks(range(len(top_new_features)))
        ax.set_yticklabels(top_new_features)
        ax.set_xlabel('Spearman Correlation with Target')
        ax.set_title('Top 15 Engineered Features by Correlation with Target')
        ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_PATH, 'engineered_features_correlation.png'), dpi=150)
        plt.close()
        print(f"    Saved: engineered_features_correlation.png")

# ============================================================
# MODEL TRAINING WITH CROSS-VALIDATION
# ============================================================
print("\n[8/8] Training LightGBM model with 5-fold CV...")

# Optimized LightGBM parameters
lgb_params = {
    'objective': 'multiclass',
    'num_class': 3,
    'metric': 'multi_logloss',
    'boosting_type': 'gbdt',
    'n_estimators': 1000,
    'learning_rate': 0.03,
    'num_leaves': 63,
    'max_depth': 8,
    'min_child_samples': 30,
    'subsample': 0.8,
    'subsample_freq': 1,
    'colsample_bytree': 0.7,
    'reg_alpha': 0.1,
    'reg_lambda': 0.1,
    'min_split_gain': 0.01,
    'random_state': RANDOM_STATE,
    'verbose': -1,
    'n_jobs': -1
}

# Stratified K-Fold
skf = StratifiedKFold(n_splits=N_FOLDS, shuffle=True, random_state=RANDOM_STATE)

# Store OOF predictions and test predictions
oof_preds = np.zeros((len(X_train_combined), 3))
test_preds = np.zeros((len(X_test_combined), 3))

# Store metrics per fold
fold_scores = []
feature_importance_list = []

for fold, (train_idx, val_idx) in enumerate(skf.split(X_train_combined, y), 1):
    print(f"\n    Fold {fold}/{N_FOLDS}...")
    
    # Split data
    X_tr = X_train_combined.iloc[train_idx]
    X_val = X_train_combined.iloc[val_idx]
    y_tr, y_val = y.iloc[train_idx], y.iloc[val_idx]
    
    # Train model
    model = lgb.LGBMClassifier(**lgb_params)
    model.fit(
        X_tr, y_tr,
        eval_set=[(X_val, y_val)],
        callbacks=[lgb.early_stopping(100, verbose=False)]
    )
    
    # Store feature importance
    feature_importance_list.append(model.feature_importances_)
    
    # Predict on validation
    val_preds_proba = model.predict_proba(X_val)
    oof_preds[val_idx] = val_preds_proba
    
    # Predict on test (accumulate)
    test_preds += model.predict_proba(X_test_combined) / N_FOLDS
    
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
print("\n" + "=" * 70)
print("CROSS-VALIDATION RESULTS")
print("=" * 70)

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
# FEATURE IMPORTANCE ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("FEATURE IMPORTANCE ANALYSIS")
print("=" * 70)

# Average feature importance across folds
avg_importance = np.mean(feature_importance_list, axis=0)
importance_df = pd.DataFrame({
    'feature': feature_cols,
    'importance': avg_importance,
    'std': np.std(feature_importance_list, axis=0)
}).sort_values('importance', ascending=False)

print("\nTop 25 Features by Importance:")
for i, row in importance_df.head(25).iterrows():
    is_new = "NEW" if row['feature'] not in raw_feature_cols else ""
    print(f"    {row['feature']:50s}: {row['importance']:>7.0f} (+/- {row['std']:>5.0f}) {is_new}")

if GENERATE_PLOTS:
    # Plot feature importance
    fig, ax = plt.subplots(figsize=(12, 10))
    top_features = importance_df.head(30)
    colors = ['green' if f not in raw_feature_cols else 'steelblue' for f in top_features['feature']]
    
    bars = ax.barh(range(len(top_features)), top_features['importance'], color=colors, alpha=0.7)
    ax.set_yticks(range(len(top_features)))
    ax.set_yticklabels(top_features['feature'])
    ax.set_xlabel('Feature Importance')
    ax.set_title('Top 30 Features by Importance\n(Green = Engineered, Blue = Original)')
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_PATH, 'feature_importance.png'), dpi=150)
    plt.close()
    print(f"\n    Saved: feature_importance.png")

# ============================================================
# SAVE MODEL
# ============================================================
print("\n" + "=" * 70)
print("SAVING MODEL AND PREDICTIONS")
print("=" * 70)

# Train final model on all data
final_model = lgb.LGBMClassifier(**lgb_params)
final_model.fit(X_train_combined, y)

# Save model and artifacts
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
# SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("V2.0 ADVANCED MODEL COMPLETE")
print("=" * 70)
print(f"""
Model: LightGBM (multi-class) with optimized hyperparameters
Original Features: {len(raw_feature_cols)}
Engineered Features: {len(feature_cols) - len(raw_feature_cols)}
Total Features: {len(feature_cols)}
CV Strategy: {N_FOLDS}-fold Stratified

Results:
  - Accuracy:  {oof_acc:.4f}
  - F1 Macro:  {oof_f1:.4f}
  - Log Loss:  {oof_logloss:.4f}

Feature Engineering Categories:
  1. Financial ratios (profit margin, expense ratios, turnover per year)
  2. Business maturity features (age categories, total months)
  3. Attitude/perception composite scores
  4. Insurance adoption scores
  5. Financial services adoption scores
  6. Business practices scores
  7. Risk indicators
  8. Country-specific features
  9. Missing value pattern features
  10. Feature interactions

Files saved:
  - Model: {MODEL_PATH}
  - Submission: {SUBMISSION_PATH}
""")

if GENERATE_PLOTS:
    print(f"  - Plots: {PLOTS_PATH}/")
