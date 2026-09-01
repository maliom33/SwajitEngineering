import * as Icons from 'lucide-react';

function AdminQuickActions() {
  const actions = [
    { label: 'Add User', icon: 'UserPlus', color: 'from-sky-500 to-cyan-500' },
    { label: 'Create Department', icon: 'Building2Plus', color: 'from-violet-500 to-purple-500' },
    { label: 'Create Role', icon: 'ShieldPlus', color: 'from-emerald-500 to-teal-500' },
    { label: 'Reset Password', icon: 'Lock', color: 'from-orange-500 to-amber-500' },
    { label: 'Backup Database', icon: 'Database', color: 'from-rose-500 to-red-500' },
    { label: 'View Activity Logs', icon: 'FileText', color: 'from-indigo-500 to-blue-500' },
  ];

  return (
    <section className="card-glass rounded-3xl border border-slate-200/80 bg-white/90 p-6 shadow-sm">
      <div className="mb-6">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Quick Actions</p>
        <h2 className="mt-3 text-2xl font-semibold text-slate-950">Workflow Shortcuts</h2>
      </div>
      <div className="space-y-3">
        {actions.map((action) => {
          const Icon = Icons[action.icon] || Icons.ArrowRight;
          return (
            <button
              key={action.label}
              type="button"
              className={`w-full group flex items-center gap-4 rounded-3xl bg-gradient-to-r ${action.color} px-6 py-4 text-left text-white shadow-lg shadow-slate-950/10 transition hover:translate-y-0.5 hover:shadow-xl`}
            >
              <span className="inline-flex h-12 w-12 min-w-12 items-center justify-center rounded-3xl bg-white/15 text-white shadow-sm">
                <Icon className="h-5 w-5" />
              </span>
              <span className="text-base font-semibold">{action.label}</span>
            </button>
          );
        })}
      </div>
    </section>
  );
}

export default AdminQuickActions;
