import { Bell, Search, Moon, LogOut } from 'lucide-react';

function Navbar({ userProfile, currentDate }) {
  return (
    <header className="sticky top-0 z-10 border-b border-white/10 bg-[color:var(--bg-surface)]/80 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex flex-1 items-center gap-4">
          <div className="relative flex-1">
            <Search className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <input
              type="search"
              placeholder="Search operations, orders, trucks..."
              className="h-11 w-full rounded-3xl border border-white/10 bg-[color:var(--bg-surface-2)] px-12 text-sm text-slate-100 outline-none transition focus:border-blue-500/60 focus:ring-2 focus:ring-blue-500/20"
            />
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button type="button" className="inline-flex h-11 w-11 items-center justify-center rounded-2xl border border-white/10 bg-white/5 text-slate-300 transition hover:border-blue-400/50 hover:text-white">
            <Bell className="h-5 w-5" />
          </button>
          <button type="button" className="inline-flex h-11 w-11 items-center justify-center rounded-2xl border border-white/10 bg-white/5 text-slate-300 transition hover:border-blue-400/50 hover:text-white">
            <Moon className="h-5 w-5" />
          </button>

          <div className="hidden min-w-[220px] items-center gap-3 rounded-3xl border border-white/10 bg-white/5 px-4 py-3 shadow-lg shadow-slate-950/20 sm:flex">
            <img src={userProfile.avatar} alt="User avatar" className="h-11 w-11 rounded-2xl object-cover" />
            <div className="flex-1 text-left">
              <p className="text-sm font-semibold text-slate-100">{userProfile.name}</p>
              <p className="text-sm text-slate-400">{userProfile.role}</p>
            </div>
            <LogOut className="h-5 w-5 text-slate-400" />
          </div>
        </div>
      </div>
    </header>
  );
}

export default Navbar;
