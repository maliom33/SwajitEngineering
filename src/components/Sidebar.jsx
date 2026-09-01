import { LayoutGrid, Menu, ChevronLeft, ChevronRight } from 'lucide-react';
import * as Icons from 'lucide-react';

function Sidebar({ links, activeItem, onSelect, isOpen, toggleSidebar }) {
  return (
    <aside className={`sticky top-0 z-20 h-screen min-h-screen border-r border-white/10 bg-[color:var(--bg-sidebar)] shadow-[0_20px_60px_rgba(2,6,23,0.35)] transition-all duration-300 ${isOpen ? 'w-72' : 'w-20'} overflow-hidden`}>
      <div className="flex h-full flex-col justify-between px-4 py-6">
        <div className="space-y-8">
          <div className="flex items-center justify-between gap-3">
            <div className="inline-flex items-center gap-3 rounded-3xl bg-gradient-to-r from-blue-600 to-blue-500 px-4 py-3 text-white shadow-lg shadow-blue-600/20">
              <LayoutGrid className="h-5 w-5" />
              {isOpen && <span className="text-sm font-semibold">SwajitERP</span>}
            </div>
            <button type="button" className="rounded-full border border-white/10 bg-white/5 p-2 text-slate-300 shadow-sm transition hover:border-blue-400/50 hover:text-white" onClick={toggleSidebar} aria-label="Toggle sidebar">
              {isOpen ? <ChevronLeft className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
            </button>
          </div>

          <nav className="space-y-1">
            {links.map((link) => {
              const Icon = Icons[link.icon] || Menu;
              const active = activeItem === link.label;
              return (
                <button
                  key={link.label}
                  onClick={() => onSelect(link.label)}
                  className={`group flex w-full items-center gap-3 rounded-3xl px-4 py-3 text-left transition ${active ? 'bg-gradient-to-r from-blue-600/20 via-blue-500/10 to-transparent text-white shadow-[inset_0_0_0_1px_rgba(255,255,255,0.05)]' : 'text-slate-400 hover:bg-white/5 hover:text-white'}`}
                >
                  <span className={`inline-flex h-10 w-10 items-center justify-center rounded-2xl ${active ? 'bg-gradient-to-br from-blue-600 to-blue-500 text-white' : 'bg-white/5 text-slate-400'} transition`}>
                    <Icon className="h-5 w-5" />
                  </span>
                  {isOpen && <span className="font-medium">{link.label}</span>}
                </button>
              );
            })}
          </nav>
        </div>

        <div className={`rounded-3xl border border-white/10 bg-white/5 p-4 backdrop-blur-md transition ${isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}>
          <p className="text-xs uppercase tracking-[0.28em] text-slate-500">Support</p>
          <p className="mt-3 text-sm font-medium text-slate-100">ERP system optimized for steel manufacturing.</p>
          <p className="mt-2 text-sm text-slate-400">Secure access, compliance-ready workflows, and unified operations.</p>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
