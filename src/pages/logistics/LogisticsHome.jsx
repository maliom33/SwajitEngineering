import { useMemo, useState } from 'react';
import AdminKpiCard from '../../components/AdminKpiCard';
import HRQuickActions from '../../components/HRQuickActions';

const kpis = [
  { title: 'Pending Orders', value: '14', icon: 'Package', trend: 'up', trendValue: '+3.2%', description: 'Awaiting dispatch' },
  { title: 'Active Deliveries', value: '9', icon: 'Truck', trend: 'up', trendValue: '+1.8%', description: 'In transit' },
  { title: 'Completed Deliveries', value: '31', icon: 'CheckCircle2', trend: 'up', trendValue: '+6.4%', description: 'This week' },
  { title: 'Delayed Deliveries', value: '4', icon: 'Clock3', trend: 'down', trendValue: '-0.8%', description: 'Needs attention' },
  { title: 'Available Trucks', value: '7', icon: 'Car', trend: 'up', trendValue: '+2.0%', description: 'Ready for assignment' },
  { title: 'Trucks On Road', value: '12', icon: 'Route', trend: 'up', trendValue: '+4.1%', description: 'Active fleet' },
  { title: 'Drivers On Duty', value: '11', icon: 'UserCircle2', trend: 'up', trendValue: '+1.2%', description: 'On shift' },
  { title: 'Fleet Utilization', value: '86%', icon: 'BarChart3', trend: 'up', trendValue: '+2.6%', description: 'Utilization' },
  { title: 'Monthly Transportation Cost', value: '₹3.2 Cr', icon: 'CircleDollarSign', trend: 'down', trendValue: '-1.4%', description: 'This month' },
  { title: 'Average Delivery Time', value: '18 hrs', icon: 'TimerReset', trend: 'down', trendValue: '-2.1%', description: 'Average transit' },
];

const recentActivities = ['Truck Assigned', 'Driver Assigned', 'Delivery Started', 'Route Optimized', 'Delivery Completed', 'Maintenance Scheduled', 'Fuel Updated'];

function LogisticsHome() {
  const currentDate = useMemo(() => new Date().toLocaleString(), []);
  const [filter, setFilter] = useState('Today');

  return (
    <>
      <section className="mb-6 rounded-[2rem] border border-slate-200/80 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-700 p-6 text-white shadow-glass">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.24em] text-slate-300">Logistics Manager</p>
            <h1 className="mt-3 text-3xl font-semibold tracking-tight">Welcome, Logistics Manager</h1>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-300">Manage transportation, fleet operations, route optimization, deliveries, and logistics performance from one centralized dashboard.</p>
          </div>
          <div className="rounded-3xl border border-white/15 bg-white/10 px-5 py-4 shadow-sm backdrop-blur-sm">
            <p className="text-sm uppercase tracking-[0.24em] text-slate-300">Current Date & Time</p>
            <p className="mt-2 text-lg font-semibold">{currentDate}</p>
          </div>
        </div>
      </section>

      <section className="mb-6 grid gap-6 lg:grid-cols-2 xl:grid-cols-5">
        {kpis.map((metric) => (
          <AdminKpiCard key={metric.title} title={metric.title} value={metric.value} icon={metric.icon} trend={metric.trend} trendValue={metric.trendValue} description={metric.description} />
        ))}
      </section>

      <section className="mb-6 grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-3xl border border-slate-200/80 bg-white/90 p-6 shadow-sm">
          <div className="flex items-center justify-between gap-3">
            <h3 className="text-lg font-semibold text-slate-950">Fleet Snapshot</h3>
            <div className="flex gap-2">
              {['Today', 'Week', 'Month'].map((item) => (
                <button key={item} type="button" onClick={() => setFilter(item)} className={`rounded-full px-3 py-1.5 text-sm ${filter === item ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-700'}`}>{item}</button>
              ))}
            </div>
          </div>
          <div className="mt-5 grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Dispatches</p>
              <p className="mt-2 text-2xl font-semibold">{filter === 'Week' ? '42' : filter === 'Month' ? '128' : '9'}</p>
            </div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Delays</p>
              <p className="mt-2 text-2xl font-semibold">{filter === 'Week' ? '3' : filter === 'Month' ? '11' : '1'}</p>
            </div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Avg. Cost</p>
              <p className="mt-2 text-2xl font-semibold">{filter === 'Week' ? '₹21k' : filter === 'Month' ? '₹84k' : '₹3.8k'}</p>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <HRQuickActions variant="logistics" />
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

export default LogisticsHome;
