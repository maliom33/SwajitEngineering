function DispatchReports() {
  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Reports</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Dispatch, Challan & Loading Reports</h1>
      </section>

      <section className="grid gap-6 lg:grid-cols-2">
        {['Dispatch Report', 'Challan Report', 'Shipment Report', 'Loading Report', 'Vehicle Dispatch Report'].map((report) => (
          <div key={report} className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-slate-950">{report}</h3>
            <p className="mt-3 text-sm text-slate-600">Export as PDF, Excel or print-ready summary for supervisor review.</p>
            <div className="mt-4 flex gap-3">
              <button type="button" className="rounded-full bg-slate-900 px-4 py-2 text-sm font-medium text-white">Export PDF</button>
              <button type="button" className="rounded-full border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700">Print</button>
            </div>
          </div>
        ))}
      </section>
    </div>
  );
}

export default DispatchReports;
