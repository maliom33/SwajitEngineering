import * as Icons from 'lucide-react';

function QuickActions({ actions }) {
  return (
    <section className="card-glass rounded-3xl border border-slate-200/80 p-6 shadow-glass">
      <div>
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Quick actions</p>
        <h2 className="mt-3 text-2xl font-semibold text-slate-950">Workflow shortcuts</h2>
      </div>
      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        {actions.map((action) => {
          const Icon = Icons[action.icon] || Icons.ArrowRight;
          return (
            <button key={action.label} type="button" className={`group flex items-center gap-3 rounded-3xl bg-gradient-to-r ${action.color} px-4 py-4 text-left text-white shadow-lg shadow-slate-950/10 transition hover:translate-y-0.5 hover:shadow-xl`}>
              <span className="inline-flex h-12 w-12 items-center justify-center rounded-3xl bg-white/15 text-white shadow-sm">
                <Icon className="h-5 w-5" />
              </span>
              <span className="text-sm font-semibold">{action.label}</span>
            </button>
          );
        })}
      </div>
    </section>
  );
}

export default QuickActions;
