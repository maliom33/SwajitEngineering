import * as Icons from 'lucide-react';

function AdminKpiCard({ title, value, icon: iconName, trend, trendValue, description, color }) {
  const Icon = Icons[iconName] || Icons.BarChart3;
  
  return (
    <article className="card-glass rounded-3xl border border-slate-200/80 bg-white/90 p-6 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium uppercase tracking-[0.24em] text-slate-400">{title}</p>
          <p className="mt-4 text-3xl font-semibold text-slate-950">{value}</p>
          <p className="mt-2 text-xs text-slate-500">{description}</p>
        </div>
        <div className={`inline-flex h-14 w-14 items-center justify-center rounded-3xl ${color}`}>
          <Icon className="h-6 w-6" />
        </div>
      </div>
      {trend && (
        <div className="mt-4 flex items-center gap-2 text-sm">
          <span className={`inline-flex items-center rounded-full px-3 py-1 font-medium ${trend === 'up' ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'}`}>
            {trendValue}
          </span>
        </div>
      )}
    </article>
  );
}

export default AdminKpiCard;
