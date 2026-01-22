# Financial Health Survey API

A comprehensive machine learning solution for assessing business financial health through survey responses. This project provides both a REST API for integration with frontend applications and command-line tools for model management.

## Features

- **REST API**: Flask-based API with CORS support for frontend integration
- **Machine Learning Model**: Random Forest classifier trained on business survey data
- **Real-time Assessment**: Instant financial health categorization (Low/Medium/High)
- **Confidence Scoring**: Probability scores for each health category
- **Actionable Recommendations**: Personalized advice based on assessment results
- **Auto-training**: Automatic model training on startup if needed

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the API Server (Recommended)
```bash
python start_api.py
```
This will:
- Automatically train the model if needed
- Start the Flask API server on `http://localhost:5000`
- Provide endpoints for the frontend application

### 3. Alternative: Manual Model Training
```bash
python financial_health_cli.py --train
```

### 4. Test the Model (Optional)
```bash
python financial_health_cli.py --test
```

## API Endpoints

### Health Check
```http
GET /api/health
```
Returns API status and model training state.

### Submit Survey for Prediction
```http
POST /api/predict
Content-Type: application/json

{
  "country": "eswatini",
  "owner_age": 35,
  "owner_sex": "Female",
  "business_age_years": 2,
  "business_age_months": 6,
  "covid_essential_service": "No",
  "personal_income": 5000,
  "business_expenses": 2000,
  "business_turnover": 8000,
  "keeps_financial_records": "Yes, always",
  "has_mobile_money": "Have now",
  "has_insurance": "Yes",
  "future_risk_theft_stock": "No",
  "attitude_stable_business_environment": "Yes",
  "compliance_income_tax": "Yes",
  "has_cellphone": "Yes",
  "motivation_make_more_money": "Yes"
}
```

### Train Model (Admin)
```http
POST /api/train
```
Retrains the model using `Train.csv`.

## Integration with Frontend

The API is designed to work with the Next.js frontend application. Ensure both the backend API and frontend are running:

1. **Backend**: `python start_api.py` (runs on port 5000)
2. **Frontend**: `npm run dev` (typically runs on port 3000)

The frontend will automatically submit survey responses to `http://localhost:5000/api/predict` and display the results.

### 4. Run Interactive Assessment
```bash
python financial_health_cli.py --predict
```

### 5. Launch Web Application
```bash
python financial_health_cli.py --web
```
Then open your browser to `http://localhost:5000`

### 6. Complete Setup (All-in-One)
```bash
python financial_health_cli.py --all
```

## Survey Categories

The assessment covers 5 key areas across 16 questions:

### 1. Demographics & Business Profile
- Country (Eswatini, Lesotho, Malawi, Zimbabwe)
- Owner age and gender
- Business age
- COVID essential service status

### 2. Financial Information
- Personal income
- Business expenses
- Business turnover
- Financial record keeping
- Mobile money usage

### 3. Insurance & Risk
- Business insurance status
- Theft risk assessment

### 4. Attitudes & Compliance
- Business environment outlook
- Tax compliance

### 5. Operations
- Cellphone usage
- Business motivation

## Model Performance

The Random Forest model achieves high accuracy in predicting financial health categories based on:
- Feature importance analysis
- Cross-validation testing
- Confidence scoring for predictions

## File Structure

```
├── financial_health_survey_model.py    # Core ML model
├── financial_health_cli.py             # Command line interface
├── survey_web_app.py                   # Flask web application
├── templates/survey.html               # Web survey interface
├── requirements.txt                    # Python dependencies
├── financial_health_model.pkl          # Trained model (generated)
├── Train.csv                          # Training data
└── README.md                          # This file
```

## Usage Examples

### Command Line Training
```bash
# Train the model
python financial_health_cli.py --train

# Test with sample data
python financial_health_cli.py --test

# Interactive assessment
python financial_health_cli.py --predict
```

### Web Interface
```bash
# Start web server
python financial_health_cli.py --web

# Access at http://localhost:5000
```

### Python API Usage
```python
from financial_health_survey_model import FinancialHealthSurveyModel

# Initialize and load model
model = FinancialHealthSurveyModel()
model.load_model('financial_health_model.pkl')

# Make prediction
survey_data = {
    'country': 'zimbabwe',
    'owner_age': 35,
    'personal_income': 50000,
    # ... other survey fields
}

result = model.predict_financial_health(survey_data)
print(f"Health Category: {result['predicted_category']}")
print(f"Recommendations: {result['recommendation']}")
```

## Output Categories

- **High**: Excellent financial health with strong indicators
- **Medium**: Good health with room for improvement
- **Low**: Needs attention and financial planning

Each prediction includes:
- Primary category prediction
- Confidence scores for all categories
- Personalized recommendations
- Risk assessment insights

## Development

### Adding New Features
1. Modify the survey questions in `templates/survey.html`
2. Update the feature mapping in `FinancialHealthSurveyModel.preprocess_survey_data()`
3. Retrain the model with new features

### Custom Models
The `FinancialHealthSurveyModel` class can be extended to use different algorithms:
- Gradient Boosting
- Neural Networks
- Ensemble methods

## Troubleshooting

### Common Issues

1. **Model not found error**
   ```bash
   python financial_health_cli.py --train
   ```

2. **Missing dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Training data not found**
   - Ensure `Train.csv` is in the project directory

4. **Web app port conflicts**
   - Change port in `survey_web_app.py` line: `app.run(debug=True, host='0.0.0.0', port=5001)`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions or issues:
- Check the troubleshooting section
- Review the example usage
- Run tests with `--test` flag to verify setup