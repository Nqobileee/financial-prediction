import Link from "next/link";

export default function ResultsPage() {
  return (
    <main className="pt-24 pb-32 px-4 max-w-md mx-auto">
      {/* Header & Category Badge */}
      <div className="text-center mb-8">
        <p className="text-primary text-xs font-bold tracking-widest uppercase mb-2">Analysis Complete</p>
        <h1 className="text-3xl font-bold mb-4">Survey Results</h1>
        <div className="inline-flex items-center gap-2 bg-success-glow/10 border border-success-glow/30 px-4 py-2 rounded-full">
          <div className="w-2 h-2 rounded-full bg-success-glow animate-pulse"></div>
          <span className="text-success-glow font-bold tracking-tight glow-text">Financial Health: HIGH</span>
        </div>
      </div>

      {/* Radar Chart Visualization */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 mb-6">
        <div className="flex justify-between items-center mb-6">
          <h3 className="font-bold text-sm tracking-tight text-slate-500 uppercase">Metric Radar</h3>
          <span className="material-symbols-outlined text-primary">query_stats</span>
        </div>
        <div className="relative flex items-center justify-center py-4">
          {/* SVG Radar Chart */}
          <svg className="w-full max-w-[240px]" viewBox="0 0 200 200">
            {/* Background Webs */}
            <circle className="text-slate-200" cx="100" cy="100" fill="none" r="80" stroke="currentColor" strokeWidth="0.5"></circle>
            <circle className="text-slate-200" cx="100" cy="100" fill="none" r="60" stroke="currentColor" strokeWidth="0.5"></circle>
            <circle className="text-slate-200" cx="100" cy="100" fill="none" r="40" stroke="currentColor" strokeWidth="0.5"></circle>
            {/* Axes */}
            <line className="text-slate-200" stroke="currentColor" strokeWidth="0.5" x1="100" x2="100" y1="20" y2="100"></line>
            <line className="text-slate-200" stroke="currentColor" strokeWidth="0.5" x1="100" x2="170" y1="100" y2="140"></line>
            <line className="text-slate-200" stroke="currentColor" strokeWidth="0.5" x1="100" x2="30" y1="100" y2="140"></line>
            {/* Data Shape */}
            <path d="M100 35 L160 130 L45 125 Z" fill="rgba(0, 191, 255, 0.15)" stroke="#00bfff" strokeWidth="2"></path>
            {/* Labels */}
            <text fill="currentColor" fontSize="10" fontWeight="700" textAnchor="middle" x="100" y="15">GROWTH</text>
            <text fill="currentColor" fontSize="10" fontWeight="700" textAnchor="middle" x="175" y="150">SOLVENCY</text>
            <text fill="currentColor" fontSize="10" fontWeight="700" textAnchor="middle" x="25" y="150">LIQUIDITY</text>
          </svg>
        </div>
        <div className="grid grid-cols-3 gap-2 mt-4 text-center">
          <div className="p-2">
            <p className="text-[10px] text-slate-500 uppercase">Growth</p>
            <p className="font-bold text-primary">82%</p>
          </div>
          <div className="p-2 border-x border-slate-100 dark:border-slate-800">
            <p className="text-[10px] text-slate-500 uppercase">Solvency</p>
            <p className="font-bold text-primary">91%</p>
          </div>
          <div className="p-2">
            <p className="text-[10px] text-slate-500 uppercase">Liquidity</p>
            <p className="font-bold text-primary">76%</p>
          </div>
        </div>
      </div>

      {/* Model Confidence */}
      <div className="bg-primary/5 border border-primary/20 rounded-xl p-6 mb-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="font-bold text-lg leading-tight">Model Confidence</h3>
            <p className="text-xs text-slate-500 mt-1">Verification: Active Stream</p>
          </div>
          <div className="bg-primary text-white text-xs font-bold px-2 py-1 rounded glow-border">
            87% ACCURACY
          </div>
        </div>
        <p className="text-xs leading-relaxed text-slate-600 dark:text-slate-400 font-mono">
          The prediction logic utilizes a gradient-boosted ensemble method (XGBoost) trained on 50k+ SME fiscal datasets. Current health rating is validated against real-time liquidity benchmarks and industry-specific solvency ratios.
        </p>
      </div>

      {/* Action Cards Section */}
      <div className="space-y-4 mb-8">
        {/* SME Card */}
        <div className="bg-white dark:bg-slate-900 border-l-4 border-l-primary border border-slate-200 dark:border-slate-800 rounded-lg p-5">
          <div className="flex items-center gap-2 mb-3">
            <span className="material-symbols-outlined text-primary text-xl">trending_up</span>
            <h4 className="font-bold">Growth Tips for You</h4>
          </div>
          <ul className="text-sm space-y-2 text-slate-600 dark:text-slate-400">
            <li className="flex items-start gap-2">
              <span className="text-primary font-bold">•</span> Optimize accounts receivable to boost liquidity.
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary font-bold">•</span> Leverage solvency rating for lower interest rates.
            </li>
          </ul>
        </div>

        {/* Insurer Card */}
        <div className="bg-white dark:bg-slate-900 border-l-4 border-l-success-glow border border-slate-200 dark:border-slate-800 rounded-lg p-5">
          <div className="flex items-center gap-2 mb-3">
            <span className="material-symbols-outlined text-success-glow text-xl">verified_user</span>
            <h4 className="font-bold">Insurer Risk Profile</h4>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-xs bg-success-glow/10 text-success-glow px-2 py-1 rounded font-bold uppercase">Low Risk Indicator</span>
            <span className="text-xs text-slate-500">Stable Debt-to-Equity</span>
          </div>
          <p className="text-sm mt-3 text-slate-600 dark:text-slate-400">
            Your profile shows strong resilience against market volatility. Share this to reduce premiums.
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
        <button className="flex-1 flex items-center justify-center gap-2 bg-primary text-white font-bold py-3 rounded-xl shadow-lg shadow-primary/20 hover:bg-primary/90 transition-colors">
          <span className="material-symbols-outlined text-lg">share</span>
          <span className="text-sm">SHARE INSURER</span>
        </button>
      </div>
    </main>
  );
}
