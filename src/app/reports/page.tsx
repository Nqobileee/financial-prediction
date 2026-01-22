import Link from "next/link";
import Image from "next/image";

const reports = [
  {
    title: "SME Growth Over Time",
    description: "Line graph showing average business turnover and growth rates by year.",
    image: "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80",
  },
  {
    title: "Risk Category Distribution",
    description: "Pie chart of businesses classified as Low, Medium, or High risk.",
    image: "https://images.unsplash.com/photo-1464983953574-0892a716854b?auto=format&fit=crop&w=400&q=80",
  },
  {
    title: "Insurance Uptake",
    description: "Bar chart showing the percentage of SMEs with different types of insurance.",
    image: "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=400&q=80",
  },
  {
    title: "Cash Flow Issues",
    description: "Stacked bar chart of reported cash flow problems by sector.",
    image: "https://images.unsplash.com/photo-1519125323398-675f0ddb6308?auto=format&fit=crop&w=400&q=80",
  },
  {
    title: "Digital Finance Adoption",
    description: "Column chart of mobile money and internet banking usage among SMEs.",
    image: "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=400&q=80",
  },
  {
    title: "Tax Compliance Rates",
    description: "Donut chart showing compliance with income tax requirements.",
    image: "https://images.unsplash.com/photo-1461344577544-4e5dc9487184?auto=format&fit=crop&w=400&q=80",
  },
];

export default function ReportsPage() {
  return (
    <main className="pt-24 pb-20 max-w-4xl mx-auto px-4">
      <div className="mb-10 text-center">
        <h1 className="text-3xl font-bold mb-2">Reports & Insights Gallery</h1>
        <p className="text-slate-600 dark:text-slate-400 text-base max-w-2xl mx-auto">
          Visualize key financial and business trends from the FinHealth survey. These charts highlight patterns in SME growth, risk, insurance, and more.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {reports.map((report, index) => (
          <div
            key={index}
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
