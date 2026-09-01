import { useMemo, useState } from 'react';
import AdminKpiCard from '../../components/AdminKpiCard';
import HRQuickActions from '../../components/HRQuickActions';

const kpis = [
  { title: 'Total Products', value: '342', icon: 'Boxes', trend: 'up', trendValue: '+5.2%', description: 'Active SKUs' },
  { title: 'Available Inventory', value: '18,420', icon: 'Package', trend: 'up', trendValue: '+8.1%', description: 'Units in stock' },
  { title: 'Low Stock Items', value: '14', icon: 'AlertTriangle', trend: 'down', trendValue: '-1.4%', description: 'Needs reorder' },
  { title: 'Warehouse Capacity', value: '78%', icon: 'HardDrive', trend: 'up', trendValue: '+2.1%', description: 'Utilized' },
  { title: 'Incoming Shipments', value: '12', icon: 'ArrowDownLeft', trend: 'up', trendValue: '+3.0%', description: 'Today' },
  { title: 'Outgoing Shipments', value: '9', icon: 'ArrowUpRight', trend: 'up', trendValue: '+2.4%', description: 'Today' },
  { title: 'Pending Stock Verification', value: '7', icon: 'CheckCircle2', trend: 'down', trendValue: '-1.0%', description: 'Orders pending' },
  { title: 'Approved Orders', value: '21', icon: 'ShieldCheck', trend: 'up', trendValue: '+6.2%', description: 'Ready for dispatch' },
];

const recentActivities = ['Inventory Updated', 'Order Approved', 'Order Rejected', 'Material Received', 'Material Allocated', 'Supplier Added'];

function WarehouseHome() {
  const currentDate = useMemo(() => new Date().toLocaleString(), []);
  const [filter, setFilter] = useState('Today');

  return (
    <>
      <section className="mb-6 rounded-[2rem] border border-slate-200/80 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-700 p-6 text-white shadow-glass">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.24em] text-slate-300">Warehouse Manager</p>
            <h1 className="mt-3 text-3xl font-semibold tracking-tight">Welcome, Warehouse Manager</h1>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-300">Manage inventory, verify stock availability, allocate materials, monitor warehouse capacity, and approve orders for dispatch.</p>
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
            <h3 className="text-lg font-semibold text-slate-950">Warehouse Pulse</h3>
            <div className="flex gap-2">
              {['Today', 'Week', 'Month'].map((item) => (
                <button key={item} type="button" onClick={() => setFilter(item)} className={`rounded-full px-3 py-1.5 text-sm ${filter === item ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-700'}`}>{item}</button>
              ))}
            </div>
          </div>
          <div className="mt-5 grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Incoming</p>
              <p className="mt-2 text-2xl font-semibold">{filter === 'Week' ? '46' : filter === 'Month' ? '132' : '12'}</p>
            </div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Outgoing</p>
              <p className="mt-2 text-2xl font-semibold">{filter === 'Week' ? '39' : filter === 'Month' ? '118' : '9'}</p>
            </div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Pending Verification</p>
              <p className="mt-2 text-2xl font-semibold">{filter === 'Week' ? '11' : filter === 'Month' ? '27' : '7'}</p>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <HRQuickActions variant="sales" />
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

export default WarehouseHome;
