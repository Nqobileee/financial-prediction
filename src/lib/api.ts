/**
 * API Configuration and Utility Functions
 * Centralized API management for the Financial Health Survey app
 */

// Get the API base URL from environment variables
export const getApiUrl = (): string => {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL;
  
  if (!apiUrl) {
    console.warn('NEXT_PUBLIC_API_URL not set, falling back to localhost');
    return 'http://localhost:5000';
  }
  
  return apiUrl;
};

// API endpoints
export const API_ENDPOINTS = {
  health: '/api/health',
  predict: '/api/predict',
  train: '/api/train',
} as const;

/**
 * Make an API request with proper error handling
 */
export async function apiRequest<T>(
  endpoint: string, 
  options: RequestInit = {}
): Promise<T> {
  const baseUrl = getApiUrl();
  const url = `${baseUrl}${endpoint}`;
  
  const defaultHeaders = {
    'Content-Type': 'application/json',
  };
  
  const config: RequestInit = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };
  
  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP ${response.status}: ${errorText}`);
    }
    
    const data = await response.json();
    return data as T;
  } catch (error) {
    console.error(`API request failed for ${url}:`, error);
    
    if (error instanceof TypeError && error.message.includes('fetch')) {
      throw new Error('Unable to connect to the prediction service. Please check your internet connection and try again.');
    }
    
    throw error;
  }
}

/**
 * Check if the API is healthy
 */
export async function checkApiHealth(): Promise<boolean> {
  try {
    const response = await apiRequest<{ success: boolean }>(API_ENDPOINTS.health);
    return response.success;
  } catch (error) {
    console.warn('API health check failed:', error);
    return false;
  }
}

/**
 * Submit survey data for prediction
 */
export interface SurveyData {
  country: string;
  owner_age: number;
  owner_sex: string;
  business_age_years: number;
  business_age_months: number;
  covid_essential_service: string;
  personal_income: number;
  business_expenses: number;
  business_turnover: number;
  keeps_financial_records: string;
  has_mobile_money: string;
  has_insurance: string;
  future_risk_theft_stock: string;
  attitude_stable_business_environment: string;
  compliance_income_tax: string;
  has_cellphone: string;
  motivation_make_more_money: string;
}

export interface PredictionResponse {
  success: boolean;
  prediction?: string;
  confidence_scores?: Record<string, number>;
  recommendation?: string;
  survey_data?: SurveyData;
  error?: string;
}

export async function submitSurveyData(data: SurveyData): Promise<PredictionResponse> {
  return apiRequest<PredictionResponse>(API_ENDPOINTS.predict, {
    method: 'POST',
    body: JSON.stringify(data),
  });
}