import Link from "next/link";
import ApiStatus from "./ApiStatus";

export default function Footer() {
  return (
    <footer className="bg-slate-50 dark:bg-slate-900/50 border-t border-slate-200 dark:border-slate-800 py-12 px-6">
      <div className="flex flex-col items-center gap-8">
        <Link href="/" className="flex items-center gap-2">
          <div className="bg-primary text-white p-1 rounded-lg">
            <span className="material-symbols-outlined text-lg">terminal</span>
          </div>
          <span className="font-bold">FinHealth</span>
        </Link>
        <div className="flex gap-6">
          <a 
            className="text-slate-400 hover:text-primary transition-colors" 
            href="https://github.com/Nqobileee"
            target="_blank"
            rel="noopener noreferrer"
            title="GitHub Profile"
          >
            <span className="material-symbols-outlined">code</span>
          </a>
          <a 
            className="text-slate-400 hover:text-primary transition-colors" 
            href="https://nqobilemportfolio.framer.website/"
            target="_blank"
            rel="noopener noreferrer"
            title="Portfolio Website"
          >
            <span className="material-symbols-outlined">person</span>
          </a>
          <a 
            className="text-slate-400 hover:text-primary transition-colors" 
            href="https://www.linkedin.com/in/nqobile-muyambiri-423522236?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app"
            target="_blank"
            rel="noopener noreferrer"
            title="LinkedIn Profile"
          >
            <span className="material-symbols-outlined">link</span>
          </a>
          <a 
            className="text-slate-400 hover:text-primary transition-colors" 
            href="mailto:nqobilemuyambiri@gmail.com"
            title="Send Email"
          >
            <span className="material-symbols-outlined">mail</span>
          </a>
        </div>
        <div className="text-center space-y-2">
          <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest">
            © 2026 FinHealth Africa. Data Driven.
          </p>
          <div className="flex justify-center items-center gap-2">
            <ApiStatus />
            <span className="text-[9px] text-slate-500">•</span>
            <Link
              href="/api-test"
              className="text-[9px] text-slate-500 hover:text-primary transition-colors underline"
            >
              API Test
            </Link>
          </div>
          <p className="text-[9px] text-slate-500">
            Data licensed under <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300 transition-colors underline">CC BY-SA 4.0</a> • 
            <a href="https://zindi.africa/rules" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300 transition-colors underline">Zindi Rules</a> Compliant
          </p>
          <p className="text-[9px] text-slate-500">
            Developed by <a href="https://nqobilemportfolio.framer.website/" target="_blank" rel="noopener noreferrer" className="hover:text-primary transition-colors">Nqobile Muyambiri</a>
          </p>
        </div>
      </div>
    </footer>
  );
}
