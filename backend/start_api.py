#!/usr/bin/env python3
"""
Financial Health Survey API Startup Script
==========================================

This script ensures the model is trained and starts the Flask API server.
Run this before starting the frontend application.
"""

import os
import sys
from financial_health_survey_model import FinancialHealthSurveyModel
from survey_web_app import app

def ensure_model_trained():
    """Ensure the model is trained before starting the API"""
    model = FinancialHealthSurveyModel()
    model_path = 'financial_health_model.pkl'
    
    # Check if trained model exists
    if os.path.exists(model_path):
        try:
            model.load_model(model_path)
            print("✅ Pre-trained model loaded successfully!")
            return True
        except Exception as e:
            print(f"❌ Error loading existing model: {e}")
            print("🔄 Will retrain the model...")
    
    # Train the model if needed
    if os.path.exists('Train.csv'):
        print("🚀 Training the financial health model...")
        try:
            accuracy = model.train_model('Train.csv')
            model.save_model(model_path)
            print(f"✅ Model trained successfully with accuracy: {accuracy:.4f}")
            return True
        except Exception as e:
            print(f"❌ Error training model: {e}")
            return False
    else:
        print("❌ Training data (Train.csv) not found!")
        print("📋 Please ensure Train.csv is in the backend directory.")
        return False

def main():
    """Main startup function"""
    print("=" * 60)
    print("🏦 Financial Health Survey API")
    print("=" * 60)
    
    # Check if model is ready
    if not ensure_model_trained():
        print("❌ Failed to prepare model. Exiting...")
        sys.exit(1)
    
    print("\n🌐 Starting Flask API server...")
    print("📡 API will be available at: http://localhost:5000")
    print("🔗 Frontend should connect to: http://localhost:5000/api/predict")
    print("\n💡 Available endpoints:")
    print("   - GET  /api/health     - Health check")
    print("   - POST /api/predict    - Submit survey for prediction")
    print("   - POST /api/train      - Retrain model (admin)")
    print("\n🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Start the Flask app
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")

if __name__ == '__main__':
    main()