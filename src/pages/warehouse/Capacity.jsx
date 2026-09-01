function Capacity() {
  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Warehouse Capacity</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Storage Utilization Overview</h1>
        <p className="mt-2 text-sm text-slate-600">Monitor storage utilization, available capacity, and inventory growth trends.</p>
      </section>

      <section className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-950">Warehouse Utilization</h3>
          <div className="mt-4 rounded-2xl border border-slate-100 bg-slate-50 p-6 text-center">
            <p className="text-4xl font-semibold text-slate-900">78%</p>
            <p className="mt-2 text-sm text-slate-500">Used Capacity</p>
          </div>
        </div>
        <div className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-950">Monthly Inventory Growth</h3>
          <div className="mt-4 rounded-2xl border border-slate-100 bg-slate-50 p-6 text-center">
            <p className="text-4xl font-semibold text-slate-900">+12%</p>
            <p className="mt-2 text-sm text-slate-500">Compared to last month</p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Capacity;
