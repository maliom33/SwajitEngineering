function FinancialReports() {
  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Financial Reports</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Revenue, Expense, GST & Payroll Reports</h1>
      </section>

      <section className="grid gap-6 lg:grid-cols-2">
        {['Revenue Report', 'Expense Report', 'Profit & Loss Report', 'Payroll Report', 'GST Report', 'Payment Report', 'Invoice Report'].map((report) => (
          <div key={report} className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-slate-950">{report}</h3>
            <p className="mt-3 text-sm text-slate-600">Export as PDF, Excel or print-ready summary for management review.</p>
          </div>
        ))}
      </section>
    </div>
  );
}

export default FinancialReports;
