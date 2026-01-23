import { NextRequest, NextResponse } from 'next/server';

interface SurveyData {
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

interface PredictionResponse {
  success: boolean;
  prediction?: string;
  confidence_scores?: Record<string, number>;
  recommendation?: string;
  survey_data?: SurveyData;
  error?: string;
}

function calculateFinancialHealthScore(data: SurveyData): number {
  let score = 0;
  let maxScore = 0;

  // Income stability factors (40% weight)
  const incomeRatio = data.business_turnover / (data.business_expenses || 1);
  score += Math.min(incomeRatio * 10, 40);
  maxScore += 40;

  // Financial management practices (25% weight)
  if (data.keeps_financial_records === 'Yes') score += 15;
  if (data.has_insurance === 'Yes') score += 10;
  maxScore += 25;

  // Technology adoption (15% weight)
  if (data.has_mobile_money === 'Yes') score += 8;
  if (data.has_cellphone === 'Yes') score += 7;
  maxScore += 15;

  // Business resilience (10% weight)
  if (data.covid_essential_service === 'Yes') score += 5;
  if (data.attitude_stable_business_environment === 'Positive') score += 5;
  maxScore += 10;

  // Compliance and planning (10% weight)
  if (data.compliance_income_tax === 'Yes') score += 5;
  if (data.motivation_make_more_money === 'High') score += 5;
  maxScore += 10;

  return (score / maxScore) * 100;
}

function categorizeFinancialHealth(score: number): {
  category: string;
  confidence_scores: Record<string, number>;
  recommendation: string;
} {
  let category: string;
  let recommendation: string;

  if (score >= 70) {
    category = 'High';
    recommendation = 'Excellent financial health! Continue maintaining good financial practices and consider expanding your business operations.';
  } else if (score >= 40) {
    category = 'Medium';
    recommendation = 'Moderate financial health. Focus on improving financial record-keeping, increasing turnover, and reducing financial risks.';
  } else {
    category = 'Low';
    recommendation = 'Financial health needs improvement. Consider seeking financial advisory services, improving cash flow management, and building emergency funds.';
  }

  // Generate confidence scores based on the score
  const confidence_scores: Record<string, number> = {
    'Low': Math.max(0, (40 - score) / 40),
    'Medium': score >= 40 && score <= 70 ? (70 - Math.abs(score - 55)) / 15 : Math.max(0, 1 - Math.abs(score - 55) / 30),
    'High': Math.max(0, (score - 30) / 70)
  };

  // Normalize confidence scores to sum to 1
  const total = Object.values(confidence_scores).reduce((a, b) => a + b, 0);
  Object.keys(confidence_scores).forEach(key => {
    confidence_scores[key] = confidence_scores[key] / total;
  });

  return { category, confidence_scores, recommendation };
}

export async function POST(request: NextRequest) {
  try {
    const data: SurveyData = await request.json();

    // Validate required fields
    const requiredFields = ['country', 'owner_age', 'personal_income', 'business_turnover'];
    for (const field of requiredFields) {
      if (!(field in data) || data[field as keyof SurveyData] === null || data[field as keyof SurveyData] === undefined) {
        return NextResponse.json({
          success: false,
          error: `Missing required field: ${field}`
        }, { status: 400 });
      }
    }

    // Calculate financial health score
    const healthScore = calculateFinancialHealthScore(data);
    
    // Get prediction and confidence scores
    const result = categorizeFinancialHealth(healthScore);

    const response: PredictionResponse = {
      success: true,
      prediction: result.category,
      confidence_scores: result.confidence_scores,
      recommendation: result.recommendation,
      survey_data: data
    };

    return NextResponse.json(response);

  } catch (error) {
    console.error('Prediction error:', error);
    return NextResponse.json({
      success: false,
      error: 'Failed to process prediction request'
    }, { status: 500 });
  }
}

export async function GET() {
  return NextResponse.json({
    message: 'Financial Health Prediction API',
    method: 'POST',
    description: 'Submit survey data to get financial health prediction'
  });
}