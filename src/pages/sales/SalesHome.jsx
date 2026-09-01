import { useMemo, useState } from 'react';
import AdminKpiCard from '../../components/AdminKpiCard';
import HRQuickActions from '../../components/HRQuickActions';

const kpis = [
  { title: 'Total Customers', value: '184', icon: 'Users', trend: 'up', trendValue: '+8.4%', description: 'Active accounts' },
  { title: 'Orders Created Today', value: '27', icon: 'ShoppingCart', trend: 'up', trendValue: '+6.2%', description: 'New orders' },
  { title: 'Pending Orders', value: '11', icon: 'Clock', trend: 'down', trendValue: '-1.3%', description: 'Awaiting approval' },
  { title: 'Approved Orders', value: '16', icon: 'CheckCircle2', trend: 'up', trendValue: '+4.8%', description: 'Approved this week' },
  { title: 'Monthly Sales', value: '₹2.4 Cr', icon: 'CircleDollarSign', trend: 'up', trendValue: '+12.5%', description: 'This month' },
  { title: 'Revenue Generated', value: '₹1.8 Cr', icon: 'TrendingUp', trend: 'up', trendValue: '+9.1%', description: 'Collected' },
  { title: 'Quotations Sent', value: '39', icon: 'FileText', trend: 'up', trendValue: '+5.6%', description: 'Recent quotes' },
  { title: 'Customer Satisfaction', value: '94%', icon: 'Smile', trend: 'up', trendValue: '+2.1%', description: 'CSAT score' },
];

const recentActivities = [
  'Customer Registered',
  'Quotation Sent',
  'Sales Order Created',
  'Purchase Order Uploaded',
  'Warehouse Approved Order',
  'Invoice Generated',
];

function SalesHome() {
  const currentDate = useMemo(() => new Date().toLocaleString(), []);
  const [activeFilter, setActiveFilter] = useState('Overview');

  return (
    <>
      <section className="mb-6 rounded-[2rem] border border-slate-200/80 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-700 p-6 text-white shadow-glass">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.24em] text-slate-300">Sales Executive</p>
            <h1 className="mt-3 text-3xl font-semibold tracking-tight">Welcome, Sales Executive</h1>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-300">Manage customers, sales orders, purchase orders, quotations, and customer communication from one centralized sales command center.</p>
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

      <section className="mb-6 grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <div className="rounded-3xl border border-slate-200/80 bg-white/90 p-6 shadow-sm">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <h3 className="text-lg font-semibold text-slate-950">Sales Snapshot</h3>
            <div className="flex gap-2">
              {['Overview', 'Today', 'This Week'].map((filter) => (
                <button
                  key={filter}
                  type="button"
                  onClick={() => setActiveFilter(filter)}
                  className={`rounded-full px-3 py-1.5 text-sm ${activeFilter === filter ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-700'}`}
                >
                  {filter}
                </button>
              ))}
            </div>
          </div>
          <div className="mt-5 grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Orders Submitted</p>
              <p className="mt-2 text-2xl font-semibold">{activeFilter === 'Today' ? '14' : activeFilter === 'This Week' ? '82' : '27'}</p>
            </div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">New Leads</p>
              <p className="mt-2 text-2xl font-semibold">{activeFilter === 'Today' ? '6' : activeFilter === 'This Week' ? '19' : '12'}</p>
            </div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Follow-ups</p>
              <p className="mt-2 text-2xl font-semibold">{activeFilter === 'Today' ? '4' : activeFilter === 'This Week' ? '17' : '8'}</p>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <HRQuickActions variant="director" />
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

export default SalesHome;
