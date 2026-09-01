import { useEffect, useState } from 'react';
import { Search, Bell, MessageCircle, LogOut, Moon, Sun } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

function AdminNavbar({ userProfile, onLogout }) {
  const navigate = useNavigate();
  const name = userProfile?.name ?? 'System Admin';
  const role = userProfile?.role ?? 'Administrator';
  const initials = name
    .split(' ')
    .filter(Boolean)
    .map((part) => part[0])
    .join('')
    .slice(0, 2)
    .toUpperCase();

  useEffect(() => {
    localStorage.setItem('swajit-theme', 'light');
    document.documentElement.classList.remove('dark');
  }, []);

  const toggleTheme = () => {
    // Theme toggle disabled for light-only default mode.
  };

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
    <motion.header
      initial={{ opacity: 0, y: -6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25 }}
      className="sticky top-0 z-10 border-b border-white/10 bg-[color:var(--bg-surface)]/80 backdrop-blur-xl"
    >
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex-1">
          <div className="relative max-w-xl">
            <Search className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <input
              type="search"
              placeholder="Search users, departments, activity..."
              className="h-11 w-full rounded-3xl border border-white/10 bg-[color:var(--bg-surface-2)] px-12 text-sm text-slate-100 outline-none transition focus:border-blue-500/60 focus:ring-2 focus:ring-blue-500/20"
            />
          </div>
        </div>

        <div className="flex items-center gap-3">
          <motion.button whileHover={{ scale: 1.04 }} whileTap={{ scale: 0.96 }} type="button" className="inline-flex h-11 w-11 items-center justify-center rounded-2xl border border-slate-200 bg-white text-slate-900 transition hover:border-slate-300 hover:text-slate-950" disabled>
            <Sun className="h-5 w-5" />
          </motion.button>
          <motion.button whileHover={{ scale: 1.04 }} whileTap={{ scale: 0.96 }} type="button" className="inline-flex h-11 w-11 items-center justify-center rounded-2xl border border-white/10 bg-white/5 text-slate-300 transition hover:border-blue-400/50 hover:text-white">
            <Bell className="h-5 w-5" />
          </motion.button>
          <motion.button whileHover={{ scale: 1.04 }} whileTap={{ scale: 0.96 }} type="button" className="inline-flex h-11 w-11 items-center justify-center rounded-2xl border border-white/10 bg-white/5 text-slate-300 transition hover:border-blue-400/50 hover:text-white">
            <MessageCircle className="h-5 w-5" />
          </motion.button>

          <div className="hidden min-w-[200px] items-center gap-3 rounded-3xl border border-white/10 bg-white/5 px-4 py-3 shadow-lg shadow-slate-950/20 sm:flex">
            <div aria-hidden="true" className="inline-flex h-10 w-10 items-center justify-center rounded-2xl bg-blue-500/20 text-sm font-semibold text-blue-200">
              {initials}
            </div>
            <div className="flex-1 text-left">
              <p className="text-sm font-semibold text-slate-100">{name}</p>
              <p className="text-sm text-slate-400">{role}</p>
            </div>
            <motion.button whileHover={{ scale: 1.04 }} whileTap={{ scale: 0.96 }} type="button" onClick={handleLogout} className="inline-flex h-9 w-9 items-center justify-center rounded-2xl text-slate-400 transition hover:bg-white/10 hover:text-white">
              <LogOut className="h-5 w-5" />
            </motion.button>
          </div>
        </div>
      </div>
    </motion.header>
  );
}

export default AdminNavbar;
