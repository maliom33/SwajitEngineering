function Reports() {
  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Reports</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Warehouse Reports</h1>
        <p className="mt-2 text-sm text-slate-600">Export inventory, stock verification, inward, outward, utilization, and low stock reports.</p>
      </section>

      <section className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {['Inventory Report', 'Stock Verification Report', 'Goods Inward Report', 'Goods Outward Report', 'Warehouse Utilization Report', 'Low Stock Report'].map((report) => (
          <div key={report} className="rounded-3xl border border-slate-200/80 bg-white/90 p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-slate-950">{report}</h3>
            <div className="mt-4 flex flex-wrap gap-2">
              <button className="rounded-2xl border border-slate-200 px-3 py-2 text-sm">View</button>
              <button className="rounded-2xl border border-slate-200 px-3 py-2 text-sm">PDF</button>
              <button className="rounded-2xl border border-slate-200 px-3 py-2 text-sm">Excel</button>
              <button className="rounded-2xl border border-slate-200 px-3 py-2 text-sm">Print</button>
            </div>
          </div>
        ))}
      </section>
    </div>
  );
}

export default Reports;
