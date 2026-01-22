"""
Financial Health Survey Web Interface
===================================

Flask web application for conducting financial health surveys and 
providing real-time predictions using the trained model.
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os
from financial_health_survey_model import FinancialHealthSurveyModel

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains and routes

# Initialize the model
model = FinancialHealthSurveyModel()

# Load the trained model if it exists
model_path = 'financial_health_model.pkl'
if os.path.exists(model_path):
    try:
        model.load_model(model_path)
        print("Pre-trained model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Please train the model first by running financial_health_survey_model.py")

@app.route('/')
def index():
    """
    Main survey page
    """
    return render_template('survey.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Handle survey submission and return prediction
    """
    try:
        # Get survey responses from the form
        survey_data = request.json
        print(f"Received survey data: {survey_data}")
        
        # Validate required fields
        required_fields = [
            'country', 'owner_age', 'owner_sex', 'business_age_years', 
            'business_age_months', 'covid_essential_service', 'personal_income',
            'business_expenses', 'business_turnover', 'keeps_financial_records',
            'has_mobile_money', 'has_insurance', 'future_risk_theft_stock',
            'attitude_stable_business_environment', 'compliance_income_tax',
            'has_cellphone', 'motivation_make_more_money'
        ]
        
        missing_fields = [field for field in required_fields if field not in survey_data or survey_data[field] is None or survey_data[field] == '']
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Make prediction
        if model.is_trained:
            result = model.predict_financial_health(survey_data)
            return jsonify({
                'success': True,
                'prediction': result['predicted_category'],
                'confidence_scores': result['confidence_scores'],
                'recommendation': result['recommendation'],
                'survey_data': survey_data
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Model not trained. Please train the model first.'
            }), 500
    
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error making prediction: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify API is running
    """
    return jsonify({
        'success': True,
        'message': 'Financial Health Survey API is running',
        'model_trained': model.is_trained
    })

@app.route('/api/train', methods=['POST'])
def train_model():
    """
    Train the model (for development/admin use)
    """
    try:
        if os.path.exists('Train.csv'):
            accuracy = model.train_model('Train.csv')
            model.save_model(model_path)
            return jsonify({
                'success': True,
                'message': f'Model trained successfully with accuracy: {accuracy:.4f}'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Training data (Train.csv) not found'
            }), 404
    except Exception as e:
        print(f"Error in training: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error training model: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)