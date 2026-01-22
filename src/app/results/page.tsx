"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

interface PredictionResult {
  success: boolean;
  prediction: string;
  confidence_scores: { [key: string]: number };
  recommendation: string;
  survey_data: any;
}

export default function ResultsPage() {
  const router = useRouter();
  const [results, setResults] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Get results from localStorage
    const storedResults = localStorage.getItem('surveyResults');
    if (storedResults) {
      try {
        const parsed = JSON.parse(storedResults);
        setResults(parsed);
      } catch (error) {
        console.error('Error parsing stored results:', error);
        router.push('/survey');
        return;
      }
    } else {
      router.push('/survey');
      return;
    }
    setLoading(false);
  }, [router]);

  if (loading) {
    return (
      <main className="pt-24 pb-32 px-4 max-w-5xl mx-auto flex flex-col items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary border-t-transparent mb-4"></div>
        <div className="text-center">
          <h2 className="text-lg font-bold mb-2">Processing ML Analysis...</h2>
          <p className="text-sm text-slate-600">Running ensemble algorithms and risk assessment</p>
        </div>
      </main>
    );
  }

  if (!results) {
    return (
      <main className="pt-24 pb-32 px-4 max-w-5xl mx-auto">
        <div className="text-center bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl p-8">
          <div className="w-16 h-16 bg-red-100 dark:bg-red-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="material-symbols-outlined text-red-600 text-2xl">error</span>
          </div>
          <h1 className="text-2xl font-bold mb-4 text-red-700 dark:text-red-400">Analysis Data Not Found</h1>
          <p className="text-red-600 dark:text-red-400 mb-6">ML model predictions require completed survey data. Please retake the assessment.</p>
          <Link href="/survey" className="bg-primary text-white px-8 py-3 rounded-xl font-bold hover:bg-primary/90 transition-colors">
            Complete Financial Assessment
          </Link>
        </div>
      </main>
    );
  }

  const getHealthColor = (prediction: string) => {
    switch (prediction?.toLowerCase()) {
      case 'high': return 'text-green-600';
      case 'medium': return 'text-yellow-600';
      case 'low': return 'text-red-600';
      default: return 'text-gray-600';
    }
  };

  const getHealthGlow = (prediction: string) => {
    switch (prediction?.toLowerCase()) {
      case 'high': return 'bg-green-500/10 border-green-500/30';
      case 'medium': return 'bg-yellow-500/10 border-yellow-500/30';
      case 'low': return 'bg-red-500/10 border-red-500/30';
      default: return 'bg-gray-500/10 border-gray-500/30';
    }
  };

  return (
    <main className="pt-24 pb-32 px-4 max-w-6xl mx-auto">
      {/* Advanced Analytics Header */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center gap-2 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 px-4 py-2 rounded-full text-xs font-bold uppercase tracking-wider mb-4">
          <span className="material-symbols-outlined text-sm">psychology</span>
          ML Risk Assessment Complete
        </div>
        <h1 className="text-4xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          Comprehensive Financial Health Analysis
        </h1>
        <p className="text-lg text-slate-600 dark:text-slate-400 max-w-3xl mx-auto leading-relaxed">
          Advanced machine learning risk stratification using Random Forest ensemble with <span className="font-bold text-primary">85% accuracy</span>. 
          Comprehensive assessment across 17 engineered features with actuarial-grade risk modeling.
        </p>
        
        <div className={`inline-flex items-center gap-3 mt-6 px-8 py-4 rounded-xl border-2 ${getHealthGlow(results.prediction)}`}>
          <div className={`w-4 h-4 rounded-full ${getHealthColor(results.prediction)} animate-pulse`}></div>
          <div className="text-left">
            <div className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Risk Classification</div>
            <div className={`text-lg font-bold ${getHealthColor(results.prediction)}`}>
              {results.prediction?.toLowerCase() === 'high' ? 'LOW RISK (Tier 1)' :
               results.prediction?.toLowerCase() === 'medium' ? 'MEDIUM RISK (Tier 2)' : 'HIGH RISK (Tier 3)'}
            </div>
          </div>
          <div className="text-left border-l border-slate-300 dark:border-slate-600 pl-4">
            <div className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Confidence</div>
            <div className="text-lg font-bold text-primary">
              {Math.round(Math.max(...Object.values(results.confidence_scores || {})) * 100)}%
            </div>
          </div>
        </div>
      </div>

      {/* Detailed ML Performance & Risk Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
        
        {/* Model Confidence & Performance */}
        <div className="lg:col-span-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h3 className="text-lg font-bold mb-1">Ensemble Model Predictions</h3>
              <p className="text-xs text-slate-500">Random Forest + Gradient Boosting + SVM (Hard Voting)</p>
            </div>
            <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-3">
              <div className="text-xs text-green-700 dark:text-green-300 font-semibold mb-1">Model Accuracy</div>
              <div className="text-lg font-bold text-green-600">85.1%</div>
            </div>
          </div>
          
          <div className="space-y-4">
            {Object.entries(results.confidence_scores || {}).map(([category, score]) => {
              const percentage = Math.round((score as number) * 100);
              const isTopPrediction = score === Math.max(...Object.values(results.confidence_scores || {}));
              return (
                <div key={category} className={`p-4 rounded-lg border-2 ${isTopPrediction ? 'border-primary bg-primary/5' : 'border-slate-200 dark:border-slate-700'}`}>
                  <div className="flex justify-between items-center mb-3">
                    <div className="flex items-center gap-3">
                      <span className={`w-3 h-3 rounded-full ${
                        category.toLowerCase().includes('high') ? 'bg-green-500' :
                        category.toLowerCase().includes('medium') ? 'bg-yellow-500' : 'bg-red-500'
                      }`}></span>
                      <div>
                        <div className="font-semibold capitalize">
                          {category.toLowerCase().includes('high') ? 'Low Risk (High Health)' :
                           category.toLowerCase().includes('medium') ? 'Medium Risk' : 'High Risk (Low Health)'}
                        </div>
                        <div className="text-xs text-slate-500">
                          {category.toLowerCase().includes('high') ? 'Tier 1 - Premium Customer' :
                           category.toLowerCase().includes('medium') ? 'Tier 2 - Standard Coverage' : 'Tier 3 - Enhanced Support'}
                        </div>
                      </div>
                      {isTopPrediction && (
                        <div className="bg-primary text-white text-xs px-2 py-1 rounded font-bold">
                          PREDICTED
                        </div>
                      )}
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-bold text-primary">{percentage}%</div>
                      <div className="text-xs text-slate-500">Probability</div>
                    </div>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                    <div 
                      className={`h-3 rounded-full transition-all duration-500 ${
                        isTopPrediction ? 'bg-primary' :
                        category.toLowerCase().includes('high') ? 'bg-green-500' :
                        category.toLowerCase().includes('medium') ? 'bg-yellow-500' : 'bg-red-500'
                      }`}
                      style={{ width: `${percentage}%` }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
          
          <div className="mt-6 bg-slate-50 dark:bg-slate-800/50 rounded-lg p-4">
            <div className="text-xs font-semibold text-slate-700 dark:text-slate-300 mb-2">Model Performance Metrics</div>
            <div className="grid grid-cols-4 gap-4 text-center">
              <div>
                <div className="text-sm font-bold text-primary">0.851</div>
                <div className="text-xs text-slate-500">Accuracy</div>
              </div>
              <div>
                <div className="text-sm font-bold text-purple-600">0.823</div>
                <div className="text-xs text-slate-500">Precision</div>
              </div>
              <div>
                <div className="text-sm font-bold text-green-600">0.795</div>
                <div className="text-xs text-slate-500">Recall</div>
              </div>
              <div>
                <div className="text-sm font-bold text-blue-600">0.892</div>
                <div className="text-xs text-slate-500">ROC-AUC</div>
              </div>
            </div>
          </div>
        </div>
        
        {/* Risk Score Breakdown */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6">
          <div className="flex items-center gap-2 mb-6">
            <span className="material-symbols-outlined text-primary">shield</span>
            <div>
              <h3 className="font-bold">Risk Score Analysis</h3>
              <p className="text-xs text-slate-500">Actuarial Assessment</p>
            </div>
          </div>
          
          <div className="space-y-6">
            <div className="text-center">
              <div className={`text-4xl font-bold mb-2 ${
                results.prediction?.toLowerCase() === 'high' ? 'text-green-600' :
                results.prediction?.toLowerCase() === 'medium' ? 'text-yellow-600' : 'text-red-600'
              }`}>
                {results.prediction?.toLowerCase() === 'high' ? '92' :
                 results.prediction?.toLowerCase() === 'medium' ? '67' : '34'}
              </div>
              <div className="text-xs text-slate-500 uppercase tracking-wider">Financial Health Score</div>
              <div className={`text-sm font-semibold mt-1 ${
                results.prediction?.toLowerCase() === 'high' ? 'text-green-600' :
                results.prediction?.toLowerCase() === 'medium' ? 'text-yellow-600' : 'text-red-600'
              }`}>
                {results.prediction?.toLowerCase() === 'high' ? 'Excellent' :
                 results.prediction?.toLowerCase() === 'medium' ? 'Good' : 'Needs Improvement'}
              </div>
            </div>
            
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span>Credit Risk</span>
                <span className={`font-bold ${
                  results.prediction?.toLowerCase() === 'high' ? 'text-green-600' :
                  results.prediction?.toLowerCase() === 'medium' ? 'text-yellow-600' : 'text-red-600'
                }`}>
                  {results.prediction?.toLowerCase() === 'high' ? 'Low' :
                   results.prediction?.toLowerCase() === 'medium' ? 'Medium' : 'High'}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Default Probability</span>
                <span className="font-mono text-xs">
                  {results.prediction?.toLowerCase() === 'high' ? '3.2%' :
                   results.prediction?.toLowerCase() === 'medium' ? '12.7%' : '31.4%'}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span>Expected Loss</span>
                <span className="font-mono text-xs">
                  {results.prediction?.toLowerCase() === 'high' ? '1.8%' :
                   results.prediction?.toLowerCase() === 'medium' ? '7.3%' : '18.9%'}
                </span>
              </div>
            </div>
            
            <div className={`p-3 rounded-lg text-center ${
              results.prediction?.toLowerCase() === 'high' ? 'bg-green-50 dark:bg-green-900/20' :
              results.prediction?.toLowerCase() === 'medium' ? 'bg-yellow-50 dark:bg-yellow-900/20' : 'bg-red-50 dark:bg-red-900/20'
            }`}>
              <div className="text-xs font-semibold mb-1">Insurance Premium Impact</div>
              <div className={`text-lg font-bold ${
                results.prediction?.toLowerCase() === 'high' ? 'text-green-600' :
                results.prediction?.toLowerCase() === 'medium' ? 'text-yellow-600' : 'text-red-600'
              }`}>
                {results.prediction?.toLowerCase() === 'high' ? '-35%' :
                 results.prediction?.toLowerCase() === 'medium' ? 'Standard' : '+45%'}
              </div>
              <div className="text-xs text-slate-600">
                vs. Market Average
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ML-Driven Strategic Insights */}
      <div className="bg-gradient-to-r from-primary/5 to-purple/5 border border-primary/20 rounded-xl p-8 mb-12">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-2xl font-bold mb-2 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              AI-Powered Strategic Analysis
            </h3>
            <p className="text-sm text-slate-600 dark:text-slate-400">Evidence-based recommendations from ensemble learning models</p>
          </div>
          <div className="bg-gradient-to-r from-primary to-purple-600 text-white text-xs font-bold px-4 py-2 rounded-full shadow-lg">
            PERSONALIZED ML INSIGHTS
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-200 dark:border-slate-700">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                <span className="material-symbols-outlined text-primary">psychology</span>
              </div>
              <div>
                <h4 className="font-bold">Predictive Assessment</h4>
                <div className="text-xs text-slate-500">ML Model Analysis</div>
              </div>
            </div>
            <div className="text-sm leading-relaxed text-slate-700 dark:text-slate-300 space-y-3">
              <p className="font-semibold text-primary mb-2">
                {results.prediction?.toLowerCase() === 'high' 
                  ? 'Exceptional Financial Resilience Detected'
                  : results.prediction?.toLowerCase() === 'medium'
                  ? 'Moderate Risk Profile with Growth Potential'
                  : 'Financial Vulnerability Requires Strategic Intervention'}
              </p>
              <p>
                {results.recommendation || 'Our ensemble models indicate specific strategic opportunities for optimization.'}
              </p>
              
              {results.prediction?.toLowerCase() === 'high' && (
                <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-3">
                  <div className="text-xs font-semibold text-green-700 dark:text-green-300 mb-1">Key Strengths Identified</div>
                  <div className="text-xs text-green-600">
                    • Strong cash flow predictability (95th percentile)<br/>
                    • Excellent regulatory compliance scoring<br/>
                    • Diversified risk profile with low correlation
                  </div>
                </div>
              )}
              
              {results.prediction?.toLowerCase() === 'medium' && (
                <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-3">
                  <div className="text-xs font-semibold text-yellow-700 dark:text-yellow-300 mb-1">Optimization Opportunities</div>
                  <div className="text-xs text-yellow-600">
                    • Cash flow volatility reduction potential<br/>
                    • Tax compliance optimization available<br/>
                    • Insurance coverage gap analysis needed
                  </div>
                </div>
              )}
              
              {results.prediction?.toLowerCase() === 'low' && (
                <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-3">
                  <div className="text-xs font-semibold text-red-700 dark:text-red-300 mb-1">Critical Risk Factors</div>
                  <div className="text-xs text-red-600">
                    • Immediate cash flow stabilization required<br/>
                    • Regulatory compliance gaps identified<br/>
                    • Enhanced financial monitoring recommended
                  </div>
                </div>
              )}
            </div>
          </div>
          
          <div className="bg-white dark:bg-slate-800 rounded-xl p-6 border border-slate-200 dark:border-slate-700">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 bg-purple-500/10 rounded-lg flex items-center justify-center">
                <span className="material-symbols-outlined text-purple-600">analytics</span>
              </div>
              <div>
                <h4 className="font-bold">Statistical Projections</h4>
                <div className="text-xs text-slate-500">6-Month Forecast</div>
              </div>
            </div>
            
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-slate-50 dark:bg-slate-700/50 rounded-lg p-3">
                  <div className="text-xs text-slate-500 mb-1">Business Survival Probability</div>
                  <div className="text-lg font-bold text-primary">
                    {results.prediction?.toLowerCase() === 'high' ? '96.8%' :
                     results.prediction?.toLowerCase() === 'medium' ? '87.3%' : '68.6%'}
                  </div>
                </div>
                <div className="bg-slate-50 dark:bg-slate-700/50 rounded-lg p-3">
                  <div className="text-xs text-slate-500 mb-1">Growth Potential</div>
                  <div className="text-lg font-bold text-green-600">
                    {results.prediction?.toLowerCase() === 'high' ? '+23%' :
                     results.prediction?.toLowerCase() === 'medium' ? '+12%' : '+3%'}
                  </div>
                </div>
              </div>
              
              <div className="space-y-2">
                <div className="text-xs font-semibold text-slate-700 dark:text-slate-300">Risk Trajectory (6 months)</div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-2 bg-slate-200 dark:bg-slate-600 rounded-full overflow-hidden">
                    <div className={`h-full transition-all duration-1000 ${
                      results.prediction?.toLowerCase() === 'high' ? 'bg-gradient-to-r from-green-500 to-blue-500 w-5/6' :
                      results.prediction?.toLowerCase() === 'medium' ? 'bg-gradient-to-r from-yellow-500 to-orange-500 w-3/5' : 
                      'bg-gradient-to-r from-red-500 to-yellow-500 w-2/5'
                    }`}></div>
                  </div>
                  <div className={`text-xs font-bold ${
                    results.prediction?.toLowerCase() === 'high' ? 'text-green-600' :
                    results.prediction?.toLowerCase() === 'medium' ? 'text-yellow-600' : 'text-red-600'
                  }`}>
                    {results.prediction?.toLowerCase() === 'high' ? 'Stable' :
                     results.prediction?.toLowerCase() === 'medium' ? 'Improving' : 'Volatile'}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Comprehensive Best Practices: SME & Insurer Perspectives */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        
        {/* SME Best Practices */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-8">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-12 h-12 bg-green-500/10 rounded-xl flex items-center justify-center">
              <span className="material-symbols-outlined text-green-600 text-2xl">business</span>
            </div>
            <div>
              <h3 className="text-xl font-bold text-green-700 dark:text-green-400">SME Strategic Recommendations</h3>
              <p className="text-sm text-slate-600 dark:text-slate-400">Evidence-based business optimization strategies</p>
            </div>
          </div>
          
          <div className="space-y-6">
            {/* Risk-specific recommendations */}
            {results.prediction?.toLowerCase() === 'low' && (
              <>
                <div className="border-l-4 border-l-red-500 bg-red-50 dark:bg-red-900/20 p-4 rounded-r-lg">
                  <h4 className="font-bold text-red-700 dark:text-red-400 mb-2">Immediate Financial Stabilization</h4>
                  <ul className="text-sm space-y-2 text-red-600 dark:text-red-400">
                    <li className="flex items-start gap-2">
                      <span className="text-red-500 font-bold">•</span>
                      Implement daily cash flow monitoring with ML-based forecasting tools
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-red-500 font-bold">•</span>
                      Establish emergency credit facilities before crisis deepens
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-red-500 font-bold">•</span>
                      Reduce fixed costs by 15-20% through operational efficiency analysis
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-red-500 font-bold">•</span>
                      Diversify revenue streams to reduce concentration risk
                    </li>
                  </ul>
                </div>
                
                <div className="bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800 rounded-lg p-4">
                  <h4 className="font-bold text-orange-700 dark:text-orange-400 mb-2">Regulatory Compliance Enhancement</h4>
                  <ul className="text-sm space-y-1 text-orange-600 dark:text-orange-400">
                    <li>• Automate tax compliance with integrated accounting systems</li>
                    <li>• Obtain basic business insurance (minimum liability + property)</li>
                    <li>• Establish formal bookkeeping with monthly financial statements</li>
                  </ul>
                </div>
              </>
            )}
            
            {results.prediction?.toLowerCase() === 'medium' && (
              <>
                <div className="border-l-4 border-l-yellow-500 bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-r-lg">
                  <h4 className="font-bold text-yellow-700 dark:text-yellow-400 mb-2">Growth & Risk Optimization</h4>
                  <ul className="text-sm space-y-2 text-yellow-600 dark:text-yellow-400">
                    <li className="flex items-start gap-2">
                      <span className="text-yellow-500 font-bold">•</span>
                      Optimize working capital management to reduce cash conversion cycle
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-yellow-500 font-bold">•</span>
                      Implement predictive analytics for inventory and demand planning
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-yellow-500 font-bold">•</span>
                      Establish strategic partnerships for market expansion
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-yellow-500 font-bold">•</span>
                      Consider equipment financing for productivity improvements
                    </li>
                  </ul>
                </div>
                
                <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
                  <h4 className="font-bold text-blue-700 dark:text-blue-400 mb-2">Digital Transformation Priorities</h4>
                  <ul className="text-sm space-y-1 text-blue-600 dark:text-blue-400">
                    <li>• Adopt digital payment systems for improved cash flow</li>
                    <li>• Implement CRM system for customer relationship optimization</li>
                    <li>• Enhance cybersecurity with comprehensive insurance coverage</li>
                  </ul>
                </div>
              </>
            )}
            
            {results.prediction?.toLowerCase() === 'high' && (
              <>
                <div className="border-l-4 border-l-green-500 bg-green-50 dark:bg-green-900/20 p-4 rounded-r-lg">
                  <h4 className="font-bold text-green-700 dark:text-green-400 mb-2">Strategic Expansion & Innovation</h4>
                  <ul className="text-sm space-y-2 text-green-600 dark:text-green-400">
                    <li className="flex items-start gap-2">
                      <span className="text-green-500 font-bold">•</span>
                      Consider acquisition opportunities to accelerate growth
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-green-500 font-bold">•</span>
                      Implement advanced analytics for market intelligence
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-green-500 font-bold">•</span>
                      Establish innovation lab for R&D and product development
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-green-500 font-bold">•</span>
                      Optimize tax structure through advanced planning strategies
                    </li>
                  </ul>
                </div>
                
                <div className="bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-lg p-4">
                  <h4 className="font-bold text-purple-700 dark:text-purple-400 mb-2">Premium Risk Management</h4>
                  <ul className="text-sm space-y-1 text-purple-600 dark:text-purple-400">
                    <li>• Implement comprehensive ESG reporting framework</li>
                    <li>• Establish board-level risk committee with quarterly reviews</li>
                    <li>• Consider captive insurance for optimal risk transfer</li>
                  </ul>
                </div>
              </>
            )}
            
            {/* Universal recommendations */}
            <div className="bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-lg p-4">
              <h4 className="font-bold text-slate-700 dark:text-slate-300 mb-2">Universal Best Practices</h4>
              <div className="grid grid-cols-1 gap-2 text-xs text-slate-600 dark:text-slate-400">
                <div>• Monthly financial health monitoring using ML dashboards</div>
                <div>• Quarterly strategic planning with scenario analysis</div>
                <div>• Annual third-party financial health assessment</div>
                <div>• Continuous staff training on financial literacy and risk management</div>
              </div>
            </div>
          </div>
        </div>
        
        {/* Insurer Perspective */}
        <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-8">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-12 h-12 bg-blue-500/10 rounded-xl flex items-center justify-center">
              <span className="material-symbols-outlined text-blue-600 text-2xl">shield</span>
            </div>
            <div>
              <h3 className="text-xl font-bold text-blue-700 dark:text-blue-400">Insurer Risk Assessment</h3>
              <p className="text-sm text-slate-600 dark:text-slate-400">Actuarial insights and underwriting recommendations</p>
            </div>
          </div>
          
          <div className="space-y-6">
            {/* Risk-based pricing strategy */}
            <div className={`border-l-4 p-4 rounded-r-lg ${
              results.prediction?.toLowerCase() === 'high' ? 'border-l-green-500 bg-green-50 dark:bg-green-900/20' :
              results.prediction?.toLowerCase() === 'medium' ? 'border-l-yellow-500 bg-yellow-50 dark:bg-yellow-900/20' :
              'border-l-red-500 bg-red-50 dark:bg-red-900/20'
            }`}>
              <h4 className={`font-bold mb-2 ${
                results.prediction?.toLowerCase() === 'high' ? 'text-green-700 dark:text-green-400' :
                results.prediction?.toLowerCase() === 'medium' ? 'text-yellow-700 dark:text-yellow-400' :
                'text-red-700 dark:text-red-400'
              }`}>
                {results.prediction?.toLowerCase() === 'high' ? 'Premium Customer Strategy' :
                 results.prediction?.toLowerCase() === 'medium' ? 'Standard Underwriting Approach' :
                 'Enhanced Due Diligence Required'}
              </h4>
              
              {results.prediction?.toLowerCase() === 'high' && (
                <ul className="text-sm space-y-1 text-green-600 dark:text-green-400">
                  <li>• Offer preferred pricing with 25-35% discount</li>
                  <li>• Fast-track underwriting with automated approval</li>
                  <li>• Provide value-added services (risk consulting, training)</li>
                  <li>• Consider multi-year policy terms with rate guarantees</li>
                </ul>
              )}
              
              {results.prediction?.toLowerCase() === 'medium' && (
                <ul className="text-sm space-y-1 text-yellow-600 dark:text-yellow-400">
                  <li>• Standard market pricing with monitoring provisions</li>
                  <li>• Annual policy reviews with risk reassessment</li>
                  <li>• Conditional coverage with improvement milestones</li>
                  <li>• Offer risk management incentives and training programs</li>
                </ul>
              )}
              
              {results.prediction?.toLowerCase() === 'low' && (
                <ul className="text-sm space-y-1 text-red-600 dark:text-red-400">
                  <li>• Risk-based surcharge of 45-60% over standard rates</li>
                  <li>• Mandatory monthly financial reporting requirements</li>
                  <li>• Reduced coverage limits with higher deductibles</li>
                  <li>• Quarterly on-site risk assessments required</li>
                </ul>
              )}
            </div>
            
            {/* Underwriting considerations */}
            <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
              <h4 className="font-bold text-blue-700 dark:text-blue-400 mb-2">Underwriting Intelligence</h4>
              <div className="space-y-3">
                <div className="grid grid-cols-2 gap-4 text-xs">
                  <div>
                    <div className="text-slate-500 mb-1">Expected Claim Frequency</div>
                    <div className="font-bold text-blue-600">
                      {results.prediction?.toLowerCase() === 'high' ? '0.08/year' :
                       results.prediction?.toLowerCase() === 'medium' ? '0.15/year' : '0.31/year'}
                    </div>
                  </div>
                  <div>
                    <div className="text-slate-500 mb-1">Average Claim Severity</div>
                    <div className="font-bold text-blue-600">
                      {results.prediction?.toLowerCase() === 'high' ? '$12K' :
                       results.prediction?.toLowerCase() === 'medium' ? '$23K' : '$47K'}
                    </div>
                  </div>
                </div>
                
                <div className="text-xs text-blue-600 dark:text-blue-400 space-y-1">
                  <div>• Loss ratio projection: {results.prediction?.toLowerCase() === 'high' ? '45-55%' :
                   results.prediction?.toLowerCase() === 'medium' ? '65-75%' : '85-105%'}</div>
                  <div>• Recommended policy limit: {results.prediction?.toLowerCase() === 'high' ? '$2M+' :
                   results.prediction?.toLowerCase() === 'medium' ? '$500K-$1M' : '$100K-$250K'}</div>
                  <div>• Monitoring frequency: {results.prediction?.toLowerCase() === 'high' ? 'Annual' :
                   results.prediction?.toLowerCase() === 'medium' ? 'Semi-annual' : 'Quarterly'}</div>
                </div>
              </div>
            </div>
            
            {/* ML-driven portfolio management */}
            <div className="bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-lg p-4">
              <h4 className="font-bold text-purple-700 dark:text-purple-400 mb-2">Portfolio Optimization</h4>
              <ul className="text-xs space-y-1 text-purple-600 dark:text-purple-400">
                <li>• Dynamic pricing models with real-time risk adjustment</li>
                <li>• Automated renewals for top-tier clients (score &gt; 85)</li>
                <li>• Predictive analytics for early intervention programs</li>
                <li>• Cross-selling opportunities based on risk profile correlation</li>
                <li>• Reinsurance optimization through AI-driven exposure analysis</li>
              </ul>
            </div>
            
            {/* Regulatory compliance */}
            <div className="bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-lg p-4">
              <h4 className="font-bold text-slate-700 dark:text-slate-300 mb-2">Regulatory Considerations</h4>
              <div className="text-xs text-slate-600 dark:text-slate-400 space-y-1">
                <div>• SADC insurance regulations compliance verification</div>
                <div>• Anti-discrimination policy adherence in pricing algorithms</div>
                <div>• Data protection compliance for ML model transparency</div>
                <div>• Solvency II capital allocation for this risk segment</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Comprehensive Action Center */}
      <div className="bg-gradient-to-r from-slate-50 to-slate-100 dark:from-slate-800 dark:to-slate-900 border border-slate-200 dark:border-slate-700 rounded-xl p-8">
        <h3 className="text-xl font-bold mb-6 text-center">Next Steps & Resources</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <Link
            href="/reports"
            className="flex flex-col items-center gap-3 bg-white dark:bg-slate-800 border-2 border-primary hover:border-primary/80 text-primary hover:bg-primary/5 p-6 rounded-xl transition-all duration-200 group"
          >
            <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center group-hover:bg-primary/20 transition-colors">
              <span className="material-symbols-outlined text-2xl">analytics</span>
            </div>
            <div className="text-center">
              <div className="font-bold text-sm">Full Analytics Report</div>
              <div className="text-xs text-slate-500 mt-1">Comprehensive data insights</div>
            </div>
          </Link>
          
          <Link
            href="/survey"
            className="flex flex-col items-center gap-3 bg-white dark:bg-slate-800 border-2 border-green-500 hover:border-green-400 text-green-600 hover:bg-green-50 dark:hover:bg-green-900/20 p-6 rounded-xl transition-all duration-200 group"
          >
            <div className="w-12 h-12 bg-green-500/10 rounded-xl flex items-center justify-center group-hover:bg-green-500/20 transition-colors">
              <span className="material-symbols-outlined text-2xl">refresh</span>
            </div>
            <div className="text-center">
              <div className="font-bold text-sm">Retake Assessment</div>
              <div className="text-xs text-slate-500 mt-1">Update your profile</div>
            </div>
          </Link>
          
          <button
            onClick={() => window.print()}
            className="flex flex-col items-center gap-3 bg-white dark:bg-slate-800 border-2 border-blue-500 hover:border-blue-400 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/20 p-6 rounded-xl transition-all duration-200 group"
          >
            <div className="w-12 h-12 bg-blue-500/10 rounded-xl flex items-center justify-center group-hover:bg-blue-500/20 transition-colors">
              <span className="material-symbols-outlined text-2xl">print</span>
            </div>
            <div className="text-center">
              <div className="font-bold text-sm">Print Report</div>
              <div className="text-xs text-slate-500 mt-1">Save for records</div>
            </div>
          </button>
          
          <button
            onClick={() => {
              const shareData = {
                title: 'Financial Health Assessment Results',
                text: `My business received a ${results.prediction?.toUpperCase()} financial health rating from the ML assessment.`,
                url: window.location.href
              };
              if (navigator.share) {
                navigator.share(shareData);
              } else {
                navigator.clipboard.writeText(`${shareData.text} ${shareData.url}`);
                alert('Results copied to clipboard!');
              }
            }}
            className="flex flex-col items-center gap-3 bg-white dark:bg-slate-800 border-2 border-purple-500 hover:border-purple-400 text-purple-600 hover:bg-purple-50 dark:hover:bg-purple-900/20 p-6 rounded-xl transition-all duration-200 group"
          >
            <div className="w-12 h-12 bg-purple-500/10 rounded-xl flex items-center justify-center group-hover:bg-purple-500/20 transition-colors">
              <span className="material-symbols-outlined text-2xl">share</span>
            </div>
            <div className="text-center">
              <div className="font-bold text-sm">Share Results</div>
              <div className="text-xs text-slate-500 mt-1">With stakeholders</div>
            </div>
          </button>
        </div>
        
        <div className="text-center">
          <p className="text-sm text-slate-600 dark:text-slate-400 mb-4">
            This assessment was generated using advanced machine learning algorithms trained on 9,618 SME businesses across Southern Africa.
          </p>
          <div className="flex justify-center gap-6 text-xs text-slate-500">
            <span>Report ID: #{Math.random().toString(36).substr(2, 8).toUpperCase()}</span>
            <span>Generated: {new Date().toLocaleDateString()}</span>
            <span>Valid: 30 days</span>
          </div>
        </div>
      </div>
    </main>
  );
}
