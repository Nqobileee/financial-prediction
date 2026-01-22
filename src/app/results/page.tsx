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
      <main className="pt-24 pb-32 px-4 max-w-md mx-auto flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-2 border-primary border-t-transparent"></div>
      </main>
    );
  }

  if (!results) {
    return (
      <main className="pt-24 pb-32 px-4 max-w-md mx-auto">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">No Results Found</h1>
          <p className="text-gray-600 mb-6">Please complete the survey first.</p>
          <Link href="/survey" className="bg-primary text-white px-6 py-3 rounded-xl font-bold">
            Take Survey
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
    <main className="pt-24 pb-32 px-4 max-w-md mx-auto">
      {/* Header & Category Badge */}
      <div className="text-center mb-8">
        <p className="text-primary text-xs font-bold tracking-widest uppercase mb-2">Analysis Complete</p>
        <h1 className="text-3xl font-bold mb-4">Survey Results</h1>
        <div className={`inline-flex items-center gap-2 ${getHealthGlow(results.prediction)} px-4 py-2 rounded-full`}>
          <div className={`w-2 h-2 rounded-full ${getHealthColor(results.prediction)} animate-pulse`}></div>
          <span className={`${getHealthColor(results.prediction)} font-bold tracking-tight`}>
            Financial Health: {results.prediction?.toUpperCase()}
          </span>
        </div>
      </div>

      {/* Confidence Scores */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 mb-6">
        <div className="flex justify-between items-center mb-6">
          <h3 className="font-bold text-sm tracking-tight text-slate-500 uppercase">Confidence Scores</h3>
          <span className="material-symbols-outlined text-primary">query_stats</span>
        </div>
        
        <div className="space-y-4">
          {Object.entries(results.confidence_scores || {}).map(([category, score]) => {
            const percentage = Math.round((score as number) * 100);
            return (
              <div key={category} className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-sm font-medium capitalize">{category}</span>
                  <span className="text-sm font-bold text-primary">{percentage}%</span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div 
                    className="bg-primary h-2 rounded-full transition-all duration-500"
                    style={{ width: `${percentage}%` }}
                  ></div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Recommendation */}
      <div className="bg-primary/5 border border-primary/20 rounded-xl p-6 mb-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="font-bold text-lg leading-tight">AI Recommendation</h3>
            <p className="text-xs text-slate-500 mt-1">Based on Survey Analysis</p>
          </div>
          <div className="bg-primary text-white text-xs font-bold px-2 py-1 rounded glow-border">
            PERSONALIZED
          </div>
        </div>
        <p className="text-sm leading-relaxed text-slate-600 dark:text-slate-400">
          {results.recommendation || 'Continue monitoring your financial health and maintain good business practices.'}
        </p>
      </div>

      {/* Action Cards Section */}
      <div className="space-y-4 mb-8">
        {/* Financial Tips Card */}
        <div className="bg-white dark:bg-slate-900 border-l-4 border-l-primary border border-slate-200 dark:border-slate-800 rounded-lg p-5">
          <div className="flex items-center gap-2 mb-3">
            <span className="material-symbols-outlined text-primary text-xl">trending_up</span>
            <h4 className="font-bold">Improvement Areas</h4>
          </div>
          <ul className="text-sm space-y-2 text-slate-600 dark:text-slate-400">
            {results.prediction?.toLowerCase() === 'low' && (
              <>
                <li className="flex items-start gap-2">
                  <span className="text-primary font-bold">•</span> Focus on increasing revenue streams and reducing expenses
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary font-bold">•</span> Improve financial record keeping for better tracking
                </li>
              </>
            )}
            {results.prediction?.toLowerCase() === 'medium' && (
              <>
                <li className="flex items-start gap-2">
                  <span className="text-primary font-bold">•</span> Optimize cash flow management
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary font-bold">•</span> Consider business insurance for risk mitigation
                </li>
              </>
            )}
            {results.prediction?.toLowerCase() === 'high' && (
              <>
                <li className="flex items-start gap-2">
                  <span className="text-primary font-bold">•</span> Maintain current financial practices
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary font-bold">•</span> Consider expansion opportunities
                </li>
              </>
            )}
          </ul>
        </div>

        {/* Risk Assessment Card */}
        <div className={`bg-white dark:bg-slate-900 border-l-4 ${
          results.prediction?.toLowerCase() === 'high' ? 'border-l-green-500' :
          results.prediction?.toLowerCase() === 'medium' ? 'border-l-yellow-500' : 'border-l-red-500'
        } border border-slate-200 dark:border-slate-800 rounded-lg p-5`}>
          <div className="flex items-center gap-2 mb-3">
            <span className="material-symbols-outlined text-xl">verified_user</span>
            <h4 className="font-bold">Risk Profile</h4>
          </div>
          <div className="flex items-center justify-between">
            <span className={`text-xs px-2 py-1 rounded font-bold uppercase ${
              results.prediction?.toLowerCase() === 'high' ? 'bg-green-500/10 text-green-600' :
              results.prediction?.toLowerCase() === 'medium' ? 'bg-yellow-500/10 text-yellow-600' : 'bg-red-500/10 text-red-600'
            }`}>
              {results.prediction?.toLowerCase() === 'high' ? 'Low Risk' :
               results.prediction?.toLowerCase() === 'medium' ? 'Medium Risk' : 'High Risk'} Profile
            </span>
          </div>
          <p className="text-sm mt-3 text-slate-600 dark:text-slate-400">
            {results.prediction?.toLowerCase() === 'high' 
              ? 'Your business shows strong financial stability and low risk indicators.'
              : results.prediction?.toLowerCase() === 'medium'
              ? 'Your business shows moderate risk with room for improvement.'
              : 'Your business may benefit from additional financial planning and risk management.'}
          </p>
        </div>
      </div>

      {/* Floating Actions */}
      <div className="fixed bottom-0 left-0 right-0 p-4 bg-background-light/80 dark:bg-background-dark/80 backdrop-blur-md flex gap-3 z-50">
        <Link
          href="/reports"
          className="flex-1 flex items-center justify-center gap-2 border-2 border-primary text-primary font-bold py-3 rounded-xl glow-border hover:bg-primary/5 transition-colors"
        >
          <span className="material-symbols-outlined text-lg">download</span>
          <span className="text-sm">FULL REPORT</span>
        </Link>
        <Link
          href="/survey"
          className="flex-1 flex items-center justify-center gap-2 bg-primary text-white font-bold py-3 rounded-xl shadow-lg shadow-primary/20 hover:bg-primary/90 transition-colors"
        >
          <span className="material-symbols-outlined text-lg">refresh</span>
          <span className="text-sm">NEW SURVEY</span>
        </Link>
      </div>
    </main>
  );
}
