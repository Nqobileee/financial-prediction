"""
Financial Health Survey Assessment Model
=====================================

This model predicts financial health categories (Low, Medium, High) based on survey responses.
The model is trained on business survey data and can be used for real-time assessment.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import warnings
warnings.filterwarnings('ignore')

class FinancialHealthSurveyModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_names = None
        self.is_trained = False
        
    def preprocess_survey_data(self, data):
        """
        Preprocess survey data to match the training format
        """
        # Define the survey questions mapping to dataset columns
        survey_mapping = {
            'country': 'country',
            'owner_age': 'owner_age',
            'owner_sex': 'owner_sex',
            'business_age_years': 'business_age_years',
            'business_age_months': 'business_age_months',
            'covid_essential_service': 'covid_essential_service',
            'personal_income': 'personal_income',
            'business_expenses': 'business_expenses',
            'business_turnover': 'business_turnover',
            'keeps_financial_records': 'keeps_financial_records',
            'has_mobile_money': 'has_mobile_money',
            'has_insurance': 'has_insurance',
            'future_risk_theft_stock': 'future_risk_theft_stock',
            'attitude_stable_business_environment': 'attitude_stable_business_environment',
            'compliance_income_tax': 'compliance_income_tax',
            'has_cellphone': 'has_cellphone',
            'motivation_make_more_money': 'motivation_make_more_money'
        }
        
        # Create dataframe from survey responses
        processed_data = pd.DataFrame()
        for survey_key, dataset_key in survey_mapping.items():
            if survey_key in data:
                processed_data[dataset_key] = [data[survey_key]]
            else:
                # Set default values for missing data
                processed_data[dataset_key] = [None]
        
        return processed_data
    
    def load_and_prepare_data(self, train_file_path):
        """
        Load and prepare training data
        """
        print("Loading training data...")
        df = pd.read_csv(train_file_path)
        
        # Select key features based on survey questions
        survey_features = [
            'country', 'owner_age', 'owner_sex', 'business_age_years', 
            'business_age_months', 'covid_essential_service', 'personal_income',
            'business_expenses', 'business_turnover', 'keeps_financial_records',
            'has_mobile_money', 'has_insurance', 'future_risk_theft_stock',
            'attitude_stable_business_environment', 'compliance_income_tax',
            'has_cellphone', 'motivation_make_more_money'
        ]
        
        # Filter to features that exist in the dataset
        available_features = [f for f in survey_features if f in df.columns]
        
        # Create feature matrix
        X = df[available_features].copy()
        y = df['Target'].copy()
        
        # Handle missing values
        for col in X.columns:
            if X[col].dtype == 'object':
                X[col] = X[col].fillna('Unknown')
            else:
                X[col] = X[col].fillna(X[col].median())
        
        self.feature_names = available_features
        return X, y
    
    def encode_features(self, X, fit=True):
        """
        Encode categorical features
        """
        X_encoded = X.copy()
        
        for col in X_encoded.columns:
            if X_encoded[col].dtype == 'object':
                if fit:
                    le = LabelEncoder()
                    X_encoded[col] = le.fit_transform(X_encoded[col].astype(str))
                    self.label_encoders[col] = le
                else:
                    if col in self.label_encoders:
                        le = self.label_encoders[col]
                        # Handle unseen categories
                        X_encoded[col] = X_encoded[col].astype(str)
                        unique_values = set(le.classes_)
                        X_encoded[col] = X_encoded[col].apply(
                            lambda x: x if x in unique_values else 'Unknown'
                        )
                        X_encoded[col] = le.transform(X_encoded[col])
                    else:
                        X_encoded[col] = 0  # Default encoding for new columns
        
        return X_encoded
    
    def train_model(self, train_file_path):
        """
        Train the financial health assessment model
        """
        print("Starting model training...")
        
        # Load and prepare data
        X, y = self.load_and_prepare_data(train_file_path)
        
        # Encode features
        X_encoded = self.encode_features(X, fit=True)
        
        # Scale numerical features
        X_scaled = self.scaler.fit_transform(X_encoded)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model
        print("Training Random Forest model...")
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Model trained successfully!")
        print(f"Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        self.is_trained = True
        return accuracy
    
    def predict_financial_health(self, survey_responses):
        """
        Predict financial health category from survey responses
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Preprocess survey data
        processed_data = self.preprocess_survey_data(survey_responses)
        
        # Add missing columns with default values
        for feature in self.feature_names:
            if feature not in processed_data.columns:
                if feature in ['personal_income', 'business_expenses', 'business_turnover', 
                             'owner_age', 'business_age_years', 'business_age_months']:
                    processed_data[feature] = [0]
                else:
                    processed_data[feature] = ['Unknown']
        
        # Reorder columns to match training data
        processed_data = processed_data[self.feature_names]
        
        # Encode features
        X_encoded = self.encode_features(processed_data, fit=False)
        
        # Scale features
        X_scaled = self.scaler.transform(X_encoded)
        
        # Make prediction
        prediction = self.model.predict(X_scaled)[0]
        probability = self.model.predict_proba(X_scaled)[0]
        
        # Get class probabilities
        classes = self.model.classes_
        prob_dict = {classes[i]: probability[i] for i in range(len(classes))}
        
        return {
            'predicted_category': prediction,
            'confidence_scores': prob_dict,
            'recommendation': self._get_recommendation(prediction, prob_dict)
        }
    
    def _get_recommendation(self, prediction, prob_dict):
        """
        Generate recommendations based on prediction
        """
        recommendations = {
            'High': "Excellent financial health! Continue current practices and consider expansion opportunities.",
            'Medium': "Good financial health with room for improvement. Focus on increasing revenue and managing expenses.",
            'Low': "Financial health needs attention. Consider financial planning, expense reduction, and revenue diversification."
        }
        
        confidence = max(prob_dict.values())
        base_rec = recommendations.get(prediction, "Financial health assessment completed.")
        
        if confidence < 0.6:
            base_rec += " Note: Prediction confidence is moderate. Consider providing more detailed financial information."
        
        return base_rec
    
    def save_model(self, model_path):
        """
        Save the trained model
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        
        model_data = {
            'model': self.model,
            'label_encoders': self.label_encoders,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, model_path)
        print(f"Model saved to {model_path}")
    
    def load_model(self, model_path):
        """
        Load a pre-trained model
        """
        model_data = joblib.load(model_path)
        
        self.model = model_data['model']
        self.label_encoders = model_data['label_encoders']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.is_trained = model_data['is_trained']
        
        print(f"Model loaded from {model_path}")


def create_sample_survey_responses():
    """
    Create sample survey responses for testing
    """
    samples = [
        {
            'country': 'zimbabwe',
            'owner_age': 35,
            'owner_sex': 'Female',
            'business_age_years': 5,
            'business_age_months': 6,
            'covid_essential_service': 'Yes',
            'personal_income': 50000,
            'business_expenses': 25000,
            'business_turnover': 80000,
            'keeps_financial_records': 'Yes, always',
            'has_mobile_money': 'Have now',
            'has_insurance': 'Yes',
            'future_risk_theft_stock': 'No',
            'attitude_stable_business_environment': 'Yes',
            'compliance_income_tax': 'Yes',
            'has_cellphone': 'Yes',
            'motivation_make_more_money': 'Yes'
        },
        {
            'country': 'malawi',
            'owner_age': 28,
            'owner_sex': 'Male',
            'business_age_years': 2,
            'business_age_months': 0,
            'covid_essential_service': 'No',
            'personal_income': 15000,
            'business_expenses': 12000,
            'business_turnover': 20000,
            'keeps_financial_records': 'Yes, sometimes',
            'has_mobile_money': 'Never had',
            'has_insurance': 'No',
            'future_risk_theft_stock': 'Yes',
            'attitude_stable_business_environment': 'Don\'t know or N/A',
            'compliance_income_tax': 'No',
            'has_cellphone': 'Yes',
            'motivation_make_more_money': 'Yes'
        }
    ]
    
    return samples


def main():
    """
    Main function to demonstrate the model
    """
    # Initialize the model
    model = FinancialHealthSurveyModel()
    
    # Train the model
    print("=" * 60)
    print("FINANCIAL HEALTH SURVEY MODEL TRAINING")
    print("=" * 60)
    
    train_accuracy = model.train_model('Train.csv')
    
    # Save the trained model
    model.save_model('financial_health_model.pkl')
    
    # Test with sample survey responses
    print("\n" + "=" * 60)
    print("TESTING WITH SAMPLE SURVEY RESPONSES")
    print("=" * 60)
    
    sample_responses = create_sample_survey_responses()
    
    for i, response in enumerate(sample_responses, 1):
        print(f"\nSample {i}:")
        print("-" * 30)
        
        # Make prediction
        result = model.predict_financial_health(response)
        
        print(f"Predicted Financial Health: {result['predicted_category']}")
        print(f"Confidence Scores:")
        for category, score in result['confidence_scores'].items():
            print(f"  {category}: {score:.3f}")
        print(f"Recommendation: {result['recommendation']}")


if __name__ == "__main__":
    main()