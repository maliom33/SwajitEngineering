import {
  ResponsiveContainer,
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  BarChart,
  Bar,
  AreaChart,
  Area,
  PieChart,
  Pie,
  Cell,
} from 'recharts';

function AnalyticsSection({ chartData }) {
  const warehouseColors = ['#1E3A5F', '#64748B', '#2563EB', '#9333EA'];

  return (
    <section className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
      <div className="grid gap-6">
        <div className="card-glass rounded-3xl border border-slate-200/80 p-6 shadow-glass">
          <div className="flex items-center justify-between gap-4">
            <div>
              <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Financial analytics</p>
              <h2 className="mt-3 text-2xl font-semibold text-slate-950">Revenue vs Expenses</h2>
            </div>
            <span className="rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-700">Monthly trend</span>
          </div>
          <div className="mt-6 h-72">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData.revenue} margin={{ top: 10, right: 12, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#cbd5e1" opacity={0.45} />
                <XAxis dataKey="month" tickLine={false} axisLine={false} tick={{ fill: '#475569', fontSize: 12 }} />
                <YAxis tickLine={false} axisLine={false} tick={{ fill: '#475569', fontSize: 12 }} />
                <Tooltip contentStyle={{ borderRadius: 16, borderColor: '#e2e8f0' }} />
                <Line type="monotone" dataKey="revenue" stroke="#1E3A5F" strokeWidth={3} dot={{ r: 4, fill: '#1E3A5F' }} />
                <Line type="monotone" dataKey="expenses" stroke="#64748B" strokeWidth={3} dot={{ r: 4, fill: '#64748B' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card-glass rounded-3xl border border-slate-200/80 p-6 shadow-glass">
          <div className="flex items-center justify-between gap-4">
            <div>
              <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Delivery analytics</p>
              <h2 className="mt-3 text-2xl font-semibold text-slate-950">Monthly Delivery Performance</h2>
            </div>
            <span className="rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-700">Logistics intel</span>
          </div>
          <div className="mt-6 h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData.delivery} margin={{ top: 10, right: 0, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#cbd5e1" opacity={0.45} />
                <XAxis dataKey="month" tickLine={false} axisLine={false} tick={{ fill: '#475569', fontSize: 12 }} />
                <YAxis tickLine={false} axisLine={false} tick={{ fill: '#475569', fontSize: 12 }} />
                <Tooltip contentStyle={{ borderRadius: 16, borderColor: '#e2e8f0' }} />
                <Bar dataKey="deliveries" radius={[10, 10, 0, 0]} fill="#2563EB" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="grid gap-6">
        <div className="card-glass rounded-3xl border border-slate-200/80 p-6 shadow-glass">
          <div className="flex items-center justify-between gap-4">
            <div>
              <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Attendance analytics</p>
              <h2 className="mt-3 text-2xl font-semibold text-slate-950">Attendance Trend</h2>
            </div>
            <span className="rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-700">Workforce pulse</span>
          </div>
          <div className="mt-6 h-56">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData.attendance} margin={{ top: 5, right: 0, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="attendanceGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#1E3A5F" stopOpacity={0.35} />
                    <stop offset="95%" stopColor="#1E3A5F" stopOpacity={0.03} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#cbd5e1" opacity={0.35} />
                <XAxis dataKey="day" tickLine={false} axisLine={false} tick={{ fill: '#475569', fontSize: 12 }} />
                <YAxis tickLine={false} axisLine={false} tick={{ fill: '#475569', fontSize: 12 }} />
                <Tooltip contentStyle={{ borderRadius: 16, borderColor: '#e2e8f0' }} />
                <Area type="monotone" dataKey="rate" stroke="#1E3A5F" strokeWidth={3} fill="url(#attendanceGradient)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card-glass rounded-3xl border border-slate-200/80 p-6 shadow-glass">
          <div className="flex items-center justify-between gap-4">
            <div>
              <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Inventory analytics</p>
              <h2 className="mt-3 text-2xl font-semibold text-slate-950">Warehouse Stock Distribution</h2>
            </div>
            <span className="rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-700">Stock share</span>
          </div>
          <div className="mt-6 h-56">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={chartData.warehouse} dataKey="value" nameKey="name" innerRadius={50} outerRadius={90} paddingAngle={5}>
                  {chartData.warehouse.map((entry, index) => (
                    <Cell key={entry.name} fill={warehouseColors[index % warehouseColors.length]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ borderRadius: 16, borderColor: '#e2e8f0' }} />
              </PieChart>
            </ResponsiveContainer>
            <div className="mt-5 grid grid-cols-2 gap-3">
              {chartData.warehouse.map((item, index) => (
                <div key={item.name} className="flex items-center gap-3 rounded-3xl border border-slate-200/80 bg-white/90 p-3 shadow-sm">
                  <div className="h-3.5 w-3.5 rounded-full" style={{ backgroundColor: warehouseColors[index % warehouseColors.length] }} />
                  <div>
                    <p className="text-sm font-semibold text-slate-950">{item.name}</p>
                    <p className="text-xs text-slate-500">{item.value}% of inventory</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default AnalyticsSection;
