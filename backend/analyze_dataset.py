#!/usr/bin/env python3
"""
Dataset Analysis Script for Reports Page
========================================
Analyzes the training dataset to generate real statistics for the reports page.
"""

import pandas as pd
import numpy as np
from collections import Counter
import json

def analyze_dataset():
    """Analyze the training dataset and return key statistics"""
    print("Loading dataset...")
    df = pd.read_csv('Train.csv')
    
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {len(df.columns)}")
    
    # Basic statistics
    stats = {
        'total_businesses': len(df),
        'countries': df['country'].value_counts().to_dict(),
        'target_distribution': df['Target'].value_counts().to_dict(),
        'average_business_age': df['business_age_years'].mean(),
        'insurance_coverage': (df['has_insurance'] == 'Yes').sum(),
        'mobile_money_adoption': (df['has_mobile_money'] == 'Have now').sum(),
        'tax_compliance': (df['compliance_income_tax'] == 'Yes').sum(),
        'financial_records_keeping': df['keeps_financial_records'].value_counts().to_dict(),
        'gender_distribution': df['owner_sex'].value_counts().to_dict(),
        'age_ranges': {
            'under_30': (df['owner_age'] < 30).sum(),
            '30_40': ((df['owner_age'] >= 30) & (df['owner_age'] < 40)).sum(),
            '40_50': ((df['owner_age'] >= 40) & (df['owner_age'] < 50)).sum(),
            'over_50': (df['owner_age'] >= 50).sum()
        }
    }
    
    # Financial metrics (excluding null values)
    financial_stats = {
        'avg_personal_income': df['personal_income'].mean(),
        'avg_business_expenses': df['business_expenses'].mean(), 
        'avg_business_turnover': df['business_turnover'].mean(),
        'income_ranges': {
            'low': (df['personal_income'] < 10000).sum(),
            'medium': ((df['personal_income'] >= 10000) & (df['personal_income'] < 50000)).sum(),
            'high': (df['personal_income'] >= 50000).sum()
        }
    }
    
    # Risk analysis by target
    risk_analysis = {}
    for target in df['Target'].unique():
        target_df = df[df['Target'] == target]
        risk_analysis[target] = {
            'count': len(target_df),
            'avg_income': target_df['personal_income'].mean(),
            'avg_turnover': target_df['business_turnover'].mean(),
            'insurance_rate': (target_df['has_insurance'] == 'Yes').mean() * 100,
            'mobile_money_rate': (target_df['has_mobile_money'] == 'Have now').mean() * 100,
            'tax_compliance_rate': (target_df['compliance_income_tax'] == 'Yes').mean() * 100
        }
    
    return {
        'basic_stats': stats,
        'financial_stats': financial_stats,
        'risk_analysis': risk_analysis
    }

if __name__ == "__main__":
    results = analyze_dataset()
    
    print("\n" + "="*60)
    print("DATASET ANALYSIS RESULTS")
    print("="*60)
    
    print(f"\nTotal Businesses: {results['basic_stats']['total_businesses']:,}")
    print(f"\nCountry Distribution:")
    for country, count in results['basic_stats']['countries'].items():
        percentage = (count / results['basic_stats']['total_businesses']) * 100
        print(f"  {country.title()}: {count:,} ({percentage:.1f}%)")
    
    print(f"\nFinancial Health Distribution:")
    for target, count in results['basic_stats']['target_distribution'].items():
        percentage = (count / results['basic_stats']['total_businesses']) * 100
        print(f"  {target}: {count:,} ({percentage:.1f}%)")
    
    print(f"\nInsurance Coverage: {results['basic_stats']['insurance_coverage']:,} businesses")
    insurance_rate = (results['basic_stats']['insurance_coverage'] / results['basic_stats']['total_businesses']) * 100
    print(f"Insurance Rate: {insurance_rate:.1f}%")
    
    print(f"\nMobile Money Adoption: {results['basic_stats']['mobile_money_adoption']:,} businesses")
    mobile_rate = (results['basic_stats']['mobile_money_adoption'] / results['basic_stats']['total_businesses']) * 100
    print(f"Mobile Money Rate: {mobile_rate:.1f}%")
    
    print(f"\nTax Compliance: {results['basic_stats']['tax_compliance']:,} businesses")
    tax_rate = (results['basic_stats']['tax_compliance'] / results['basic_stats']['total_businesses']) * 100
    print(f"Tax Compliance Rate: {tax_rate:.1f}%")
    
    print(f"\nRisk Analysis by Category:")
    for category, data in results['risk_analysis'].items():
        print(f"  {category}:")
        print(f"    Count: {data['count']:,}")
        print(f"    Avg Income: ${data['avg_income']:.0f}")
        print(f"    Avg Turnover: ${data['avg_turnover']:.0f}")
        print(f"    Insurance Rate: {data['insurance_rate']:.1f}%")
        print(f"    Mobile Money Rate: {data['mobile_money_rate']:.1f}%")
        print(f"    Tax Compliance Rate: {data['tax_compliance_rate']:.1f}%")
        print()
    
    # Save results to JSON for frontend use
    with open('dataset_analysis.json', 'w') as f:
        # Convert numpy types to regular Python types for JSON serialization
        def convert_types(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {key: convert_types(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_types(item) for item in obj]
            return obj
        
        clean_results = convert_types(results)
        json.dump(clean_results, f, indent=2, default=str)
    
    print("Analysis saved to dataset_analysis.json")