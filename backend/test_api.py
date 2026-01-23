#!/usr/bin/env python3
"""
Local Test Script for Financial Health API
========================================

Run this script to test the API endpoints locally before deploying.
"""

import requests
import json
import time

def test_api_locally():
    """Test the API endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Financial Health API...")
    print("=" * 50)
    
    # Test 1: Root endpoint
    print("\n1. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Health endpoint
    print("\n2. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Prediction endpoint
    print("\n3. Testing prediction endpoint...")
    sample_data = {
        'country': 'Eswatini',
        'owner_age': 35,
        'owner_sex': 'M',
        'business_age_years': 5,
        'business_age_months': 2,
        'covid_essential_service': 'Yes',
        'personal_income': 50000,
        'business_expenses': 30000,
        'business_turnover': 80000,
        'keeps_financial_records': 'Yes',
        'has_mobile_money': 'Yes',
        'has_insurance': 'No',
        'future_risk_theft_stock': 'Medium',
        'attitude_stable_business_environment': 'Agree',
        'compliance_income_tax': 'Yes',
        'has_cellphone': 'Yes',
        'motivation_make_more_money': 'Strongly Agree'
    }
    
    try:
        response = requests.post(f"{base_url}/api/predict", json=sample_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Make sure the API is running first:")
    print("   python main.py")
    print("\nThen run this test in another terminal:")
    print("   python test_api.py")
    print("\n" + "=" * 50)
    
    input("Press Enter when API is ready...")
    test_api_locally()