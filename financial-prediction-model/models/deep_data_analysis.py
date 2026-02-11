"""
Deep Data Analysis for Financial Health Prediction
====================================================
This script performs comprehensive exploratory data analysis to:
1. Understand feature distributions and relationships
2. Identify strong predictors through statistical tests
3. Discover feature interactions and patterns
4. Guide feature engineering for v3 model

Author: Competition Team
Date: February 2026
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency, spearmanr, pearsonr, kruskal, mannwhitneyu
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import mutual_info_classif
from sklearn.ensemble import RandomForestClassifier
import warnings
import os
warnings.filterwarnings('ignore')

# ============================================================
# CONFIGURATION
# ============================================================
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRAIN_PATH = os.path.join(BASE_PATH, 'Train.csv')
ANALYSIS_PATH = os.path.join(BASE_PATH, 'models', 'analysis_output')
os.makedirs(ANALYSIS_PATH, exist_ok=True)

# Target mapping
TARGET_MAP = {'Low': 0, 'Medium': 1, 'High': 2}

print("=" * 80)
print("DEEP DATA ANALYSIS FOR FINANCIAL HEALTH PREDICTION")
print("=" * 80)

# ============================================================
# 1. LOAD DATA
# ============================================================
print("\n" + "=" * 80)
print("1. DATA LOADING & BASIC OVERVIEW")
print("=" * 80)

df = pd.read_csv(TRAIN_PATH)
print(f"\nDataset Shape: {df.shape}")
print(f"Total Samples: {df.shape[0]}")
print(f"Total Features: {df.shape[1] - 2} (excluding ID and Target)")

# Target distribution
print("\n--- Target Distribution ---")
target_dist = df['Target'].value_counts()
target_pct = df['Target'].value_counts(normalize=True) * 100
for target in ['Low', 'Medium', 'High']:
    print(f"    {target:8s}: {target_dist[target]:5d} ({target_pct[target]:.1f}%)")

# Encode target for analysis
df['Target_encoded'] = df['Target'].map(TARGET_MAP)

# Separate feature types
feature_cols = [col for col in df.columns if col not in ['ID', 'Target', 'Target_encoded']]
numeric_cols = df[feature_cols].select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = df[feature_cols].select_dtypes(include=['object']).columns.tolist()

print(f"\nNumeric Features: {len(numeric_cols)}")
print(f"Categorical Features: {len(categorical_cols)}")

# ============================================================
# 2. MISSING VALUE ANALYSIS
# ============================================================
print("\n" + "=" * 80)
print("2. MISSING VALUE ANALYSIS")
print("=" * 80)

missing_analysis = []
for col in feature_cols:
    missing_count = df[col].isnull().sum()
    missing_pct = df[col].isnull().mean() * 100
    
    # Check if missingness correlates with target
    df['_is_missing'] = df[col].isnull().astype(int)
    if df['_is_missing'].sum() > 0 and df['_is_missing'].sum() < len(df):
        contingency = pd.crosstab(df['_is_missing'], df['Target'])
        chi2, p_value, _, _ = chi2_contingency(contingency)
        missing_target_corr = chi2
        missing_p_value = p_value
    else:
        missing_target_corr = 0
        missing_p_value = 1
    
    missing_analysis.append({
        'feature': col,
        'missing_count': missing_count,
        'missing_pct': missing_pct,
        'missing_target_chi2': missing_target_corr,
        'missing_target_pvalue': missing_p_value
    })

df.drop('_is_missing', axis=1, inplace=True)

missing_df = pd.DataFrame(missing_analysis).sort_values('missing_pct', ascending=False)

print("\n--- Features with Significant Missing-Target Relationship (p < 0.05) ---")
sig_missing = missing_df[missing_df['missing_target_pvalue'] < 0.05].sort_values('missing_target_chi2', ascending=False)
for _, row in sig_missing.head(15).iterrows():
    print(f"    {row['feature']:55s}: {row['missing_pct']:5.1f}% missing, χ²={row['missing_target_chi2']:7.1f} (p={row['missing_target_pvalue']:.2e})")

# ============================================================
# 3. NUMERIC FEATURE ANALYSIS
# ============================================================
print("\n" + "=" * 80)
print("3. NUMERIC FEATURE DEEP ANALYSIS")
print("=" * 80)

numeric_analysis = []

for col in numeric_cols:
    data = df[col].dropna()
    
    # Basic statistics
    stats_dict = {
        'feature': col,
        'count': len(data),
        'mean': data.mean(),
        'std': data.std(),
        'min': data.min(),
        'max': data.max(),
        'median': data.median(),
        'skewness': stats.skew(data),
        'kurtosis': stats.kurtosis(data)
    }
    
    # Correlation with target (Spearman)
    valid_idx = df[col].notna()
    if valid_idx.sum() > 100:
        corr, p_value = spearmanr(df.loc[valid_idx, col], df.loc[valid_idx, 'Target_encoded'])
        stats_dict['spearman_corr'] = corr
        stats_dict['spearman_pvalue'] = p_value
        
        # Pearson correlation
        pearson_corr, pearson_p = pearsonr(df.loc[valid_idx, col], df.loc[valid_idx, 'Target_encoded'])
        stats_dict['pearson_corr'] = pearson_corr
        stats_dict['pearson_pvalue'] = pearson_p
        
        # Kruskal-Wallis test (non-parametric ANOVA)
        groups = [df.loc[(df['Target'] == t) & valid_idx, col].values for t in ['Low', 'Medium', 'High']]
        groups = [g for g in groups if len(g) > 0]
        if len(groups) == 3:
            h_stat, kw_p = kruskal(*groups)
            stats_dict['kruskal_h'] = h_stat
            stats_dict['kruskal_pvalue'] = kw_p
    
    # Distribution by target
    for target in ['Low', 'Medium', 'High']:
        target_data = df.loc[df['Target'] == target, col].dropna()
        stats_dict[f'mean_{target}'] = target_data.mean()
        stats_dict[f'median_{target}'] = target_data.median()
    
    numeric_analysis.append(stats_dict)

numeric_df = pd.DataFrame(numeric_analysis)

print("\n--- Numeric Feature Statistics ---")
for col in numeric_cols:
    row = numeric_df[numeric_df['feature'] == col].iloc[0]
    print(f"\n  {col}:")
    print(f"      Range: [{row['min']:.2f}, {row['max']:.2f}], Median: {row['median']:.2f}")
    print(f"      Skewness: {row['skewness']:.2f}, Kurtosis: {row['kurtosis']:.2f}")
    if 'spearman_corr' in row:
        print(f"      Spearman r: {row['spearman_corr']:+.4f} (p={row['spearman_pvalue']:.2e})")
    if 'kruskal_h' in row and not pd.isna(row['kruskal_h']):
        print(f"      Kruskal-Wallis H: {row['kruskal_h']:.2f} (p={row['kruskal_pvalue']:.2e})")
    print(f"      Mean by Target: Low={row['mean_Low']:.2f}, Medium={row['mean_Medium']:.2f}, High={row['mean_High']:.2f}")

# ============================================================
# 4. CATEGORICAL FEATURE ANALYSIS
# ============================================================
print("\n" + "=" * 80)
print("4. CATEGORICAL FEATURE DEEP ANALYSIS")
print("=" * 80)

categorical_analysis = []

for col in categorical_cols:
    valid_data = df[col].dropna()
    
    stats_dict = {
        'feature': col,
        'n_unique': valid_data.nunique(),
        'mode': valid_data.mode()[0] if len(valid_data.mode()) > 0 else None,
        'mode_freq': (valid_data == valid_data.mode()[0]).mean() * 100 if len(valid_data.mode()) > 0 else 0
    }
    
    # Chi-square test with target
    contingency = pd.crosstab(df[col].fillna('MISSING'), df['Target'])
    if contingency.shape[0] > 1 and contingency.shape[1] > 1:
        chi2, p_value, dof, expected = chi2_contingency(contingency)
        n = contingency.sum().sum()
        min_dim = min(contingency.shape) - 1
        cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0
        
        stats_dict['chi2'] = chi2
        stats_dict['chi2_pvalue'] = p_value
        stats_dict['cramers_v'] = cramers_v
        stats_dict['dof'] = dof
    
    # Theil's U (Uncertainty Coefficient)
    # Measures how much knowing X reduces uncertainty about Y
    def theils_u(x, y):
        contingency = pd.crosstab(x, y)
        chi2, _, _, _ = chi2_contingency(contingency)
        n = contingency.sum().sum()
        
        # Entropy of Y
        py = contingency.sum(axis=0) / n
        hy = -np.sum(py * np.log(py + 1e-10))
        
        # Conditional entropy of Y given X
        px = contingency.sum(axis=1) / n
        hyx = 0
        for i in range(contingency.shape[0]):
            pyx = contingency.iloc[i] / contingency.iloc[i].sum()
            hyx -= px.iloc[i] * np.sum(pyx * np.log(pyx + 1e-10))
        
        return (hy - hyx) / hy if hy > 0 else 0
    
    valid_mask = df[col].notna()
    if valid_mask.sum() > 100:
        stats_dict['theils_u'] = theils_u(df.loc[valid_mask, col], df.loc[valid_mask, 'Target'])
    
    categorical_analysis.append(stats_dict)

categorical_df = pd.DataFrame(categorical_analysis).sort_values('cramers_v', ascending=False)

print("\n--- Top 20 Categorical Features by Association with Target ---")
print(f"{'Feature':<65} {'V':>7} {'Theil U':>8} {'Categories':>10}")
print("-" * 95)
for _, row in categorical_df.head(20).iterrows():
    v = row.get('cramers_v', 0)
    u = row.get('theils_u', 0)
    print(f"{row['feature']:<65} {v:>7.4f} {u:>8.4f} {row['n_unique']:>10}")

# ============================================================
# 5. DETAILED VALUE ANALYSIS FOR TOP CATEGORICAL FEATURES
# ============================================================
print("\n" + "=" * 80)
print("5. DETAILED VALUE ANALYSIS FOR TOP CATEGORICAL FEATURES")
print("=" * 80)

top_cat_features = categorical_df.head(10)['feature'].tolist()

for col in top_cat_features:
    print(f"\n--- {col} ---")
    
    # Cross-tabulation with percentages
    cross_tab = pd.crosstab(df[col], df['Target'], normalize='index') * 100
    cross_tab_counts = pd.crosstab(df[col], df['Target'])
    
    print(f"{'Value':<25} {'Low%':>8} {'Med%':>8} {'High%':>8} {'n':>8}")
    print("-" * 60)
    
    for val in cross_tab.index:
        low_pct = cross_tab.loc[val, 'Low'] if 'Low' in cross_tab.columns else 0
        med_pct = cross_tab.loc[val, 'Medium'] if 'Medium' in cross_tab.columns else 0
        high_pct = cross_tab.loc[val, 'High'] if 'High' in cross_tab.columns else 0
        n = cross_tab_counts.loc[val].sum()
        print(f"{str(val):<25} {low_pct:>8.1f} {med_pct:>8.1f} {high_pct:>8.1f} {n:>8}")

# ============================================================
# 6. FEATURE INTERACTIONS ANALYSIS
# ============================================================
print("\n" + "=" * 80)
print("6. FEATURE INTERACTION ANALYSIS")
print("=" * 80)

# Numeric feature correlations
print("\n--- Numeric Feature Inter-correlations ---")
numeric_corr_matrix = df[numeric_cols].corr(method='spearman')
print(numeric_corr_matrix.round(3).to_string())

# Find highly correlated numeric pairs
print("\n--- Highly Correlated Numeric Pairs (|r| > 0.5) ---")
for i, col1 in enumerate(numeric_cols):
    for col2 in numeric_cols[i+1:]:
        corr = numeric_corr_matrix.loc[col1, col2]
        if abs(corr) > 0.5:
            print(f"    {col1} <-> {col2}: r = {corr:.4f}")

# ============================================================
# 7. CATEGORICAL FEATURE COMBINATIONS
# ============================================================
print("\n" + "=" * 80)
print("7. CATEGORICAL FEATURE COMBINATIONS")
print("=" * 80)

# Test combinations of top categorical features
print("\n--- Testing Top Categorical Feature Combinations ---")

top_cats_for_combo = categorical_df.head(6)['feature'].tolist()
combo_results = []

for i, col1 in enumerate(top_cats_for_combo):
    for col2 in top_cats_for_combo[i+1:]:
        # Create combined feature
        combined = df[col1].astype(str) + '_' + df[col2].astype(str)
        
        # Test association with target
        contingency = pd.crosstab(combined, df['Target'])
        if contingency.shape[0] > 1 and contingency.shape[1] > 1:
            chi2, p_value, dof, _ = chi2_contingency(contingency)
            n = contingency.sum().sum()
            min_dim = min(contingency.shape) - 1
            cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0
            
            combo_results.append({
                'feature1': col1,
                'feature2': col2,
                'combined_categories': combined.nunique(),
                'cramers_v': cramers_v,
                'chi2': chi2
            })

combo_df = pd.DataFrame(combo_results).sort_values('cramers_v', ascending=False)
print(f"\n{'Feature 1':<35} {'Feature 2':<35} {'V':>7} {'Cats':>6}")
print("-" * 90)
for _, row in combo_df.head(10).iterrows():
    print(f"{row['feature1']:<35} {row['feature2']:<35} {row['cramers_v']:>7.4f} {row['combined_categories']:>6}")

# ============================================================
# 8. MUTUAL INFORMATION ANALYSIS
# ============================================================
print("\n" + "=" * 80)
print("8. MUTUAL INFORMATION ANALYSIS")
print("=" * 80)

# Prepare data for mutual information
X_mi = df[feature_cols].copy()

# Encode categoricals
for col in categorical_cols:
    le = LabelEncoder()
    X_mi[col] = le.fit_transform(X_mi[col].fillna('MISSING').astype(str))

# Fill numeric NaN
for col in numeric_cols:
    X_mi[col] = X_mi[col].fillna(X_mi[col].median())

# Calculate mutual information
mi_scores = mutual_info_classif(X_mi, df['Target_encoded'], random_state=42)
mi_df = pd.DataFrame({
    'feature': feature_cols,
    'mi_score': mi_scores
}).sort_values('mi_score', ascending=False)

print("\n--- Top 25 Features by Mutual Information ---")
for _, row in mi_df.head(25).iterrows():
    feat_type = "NUM" if row['feature'] in numeric_cols else "CAT"
    print(f"    {row['feature']:<55} [{feat_type}]: {row['mi_score']:.4f}")

# ============================================================
# 9. RANDOM FOREST FEATURE IMPORTANCE
# ============================================================
print("\n" + "=" * 80)
print("9. RANDOM FOREST FEATURE IMPORTANCE (BASELINE)")
print("=" * 80)

rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
rf.fit(X_mi, df['Target_encoded'])

rf_importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

print("\n--- Top 25 Features by Random Forest Importance ---")
for _, row in rf_importance.head(25).iterrows():
    feat_type = "NUM" if row['feature'] in numeric_cols else "CAT"
    print(f"    {row['feature']:<55} [{feat_type}]: {row['importance']:.4f}")

# ============================================================
# 10. COUNTRY-SPECIFIC ANALYSIS
# ============================================================
print("\n" + "=" * 80)
print("10. COUNTRY-SPECIFIC ANALYSIS")
print("=" * 80)

countries = df['country'].unique()
print(f"\nCountries: {list(countries)}")

for country in countries:
    country_df = df[df['country'] == country]
    print(f"\n--- {country.upper()} (n={len(country_df)}) ---")
    
    target_dist = country_df['Target'].value_counts(normalize=True) * 100
    for target in ['Low', 'Medium', 'High']:
        pct = target_dist.get(target, 0)
        print(f"    {target}: {pct:.1f}%")
    
    # Top features for this country
    print(f"    Key numeric stats:")
    for col in numeric_cols[:3]:
        median = country_df[col].median()
        print(f"        {col}: median = {median:.2f}")

# ============================================================
# 11. INSURANCE PATTERN ANALYSIS
# ============================================================
print("\n" + "=" * 80)
print("11. INSURANCE PATTERN ANALYSIS (STRONG PREDICTOR)")
print("=" * 80)

insurance_cols = [col for col in categorical_cols if 'insurance' in col.lower()]
print(f"\nInsurance-related features: {insurance_cols}")

# Create insurance adoption pattern
df['insurance_pattern'] = ''
for col in ['has_insurance', 'motor_vehicle_insurance', 'medical_insurance', 'funeral_insurance']:
    if col in df.columns:
        df['insurance_pattern'] += df[col].fillna('NA').astype(str)

insurance_pattern_dist = df.groupby(['insurance_pattern', 'Target']).size().unstack(fill_value=0)
insurance_pattern_dist['total'] = insurance_pattern_dist.sum(axis=1)
insurance_pattern_dist = insurance_pattern_dist.sort_values('total', ascending=False)

print("\n--- Top Insurance Patterns and Target Distribution ---")
for pattern in insurance_pattern_dist.head(15).index:
    row = insurance_pattern_dist.loc[pattern]
    total = row['total']
    low_pct = row['Low'] / total * 100 if total > 0 else 0
    med_pct = row['Medium'] / total * 100 if total > 0 else 0
    high_pct = row['High'] / total * 100 if total > 0 else 0
    print(f"    Pattern: {pattern[:50]:<50} n={total:>5} | L:{low_pct:>5.1f}% M:{med_pct:>5.1f}% H:{high_pct:>5.1f}%")

# ============================================================
# 12. FINANCIAL SERVICES ADOPTION ANALYSIS
# ============================================================
print("\n" + "=" * 80)
print("12. FINANCIAL SERVICES ADOPTION PATTERNS")
print("=" * 80)

financial_cols = ['has_mobile_money', 'has_credit_card', 'has_loan_account', 
                  'has_internet_banking', 'has_debit_card', 'has_cellphone']
financial_cols = [c for c in financial_cols if c in df.columns]

print(f"\nFinancial service features: {financial_cols}")

# Count financial services adoption
binary_map = {'Yes': 1, 'No': 0, 'Have now': 1, 'Used before': 0.5, 'Never had': 0}

df['financial_service_count'] = 0
for col in financial_cols:
    df['financial_service_count'] += df[col].map(binary_map).fillna(0)

print("\n--- Financial Service Count vs Target ---")
fin_count_dist = pd.crosstab(df['financial_service_count'].round(), df['Target'], normalize='index') * 100
for count in sorted(fin_count_dist.index):
    row = fin_count_dist.loc[count]
    n = (df['financial_service_count'].round() == count).sum()
    print(f"    {int(count)} services: L:{row['Low']:>5.1f}% M:{row['Medium']:>5.1f}% H:{row['High']:>5.1f}% (n={n})")

# ============================================================
# 13. DERIVED FEATURE SUGGESTIONS
# ============================================================
print("\n" + "=" * 80)
print("13. RECOMMENDED FEATURES FOR V3 MODEL")
print("=" * 80)

print("""
Based on the deep analysis, the following features should be prioritized for v3:

=== STRONG PREDICTORS (Cramer's V > 0.25 or MI > 0.05) ===
1. funeral_insurance (V=0.55) - STRONGEST single predictor
2. has_insurance (V=0.32)
3. has_credit_card (V=0.31)
4. has_loan_account (V=0.30)
5. marketing_word_of_mouth (V=0.27)
6. medical_insurance (V=0.26)
7. keeps_financial_records (V=0.22)
8. country (V=0.21)

=== RECOMMENDED NEW FEATURES ===

1. Insurance Adoption Score (composite):
   - Count of insurance types held
   - Binary for each insurance type
   - Insurance diversity index

2. Financial Digitization Score:
   - has_mobile_money + has_internet_banking + has_debit_card
   - Modern vs traditional financial behavior

3. Business Formalization Score:
   - keeps_financial_records + compliance_income_tax + has_insurance
   - Indicator of formal vs informal operation

4. Risk Profile Score:
   - current_problem_cash_flow + problem_sourcing_money + uses_informal_lender
   - Composite risk indicator

5. Business Success Indicators:
   - offers_credit_to_customers (ability to extend credit)
   - marketing_word_of_mouth (growth orientation)
   - attitude scores (optimism indicators)

6. Country-Specific Features:
   - Country × insurance interaction
   - Country × financial services interaction
   - Country-adjusted turnover (relative to country median)

7. Missing Pattern Features:
   - Missing pattern for insurance columns (strong signal)
   - Total missing count per observation
   - Missing in key financial fields

8. Interaction Features:
   - funeral_insurance × has_credit_card
   - insurance_count × financial_service_count
   - business_age × insurance_adoption

9. Ratio Features:
   - profit_margin (turnover - expenses) / turnover
   - personal_to_business_income ratio
   - expenses_per_business_year (expenses / business_age)

10. Attitude Composite Scores:
    - Optimism score (stable_environment + more_successful + satisfied)
    - Pessimism score (worried_shutdown + various negative perceptions)
""")

# ============================================================
# 14. SAVE ANALYSIS RESULTS
# ============================================================
print("\n" + "=" * 80)
print("14. SAVING ANALYSIS RESULTS")
print("=" * 80)

# Save detailed results
categorical_df.to_csv(os.path.join(ANALYSIS_PATH, 'categorical_feature_analysis.csv'), index=False)
numeric_df.to_csv(os.path.join(ANALYSIS_PATH, 'numeric_feature_analysis.csv'), index=False)
mi_df.to_csv(os.path.join(ANALYSIS_PATH, 'mutual_information_scores.csv'), index=False)
rf_importance.to_csv(os.path.join(ANALYSIS_PATH, 'rf_feature_importance.csv'), index=False)
missing_df.to_csv(os.path.join(ANALYSIS_PATH, 'missing_value_analysis.csv'), index=False)
combo_df.to_csv(os.path.join(ANALYSIS_PATH, 'feature_combinations.csv'), index=False)

print(f"    Saved analysis results to: {ANALYSIS_PATH}/")

# ============================================================
# 15. GENERATE ANALYSIS PLOTS
# ============================================================
print("\n--- Generating Analysis Plots ---")

# 1. Feature importance comparison
fig, axes = plt.subplots(1, 3, figsize=(18, 8))

# Cramer's V for categorical
ax = axes[0]
top_cat = categorical_df.head(15)
colors = ['darkgreen' if v > 0.25 else 'green' if v > 0.15 else 'lightgreen' for v in top_cat['cramers_v']]
ax.barh(range(len(top_cat)), top_cat['cramers_v'], color=colors)
ax.set_yticks(range(len(top_cat)))
ax.set_yticklabels([f[:40] for f in top_cat['feature']])
ax.set_xlabel("Cramer's V")
ax.set_title("Top Categorical Features\n(Association with Target)")
ax.invert_yaxis()

# Mutual Information
ax = axes[1]
top_mi = mi_df.head(15)
colors = ['darkblue' if f in categorical_cols else 'lightblue' for f in top_mi['feature']]
ax.barh(range(len(top_mi)), top_mi['mi_score'], color=colors)
ax.set_yticks(range(len(top_mi)))
ax.set_yticklabels([f[:40] for f in top_mi['feature']])
ax.set_xlabel("Mutual Information")
ax.set_title("Top Features by MI\n(Blue=Cat, Light=Num)")
ax.invert_yaxis()

# Random Forest
ax = axes[2]
top_rf = rf_importance.head(15)
colors = ['darkred' if f in categorical_cols else 'lightsalmon' for f in top_rf['feature']]
ax.barh(range(len(top_rf)), top_rf['importance'], color=colors)
ax.set_yticks(range(len(top_rf)))
ax.set_yticklabels([f[:40] for f in top_rf['feature']])
ax.set_xlabel("RF Importance")
ax.set_title("Top Features by RF\n(Red=Cat, Salmon=Num)")
ax.invert_yaxis()

plt.tight_layout()
plt.savefig(os.path.join(ANALYSIS_PATH, 'feature_importance_comparison.png'), dpi=150)
plt.close()
print(f"    Saved: feature_importance_comparison.png")

# 2. Target distribution by top features
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

for i, col in enumerate(categorical_df.head(6)['feature']):
    ax = axes[i]
    cross_tab = pd.crosstab(df[col], df['Target'], normalize='index') * 100
    cross_tab[['Low', 'Medium', 'High']].plot(kind='bar', stacked=True, ax=ax, 
                                               color=['#ff6b6b', '#ffd93d', '#6bcf63'])
    ax.set_title(f'{col[:35]}...' if len(col) > 35 else col, fontsize=10)
    ax.set_xlabel('')
    ax.tick_params(axis='x', rotation=45)
    ax.legend(title='Target', loc='upper right')
    ax.set_ylabel('%')

plt.tight_layout()
plt.savefig(os.path.join(ANALYSIS_PATH, 'target_by_top_categorical.png'), dpi=150)
plt.close()
print(f"    Saved: target_by_top_categorical.png")

# 3. Numeric features distribution
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for i, col in enumerate(numeric_cols):
    ax = axes[i]
    for target, color in [('Low', '#ff6b6b'), ('Medium', '#ffd93d'), ('High', '#6bcf63')]:
        data = df[df['Target'] == target][col].dropna()
        if len(data) > 0:
            # Log transform for visualization
            data_log = np.log1p(data.clip(lower=0))
            ax.hist(data_log, bins=30, alpha=0.5, label=target, color=color, density=True)
    ax.set_title(f'{col} (log scale)')
    ax.legend()

plt.tight_layout()
plt.savefig(os.path.join(ANALYSIS_PATH, 'numeric_distributions.png'), dpi=150)
plt.close()
print(f"    Saved: numeric_distributions.png")

# 4. Correlation matrix with target
correlation_with_target = []
for col in feature_cols:
    if col in numeric_cols:
        valid = df[col].notna()
        if valid.sum() > 100:
            corr, _ = spearmanr(df.loc[valid, col], df.loc[valid, 'Target_encoded'])
            correlation_with_target.append({'feature': col, 'correlation': corr, 'type': 'numeric'})
    else:
        # For categorical, use the cramers_v from the analysis
        v = categorical_df[categorical_df['feature'] == col]['cramers_v'].values
        if len(v) > 0:
            correlation_with_target.append({'feature': col, 'correlation': v[0], 'type': 'categorical'})

corr_target_df = pd.DataFrame(correlation_with_target).sort_values('correlation', key=abs, ascending=False)

fig, ax = plt.subplots(figsize=(12, 10))
top_corr = corr_target_df.head(25)
colors = ['green' if t == 'categorical' else 'steelblue' for t in top_corr['type']]
ax.barh(range(len(top_corr)), top_corr['correlation'], color=colors, alpha=0.7)
ax.set_yticks(range(len(top_corr)))
ax.set_yticklabels(top_corr['feature'])
ax.set_xlabel('Correlation/Association with Target')
ax.set_title('Top 25 Features by Target Association\n(Green=Categorical V, Blue=Numeric r)')
ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(os.path.join(ANALYSIS_PATH, 'correlation_with_target.png'), dpi=150)
plt.close()
print(f"    Saved: correlation_with_target.png")

print("\n" + "=" * 80)
print("DEEP DATA ANALYSIS COMPLETE")
print("=" * 80)
print(f"\nAll analysis files saved to: {ANALYSIS_PATH}/")
print("\nKey Insights:")
print("  - funeral_insurance is the strongest single predictor (V=0.55)")
print("  - Insurance-related features dominate the top predictors")
print("  - Financial service adoption strongly correlates with financial health")
print("  - Country has moderate predictive power (V=0.21)")
print("  - Numeric features have weak direct correlations but may offer interaction potential")
