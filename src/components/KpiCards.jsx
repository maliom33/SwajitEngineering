import * as Icons from 'lucide-react';

function KpiCards({ metrics }) {
  return (
    <section className="grid gap-6 lg:grid-cols-2 xl:grid-cols-4">
      {metrics.map((metric) => {
        const Icon = Icons[metric.icon] || Icons.BarChart3;
        return (
          <article key={metric.title} className="card-glass rounded-3xl border border-slate-200/80 p-6 shadow-glass transition hover:-translate-y-0.5">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-sm font-medium uppercase tracking-[0.24em] text-slate-400">{metric.title}</p>
                <p className="mt-4 text-3xl font-semibold text-slate-950">{metric.value}</p>
              </div>
              <div className={`inline-flex h-14 w-14 items-center justify-center rounded-3xl ${metric.color}`}>
                <Icon className="h-6 w-6" />
              </div>
            </div>
            <div className="mt-5 flex items-center gap-2 text-sm text-slate-500">
              <span className={`inline-flex items-center rounded-full px-3 py-1 font-medium ${metric.trend === 'up' ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'}`}>
                {metric.percent}
              </span>
              <span>{metric.trend === 'up' ? 'Month-over-month growth' : 'Month-over-month change'}</span>
            </div>
          </article>
        );
      })}
    </section>
  );
}

export default KpiCards;
