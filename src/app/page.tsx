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
                <p className="text-[10px] uppercase tracking-widest text-slate-500 font-bold mb-1">High Health Rate</p>
                <div className="flex items-end gap-1">
                  <span className="text-2xl font-bold">4.9</span>
                  <span className="text-yellow-600 text-xs font-bold mb-1 flex items-center">
                    <span className="material-symbols-outlined text-xs">trending_flat</span>%
                  </span>
                </div>
              </div>
              <div className="bg-white dark:bg-slate-900 p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
                <p className="text-[10px] uppercase tracking-widest text-slate-500 font-bold mb-1">Businesses Analyzed</p>
                <span className="text-2xl font-bold text-primary">9.6K</span>
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
        <div className="grid grid-cols-3 gap-4 px-4">
          <div className="flex flex-col gap-2 rounded-2xl p-5 bg-primary/5 border border-primary/10">
            <p className="text-slate-500 text-xs font-bold uppercase tracking-widest">Model Accuracy</p>
            <div className="flex items-center gap-2">
              <p className="text-primary tracking-tighter text-2xl font-bold leading-tight">85%</p>
              <span className="material-symbols-outlined text-primary text-sm">verified</span>
            </div>
          </div>
          <div className="flex flex-col gap-2 rounded-2xl p-5 bg-green-500/5 border border-green-500/10">
            <p className="text-slate-500 text-xs font-bold uppercase tracking-widest">Countries</p>
            <div className="flex items-center gap-2">
              <p className="text-green-600 tracking-tighter text-2xl font-bold leading-tight">4</p>
              <span className="material-symbols-outlined text-green-600 text-sm">public</span>
            </div>
          </div>
          <div className="flex flex-col gap-2 rounded-2xl p-5 bg-blue-500/5 border border-blue-500/10">
            <p className="text-slate-500 text-xs font-bold uppercase tracking-widest">Features</p>
            <div className="flex items-center gap-2">
              <p className="text-blue-600 tracking-tighter text-2xl font-bold leading-tight">17</p>
              <span className="material-symbols-outlined text-blue-600 text-sm">dataset</span>
            </div>
          </div>
        </div>
        {/* Risk Distribution Chart */}
        <div className="px-4">
          <div className="bg-slate-900 text-white rounded-3xl p-6 overflow-hidden relative">
            <div className="absolute top-0 right-0 p-4 opacity-10">
              <span className="material-symbols-outlined text-[120px]">assessment</span>
            </div>
            <div className="relative z-10 flex flex-col gap-2">
              <p className="text-slate-400 text-xs font-bold uppercase tracking-widest">Financial Health Distribution</p>
              <h3 className="text-3xl font-bold">Risk Categories</h3>
              <p className="text-primary text-sm font-medium">Across 9,618 SME Businesses</p>
              <div className="mt-6 flex h-[120px] items-end gap-2">
                <div className="flex flex-col items-center gap-2">
                  <div className="bg-red-500 h-[78px] w-12 rounded-t-lg glow-red"></div>
                  <span className="text-[10px] text-slate-400">HIGH RISK</span>
                  <span className="text-xs font-bold">65.3%</span>
                </div>
                <div className="flex flex-col items-center gap-2">
                  <div className="bg-yellow-500 h-[36px] w-12 rounded-t-lg"></div>
                  <span className="text-[10px] text-slate-400">MEDIUM</span>
                  <span className="text-xs font-bold">29.8%</span>
                </div>
                <div className="flex flex-col items-center gap-2">
                  <div className="bg-green-500 h-[6px] w-12 rounded-t-lg"></div>
                  <span className="text-[10px] text-slate-400">LOW RISK</span>
                  <span className="text-xs font-bold">4.9%</span>
                </div>
              </div>
              <div className="mt-4 text-xs text-slate-400">
                Low risk businesses have 5x higher average income ($882K vs $254K)
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Data Insights Section */}
      <section className="bg-card-light dark:bg-card-dark py-12 px-4 space-y-8">
        <div className="text-center space-y-2">
          <div className="bg-primary/20 text-primary text-[10px] font-bold px-3 py-1 rounded-full w-fit mx-auto uppercase">Real Dataset Analysis</div>
          <h2 className="text-3xl font-bold tracking-tight">Insights from 9,618 SMEs</h2>
          <p className="text-slate-500 text-sm max-w-xs mx-auto">Real-world data from Southern African businesses across 4 countries.</p>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-5 rounded-2xl text-center">
            <div className="bg-red-500/10 p-3 rounded-xl w-fit mx-auto mb-3">
              <span className="material-symbols-outlined text-red-500">warning</span>
            </div>
            <div className="text-2xl font-bold text-red-500 mb-1">65.3%</div>
            <h4 className="font-bold text-sm">High Risk</h4>
            <p className="text-xs text-slate-500">Businesses classified as low financial health</p>
          </div>
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-5 rounded-2xl text-center">
            <div className="bg-green-500/10 p-3 rounded-xl w-fit mx-auto mb-3">
              <span className="material-symbols-outlined text-green-500">payments</span>
            </div>
            <div className="text-2xl font-bold text-green-500 mb-1">50.7%</div>
            <h4 className="font-bold text-sm">Mobile Money</h4>
            <p className="text-xs text-slate-500">Digital payment adoption rate</p>
          </div>
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-5 rounded-2xl text-center">
            <div className="bg-blue-500/10 p-3 rounded-xl w-fit mx-auto mb-3">
              <span className="material-symbols-outlined text-blue-500">receipt_long</span>
            </div>
            <div className="text-2xl font-bold text-blue-500 mb-1">13%</div>
            <h4 className="font-bold text-sm">Tax Compliance</h4>
            <p className="text-xs text-slate-500">Businesses filing income tax</p>
          </div>
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-5 rounded-2xl text-center">
            <div className="bg-purple-500/10 p-3 rounded-xl w-fit mx-auto mb-3">
              <span className="material-symbols-outlined text-purple-500">shield</span>
            </div>
            <div className="text-2xl font-bold text-purple-500 mb-1">3%</div>
            <h4 className="font-bold text-sm">Insurance Coverage</h4>
            <p className="text-xs text-slate-500">Businesses with active insurance</p>
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
          <p className="text-xs text-slate-500 font-medium">Analysis covers Eswatini, Zimbabwe, Malawi & Lesotho SMEs.</p>
        </div>
      </section>
    </main>
  );
}
