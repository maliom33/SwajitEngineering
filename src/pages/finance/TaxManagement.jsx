const taxSummary = [
  { label: 'GST Collected', value: '₹3.8 L' },
  { label: 'GST Paid', value: '₹2.1 L' },
  { label: 'Tax Summary', value: '₹1.7 L' },
  { label: 'Monthly Tax', value: '₹48,000' },
];

function TaxManagement() {
  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">GST & Tax Management</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Tax Assessment & GST Summary</h1>
      </section>

      <section className="grid gap-6 lg:grid-cols-2">
        {taxSummary.map((item) => (
          <div key={item.label} className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-slate-950">{item.label}</h3>
            <p className="mt-3 text-2xl font-semibold text-slate-900">{item.value}</p>
          </div>
        ))}
      </section>
    </div>
  );
}

export default TaxManagement;
