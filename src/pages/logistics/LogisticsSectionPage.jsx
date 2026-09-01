import ApiResourceTable from '../../components/ApiResourceTable';

function LogisticsSectionPage({ title = 'Logistics Module', description = 'This section is ready for deeper logistics operations workflows.', highlights = [] }) {
  const endpoint = title.includes('Driver') ? 'logistics/drivers/' : title.includes('Route') ? 'logistics/routes/' : null;
  if (endpoint) {
    return <ApiResourceTable title={title} description={description} endpoint={endpoint} columns={[{ key: 'id', label: 'ID' }, { key: 'status', label: 'Status' }, { key: 'created_at', label: 'Created' }]} />;
  }
  const fallbackHighlights = [
    'Dispatch visibility',
    'Warehouse handoff tracking',
    'Fleet utilization insights',
  ];

  const items = highlights.length > 0 ? highlights : fallbackHighlights;

  return (
    <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-8 shadow-glass">
      <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Logistics Manager</p>
      <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">{title}</h1>
      <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-600">{description}</p>
      <div className="mt-6 grid gap-4 md:grid-cols-3">
        {items.map((item) => (
          <div key={item} className="rounded-2xl border border-slate-100 bg-slate-50 p-4 text-sm text-slate-700">
            {item}
          </div>
        ))}
      </div>
      <p className="mt-6 rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">No dedicated backend endpoint currently exists for this workflow.</p>
    </section>
  );
}

export default LogisticsSectionPage;
