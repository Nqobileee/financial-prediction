import Link from "next/link";

export default function Home() {
  return (
    <main className="pt-24 pb-20 space-y-12 overflow-x-hidden">
      {/* HeroSection */}
      <section className="px-4">
        <div className="relative overflow-hidden bg-card-light dark:bg-card-dark rounded-3xl border border-slate-200 dark:border-slate-800 p-6 code-bg">
          <div className="relative z-10 flex flex-col gap-6">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary w-fit">
              <span className="material-symbols-outlined text-sm">rocket_launch</span>
              <span className="text-xs font-bold uppercase tracking-tighter">Next-Gen Predictive Engine</span>
            </div>
            <h1 className="text-4xl md:text-5xl font-bold leading-[1.1] tracking-tight">
              Financial Prediction for <span className="text-primary">African SMEs</span>
            </h1>
            <p className="text-slate-600 dark:text-slate-400 text-base leading-relaxed max-w-md">
              Harnessing a question-based model to predict financial health for the next generation of African enterprises.
            </p>
            {/* Dashboard Preview (Mini-Bento) */}
            <div className="grid grid-cols-2 gap-3 py-4">
              <div className="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
                <p className="text-[10px] uppercase tracking-widest text-slate-500 font-bold mb-1">Health Score</p>
                <div className="flex items-end gap-1">
                  <span className="text-2xl font-bold">84</span>
                  <span className="text-accent-green text-xs font-bold mb-1 flex items-center">
                    <span className="material-symbols-outlined text-xs">arrow_upward</span>5%
                  </span>
                </div>
              </div>
              <div className="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
                <p className="text-[10px] uppercase tracking-widest text-slate-500 font-bold mb-1">Risk Status</p>
                <span className="inline-block px-2 py-0.5 rounded bg-accent-green/20 text-accent-green text-[10px] font-bold">STABLE</span>
              </div>
            </div>
            <Link
              href="/survey"
              className="bg-primary text-white h-14 rounded-xl font-bold text-lg glow-cyan flex items-center justify-center gap-2 group hover:bg-primary/90 transition-colors"
            >
              Get Started
              <span className="material-symbols-outlined group-hover:translate-x-1 transition-transform">chevron_right</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Model Performance Section */}
      <section className="space-y-6">
        <div className="px-4">
          <h2 className="text-2xl font-bold tracking-tight">Model Performance</h2>
          <p className="text-sm text-slate-500">Live accuracy metrics &amp; predictive modeling</p>
        </div>
        {/* Stats Components */}
        <div className="flex flex-wrap gap-4 px-4">
          <div className="flex flex-1 flex-col gap-2 rounded-2xl p-5 bg-primary/5 border border-primary/10">
            <p className="text-slate-500 text-xs font-bold uppercase tracking-widest">Model Accuracy</p>
            <div className="flex items-center gap-3">
              <p className="text-primary tracking-tighter text-3xl font-bold leading-tight">87%</p>
              <span className="text-accent-green text-sm font-bold bg-accent-green/10 px-2 py-1 rounded">+12%</span>
            </div>
          </div>
          <div className="flex flex-1 flex-col gap-2 rounded-2xl p-5 bg-primary/5 border border-primary/10">
            <p className="text-slate-500 text-xs font-bold uppercase tracking-widest">Latency</p>
            <div className="flex items-center gap-3">
              <p className="text-slate-900 dark:text-white tracking-tighter text-3xl font-bold leading-tight">&lt;2s</p>
              <span className="material-symbols-outlined text-primary">bolt</span>
            </div>
          </div>
        </div>
        {/* Chart Section */}
        <div className="px-4">
          <div className="bg-slate-900 text-white rounded-3xl p-6 overflow-hidden relative">
            <div className="absolute top-0 right-0 p-4 opacity-10">
              <span className="material-symbols-outlined text-[120px]">query_stats</span>
            </div>
            <div className="relative z-10 flex flex-col gap-2">
              <p className="text-slate-400 text-xs font-bold uppercase tracking-widest">Predictive Power</p>
              <h3 className="text-3xl font-bold">0.92 AUC</h3>
              <p className="text-primary text-sm font-medium">Model Precision Trend (12M)</p>
              <div className="mt-6 flex h-[120px] items-end gap-1">
                <div className="flex-1 bg-primary/30 h-[40%] rounded-t-sm"></div>
                <div className="flex-1 bg-primary/40 h-[60%] rounded-t-sm"></div>
                <div className="flex-1 bg-primary/50 h-[50%] rounded-t-sm"></div>
                <div className="flex-1 bg-primary/60 h-[80%] rounded-t-sm"></div>
                <div className="flex-1 bg-primary/70 h-[70%] rounded-t-sm"></div>
                <div className="flex-1 bg-primary h-[90%] rounded-t-sm glow-cyan"></div>
                <div className="flex-1 bg-primary/60 h-[75%] rounded-t-sm"></div>
                <div className="flex-1 bg-primary/80 h-[95%] rounded-t-sm glow-cyan"></div>
              </div>
              <div className="flex justify-between mt-2 text-[10px] text-slate-500 font-bold">
                <span>JAN</span>
                <span>MAR</span>
                <span>JUN</span>
                <span>SEP</span>
                <span>DEC</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Data Insights Section */}
      <section className="bg-card-light dark:bg-card-dark py-12 px-4 space-y-8">
        <div className="text-center space-y-2">
          <div className="bg-accent-green/20 text-accent-green text-[10px] font-bold px-3 py-1 rounded-full w-fit mx-auto uppercase">Large Scale Validation</div>
          <h2 className="text-3xl font-bold tracking-tight">Insights from 50k+ SMEs</h2>
          <p className="text-slate-500 text-sm max-w-xs mx-auto">Deep dive into the financial patterns of African enterprises.</p>
        </div>
        <div className="grid grid-cols-1 gap-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-5 rounded-2xl flex items-start gap-4">
            <div className="bg-accent-pink/10 p-3 rounded-xl">
              <span className="material-symbols-outlined text-accent-pink">pie_chart</span>
            </div>
            <div>
              <h4 className="font-bold">Debt Ratios</h4>
              <p className="text-sm text-slate-500">Correlation identified between mobile-ledger usage and lower default rates.</p>
            </div>
          </div>
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-5 rounded-2xl flex items-start gap-4">
            <div className="bg-accent-green/10 p-3 rounded-xl">
              <span className="material-symbols-outlined text-accent-green">trending_up</span>
            </div>
            <div>
              <h4 className="font-bold">Growth Potential</h4>
              <p className="text-sm text-slate-500">68% of SMEs with structured inventory records showed positive 12-month trajectory.</p>
            </div>
          </div>
        </div>
        <Link
          href="/survey"
          className="w-full bg-slate-900 dark:bg-white text-white dark:text-slate-900 h-14 rounded-xl font-bold flex items-center justify-center gap-2 hover:opacity-90 transition-opacity"
        >
          <span className="material-symbols-outlined">description</span>
          Take Survey
        </Link>
      </section>

      {/* B2B Section */}
      <section className="px-4 space-y-6">
        <div className="bg-primary p-8 rounded-[2.5rem] text-white relative overflow-hidden">
          <div className="absolute -right-12 -top-12 size-48 bg-white/10 rounded-full"></div>
          <div className="relative z-10 space-y-6">
            <h2 className="text-3xl font-bold leading-tight">Risk Mitigation for Insurers</h2>
            <ul className="space-y-4">
              <li className="flex items-center gap-3">
                <span className="material-symbols-outlined text-accent-green">check_circle</span>
                <span className="text-sm font-medium">Real-time SME health monitoring</span>
              </li>
              <li className="flex items-center gap-3">
                <span className="material-symbols-outlined text-accent-green">check_circle</span>
                <span className="text-sm font-medium">Automated risk categorization</span>
              </li>
              <li className="flex items-center gap-3">
                <span className="material-symbols-outlined text-accent-green">check_circle</span>
                <span className="text-sm font-medium">Reduced administrative overhead</span>
              </li>
            </ul>
            <Link
              href="/reports"
              className="w-full bg-white text-primary h-14 rounded-xl font-bold shadow-xl flex items-center justify-center hover:bg-slate-50 transition-colors"
            >
              Download Trends
            </Link>
          </div>
        </div>
      </section>

      {/* Final Call to Action */}
      <section className="px-4 text-center py-10 space-y-6">
        <h2 className="text-2xl font-bold">Ready to analyze?</h2>
        <div className="flex flex-col gap-3">
          <Link
            href="/results"
            className="bg-primary text-white h-14 rounded-xl font-bold glow-cyan flex items-center justify-center hover:bg-primary/90 transition-colors"
          >
            Download Full Report
          </Link>
          <p className="text-xs text-slate-500 font-medium">Join 500+ insurance providers using FinHealth.</p>
        </div>
      </section>
    </main>
  );
}
