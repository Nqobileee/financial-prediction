#!/usr/bin/env python3
"""
Dummy Dataset Generator
======================
Generate synthetic data that matches the original structure but contains no real data
to avoid copyright issues while maintaining functionality.
"""

import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_dummy_data(num_samples=1000):
    """Generate dummy financial health data"""
    
    # Define possible values for categorical variables
    countries = ['eswatini', 'zimbabwe', 'malawi', 'lesotho']
    binary_responses = ['Yes', 'No', 'Don\'t know or N/A']
    sex_options = ['Male', 'Female']
    insurance_options = ['Never had', 'Have now', 'Used to have but don\'t have now']
    credit_options = ['Yes, always', 'Yes, sometimes', 'No']
    
    data = []
    
    for i in range(num_samples):
        # Generate synthetic data
        record = {
            'ID': f'ID_DUMMY{i:06d}',
            'country': random.choice(countries),
            'owner_age': np.random.normal(40, 12),  # Age around 40 +/- 12 years
            'attitude_stable_business_environment': random.choice(binary_responses),
            'attitude_worried_shutdown': random.choice(['Yes', 'No']),
            'compliance_income_tax': random.choice(['Yes', 'No']),
            'perception_insurance_doesnt_cover_losses': random.choice(binary_responses),
            'perception_cannot_afford_insurance': random.choice(binary_responses),
            'personal_income': np.random.lognormal(8, 2),  # Log-normal distribution for income
            'business_expenses': np.random.lognormal(7, 1.5),
            'business_turnover': np.random.lognormal(7.5, 1.8),
            'business_age_years': max(0, np.random.exponential(5)),  # Exponential for business age
            'motor_vehicle_insurance': random.choice(insurance_options),
            'has_mobile_money': random.choice(insurance_options),
            'current_problem_cash_flow': random.choice(['Yes', 'No', '']),
            'has_cellphone': random.choice(['Yes', 'No']),
            'owner_sex': random.choice(sex_options),
            'offers_credit_to_customers': random.choice(credit_options),
            'attitude_satisfied_with_achievement': random.choice(['Yes', 'No']),
            'has_credit_card': random.choice(insurance_options),
            'keeps_financial_records': random.choice(credit_options),
            'perception_insurance_companies_dont_insure_businesses_like_yours': random.choice(binary_responses),
            'perception_insurance_important': random.choice(binary_responses),
            'has_insurance': random.choice(['Yes', 'No']),
            'covid_essential_service': random.choice(['Yes', 'No']),
            'attitude_more_successful_next_year': random.choice(['Yes', 'No', 'Don\'t know']),
            'problem_sourcing_money': random.choice(['Yes', 'No']),
            'marketing_word_of_mouth': random.choice(['Yes', 'No']),
            'has_loan_account': random.choice(insurance_options),
            'has_internet_banking': random.choice(insurance_options),
            'has_debit_card': random.choice(insurance_options),
            'future_risk_theft_stock': random.choice(['Yes', 'No']),
            'business_age_months': np.random.uniform(0, 120),
            'medical_insurance': random.choice(insurance_options),
            'funeral_insurance': random.choice(insurance_options),
            'motivation_make_more_money': random.choice(['Yes', 'No']),
            'uses_friends_family_savings': random.choice(insurance_options),
            'uses_informal_lender': random.choice(insurance_options),
        }
        
        # Generate target based on some basic rules to make it realistic
        income_score = 1 if record['personal_income'] > 50000 else 0
        business_score = 1 if record['business_turnover'] > 30000 else 0
        age_score = 1 if record['business_age_years'] > 3 else 0
        records_score = 1 if record['keeps_financial_records'] in ['Yes, always', 'Yes, sometimes'] else 0
        insurance_score = 1 if record['has_insurance'] == 'Yes' else 0
        
        total_score = income_score + business_score + age_score + records_score + insurance_score
        
        if total_score >= 4:
            record['Target'] = 'High'
        elif total_score >= 2:
            record['Target'] = 'Medium' 
        else:
            record['Target'] = 'Low'
            
        data.append(record)
    
    return pd.DataFrame(data)

def main():
    print("Generating dummy training dataset...")
    
    # Generate dummy data
    dummy_df = generate_dummy_data(1000)
    
    # Display basic statistics
    print(f"Generated {len(dummy_df)} dummy records")
    print(f"Target distribution:")
    print(dummy_df['Target'].value_counts())
    print(f"\\nCountry distribution:")
    print(dummy_df['country'].value_counts())
    
    # Save dummy dataset
    dummy_df.to_csv('Train_dummy.csv', index=False)
    print("\\nDummy training dataset saved as 'Train_dummy.csv'")
    
    # Generate smaller test set
    test_df = generate_dummy_data(200)
    test_df.to_csv('Test_dummy.csv', index=False)
    print("Dummy test dataset saved as 'Test_dummy.csv'")

if __name__ == "__main__":
    main()