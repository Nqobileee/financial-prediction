/**
 * API Test Page - For testing API connectivity and endpoints
 */
"use client";

import { useState } from 'react';
import { checkApiHealth, submitSurveyData, getApiUrl, type SurveyData } from '@/lib/api';
import ApiStatus from '@/components/ApiStatus';
import Link from 'next/link';

export default function ApiTestPage() {
  const [healthResult, setHealthResult] = useState<string>('');
  const [predictResult, setPredictResult] = useState<string>('');
  const [loading, setLoading] = useState<{ health: boolean; predict: boolean }>({
    health: false,
    predict: false,
  });

  const testHealthEndpoint = async () => {
    setLoading(prev => ({ ...prev, health: true }));
    try {
      const isHealthy = await checkApiHealth();
      setHealthResult(`✅ Health check passed: ${isHealthy}`);
    } catch (error) {
      setHealthResult(`❌ Health check failed: ${error}`);
    } finally {
      setLoading(prev => ({ ...prev, health: false }));
    }
  };

  const testPredictEndpoint = async () => {
    setLoading(prev => ({ ...prev, predict: true }));
    try {
      const sampleData: SurveyData = {
        country: 'Eswatini',
        owner_age: 35,
        owner_sex: 'M',
        business_age_years: 5,
        business_age_months: 2,
        covid_essential_service: 'Yes',
        personal_income: 50000,
        business_expenses: 30000,
        business_turnover: 80000,
        keeps_financial_records: 'Yes',
        has_mobile_money: 'Yes',
        has_insurance: 'No',
        future_risk_theft_stock: 'Medium',
        attitude_stable_business_environment: 'Agree',
        compliance_income_tax: 'Yes',
        has_cellphone: 'Yes',
        motivation_make_more_money: 'Strongly Agree'
      };

      const result = await submitSurveyData(sampleData);
      setPredictResult(`✅ Prediction successful: ${JSON.stringify(result, null, 2)}`);
    } catch (error) {
      setPredictResult(`❌ Prediction failed: ${error}`);
    } finally {
      setLoading(prev => ({ ...prev, predict: false }));
    }
  };

  return (
    <main className="pt-16 sm:pt-24 pb-12 sm:pb-20 max-w-4xl mx-auto px-4">
      <div className="space-y-8">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-3xl font-bold mb-4">API Connectivity Test</h1>
          <p className="text-slate-600 dark:text-slate-400 mb-6">
            Test your API endpoints to ensure everything is working correctly.
          </p>
          <div className="flex justify-center mb-6">
            <ApiStatus />
          </div>
          <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
            <p className="text-sm">
              <strong>Current API URL:</strong> {getApiUrl()}
            </p>
          </div>
        </div>

        {/* Test Buttons */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          {/* Health Test */}
          <div className="bg-white dark:bg-slate-800 rounded-xl p-6 border">
            <h2 className="text-xl font-bold mb-4">Health Endpoint Test</h2>
            <p className="text-sm text-slate-600 dark:text-slate-400 mb-4">
              Tests the <code>/api/health</code> endpoint to verify the API is running.
            </p>
            <button
              onClick={testHealthEndpoint}
              disabled={loading.health}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 mb-4"
            >
              {loading.health ? 'Testing...' : 'Test Health Endpoint'}
            </button>
            {healthResult && (
              <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded-lg">
                <pre className="text-sm whitespace-pre-wrap">{healthResult}</pre>
              </div>
            )}
          </div>

          {/* Predict Test */}
          <div className="bg-white dark:bg-slate-800 rounded-xl p-6 border">
            <h2 className="text-xl font-bold mb-4">Predict Endpoint Test</h2>
            <p className="text-sm text-slate-600 dark:text-slate-400 mb-4">
              Tests the <code>/api/predict</code> endpoint with sample survey data.
            </p>
            <button
              onClick={testPredictEndpoint}
              disabled={loading.predict}
              className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50 mb-4"
            >
              {loading.predict ? 'Testing...' : 'Test Predict Endpoint'}
            </button>
            {predictResult && (
              <div className="bg-gray-50 dark:bg-gray-900 p-3 rounded-lg max-h-64 overflow-y-auto">
                <pre className="text-xs whitespace-pre-wrap">{predictResult}</pre>
              </div>
            )}
          </div>
        </div>

        {/* Environment Info */}
        <div className="bg-yellow-50 dark:bg-yellow-900/20 p-6 rounded-xl border border-yellow-200 dark:border-yellow-800">
          <h3 className="text-lg font-bold mb-3">Environment Information</h3>
          <div className="space-y-2 text-sm">
            <p><strong>NODE_ENV:</strong> {process.env.NODE_ENV || 'development'}</p>
            <p><strong>API URL Source:</strong> {process.env.NEXT_PUBLIC_API_URL ? 'Environment Variable' : 'Default (localhost:5000)'}</p>
            <p><strong>Expected URLs:</strong></p>
            <ul className="list-disc list-inside ml-4 space-y-1">
              <li><strong>Development:</strong> http://localhost:5000</li>
              <li><strong>Production:</strong> https://financial-prediction.onrender.com</li>
            </ul>
          </div>
        </div>

        {/* CORS Test Instructions */}
        <div className="bg-purple-50 dark:bg-purple-900/20 p-6 rounded-xl border border-purple-200 dark:border-purple-800">
          <h3 className="text-lg font-bold mb-3">🔧 Troubleshooting Guide</h3>
          <div className="space-y-3 text-sm">
            <div>
              <strong>❌ If tests fail:</strong>
              <ul className="list-disc list-inside ml-4 mt-2 space-y-1">
                <li>Check that your backend is deployed and running on Render</li>
                <li>Verify the API URL in your environment variables</li>
                <li>Open browser dev tools and check the Network tab for CORS errors</li>
                <li>Ensure your Render app has CORS enabled (flask-cors)</li>
              </ul>
            </div>
            <div>
              <strong>✅ If tests pass:</strong>
              <ul className="list-disc list-inside ml-4 mt-2 space-y-1">
                <li>Your API is working correctly!</li>
                <li>Try the actual survey to test the full flow</li>
                <li>Test on mobile devices to ensure responsive design</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/survey"
            className="bg-primary text-white px-6 py-3 rounded-xl font-bold text-center hover:bg-primary/90 transition-colors"
          >
            Try Real Survey
          </Link>
          <Link
            href="/"
            className="bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-6 py-3 rounded-xl font-bold text-center hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
          >
            Back to Home
          </Link>
        </div>
      </div>
    </main>
  );
}