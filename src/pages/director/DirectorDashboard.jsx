import HRQuickActions from '../../components/HRQuickActions';
import ApiAnalyticsSummary from '../../components/ApiAnalyticsSummary';

function DirectorDashboard() {
  return (
    <>
      <section className="mb-6 rounded-[2rem] border border-slate-200/80 bg-gradient-to-br from-amber-50 via-white to-slate-100 p-6 shadow-glass">
        <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Executive Overview</p>
            <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">Executive Command Center</h1>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-600">Track business health, operational performance, delivery reliability, warehouse throughput, and financial outlook from one leadership dashboard.</p>
          </div>
          <div className="rounded-3xl border border-slate-200/80 bg-white/80 px-5 py-4 shadow-sm">
            <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Current Date & Time</p>
            <p className="mt-2 text-lg font-semibold text-slate-950">Live API analytics</p>
          </div>
        </div>
      </section>

      <section className="mb-6 grid gap-6 xl:grid-cols-[1.35fr_0.85fr]">
        <ApiAnalyticsSummary title="Executive Metrics" description="Live workforce, sales, warehouse, logistics, dispatch, and finance metrics." endpoint="analytics/executive-dashboard/" groups={[{ label: 'Workforce', key: 'workforce' }, { label: 'Sales', key: 'sales' }, { label: 'Warehouse', key: 'warehouse' }, { label: 'Logistics', key: 'logistics' }, { label: 'Dispatch', key: 'dispatch' }, { label: 'Finance', key: 'finance' }]} />
        <HRQuickActions variant="director" />
      </section>
    </>
  );
}

export default DirectorDashboard;
