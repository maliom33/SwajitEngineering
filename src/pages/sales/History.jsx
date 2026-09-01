const historyCards = [
  { title: 'Past Orders', value: '64', detail: 'Completed orders' },
  { title: 'Purchase History', value: '31', detail: 'Purchase documents linked' },
  { title: 'Invoices', value: '48', detail: 'Raised this quarter' },
  { title: 'Payments', value: '₹1.2 Cr', detail: 'Received' },
  { title: 'Customer Communication', value: '12', detail: 'Open conversations' },
  { title: 'Recent Activities', value: '9', detail: 'Today' },
];

function History() {
  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Customer History</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Client Relationship Timeline</h1>
        <p className="mt-2 text-sm text-slate-600">Track order history, invoices, payments, communication, and recent activities for each customer.</p>
      </section>

      <section className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {historyCards.map((card) => (
          <div key={card.title} className="rounded-3xl border border-slate-200/80 bg-white/90 p-6 shadow-sm">
            <h3 className="text-lg font-semibold text-slate-950">{card.title}</h3>
            <p className="mt-4 text-3xl font-semibold text-slate-900">{card.value}</p>
            <p className="mt-2 text-sm text-slate-500">{card.detail}</p>
          </div>
        ))}
      </section>
    </div>
  );
}

export default History;
