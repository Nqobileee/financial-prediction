#!/usr/bin/env python3
"""
Model Training Script
====================
Train a Random Forest model on the existing data and save it for production use.
This script will train the model once and save it to avoid copyright issues.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, roc_auc_score
import joblib
import json
import warnings
warnings.filterwarnings('ignore')

def load_and_prepare_data():
    """Load and prepare the training data"""
    print("Loading training data...")
    df = pd.read_csv('Train.csv')
    
    print(f"Dataset shape: {df.shape}")
    print(f"Target distribution:\n{df['Target'].value_counts()}")
    
    # Select key features for the model
    feature_columns = [
        'country', 'owner_age', 'owner_sex', 'business_age_years', 
        'covid_essential_service', 'personal_income', 'business_expenses', 
        'business_turnover', 'keeps_financial_records', 'has_mobile_money', 
        'has_insurance', 'compliance_income_tax', 'has_cellphone',
        'attitude_stable_business_environment', 'future_risk_theft_stock'
    ]
    
    # Create feature dataframe
    X = df[feature_columns].copy()
    y = df['Target'].copy()
    
    return X, y, feature_columns

def preprocess_features(X_train, X_test, feature_columns):
    """Preprocess features with label encoding and handle missing values"""
    
    label_encoders = {}
    
    # Handle missing values
    for col in X_train.columns:
        if X_train[col].dtype == 'object':
            X_train[col] = X_train[col].fillna('Unknown')
            X_test[col] = X_test[col].fillna('Unknown')
        else:
            X_train[col] = X_train[col].fillna(X_train[col].median())
            X_test[col] = X_test[col].fillna(X_train[col].median())
    
    # Encode categorical variables
    categorical_columns = X_train.select_dtypes(include=['object']).columns
    
    for col in categorical_columns:
        le = LabelEncoder()
        # Fit on combined data to handle unseen categories
        combined_values = pd.concat([X_train[col], X_test[col]]).unique()
        le.fit(combined_values)
        
        X_train[col] = le.transform(X_train[col])
        X_test[col] = le.transform(X_test[col])
        
        label_encoders[col] = le
    
    return X_train, X_test, label_encoders

def train_model():
    """Train the Random Forest model"""
    
    # Load data
    X, y, feature_columns = load_and_prepare_data()
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Preprocess features
    X_train_processed, X_test_processed, label_encoders = preprocess_features(
        X_train, X_test, feature_columns
    )
    
    # Train Random Forest model
    print("Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=500,
        max_depth=15,
        min_samples_split=20,
        min_samples_leaf=5,
        random_state=42,
        class_weight='balanced'
    )
    
    model.fit(X_train_processed, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test_processed)
    y_pred_proba = model.predict_proba(X_test_processed)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\\nModel Performance:")
    print(f"Accuracy: {accuracy:.3f}")
    print(f"\\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\\nTop 10 Feature Importances:")
    print(feature_importance.head(10))
    
    # Save the model and encoders
    print("\\nSaving model and preprocessors...")
    
    model_data = {
        'model': model,
        'label_encoders': label_encoders,
        'feature_columns': feature_columns,
        'model_metrics': {
            'accuracy': accuracy,
            'feature_importance': feature_importance.to_dict('records')
        }
    }
    
    joblib.dump(model_data, 'trained_financial_health_model.pkl')
    
    # Save feature mappings for the survey
    feature_mappings = {
        'feature_columns': feature_columns,
        'categorical_columns': list(label_encoders.keys()),
        'target_classes': list(model.classes_)
    }
    
    with open('model_config.json', 'w') as f:
        json.dump(feature_mappings, f, indent=2)
    
    print("Model saved successfully!")
    return model_data

if __name__ == "__main__":
    model_data = train_model()