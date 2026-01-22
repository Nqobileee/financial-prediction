"""
Command Line Interface for Financial Health Survey Model
======================================================

This script provides a command-line interface for training the model,
making predictions, and running the web application.
"""

import sys
import argparse
import json
from financial_health_survey_model import FinancialHealthSurveyModel, create_sample_survey_responses
import os

def train_model():
    """Train the financial health model"""
    print("=" * 60)
    print("TRAINING FINANCIAL HEALTH MODEL")
    print("=" * 60)
    
    if not os.path.exists('Train.csv'):
        print("❌ Error: Train.csv not found!")
        print("Please ensure the training data file is in the current directory.")
        return False
    
    model = FinancialHealthSurveyModel()
    
    try:
        accuracy = model.train_model('Train.csv')
        model.save_model('financial_health_model.pkl')
        print(f"\n✅ Model training completed successfully!")
        print(f"📊 Model accuracy: {accuracy:.4f}")
        print(f"💾 Model saved as 'financial_health_model.pkl'")
        return True
    except Exception as e:
        print(f"❌ Error during training: {e}")
        return False

def test_model():
    """Test the model with sample data"""
    print("=" * 60)
    print("TESTING FINANCIAL HEALTH MODEL")
    print("=" * 60)
    
    if not os.path.exists('financial_health_model.pkl'):
        print("❌ Error: Trained model not found!")
        print("Please train the model first using: python financial_health_cli.py --train")
        return False
    
    model = FinancialHealthSurveyModel()
    
    try:
        model.load_model('financial_health_model.pkl')
        print("✅ Model loaded successfully!")
        
        # Test with sample responses
        sample_responses = create_sample_survey_responses()
        
        for i, response in enumerate(sample_responses, 1):
            print(f"\n🔍 Testing Sample {i}:")
            print("-" * 40)
            
            # Show some key survey details
            print(f"Country: {response.get('country', 'N/A')}")
            print(f"Owner Age: {response.get('owner_age', 'N/A')}")
            print(f"Business Age: {response.get('business_age_years', 0)} years")
            print(f"Personal Income: {response.get('personal_income', 0)}")
            
            # Make prediction
            result = model.predict_financial_health(response)
            
            print(f"\n📊 Prediction Results:")
            print(f"   Financial Health: {result['predicted_category']}")
            print(f"   Confidence Scores:")
            for category, score in result['confidence_scores'].items():
                print(f"      {category}: {score:.3f} ({score*100:.1f}%)")
            print(f"\n💡 Recommendation:")
            print(f"   {result['recommendation']}")
        
        return True
    
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

def predict_interactive():
    """Interactive prediction mode"""
    print("=" * 60)
    print("INTERACTIVE FINANCIAL HEALTH ASSESSMENT")
    print("=" * 60)
    
    if not os.path.exists('financial_health_model.pkl'):
        print("❌ Error: Trained model not found!")
        print("Please train the model first using: python financial_health_cli.py --train")
        return False
    
    model = FinancialHealthSurveyModel()
    
    try:
        model.load_model('financial_health_model.pkl')
        print("✅ Model loaded successfully!\n")
        
        print("Please answer the following questions to assess your business financial health:")
        print("(Press Enter to skip optional questions)\n")
        
        survey_data = {}
        
        # Country
        print("1. Country:")
        print("   1) Eswatini  2) Lesotho  3) Malawi  4) Zimbabwe")
        choice = input("   Enter choice (1-4): ").strip()
        countries = {'1': 'eswatini', '2': 'lesotho', '3': 'malawi', '4': 'zimbabwe'}
        survey_data['country'] = countries.get(choice, 'zimbabwe')
        
        # Owner Age
        age = input("\n2. Owner Age: ").strip()
        try:
            survey_data['owner_age'] = float(age) if age else 35
        except ValueError:
            survey_data['owner_age'] = 35
        
        # Owner Sex
        print("\n3. Owner Sex:")
        print("   1) Female  2) Male")
        choice = input("   Enter choice (1-2): ").strip()
        survey_data['owner_sex'] = 'Female' if choice == '1' else 'Male'
        
        # Business Age
        years = input("\n4. Business Age (years): ").strip()
        months = input("   Business Age (additional months): ").strip()
        try:
            survey_data['business_age_years'] = float(years) if years else 2
            survey_data['business_age_months'] = float(months) if months else 0
        except ValueError:
            survey_data['business_age_years'] = 2
            survey_data['business_age_months'] = 0
        
        # COVID Essential Service
        print("\n5. Was your business considered essential during COVID?")
        print("   1) Yes  2) No  3) Don't know")
        choice = input("   Enter choice (1-3): ").strip()
        covid_choices = {'1': 'Yes', '2': 'No', '3': "Don't know"}
        survey_data['covid_essential_service'] = covid_choices.get(choice, 'No')
        
        # Financial Information
        income = input("\n6. Monthly Personal Income: ").strip()
        expenses = input("7. Monthly Business Expenses: ").strip()
        turnover = input("8. Annual Business Turnover: ").strip()
        
        try:
            survey_data['personal_income'] = float(income) if income else 0
            survey_data['business_expenses'] = float(expenses) if expenses else 0
            survey_data['business_turnover'] = float(turnover) if turnover else 0
        except ValueError:
            survey_data['personal_income'] = 0
            survey_data['business_expenses'] = 0
            survey_data['business_turnover'] = 0
        
        # Simplified yes/no questions
        questions = [
            ('keeps_financial_records', "9. Do you keep financial records regularly?"),
            ('has_mobile_money', "10. Do you use mobile money?"),
            ('has_insurance', "11. Does your business have insurance?"),
            ('future_risk_theft_stock', "12. Is theft of stock a risk for your business?"),
            ('attitude_stable_business_environment', "13. Do you believe the business environment will be stable?"),
            ('compliance_income_tax', "14. Does your business comply with income tax?"),
            ('has_cellphone', "15. Does your business use cellphones?"),
            ('motivation_make_more_money', "16. Was making money a motivation to start the business?")
        ]
        
        for key, question in questions:
            print(f"\n{question}")
            print("   1) Yes  2) No")
            choice = input("   Enter choice (1-2): ").strip()
            survey_data[key] = 'Yes' if choice == '1' else 'No'
        
        # Make prediction
        print("\n" + "="*60)
        print("PROCESSING YOUR RESPONSES...")
        print("="*60)
        
        result = model.predict_financial_health(survey_data)
        
        print(f"\n🎯 FINANCIAL HEALTH ASSESSMENT RESULT")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"\n💼 Your Business Financial Health: {result['predicted_category'].upper()}")
        
        print(f"\n📊 Confidence Breakdown:")
        for category, score in result['confidence_scores'].items():
            bar_length = int(score * 20)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(f"   {category:8} {bar} {score*100:.1f}%")
        
        print(f"\n💡 Recommendation:")
        print(f"   {result['recommendation']}")
        
        print(f"\n✨ Thank you for using the Financial Health Assessment Tool!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        return False

def run_web_app():
    """Run the web application"""
    print("=" * 60)
    print("STARTING WEB APPLICATION")
    print("=" * 60)
    
    try:
        from survey_web_app import app
        print("✅ Starting Flask web server...")
        print("🌐 Open your browser and go to: http://localhost:5000")
        print("📱 Or access from network: http://0.0.0.0:5000")
        print("\n⚠️  Press Ctrl+C to stop the server")
        
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError:
        print("❌ Error: Flask not installed!")
        print("Please install Flask: pip install flask")
    except Exception as e:
        print(f"❌ Error starting web app: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Financial Health Survey Model - Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python financial_health_cli.py --train          Train the model
  python financial_health_cli.py --test           Test with sample data
  python financial_health_cli.py --predict        Interactive prediction
  python financial_health_cli.py --web           Run web application
  python financial_health_cli.py --all           Train, test, and run web app
        """
    )
    
    parser.add_argument('--train', action='store_true', help='Train the model')
    parser.add_argument('--test', action='store_true', help='Test the model with sample data')
    parser.add_argument('--predict', action='store_true', help='Interactive prediction mode')
    parser.add_argument('--web', action='store_true', help='Run web application')
    parser.add_argument('--all', action='store_true', help='Train, test, and run web app')
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    success = True
    
    if args.all or args.train:
        success &= train_model()
        if success:
            print("\n" + "="*60 + "\n")
    
    if (args.all or args.test) and success:
        success &= test_model()
        if success:
            print("\n" + "="*60 + "\n")
    
    if args.predict and success:
        predict_interactive()
    
    if (args.all or args.web) and success:
        run_web_app()

if __name__ == "__main__":
    main()