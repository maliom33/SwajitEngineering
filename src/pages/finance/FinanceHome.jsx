import { useMemo, useState } from 'react';
import AdminKpiCard from '../../components/AdminKpiCard';
import HRQuickActions from '../../components/HRQuickActions';

const kpis = [
  { title: 'Total Revenue', value: '₹18.4 Cr', icon: 'Wallet', trend: 'up', trendValue: '+8.4%', description: 'Year to date' },
  { title: 'Monthly Revenue', value: '₹1.52 Cr', icon: 'BadgeDollarSign', trend: 'up', trendValue: '+4.7%', description: 'Current month' },
  { title: 'Pending Payments', value: '₹36 L', icon: 'Clock3', trend: 'down', trendValue: '-1.6%', description: 'Awaiting clearance' },
  { title: 'Completed Payments', value: '₹12.8 Cr', icon: 'CheckCircle2', trend: 'up', trendValue: '+6.1%', description: 'Collected this month' },
  { title: 'Outstanding Invoices', value: '48', icon: 'FileText', trend: 'up', trendValue: '+2.2%', description: 'Open invoices' },
  { title: 'Monthly Expenses', value: '₹74 L', icon: 'TrendingDown', trend: 'down', trendValue: '-2.4%', description: 'Operational spend' },
  { title: 'Payroll Processed', value: '182', icon: 'Users', trend: 'up', trendValue: '+3.8%', description: 'Employees paid' },
  { title: 'Net Profit', value: '₹6.2 Cr', icon: 'ChartNoAxesCombined', trend: 'up', trendValue: '+7.2%', description: 'Net margin' },
];

const recentActivities = ['Invoice Generated', 'Payment Received', 'Salary Processed', 'Payslip Generated', 'GST Report Exported', 'Financial Report Generated'];

function FinanceHome() {
  const [filter, setFilter] = useState('Month');
  const currentDate = useMemo(() => new Date().toLocaleString(), []);

  return (
    <>
      <section className="mb-6 rounded-[2rem] border border-slate-200/80 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-700 p-6 text-white shadow-glass">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.24em] text-slate-300">Finance Manager</p>
            <h1 className="mt-3 text-3xl font-semibold tracking-tight">Welcome Finance Manager</h1>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-300">Manage billing, invoices, payments, payroll, taxation and financial reporting from one centralized finance dashboard.</p>
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
            <h3 className="text-lg font-semibold text-slate-950">Financial Snapshot</h3>
            <div className="flex gap-2">
              {['Month', 'Quarter', 'Year'].map((item) => (
                <button key={item} type="button" onClick={() => setFilter(item)} className={`rounded-full px-3 py-1.5 text-sm ${filter === item ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-700'}`}>{item}</button>
              ))}
            </div>
          </div>
          <div className="mt-5 grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Collection</p>
              <p className="mt-2 text-2xl font-semibold">{filter === 'Quarter' ? '₹4.8 Cr' : filter === 'Year' ? '₹16.1 Cr' : '₹1.52 Cr'}</p>
            </div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Expenses</p>
              <p className="mt-2 text-2xl font-semibold">{filter === 'Quarter' ? '₹2.2 Cr' : filter === 'Year' ? '₹8.6 Cr' : '₹74 L'}</p>
            </div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Margin</p>
              <p className="mt-2 text-2xl font-semibold">{filter === 'Quarter' ? '31%' : filter === 'Year' ? '34%' : '28%'}</p>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <HRQuickActions variant="finance" />
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

export default FinanceHome;
