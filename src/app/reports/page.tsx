"use client";

import Link from "next/link";
import { useState } from "react";

interface ChartData {
  label: string;
  value: number;
  percentage?: number;
  color: string;
}

const ReportCard = ({ title, description, children, insight }: {
  title: string;
  description: string;
  children: React.ReactNode;
  insight: string;
}) => (
  <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm">
    <div className="mb-4">
      <h3 className="text-lg font-bold mb-2">{title}</h3>
      <p className="text-sm text-slate-600 dark:text-slate-400">{description}</p>
    </div>
    
    <div className="mb-4">
      {children}
    </div>
    
    <div className="border-t border-slate-200 dark:border-slate-800 pt-4">
      <div className="flex items-center gap-2 mb-2">
        <span className="material-symbols-outlined text-primary text-sm">insights</span>
        <span className="text-xs font-bold uppercase tracking-wider text-primary">Key Insight</span>
      </div>
      <p className="text-sm text-slate-700 dark:text-slate-300">{insight}</p>
    </div>
  </div>
);

const PieChart = ({ data, size = 200 }: { data: ChartData[]; size?: number }) => {
  const total = data.reduce((sum, item) => sum + item.value, 0);
  let cumulativeAngle = 0;

  return (
    <div className="flex items-center justify-center">
      <svg width={size} height={size} className="transform -rotate-90">
        {data.map((item, index) => {
          const angle = (item.value / total) * 360;
          const startAngle = cumulativeAngle;
          const endAngle = startAngle + angle;
          
          const x1 = size/2 + (size/2 - 20) * Math.cos(startAngle * Math.PI / 180);
          const y1 = size/2 + (size/2 - 20) * Math.sin(startAngle * Math.PI / 180);
          const x2 = size/2 + (size/2 - 20) * Math.cos(endAngle * Math.PI / 180);
          const y2 = size/2 + (size/2 - 20) * Math.sin(endAngle * Math.PI / 180);
          
          const largeArcFlag = angle > 180 ? 1 : 0;
          
          const pathData = [
            `M ${size/2} ${size/2}`,
            `L ${x1} ${y1}`,
            `A ${size/2 - 20} ${size/2 - 20} 0 ${largeArcFlag} 1 ${x2} ${y2}`,
            'Z'
          ].join(' ');
          
          cumulativeAngle = endAngle;
          
          return (
            <path
              key={index}
              d={pathData}
              fill={item.color}
              stroke="white"
              strokeWidth="2"
            />
          );
        })}
      </svg>
    </div>
  );
};

const BarChart = ({ data, maxValue }: { data: ChartData[]; maxValue?: number }) => {
  const max = maxValue || Math.max(...data.map(d => d.value));
  
  return (
    <div className="space-y-4">
      {data.map((item, index) => (
        <div key={index} className="space-y-2">
          <div className="flex justify-between items-center">
            <span className="text-sm font-medium">{item.label}</span>
            <span className="text-sm font-bold text-primary">{item.value.toLocaleString()}</span>
          </div>
          <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-3">
            <div
              className="h-3 rounded-full transition-all duration-500"
              style={{
                width: `${(item.value / max) * 100}%`,
                backgroundColor: item.color
              }}
            ></div>
          </div>
        </div>
      ))}
    </div>
  );
};

const PercentageChart = ({ data }: { data: ChartData[] }) => (
  <div className="space-y-3">
    {data.map((item, index) => (
      <div key={index} className="space-y-1">
        <div className="flex justify-between items-center">
          <span className="text-sm font-medium">{item.label}</span>
          <span className="text-sm font-bold" style={{ color: item.color }}>
            {item.percentage?.toFixed(1)}%
          </span>
        </div>
        <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2">
          <div
            className="h-2 rounded-full transition-all duration-500"
            style={{
              width: `${item.percentage}%`,
              backgroundColor: item.color
            }}
          ></div>
        </div>
      </div>
    ))}
  </div>
);

export default function ReportsPage() {
  // Real data from training dataset analysis
  const financialHealthData: ChartData[] = [
    { label: "High Risk (Low Health)", value: 6280, percentage: 65.3, color: "#ef4444" },
    { label: "Medium Risk", value: 2868, percentage: 29.8, color: "#f59e0b" },
    { label: "Low Risk (High Health)", value: 470, percentage: 4.9, color: "#10b981" }
  ];

  const countryData: ChartData[] = [
    { label: "Eswatini", value: 2674, percentage: 27.8, color: "#3b82f6" },
    { label: "Zimbabwe", value: 2612, percentage: 27.2, color: "#8b5cf6" },
    { label: "Malawi", value: 2388, percentage: 24.8, color: "#f59e0b" },
    { label: "Lesotho", value: 1944, percentage: 20.2, color: "#10b981" }
  ];

  const digitalAdoptionData: ChartData[] = [
    { label: "Mobile Money Users", value: 4876, percentage: 50.7, color: "#10b981" },
    { label: "Tax Compliant", value: 1252, percentage: 13.0, color: "#3b82f6" },
    { label: "Have Insurance", value: 287, percentage: 3.0, color: "#8b5cf6" }
  ];

  const riskAnalysisData: ChartData[] = [
    { label: "Low Risk Businesses", value: 470, color: "#10b981" },
    { label: "Medium Risk Businesses", value: 2868, color: "#f59e0b" },
    { label: "High Risk Businesses", value: 6280, color: "#ef4444" }
  ];

  return (
    <main className="pt-24 pb-20 max-w-6xl mx-auto px-4">
      <div className="mb-10 text-center">
        <h1 className="text-3xl font-bold mb-2">Financial Health Analytics</h1>
        <p className="text-slate-600 dark:text-slate-400 text-base max-w-3xl mx-auto">
          Comprehensive analysis of {(9618).toLocaleString()} SME businesses across 4 countries, providing insights into financial health patterns, digital adoption, and risk factors.
        </p>
      </div>

      {/* Key Metrics Summary */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-primary/10 border border-primary/20 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-primary">{(9618).toLocaleString()}</div>
          <div className="text-sm text-slate-600 dark:text-slate-400">Total Businesses</div>
        </div>
        <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-green-600">4.9%</div>
          <div className="text-sm text-slate-600 dark:text-slate-400">High Financial Health</div>
        </div>
        <div className="bg-yellow-500/10 border border-yellow-500/20 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-yellow-600">50.7%</div>
          <div className="text-sm text-slate-600 dark:text-slate-400">Mobile Money Adoption</div>
        </div>
        <div className="bg-blue-500/10 border border-blue-500/20 rounded-lg p-4 text-center">
          <div className="text-2xl font-bold text-blue-600">13.0%</div>
          <div className="text-sm text-slate-600 dark:text-slate-400">Tax Compliance Rate</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Financial Health Distribution */}
        <ReportCard
          title="Financial Health Distribution"
          description="Distribution of businesses across low, medium, and high financial health categories based on ML model analysis."
          insight="65.3% of SMEs are classified as high-risk (low financial health), indicating significant challenges in the SME sector. Only 4.9% achieve high financial health status."
        >
          <div className="flex flex-col lg:flex-row items-center gap-6">
            <PieChart data={financialHealthData} size={160} />
            <div className="space-y-2 w-full">
              {financialHealthData.map((item, index) => (
                <div key={index} className="flex items-center gap-3">
                  <div 
                    className="w-4 h-4 rounded-full"
                    style={{ backgroundColor: item.color }}
                  ></div>
                  <span className="text-sm flex-1">{item.label}</span>
                  <span className="text-sm font-bold">{item.percentage}%</span>
                </div>
              ))}
            </div>
          </div>
        </ReportCard>

        {/* Country Distribution */}
        <ReportCard
          title="Geographic Distribution"
          description="Distribution of surveyed businesses across the four Southern African countries in the study."
          insight="Eswatini and Zimbabwe represent the largest samples at 27.8% and 27.2% respectively, providing balanced regional representation for reliable insights."
        >
          <BarChart data={countryData} />
        </ReportCard>

        {/* Digital Adoption Rates */}
        <ReportCard
          title="Digital & Compliance Adoption"
          description="Adoption rates of digital financial services, tax compliance, and insurance coverage among SMEs."
          insight="Mobile money shows strong adoption at 50.7%, but tax compliance (13%) and insurance coverage (3%) remain critically low, indicating significant policy and education gaps."
        >
          <PercentageChart data={digitalAdoptionData} />
        </ReportCard>

        {/* Risk Analysis by Category */}
        <ReportCard
          title="Business Count by Risk Level"
          description="Absolute numbers of businesses in each financial health risk category."
          insight="With 6,280 businesses in the high-risk category versus only 470 in low-risk, there's a clear opportunity for targeted interventions and support programs."
        >
          <BarChart data={riskAnalysisData} maxValue={7000} />
        </ReportCard>

        {/* Financial Performance Analysis */}
        <ReportCard
          title="Average Income by Risk Category"
          description="Average personal income levels across different financial health risk categories."
          insight="High financial health businesses have dramatically higher average incomes ($882K vs $254K), showing the strong correlation between personal wealth and business health."
        >
          <div className="space-y-4">
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm">Low Risk (High Health)</span>
                <span className="font-bold text-green-600">$882,802</span>
              </div>
              <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-3">
                <div className="w-full h-3 rounded-full bg-green-500"></div>
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm">Medium Risk</span>
                <span className="font-bold text-yellow-600">$180,200</span>
              </div>
              <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-3">
                <div className="w-1/5 h-3 rounded-full bg-yellow-500"></div>
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm">High Risk (Low Health)</span>
                <span className="font-bold text-red-600">$254,095</span>
              </div>
              <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-3">
                <div className="w-1/3 h-3 rounded-full bg-red-500"></div>
              </div>
            </div>
          </div>
        </ReportCard>

        {/* Key Trends Analysis */}
        <ReportCard
          title="Critical Success Factors"
          description="Comparison of key metrics across risk categories showing success patterns."
          insight="High-performing businesses show 44.7% tax compliance vs 8.8% for high-risk businesses. Insurance adoption correlates strongly with business health (21.9% vs 0%)."
        >
          <div className="space-y-4">
            <div className="grid grid-cols-3 gap-2 text-center">
              <div className="text-xs font-semibold text-slate-500">Metric</div>
              <div className="text-xs font-semibold text-slate-500">Low Risk</div>
              <div className="text-xs font-semibold text-slate-500">High Risk</div>
            </div>
            
            <div className="grid grid-cols-3 gap-2 text-center items-center">
              <div className="text-sm">Tax Compliance</div>
              <div className="text-sm font-bold text-green-600">44.7%</div>
              <div className="text-sm font-bold text-red-600">8.8%</div>
            </div>
            
            <div className="grid grid-cols-3 gap-2 text-center items-center">
              <div className="text-sm">Insurance Coverage</div>
              <div className="text-sm font-bold text-green-600">21.9%</div>
              <div className="text-sm font-bold text-red-600">0.0%</div>
            </div>
            
            <div className="grid grid-cols-3 gap-2 text-center items-center">
              <div className="text-sm">Mobile Money</div>
              <div className="text-sm font-bold text-green-600">73.0%</div>
              <div className="text-sm font-bold text-red-600">46.3%</div>
            </div>
          </div>
        </ReportCard>
      </div>

      {/* Action Items */}
      <div className="mt-12 bg-primary/5 border border-primary/20 rounded-xl p-8">
        <h2 className="text-2xl font-bold mb-4 text-center">Key Recommendations</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="w-12 h-12 bg-yellow-500 rounded-full flex items-center justify-center mx-auto mb-3">
              <span className="material-symbols-outlined text-white">school</span>
            </div>
            <h3 className="font-bold mb-2">Financial Literacy Programs</h3>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Target the 65.3% of high-risk businesses with comprehensive financial management training.
            </p>
          </div>
          <div className="text-center">
            <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-3">
              <span className="material-symbols-outlined text-white">policy</span>
            </div>
            <h3 className="font-bold mb-2">Tax Compliance Support</h3>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Improve the 13% tax compliance rate through simplified processes and education.
            </p>
          </div>
          <div className="text-center">
            <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-3">
              <span className="material-symbols-outlined text-white">shield</span>
            </div>
            <h3 className="font-bold mb-2">Insurance Accessibility</h3>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              Address the 3% insurance coverage rate with affordable, tailored SME insurance products.
            </p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="mt-8 text-center">
        <Link
          href="/"
          className="inline-flex items-center gap-2 bg-primary text-white px-6 py-3 rounded-xl font-bold hover:bg-primary/90 transition-colors"
        >
          <span className="material-symbols-outlined">home</span>
          Back to Home
        </Link>
      </div>
    </main>
  );
}
            className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow p-4 flex flex-col items-center hover:shadow-lg transition-shadow"
          >
            <div className="relative w-full h-48 mb-3 rounded-lg overflow-hidden">
              <Image
                src={report.image}
                alt={report.title}
                fill
                className="object-cover"
                unoptimized
              />
            </div>
            <h3 className="font-bold text-lg mb-1">{report.title}</h3>
            <p className="text-sm text-slate-500 text-center">{report.description}</p>
          </div>
        ))}
      </div>

      {/* CTA Section */}
      <div className="mt-12 text-center space-y-4">
        <h2 className="text-2xl font-bold">Want personalized insights?</h2>
        <p className="text-slate-500">Take our financial health survey to get a customized report for your business.</p>
        <Link
          href="/survey"
          className="inline-flex items-center gap-2 bg-primary text-white px-8 py-4 rounded-xl font-bold hover:bg-primary/90 transition-colors"
        >
          <span className="material-symbols-outlined">description</span>
          Take Survey Now
        </Link>
      </div>
    </main>
  );
}
