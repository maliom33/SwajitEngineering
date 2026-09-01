import { useMemo, useState } from 'react';
import AdminKpiCard from '../../components/AdminKpiCard';
import HRQuickActions from '../../components/HRQuickActions';

const kpis = [
  { title: 'Pending Dispatch Orders', value: '12', icon: 'Package', trend: 'up', trendValue: '+4.1%', description: 'Awaiting preparation' },
  { title: 'Ready Shipments', value: '8', icon: 'CheckCircle2', trend: 'up', trendValue: '+2.3%', description: 'Ready for vehicle dispatch' },
  { title: 'Dispatches Today', value: '6', icon: 'Truck', trend: 'up', trendValue: '+1.7%', description: 'Planned for today' },
  { title: 'Completed Dispatches', value: '24', icon: 'BadgeCheck', trend: 'up', trendValue: '+6.2%', description: 'Completed this week' },
  { title: 'Delivery Challans Generated', value: '18', icon: 'FileText', trend: 'up', trendValue: '+3.4%', description: 'Documentation completed' },
  { title: 'Vehicles Ready', value: '5', icon: 'Car', trend: 'up', trendValue: '+1.1%', description: 'Available trucks' },
  { title: 'Loading Completed', value: '7', icon: 'PackageCheck', trend: 'up', trendValue: '+2.8%', description: 'Verified loads' },
  { title: 'Delayed Dispatches', value: '2', icon: 'Clock3', trend: 'down', trendValue: '-0.9%', description: 'Needs follow-up' },
];

const recentActivities = ['Shipment Prepared', 'Loading Verified', 'Challan Generated', 'Vehicle Dispatched', 'Dispatch Completed', 'Schedule Updated'];

function DispatchHome() {
  const [filter, setFilter] = useState('Today');
  const currentDate = useMemo(() => new Date().toLocaleString(), []);

  return (
    <>
      <section className="mb-6 rounded-[2rem] border border-slate-200/80 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-700 p-6 text-white shadow-glass">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.24em] text-slate-300">Dispatch Executive</p>
            <h1 className="mt-3 text-3xl font-semibold tracking-tight">Welcome Dispatch Executive</h1>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-300">Manage shipment preparation, loading verification, dispatch documentation and vehicle dispatch operations from one centralized dashboard.</p>
          </div>
          <div className="rounded-3xl border border-white/15 bg-white/10 px-5 py-4 shadow-sm backdrop-blur-sm">
            <p className="text-sm uppercase tracking-[0.24em] text-slate-300">Current Date & Time</p>
            <p className="mt-2 text-lg font-semibold">{currentDate}</p>
          </div>
        </div>
      </section>

      <section className="mb-6 grid gap-6 lg:grid-cols-2 xl:grid-cols-4">
        {kpis.map((metric) => (
          <AdminKpiCard key={metric.title} title={metric.title} value={metric.value} icon={metric.icon} trend={metric.trend} trendValue={metric.trendValue} description={metric.description} />
        ))}
      </section>

      <section className="mb-6 grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
        <div className="rounded-3xl border border-slate-200/80 bg-white/90 p-6 shadow-sm">
          <div className="flex items-center justify-between gap-3">
            <h3 className="text-lg font-semibold text-slate-950">Dispatch Overview</h3>
            <div className="flex gap-2">
              {['Today', 'Week', 'Month'].map((item) => (
                <button key={item} type="button" onClick={() => setFilter(item)} className={`rounded-full px-3 py-1.5 text-sm ${filter === item ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-700'}`}>{item}</button>
              ))}
            </div>
          </div>
          <div className="mt-5 grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Planned</p>
              <p className="mt-2 text-2xl font-semibold">{filter === 'Week' ? '34' : filter === 'Month' ? '112' : '6'}</p>
            </div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Completed</p>
              <p className="mt-2 text-2xl font-semibold">{filter === 'Week' ? '28' : filter === 'Month' ? '96' : '4'}</p>
            </div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Delayed</p>
              <p className="mt-2 text-2xl font-semibold">{filter === 'Week' ? '3' : filter === 'Month' ? '9' : '1'}</p>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <HRQuickActions variant="dispatch" />
          <div className="rounded-3xl border border-slate-200/80 bg-white/90 p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-slate-950">Recent Activities</h3>
            <div className="mt-4 space-y-3">
              {recentActivities.map((item) => (
                <div key={item} className="rounded-2xl border border-slate-100 bg-slate-50 p-4 text-sm text-slate-700">{item}</div>
              ))}
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

export default DispatchHome;
