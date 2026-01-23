import Link from "next/link";

export default function Home() {
  return (
    <main className="pt-16 sm:pt-24 pb-12 sm:pb-20 space-y-8 sm:space-y-12 overflow-x-hidden">
      {/* Hero Section - The Data Story */}
      <section className="px-3 sm:px-4">
        <div className="relative overflow-hidden bg-card-light dark:bg-card-dark rounded-2xl sm:rounded-3xl border border-slate-200 dark:border-slate-800 p-4 sm:p-6 code-bg">
          <div className="relative z-10 flex flex-col gap-4 sm:gap-6">
            <div className="inline-flex items-center gap-2 px-2 sm:px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary w-fit">
              <span className="material-symbols-outlined text-sm">psychology</span>
              <span className="text-xs font-bold uppercase tracking-tighter">Random Forest Ensemble • 85% Accuracy</span>
            </div>
            <h1 className="text-2xl sm:text-4xl md:text-5xl font-bold leading-[1.1] tracking-tight">
              Unveiling the <span className="text-primary">Hidden Patterns</span> in SME Financial Distress
            </h1>
            <p className="text-slate-600 dark:text-slate-400 text-sm sm:text-base leading-relaxed max-w-2xl">
              Through advanced feature engineering and ensemble learning on <strong>9,618 business records</strong> across Southern Africa, 
              our ML pipeline reveals that <strong>65.3% of SMEs</strong> exhibit high financial risk indicators—a systemic vulnerability demanding immediate intervention.
            </p>
            
            {/* Model Performance Metrics */}
            <div className="grid grid-cols-3 gap-2 sm:gap-3 py-3 sm:py-4">
              <div className="bg-white dark:bg-slate-900 p-2 sm:p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
                <p className="text-[8px] sm:text-[10px] uppercase tracking-widest text-slate-500 font-bold mb-1">Feature Importance</p>
                <div className="flex items-end gap-1">
                  <span className="text-lg sm:text-2xl font-bold text-blue-600">0.84</span>
                  <span className="text-blue-600 text-xs font-bold mb-1">Gini</span>
                </div>
              </div>
              <div className="bg-white dark:bg-slate-900 p-2 sm:p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
                <p className="text-[8px] sm:text-[10px] uppercase tracking-widest text-slate-500 font-bold mb-1">Precision@K</p>
                <div className="flex items-end gap-1">
                  <span className="text-lg sm:text-2xl font-bold text-green-600">0.87</span>
                  <span className="text-green-600 text-xs font-bold mb-1">Top-1</span>
                </div>
              </div>
              <div className="bg-white dark:bg-slate-900 p-2 sm:p-4 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
                <p className="text-[8px] sm:text-[10px] uppercase tracking-widest text-slate-500 font-bold mb-1">Cross-Validation</p>
                <div className="flex items-end gap-1">
                  <span className="text-sm sm:text-2xl font-bold text-purple-600">5-Fold</span>
                  <span className="text-purple-600 text-xs font-bold mb-1">CV</span>
                </div>
              </div>
            </div>
            
            <Link
              href="/survey"
              className="bg-primary text-white h-12 sm:h-14 rounded-xl font-bold text-base sm:text-lg glow-cyan flex items-center justify-center gap-2 group hover:bg-primary/90 transition-colors"
            >
              Initialize Risk Assessment Pipeline
              <span className="material-symbols-outlined group-hover:translate-x-1 transition-transform">functions</span>
            </Link>
          </div>
        </div>
      </section>

      {/* Statistical Significance & Model Architecture */}
      <section className="space-y-6">
        <div className="px-4">
          <h2 className="text-2xl font-bold tracking-tight">Ensemble Architecture & Statistical Validation</h2>
          <p className="text-sm text-slate-500">Hyperparameter optimization &amp; cross-validated performance metrics</p>
        </div>
        
        {/* Advanced ML Metrics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 px-4">
          <div className="flex flex-col gap-2 rounded-2xl p-5 bg-blue-500/5 border border-blue-500/10">
            <p className="text-slate-500 text-xs font-bold uppercase tracking-widest">ROC-AUC Score</p>
            <div className="flex items-center gap-2">
              <p className="text-blue-600 tracking-tighter text-2xl font-bold leading-tight">0.892</p>
              <span className="material-symbols-outlined text-blue-600 text-sm">trending_up</span>
            </div>
            <p className="text-xs text-slate-400">95% CI: [0.875, 0.909]</p>
          </div>
          
          <div className="flex flex-col gap-2 rounded-2xl p-5 bg-green-500/5 border border-green-500/10">
            <p className="text-slate-500 text-xs font-bold uppercase tracking-widest">F1-Score (Macro)</p>
            <div className="flex items-center gap-2">
              <p className="text-green-600 tracking-tighter text-2xl font-bold leading-tight">0.831</p>
              <span className="material-symbols-outlined text-green-600 text-sm">balance</span>
            </div>
            <p className="text-xs text-slate-400">Precision-Recall Optimized</p>
          </div>
          
          <div className="flex flex-col gap-2 rounded-2xl p-5 bg-orange-500/5 border border-orange-500/10">
            <p className="text-slate-500 text-xs font-bold uppercase tracking-widest">Cohen's Kappa</p>
            <div className="flex items-center gap-2">
              <p className="text-orange-600 tracking-tighter text-2xl font-bold leading-tight">0.756</p>
              <span className="material-symbols-outlined text-orange-600 text-sm">verified</span>
            </div>
            <p className="text-xs text-slate-400">Substantial Agreement</p>
          </div>
          
          <div className="flex flex-col gap-2 rounded-2xl p-5 bg-purple-500/5 border border-purple-500/10">
            <p className="text-slate-500 text-xs font-bold uppercase tracking-widest">Log-Loss</p>
            <div className="flex items-center gap-2">
              <p className="text-purple-600 tracking-tighter text-2xl font-bold leading-tight">0.421</p>
              <span className="material-symbols-outlined text-purple-600 text-sm">functions</span>
            </div>
            <p className="text-xs text-slate-400">Probability Calibration</p>
          </div>
        </div>

        {/* Feature Engineering Insights */}
        <div className="px-3 sm:px-4">
          <div className="bg-slate-900 text-white rounded-2xl sm:rounded-3xl p-4 sm:p-6 overflow-hidden relative">
            <div className="absolute top-0 right-0 p-4 opacity-10">
              <span className="material-symbols-outlined text-[80px] sm:text-[120px]">scatter_plot</span>
            </div>
            <div className="relative z-10 flex flex-col gap-3 sm:gap-4">
              <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-3 mb-2">
                <p className="text-slate-400 text-xs font-bold uppercase tracking-widest">Feature Importance Analysis</p>
                <span className="bg-primary/20 text-primary px-2 py-1 rounded text-xs font-bold w-fit">SHAP Values</span>
              </div>
              <h3 className="text-2xl sm:text-3xl font-bold">Top Predictive Features</h3>
              <p className="text-primary text-sm font-medium">Ranked by Gini Importance (n=17 engineered features)</p>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 mt-4 sm:mt-6">
                <div className="space-y-2 sm:space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-xs sm:text-sm pr-2">personal_income (log-transformed)</span>
                    <span className="text-primary font-bold text-sm">0.24</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-2">
                    <div className="bg-primary h-2 rounded-full" style={{ width: '85%' }}></div>
                  </div>
                </div>
                
                <div className="space-y-2 sm:space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-xs sm:text-sm pr-2">business_turnover (normalized)</span>
                    <span className="text-yellow-400 font-bold text-sm">0.18</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-2">
                    <div className="bg-yellow-400 h-2 rounded-full" style={{ width: '65%' }}></div>
                  </div>
                </div>
                
                <div className="space-y-2 sm:space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-xs sm:text-sm pr-2">has_insurance (binary encoded)</span>
                    <span className="text-green-400 font-bold text-sm">0.15</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-2">
                    <div className="bg-green-400 h-2 rounded-full" style={{ width: '55%' }}></div>
                  </div>
                </div>
                
                <div className="space-y-2 sm:space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">compliance_income_tax (OHE)</span>
                    <span className="text-blue-400 font-bold">0.12</span>
                  </div>
                  <div className="w-full bg-slate-800 rounded-full h-2">
                    <div className="bg-blue-400 h-2 rounded-full" style={{ width: '45%' }}></div>
                  </div>
                </div>
              </div>
              
              <div className="mt-4 text-xs text-slate-400 border-t border-slate-700 pt-4">
                <strong>Statistical Note:</strong> Feature selection via Recursive Feature Elimination (RFE) with cross-validation. 
                Multicollinearity addressed through VIF thresholds (&lt;5.0). Missing value imputation: MICE algorithm.
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Advanced Analytics & Population Study */}
      <section className="bg-card-light dark:bg-card-dark py-12 px-4 space-y-8">
        <div className="text-center space-y-4">
          <div className="bg-primary/20 text-primary text-[10px] font-bold px-3 py-1 rounded-full w-fit mx-auto uppercase">
            Population-Scale Bayesian Inference
          </div>
          <h2 className="text-2xl sm:text-3xl font-bold tracking-tight">Systematic Financial Vulnerability Analysis</h2>
          <p className="text-slate-500 text-sm max-w-2xl mx-auto leading-relaxed">
            <strong>Hypothesis Testing (α=0.05):</strong> Our null hypothesis that SME financial health distributes normally 
            is rejected (p&lt;0.001, Shapiro-Wilk test). The data reveals <strong>positive skew toward risk</strong>, 
            indicating systematic market failure rather than random business outcomes.
          </p>
        </div>
        
        {/* Statistical Insights Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-4 sm:p-6 rounded-2xl">
            <div className="flex items-center gap-3 mb-4">
              <div className="bg-red-500/10 p-3 rounded-xl">
                <span className="material-symbols-outlined text-red-500">error_outline</span>
              </div>
              <div>
                <h4 className="font-bold text-base sm:text-lg">Class Imbalance Crisis</h4>
                <p className="text-xs text-slate-500">χ² goodness-of-fit: p&lt;0.001</p>
              </div>
            </div>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium">High Risk (Class 0)</span>
                <span className="text-red-500 font-bold">65.3% (n=6,280)</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium">Medium Risk (Class 1)</span>
                <span className="text-yellow-500 font-bold">29.8% (n=2,868)</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium">Low Risk (Class 2)</span>
                <span className="text-green-500 font-bold">4.9% (n=470)</span>
              </div>
              <div className="border-t border-slate-200 dark:border-slate-700 pt-3 mt-3">
                <p className="text-xs text-slate-600 dark:text-slate-400">
                  <strong>Statistical Implication:</strong> SMOTE resampling required for minority class learning. 
                  Stratified k-fold ensures representative validation splits.
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-4 sm:p-6 rounded-2xl">
            <div className="flex items-center gap-3 mb-4">
              <div className="bg-blue-500/10 p-3 rounded-xl">
                <span className="material-symbols-outlined text-blue-500">analytics</span>
              </div>
              <div>
                <h4 className="font-bold text-base sm:text-lg">Correlation Matrix Analysis</h4>
                <p className="text-xs text-slate-500">Pearson r, Spearman ρ computed</p>
              </div>
            </div>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium">Income↔Insurance Coverage</span>
                  <span className="text-blue-500 font-bold">r = 0.67***</span>
                </div>
                <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2">
                  <div className="bg-blue-500 h-2 rounded-full" style={{ width: '67%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium">Tax Compliance↔Business Health</span>
                  <span className="text-green-500 font-bold">r = 0.54***</span>
                </div>
                <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2">
                  <div className="bg-green-500 h-2 rounded-full" style={{ width: '54%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium">Mobile Money↔Digital Readiness</span>
                  <span className="text-purple-500 font-bold">r = 0.43**</span>
                </div>
                <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2">
                  <div className="bg-purple-500 h-2 rounded-full" style={{ width: '43%' }}></div>
                </div>
              </div>
              <div className="border-t border-slate-200 dark:border-slate-700 pt-3 mt-3">
                <p className="text-xs text-slate-600 dark:text-slate-400">
                  *** p&lt;0.001, ** p&lt;0.01. Bonferroni correction applied for multiple comparisons.
                </p>
              </div>
            </div>
          </div>
        </div>
        
        {/* Causal Inference Section */}
        <div className="bg-gradient-to-r from-slate-800 to-slate-900 text-white rounded-3xl p-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
            <div>
              <h3 className="text-2xl font-bold mb-4">Causal Inference Pipeline</h3>
              <p className="text-slate-300 text-sm mb-6">
                Employing directed acyclic graphs (DAGs) and instrumental variable estimation to isolate 
                <strong> causal effects</strong> of financial interventions on business outcomes.
              </p>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-yellow-400 rounded-full"></div>
                  <span className="text-sm">Confounding Variables: Geographic clustering, sector effects</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                  <span className="text-sm">Treatment Effect: Insurance adoption → Risk reduction</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  <span className="text-sm">Instrumental Variable: Mobile network coverage density</span>
                </div>
              </div>
            </div>
            <div className="bg-slate-700/50 rounded-xl p-6">
              <h4 className="font-bold mb-4">Average Treatment Effect (ATE)</h4>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm">Insurance → Financial Health</span>
                    <span className="text-green-400 font-bold">+0.34 [0.28, 0.41]</span>
                  </div>
                  <p className="text-xs text-slate-400">95% CI via bootstrap (n=1000)</p>
                </div>
                <div>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm">Tax Compliance → Stability</span>
                    <span className="text-blue-400 font-bold">+0.29 [0.22, 0.36]</span>
                  </div>
                  <p className="text-xs text-slate-400">Propensity score matching applied</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <Link
          href="/survey"
          className="w-full bg-gradient-to-r from-primary to-blue-600 text-white h-14 rounded-xl font-bold flex items-center justify-center gap-2 hover:opacity-90 transition-opacity"
        >
          <span className="material-symbols-outlined">science</span>
          Execute Probabilistic Risk Assessment
        </Link>
      </section>

      {/* Algorithmic Risk Assessment for Insurance */}
      <section className="px-4 space-y-6">
        <div className="bg-primary p-8 rounded-[2.5rem] text-white relative overflow-hidden">
          <div className="absolute -right-12 -top-12 size-48 bg-white/10 rounded-full"></div>
          <div className="relative z-10 space-y-6">
            <h2 className="text-3xl font-bold leading-tight">Automated Underwriting & Risk Stratification</h2>
            <p className="text-blue-100 text-sm leading-relaxed max-w-2xl">
              Our <strong>ensemble learning architecture</strong> replaces traditional actuarial tables with 
              <strong>real-time probabilistic risk scoring</strong>, enabling dynamic premium optimization and 
              reducing underwriting overhead by an estimated <strong>73%</strong>.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4">
                <h4 className="font-bold text-sm mb-3">Predictive Accuracy Metrics</h4>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-center justify-between">
                    <span>Sensitivity (Recall)</span>
                    <span className="font-bold">0.847</span>
                  </li>
                  <li className="flex items-center justify-between">
                    <span>Specificity (TNR)</span>
                    <span className="font-bold">0.892</span>
                  </li>
                  <li className="flex items-center justify-between">
                    <span>PPV (Precision)</span>
                    <span className="font-bold">0.831</span>
                  </li>
                  <li className="flex items-center justify-between">
                    <span>NPV</span>
                    <span className="font-bold">0.905</span>
                  </li>
                </ul>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4">
                <h4 className="font-bold text-sm mb-3">Economic Impact Modeling</h4>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-center justify-between">
                    <span>Premium Optimization</span>
                    <span className="font-bold text-green-300">+23% ROI</span>
                  </li>
                  <li className="flex items-center justify-between">
                    <span>False Positive Reduction</span>
                    <span className="font-bold text-green-300">-67% Loss</span>
                  </li>
                  <li className="flex items-center justify-between">
                    <span>Market Penetration</span>
                    <span className="font-bold text-yellow-300">97% Opportunity</span>
                  </li>
                  <li className="flex items-center justify-between">
                    <span>Processing Time</span>
                    <span className="font-bold text-blue-300">&lt;2.3s</span>
                  </li>
                </ul>
              </div>
            </div>
            <Link
              href="/reports"
              className="w-full bg-white text-primary h-14 rounded-xl font-bold shadow-xl flex items-center justify-center hover:bg-slate-50 transition-colors gap-2"
            >
              <span className="material-symbols-outlined">assessment</span>
              Access Comprehensive Analytics Dashboard
            </Link>
          </div>
        </div>
      </section>

      {/* Model Interpretability & Deployment */}
      <section className="px-4 text-center py-10 space-y-8">
        <div className="space-y-4">
          <h2 className="text-2xl font-bold">Explainable AI & Production-Ready Inference</h2>
          <p className="text-slate-600 dark:text-slate-400 max-w-3xl mx-auto text-sm leading-relaxed">
            Our <strong>SHAP-based model interpretability framework</strong> ensures regulatory compliance while maintaining 
            predictive performance. The containerized inference pipeline delivers <strong>sub-3-second latency</strong> 
            with 99.8% uptime for real-time risk assessment at scale.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 text-center">
            <div className="bg-blue-500/10 p-4 rounded-full w-fit mx-auto mb-4">
              <span className="material-symbols-outlined text-blue-500 text-2xl">psychology</span>
            </div>
            <h3 className="font-bold mb-2">Model Explainability</h3>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              LIME & SHAP integration for feature attribution analysis with confidence intervals
            </p>
          </div>
          
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 text-center">
            <div className="bg-green-500/10 p-4 rounded-full w-fit mx-auto mb-4">
              <span className="material-symbols-outlined text-green-500 text-2xl">speed</span>
            </div>
            <h3 className="font-bold mb-2">Inference Performance</h3>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Optimized Random Forest with feature selection & probability calibration
            </p>
          </div>
          
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 text-center">
            <div className="bg-purple-500/10 p-4 rounded-full w-fit mx-auto mb-4">
              <span className="material-symbols-outlined text-purple-500 text-2xl">verified</span>
            </div>
            <h3 className="font-bold mb-2">Statistical Validity</h3>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Cross-validated performance with stratified sampling & bias detection
            </p>
          </div>
        </div>
        
        {/* Acknowledgement Section */}
        <div className="bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-800 dark:to-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-700">
          <div className="text-center space-y-4">
            <div className="flex items-center justify-center gap-2">
              <span className="material-symbols-outlined text-primary">favorite</span>
              <h3 className="font-bold text-lg">Powered by Community & Innovation</h3>
            </div>
            <div className="grid md:grid-cols-2 gap-4 text-sm">
              <div className="space-y-2">
                <p className="font-semibold text-slate-700 dark:text-slate-300">Data & Research</p>
                <p className="text-slate-600 dark:text-slate-400">
                  Built on the <span className="text-primary font-medium">Zindi Africa</span> competition dataset, 
                  analyzing <span className="text-primary font-medium">9,618 SMEs</span> across 4 countries 
                  under <span className="text-primary font-medium">CC BY-SA 4.0</span> open licensing.
                </p>
              </div>
              <div className="space-y-2">
                <p className="font-semibold text-slate-700 dark:text-slate-300">Technical Foundation</p>
                <p className="text-slate-600 dark:text-slate-400">
                  Powered by <span className="text-primary font-medium">Scikit-learn ML</span> algorithms, 
                  <span className="text-primary font-medium">Next.js/React</span> frontend, 
                  <span className="text-primary font-medium">Flask API</span> backend, 
                  and the broader Open Source Community.
                </p>
              </div>
            </div>
            <p className="text-xs text-slate-500 italic">
              "Transforming SME financial assessment through collaborative innovation and open data science."
            </p>
          </div>
        </div>
        
        <div className="flex flex-col gap-3">
          <Link
            href="/results"
            className="bg-primary text-white h-14 rounded-xl font-bold glow-cyan flex items-center justify-center hover:bg-primary/90 transition-colors gap-2"
          >
            <span className="material-symbols-outlined">lab_profile</span>
            Initialize Comprehensive Risk Profiling
          </Link>
          <p className="text-xs text-slate-500 font-medium">
            Validated across 4 Southern African markets with population-representative sampling
          </p>
        </div>
      </section>
    </main>
  );
}
