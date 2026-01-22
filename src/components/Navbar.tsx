import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 px-4 py-3">
      <div className="neo-blur dark:neo-blur border border-slate-200 dark:border-slate-800 rounded-2xl flex items-center justify-between px-4 h-14 glow-cyan">
        <Link href="/" className="flex items-center gap-2">
          <div className="bg-primary text-white p-1 rounded-lg">
            <span className="material-symbols-outlined text-lg">terminal</span>
          </div>
          <h2 className="text-lg font-bold tracking-tight">FinHealth</h2>
        </Link>
        <div className="flex items-center gap-4">
          <Link
            href="/reports"
            className="hidden md:block text-sm font-medium hover:text-primary transition-colors"
          >
            Reports
          </Link>
          <Link
            href="/survey"
            className="bg-primary text-white px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-wider hover:bg-primary/90 transition-colors"
          >
            Take Survey
          </Link>
        </div>
      </div>
    </nav>
  );
}
