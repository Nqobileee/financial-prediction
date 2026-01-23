#!/bin/bash

# Build script for Render deployment
echo "🔧 Starting build process..."

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Verify critical files exist
echo "🔍 Verifying files..."
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found!"
    exit 1
fi

if [ ! -f "trained_financial_health_model.pkl" ]; then
    echo "❌ trained_financial_health_model.pkl not found!"
    exit 1
fi

echo "✅ Build completed successfully!"