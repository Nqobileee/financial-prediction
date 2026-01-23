#!/usr/bin/env python3
"""
Main entry point for Financial Health Survey API
==============================================

This is the main file that Render will use to start the application.
It ensures the model is ready and starts the Flask server.
"""

import os
import sys
import logging
from financial_health_survey_model import FinancialHealthSurveyModel
from survey_web_app import app

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def ensure_model_ready():
    """Ensure the model is ready for predictions"""
    try:
        # The model is already loaded in survey_web_app.py
        # Just verify it's working
        model = FinancialHealthSurveyModel()
        if model.is_trained:
            logger.info("✅ Model is ready for predictions")
            return True
        else:
            logger.warning("⚠️ Model not fully trained, but API will start")
            return True  # Still start the API
    except Exception as e:
        logger.error(f"❌ Error checking model: {e}")
        return False

def create_app():
    """Create and configure the Flask app for production"""
    
    # Ensure model is ready
    if not ensure_model_ready():
        logger.error("Failed to prepare model")
        sys.exit(1)
    
    # Configure app for production
    app.config['DEBUG'] = False
    app.config['TESTING'] = False
    
    logger.info("🏦 Financial Health Survey API is starting...")
    logger.info("🌐 API endpoints available:")
    logger.info("   - GET  /              - API info")
    logger.info("   - GET  /api/health    - Health check")
    logger.info("   - POST /api/predict   - Submit survey for prediction")
    logger.info("   - POST /api/train     - Retrain model")
    
    return app

# This is what Render will call
application = create_app()

if __name__ == '__main__':
    # For local development
    port = int(os.environ.get('PORT', 5000))
    application.run(debug=False, host='0.0.0.0', port=port)