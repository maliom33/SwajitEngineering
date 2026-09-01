import { NavLink, useNavigate } from 'react-router-dom';
import * as Icons from 'lucide-react';

const sidebarLinks = [
  { label: 'Dashboard', icon: 'LayoutGrid' },
  { label: 'User Management', icon: 'Users' },
  { label: 'Role & Permission', icon: 'Shield' },
  { label: 'Department Management', icon: 'Building2' },
  { label: 'Attendance Config', icon: 'Clock' },
  { label: 'System Monitoring', icon: 'BarChart3' },
  { label: 'Database Management', icon: 'Database' },
  { label: 'Backup & Restore', icon: 'HardDrive' },
  { label: 'Activity Logs', icon: 'Activity' },
  { label: 'Notifications', icon: 'Bell' },
  { label: 'System Settings', icon: 'Settings' },
];

function DashboardSidebar({ activeItem, onSelect = () => {}, isOpen = true, toggleSidebar = () => {}, links = sidebarLinks, title = 'Admin', onLogout }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    const shouldLogout = window.confirm('Are you sure you want to logout?');
    if (shouldLogout) {
      if (onLogout) {
        onLogout();
      } else {
        navigate('/login');
      }
    }
  };

  return (
    <>
      <aside className={`sticky top-0 z-20 h-screen min-h-screen border-r border-white/10 bg-[color:var(--bg-sidebar)] shadow-[0_20px_60px_rgba(2,6,23,0.35)] transition-all duration-300 ${isOpen ? 'w-72' : 'w-20'} overflow-hidden`}>
        <div className="flex h-full flex-col justify-between px-4 py-6">
          <div className="space-y-8">
            <div className="flex items-center justify-between gap-3">
              <div className="inline-flex items-center gap-3 rounded-3xl bg-gradient-to-r from-blue-600 to-blue-500 px-4 py-3 text-white shadow-lg shadow-blue-600/20">
                <Icons.LayoutGrid className="h-5 w-5" />
                {isOpen && <span className="text-sm font-semibold">{title}</span>}
              </div>
              <button
                type="button"
                className="rounded-full border border-white/10 bg-[color:var(--bg-surface)] p-2 text-slate-300 shadow-sm transition hover:border-blue-400/50 hover:text-white"
                onClick={toggleSidebar}
                aria-label="Toggle sidebar"
              >
                {isOpen ? <Icons.ChevronLeft className="h-4 w-4" /> : <Icons.ChevronRight className="h-4 w-4" />}
              </button>
            </div>

            <nav className="space-y-1">
              {links.map((link) => {
                const Icon = Icons[link.icon] || Icons.LayoutGrid;
                const active = activeItem === link.label;
                if (link.label === 'Logout') {
                  return (
                    <button
                      key={link.label}
                      type="button"
                      onClick={() => {
                        onSelect(link.label);
                        handleLogout();
                      }}
                      className="group relative flex w-full items-center gap-3 rounded-3xl px-4 py-3 text-left text-slate-400 transition hover:bg-white/5 hover:text-white"
                    >
                      <span className="inline-flex h-10 w-10 items-center justify-center rounded-2xl bg-white/5 text-slate-400 transition group-hover:text-white">
                        <Icon className="h-5 w-5" />
                      </span>
                      {isOpen ? (
                        <span className="font-medium">{link.label}</span>
                      ) : (
                        <span className="pointer-events-none absolute left-full top-1/2 z-40 hidden -translate-y-1/2 whitespace-nowrap rounded-md bg-slate-900 px-3 py-2 text-sm text-slate-100 shadow-lg group-hover:block">
                          {link.label}
                        </span>
                      )}
                    </button>
                  );
                }

                if (link.to) {
                  return (
                    <NavLink
                      key={link.label}
                      to={link.to}
                      onClick={() => onSelect(link.label)}
                      className={({ isActive }) => `group relative flex w-full items-center gap-3 rounded-3xl px-4 py-3 text-left transition ${isActive ? 'bg-gradient-to-r from-blue-600/20 via-blue-500/10 to-transparent text-white shadow-[inset_0_0_0_1px_rgba(255,255,255,0.05)]' : 'text-slate-400 hover:bg-white/5 hover:text-white'}`}
                    >
                      <span className="inline-flex h-10 w-10 items-center justify-center rounded-2xl bg-white/5 text-slate-400 transition group-hover:bg-white/10 group-hover:text-white">
                        <Icon className="h-5 w-5" />
                      </span>
                      {isOpen ? (
                        <span className="font-medium">{link.label}</span>
                      ) : (
                        <span className="pointer-events-none absolute left-full top-1/2 z-40 hidden -translate-y-1/2 whitespace-nowrap rounded-md bg-slate-900 px-3 py-2 text-sm text-slate-100 shadow-lg group-hover:block">
                          {link.label}
                        </span>
                      )}
                    </NavLink>
                  );
                }
                return (
                  <button
                    key={link.label}
                    onClick={() => onSelect(link.label)}
                    className={`group relative flex w-full items-center gap-3 rounded-3xl px-4 py-3 text-left transition ${active ? 'bg-gradient-to-r from-blue-600/20 via-blue-500/10 to-transparent text-white shadow-[inset_0_0_0_1px_rgba(255,255,255,0.05)]' : 'text-slate-400 hover:bg-white/5 hover:text-white'}`}
                  >
                    <span className={`inline-flex h-10 w-10 items-center justify-center rounded-2xl ${active ? 'bg-gradient-to-br from-blue-600 to-blue-500 text-white' : 'bg-white/5 text-slate-400'} transition`}>
                      <Icon className="h-5 w-5" />
                    </span>
                    {isOpen ? (
                      <span className="font-medium">{link.label}</span>
                    ) : (
                      <span className="pointer-events-none absolute left-full top-1/2 z-40 hidden -translate-y-1/2 whitespace-nowrap rounded-md bg-slate-900 px-3 py-2 text-sm text-slate-100 shadow-lg group-hover:block">
                        {link.label}
                      </span>
                    )}
                  </button>
                );
              })}
            </nav>
          </div>

          <div className={`rounded-3xl border border-white/10 bg-white/5 p-4 backdrop-blur-md transition ${isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}>
            <p className="text-xs uppercase tracking-[0.28em] text-slate-500">Admin Panel</p>
            <p className="mt-3 text-sm font-medium text-slate-100">Full System Access</p>
            <p className="mt-2 text-sm text-slate-400">Manage all ERP operations and user permissions.</p>
          </div>
        </div>
      </aside>
      {!isOpen && (
        <button
          aria-label="Open sidebar"
          onClick={toggleSidebar}
          className="fixed left-2 top-1/2 z-30 -translate-y-1/2 rounded-full border border-white/10 bg-slate-900/90 p-2 text-slate-200 shadow-lg transition hover:bg-slate-800"
        >
          <Icons.ChevronRight className="h-4 w-4" />
        </button>
      )}
    </>
  );
}

export default DashboardSidebar;
