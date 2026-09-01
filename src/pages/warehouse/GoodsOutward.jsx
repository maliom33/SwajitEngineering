const outward = [
  { order: 'SO-1001', product: 'MS Plate', quantity: '50 Tons', date: '2026-07-01', status: 'Prepared' },
  { order: 'SO-1002', product: 'Angle Iron', quantity: '20 Tons', date: '2026-07-02', status: 'Pending' },
];

function GoodsOutward() {
  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Goods Outward</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Dispatch Planning</h1>
        <p className="mt-2 text-sm text-slate-600">Allocate goods, prepare dispatch, and move approved orders to logistics.</p>
      </section>

      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500">
                <th className="px-3 py-3">Sales Order</th>
                <th className="px-3 py-3">Product</th>
                <th className="px-3 py-3">Quantity</th>
                <th className="px-3 py-3">Dispatch Date</th>
                <th className="px-3 py-3">Dispatch Status</th>
              </tr>
            </thead>
            <tbody>
              {outward.map((item) => (
                <tr key={item.order} className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="px-3 py-3 font-medium text-slate-900">{item.order}</td>
                  <td className="px-3 py-3">{item.product}</td>
                  <td className="px-3 py-3">{item.quantity}</td>
                  <td className="px-3 py-3">{item.date}</td>
                  <td className="px-3 py-3">{item.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

export default GoodsOutward;
