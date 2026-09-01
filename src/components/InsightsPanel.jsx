function InsightsPanel({ insights }) {
  return (
    <section className="card-glass rounded-3xl border border-slate-200/80 p-6 shadow-glass">
      <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.24em] text-slate-400">AI Insights</p>
          <h2 className="mt-3 text-2xl font-semibold text-slate-950">AI Business Insights</h2>
        </div>
        <span className="inline-flex rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-700">Intelligent recommendations</span>
      </div>
      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        {insights.map((item) => (
          <div key={item.title} className="rounded-3xl border border-slate-200/80 bg-white/90 p-5 shadow-sm transition hover:-translate-y-0.5">
            <p className="text-sm font-semibold text-slate-950">{item.title}</p>
            <p className="mt-3 text-sm leading-6 text-slate-600">{item.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

export default InsightsPanel;
