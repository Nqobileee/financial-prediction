"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function SurveyPage() {
  const router = useRouter();
  const [currentStep] = useState(3);
  const totalSteps = 10;
  const progress = (currentStep / totalSteps) * 100;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    router.push("/results");
  };

  return (
    <>
      {/* TopAppBar & ProgressBar Combined */}
      <header className="sticky top-0 z-50 glass-header bg-background-light/80 dark:bg-background-dark/80 border-b border-gray-200 dark:border-gray-800">
        <div className="h-1 w-full bg-gray-200 dark:bg-gray-800">
          <div className="h-full bg-primary transition-all" style={{ width: `${progress}%` }}></div>
        </div>
        <div className="flex items-center justify-between px-4 py-3">
          <Link href="/" className="flex items-center justify-center p-1 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800">
            <span className="material-symbols-outlined text-2xl">close</span>
          </Link>
          <div className="text-center">
            <h2 className="text-sm font-bold tracking-tight uppercase opacity-60">FinHealth Survey</h2>
            <p className="text-[10px] font-medium tracking-widest text-primary">STEP 0{currentStep} OF {totalSteps}</p>
          </div>
          <div className="w-8 flex justify-end">
            <span className="material-symbols-outlined text-primary neon-accent">analytics</span>
          </div>
        </div>
      </header>

      <main className="flex-1 px-4 py-6 max-w-2xl mx-auto w-full pb-32">
        {/* Progress Indicator Text */}
        <div className="mb-6">
          <p className="text-xs font-semibold text-primary uppercase tracking-[0.2em] mb-1">Financial Health Survey</p>
          <h1 className="text-2xl font-bold leading-tight tracking-tight">Business Risk Assessment</h1>
        </div>

        <form id="surveyForm" className="space-y-6" onSubmit={handleSubmit}>
          {/* Section 1: Demographics & Business Profile */}
          <div className="bg-card-light dark:bg-card-dark border border-gray-200 dark:border-gray-800 rounded-xl p-5 shadow-sm">
            <h2 className="text-xl font-bold mb-4 text-primary">Section 1: Demographics & Business Profile</h2>

            {/* Q1: Country */}
            <div className="mb-6">
              <label className="text-sm font-bold mb-3 block">1. Country</label>
              <div className="space-y-2">
                {["Eswatini", "Lesotho", "Malawi", "Zimbabwe"].map((country) => (
                  <label key={country} className="flex items-center gap-3 p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary/50 cursor-pointer">
                    <input type="radio" name="country" value={country.toLowerCase()} className="text-primary focus:ring-primary" />
                    <span>{country}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Q2: Owner Age */}
            <div className="mb-6">
              <label className="text-sm font-bold mb-3 block">2. Owner Age</label>
              <input type="number" name="owner_age" placeholder="Enter age" className="w-full glow-border rounded-lg border border-gray-200 dark:border-gray-700 bg-background-light dark:bg-zinc-900 p-4 text-lg" />
            </div>

            {/* Q3: Owner Sex */}
            <div className="mb-6">
              <label className="text-sm font-bold mb-3 block">3. Owner Sex</label>
              <div className="grid grid-cols-2 gap-3">
                {["Female", "Male"].map((sex) => (
                  <label key={sex} className="flex items-center justify-center gap-3 p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary/50 cursor-pointer">
                    <input type="radio" name="owner_sex" value={sex} className="text-primary focus:ring-primary" />
                    <span>{sex}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Q4: Business Age */}
            <div className="mb-6">
              <label className="text-sm font-bold mb-3 block">4. Business Age</label>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-xs uppercase tracking-wider opacity-60 mb-2 block">Years</label>
                  <input type="number" name="business_age_years" placeholder="0" className="w-full glow-border rounded-lg border border-gray-200 dark:border-gray-700 bg-background-light dark:bg-zinc-900 p-3" />
                </div>
                <div>
                  <label className="text-xs uppercase tracking-wider opacity-60 mb-2 block">Months</label>
                  <input type="number" name="business_age_months" placeholder="0" className="w-full glow-border rounded-lg border border-gray-200 dark:border-gray-700 bg-background-light dark:bg-zinc-900 p-3" />
                </div>
              </div>
            </div>

            {/* Q5: COVID Essential Service */}
            <div className="mb-6">
              <label className="text-sm font-bold mb-3 block">5. COVID Essential Service</label>
              <div className="space-y-2">
                {["Yes", "No", "Don't know"].map((option) => (
                  <label key={option} className="flex items-center gap-3 p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary/50 cursor-pointer">
                    <input type="radio" name="covid_essential_service" value={option} className="text-primary focus:ring-primary" />
                    <span>{option}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>

          {/* Section 2: Financial Information */}
          <div className="bg-card-light dark:bg-card-dark border border-gray-200 dark:border-gray-800 rounded-xl p-5 shadow-sm">
            <h2 className="text-xl font-bold mb-4 text-primary">Section 2: Financial Information</h2>

            {/* Q6: Personal Income */}
            <div className="mb-6">
              <label className="text-sm font-bold mb-3 block">6. Personal Income</label>
              <div className="relative flex items-center glow-border rounded-lg border border-gray-200 dark:border-gray-700 bg-background-light dark:bg-zinc-900">
                <input type="number" name="personal_income" placeholder="Enter amount" className="w-full bg-transparent border-none focus:ring-0 p-4 text-lg" />
                <span className="material-symbols-outlined text-primary pr-4">payments</span>
              </div>
            </div>

            {/* Q7: Business Expenses */}
            <div className="mb-6">
              <label className="text-sm font-bold mb-3 block">7. Business Expenses</label>
              <div className="relative flex items-center glow-border rounded-lg border border-gray-200 dark:border-gray-700 bg-background-light dark:bg-zinc-900">
                <input type="number" name="business_expenses" placeholder="Enter amount" className="w-full bg-transparent border-none focus:ring-0 p-4 text-lg" />
                <span className="material-symbols-outlined text-primary pr-4">receipt_long</span>
              </div>
            </div>

            {/* Q8: Business Turnover */}
            <div className="mb-6">
              <label className="text-sm font-bold mb-3 block">8. Business Turnover</label>
              <div className="relative flex items-center glow-border rounded-lg border border-gray-200 dark:border-gray-700 bg-background-light dark:bg-zinc-900">
                <input type="number" name="business_turnover" placeholder="Enter amount" className="w-full bg-transparent border-none focus:ring-0 p-4 text-lg" />
                <span className="material-symbols-outlined text-primary pr-4">trending_up</span>
              </div>
            </div>

            {/* Q9: Keeps Financial Records */}
            <div className="mb-6">
              <label className="text-sm font-bold mb-3 block">9. Keeps Financial Records</label>
              <div className="space-y-2">
                {["Yes, always", "Yes, sometimes", "No"].map((option) => (
                  <label key={option} className="flex items-center gap-3 p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary/50 cursor-pointer">
                    <input type="radio" name="keeps_financial_records" value={option} className="text-primary focus:ring-primary" />
                    <span>{option}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Q10: Has Mobile Money */}
            <div className="mb-6">
              <label className="text-sm font-bold mb-3 block">10. Has Mobile Money</label>
              <div className="space-y-2">
                {["Have now", "Used to have but don't have now", "Never had"].map((option) => (
                  <label key={option} className="flex items-center gap-3 p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary/50 cursor-pointer">
                    <input type="radio" name="has_mobile_money" value={option} className="text-primary focus:ring-primary" />
                    <span>{option}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>

          {/* Section 3: Insurance & Risk */}
          <div className="bg-card-light dark:bg-card-dark border border-gray-200 dark:border-gray-800 rounded-xl p-5 shadow-sm">
            <h2 className="text-xl font-bold mb-4 text-primary">Section 3: Insurance & Risk</h2>

            {/* Q15: Has Business Insurance */}
            <div className="mb-6">
              <label className="text-sm font-bold mb-3 block">11. Has Business Insurance</label>
              <div className="grid grid-cols-2 gap-3">
                {["Yes", "No"].map((option) => (
                  <label key={option} className="flex items-center justify-center gap-3 p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary/50 cursor-pointer">
                    <input type="radio" name="has_insurance" value={option} className="text-primary focus:ring-primary" />
                    <span>{option}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Q17: Future Risk Theft Stock */}
            <div className="mb-6">
              <label className="text-sm font-bold mb-3 block">12. Future Risk: Theft of Stock</label>
              <div className="grid grid-cols-2 gap-3">
                {["Yes", "No"].map((option) => (
                  <label key={option} className="flex items-center justify-center gap-3 p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary/50 cursor-pointer">
                    <input type="radio" name="future_risk_theft_stock" value={option} className="text-primary focus:ring-primary" />
                    <span>{option}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>

          {/* Section 4: Attitudes & Compliance */}
          <div className="bg-card-light dark:bg-card-dark border border-gray-200 dark:border-gray-800 rounded-xl p-5 shadow-sm">
            <h2 className="text-xl font-bold mb-4 text-primary">Section 4: Attitudes & Compliance</h2>

            {/* Q18: Attitude Stable Business Environment */}
            <div className="mb-6">
              <label className="text-sm font-bold mb-3 block">13. Attitude: Stable Business Environment</label>
              <div className="space-y-2">
                {["Yes", "No", "Don't know or N/A"].map((option) => (
                  <label key={option} className="flex items-center gap-3 p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary/50 cursor-pointer">
                    <input type="radio" name="attitude_stable_business_environment" value={option} className="text-primary focus:ring-primary" />
                    <span>{option}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Q22: Compliance Income Tax */}
            <div className="mb-6">
              <label className="text-sm font-bold mb-3 block">14. Compliance: Income Tax</label>
              <div className="space-y-2">
                {["Yes", "No", "Don't know"].map((option) => (
                  <label key={option} className="flex items-center gap-3 p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary/50 cursor-pointer">
                    <input type="radio" name="compliance_income_tax" value={option} className="text-primary focus:ring-primary" />
                    <span>{option}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>

          {/* Section 5: Operations */}
          <div className="bg-card-light dark:bg-card-dark border border-gray-200 dark:border-gray-800 rounded-xl p-5 shadow-sm">
            <h2 className="text-xl font-bold mb-4 text-primary">Section 5: Operations</h2>

            {/* Q23: Has Cellphone */}
            <div className="mb-6">
              <label className="text-sm font-bold mb-3 block">15. Has Cellphone</label>
              <div className="grid grid-cols-2 gap-3">
                {["Yes", "No"].map((option) => (
                  <label key={option} className="flex items-center justify-center gap-3 p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary/50 cursor-pointer">
                    <input type="radio" name="has_cellphone" value={option} className="text-primary focus:ring-primary" />
                    <span>{option}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Q26: Motivation Make More Money */}
            <div className="mb-6">
              <label className="text-sm font-bold mb-3 block">16. Motivation: Make More Money</label>
              <div className="grid grid-cols-2 gap-3">
                {["Yes", "No"].map((option) => (
                  <label key={option} className="flex items-center justify-center gap-3 p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-primary/50 cursor-pointer">
                    <input type="radio" name="motivation_make_more_money" value={option} className="text-primary focus:ring-primary" />
                    <span>{option}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>

          {/* Model Insight Box */}
          <div className="mt-6 p-4 bg-gray-50 dark:bg-zinc-800/50 rounded-lg border-l-2 border-primary">
            <div className="flex items-center gap-2 mb-2">
              <span className="material-symbols-outlined text-primary text-sm">monitoring</span>
              <span className="text-[10px] font-bold uppercase tracking-widest text-primary">Model Insight</span>
            </div>
            <p className="text-sm font-normal text-gray-600 dark:text-gray-400 leading-relaxed">
              Your responses will help us assess your business financial health and risk profile. This survey contains <span className="text-primary font-bold">16 questions</span> across 5 categories.
            </p>
            <div className="mt-2 flex gap-1">
              <div className="w-1 h-1 bg-primary rounded-full animate-pulse"></div>
              <div className="w-1 h-1 bg-primary/40 rounded-full"></div>
              <div className="w-1 h-1 bg-primary/20 rounded-full"></div>
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            className="w-full bg-primary text-white h-14 rounded-xl font-bold text-lg glow-cyan flex items-center justify-center gap-2 hover:bg-primary/90 transition-colors mt-8"
          >
            Submit Survey
            <span className="material-symbols-outlined">send</span>
          </button>
        </form>
      </main>
    </>
  );
}
