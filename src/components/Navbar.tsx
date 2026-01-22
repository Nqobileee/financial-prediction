import Link from "next/link";
import { useState } from "react";

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 px-2 sm:px-4 py-3">
      <div className="neo-blur dark:neo-blur border border-slate-200 dark:border-slate-800 rounded-2xl flex items-center justify-between px-3 sm:px-4 h-12 sm:h-14 glow-cyan">
        <Link href="/" className="flex items-center gap-1 sm:gap-2">
          <div className="bg-primary text-white p-1 rounded-lg">
            <span className="material-symbols-outlined text-base sm:text-lg">terminal</span>
          </div>
          <h2 className="text-base sm:text-lg font-bold tracking-tight">FinHealth</h2>
        </Link>
        
        {/* Desktop Navigation */}
        <div className="hidden sm:flex items-center gap-4">
          <Link
            href="/reports"
            className="text-sm font-medium hover:text-primary transition-colors"
          >
            Reports
          </Link>
          <Link
            href="/survey"
            className="bg-primary text-white px-3 sm:px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-wider hover:bg-primary/90 transition-colors"
          >
            Take Survey
          </Link>
        </div>
        
        {/* Mobile Navigation */}
        <div className="flex sm:hidden items-center gap-2">
          <Link
            href="/survey"
            className="bg-primary text-white px-2 py-1 rounded-lg text-xs font-bold uppercase tracking-wider hover:bg-primary/90 transition-colors"
          >
            Survey
          </Link>
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="p-1 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors"
          >
            <span className="material-symbols-outlined text-lg">
              {isMenuOpen ? 'close' : 'menu'}
            </span>
          </button>
        </div>
      </div>
      
      {/* Mobile Dropdown Menu */}
      {isMenuOpen && (
        <div className="sm:hidden mt-2 mx-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-lg overflow-hidden">
          <Link
            href="/reports"
            className="block px-4 py-3 text-sm font-medium hover:bg-slate-50 dark:hover:bg-slate-800 border-b border-slate-200 dark:border-slate-800"
            onClick={() => setIsMenuOpen(false)}
          >
            Reports
          </Link>
          <Link
            href="/"
            className="block px-4 py-3 text-sm font-medium hover:bg-slate-50 dark:hover:bg-slate-800"
            onClick={() => setIsMenuOpen(false)}
          >
            Home
          </Link>
        </div>
      )}
    </nav>
  );
}
