import Link from "next/link";

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
          <a className="text-slate-400 hover:text-primary" href="#">
            <span className="material-symbols-outlined">code</span>
          </a>
          <a className="text-slate-400 hover:text-primary" href="#">
            <span className="material-symbols-outlined">person</span>
          </a>
          <a className="text-slate-400 hover:text-primary" href="#">
            <span className="material-symbols-outlined">link</span>
          </a>
          <a className="text-slate-400 hover:text-primary" href="#">
            <span className="material-symbols-outlined">mail</span>
          </a>
        </div>
        <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest">
          © 2024 FinHealth Africa. Data Driven.
        </p>
      </div>
    </footer>
  );
}
