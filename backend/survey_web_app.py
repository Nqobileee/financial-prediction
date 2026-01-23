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
def root():
    """
    Root endpoint for health checking and basic API info
    """
    return jsonify({
        'message': 'Financial Health Survey API',
        'status': 'running',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'predict': '/api/predict (POST)',
            'train': '/api/train (POST)'
        },
        'model_status': 'trained' if model.is_trained else 'not_trained'
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify API is running
    """
    return jsonify({
        'success': True,
        'message': 'Financial Health Survey API is running',
        'status': 'healthy',
        'model_trained': model.is_trained,
        'timestamp': pd.Timestamp.now().isoformat()
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

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Process survey data and return financial health prediction
    """
    try:
        # Check if model is trained
        if not model.is_trained:
            return jsonify({
                'success': False,
                'error': 'Model is not trained. Please train the model first.'
            }), 503

        # Get survey data from request
        survey_data = request.get_json()
        
        if not survey_data:
            return jsonify({
                'success': False,
                'error': 'No survey data provided'
            }), 400
        
        # Make prediction using the model
        result = model.predict_financial_health(survey_data)
        
        return jsonify({
            'success': True,
            'prediction': result['predicted_category'],
            'confidence_scores': result['confidence_scores'],
            'recommendation': result['recommendation'],
            'survey_data': survey_data
        })
        
    except Exception as e:
        # Log error details for debugging (avoid exposing in production responses)
        import logging
        logging.error(f"Prediction error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while processing your survey. Please try again.'
        }), 500

if __name__ == '__main__':
    # For development
    app.run(debug=True, host='0.0.0.0', port=5000)
else:
    # For production (when imported by main.py or gunicorn)
    pass