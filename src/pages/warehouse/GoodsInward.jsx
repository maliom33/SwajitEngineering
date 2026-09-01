const deliveries = [
  { supplier: 'Suryametal', material: 'Hot Rolled Coil', quantity: '120 Tons', status: 'Received' },
  { supplier: 'Metro Supply', material: 'Scrap Steel', quantity: '80 Tons', status: 'Pending' },
];

function GoodsInward() {
  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Goods Inward</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Receive Goods</h1>
        <p className="mt-2 text-sm text-slate-600">Record incoming materials, verify quantities, and update inventory records.</p>
      </section>

      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500">
                <th className="px-3 py-3">Supplier</th>
                <th className="px-3 py-3">Material</th>
                <th className="px-3 py-3">Quantity</th>
                <th className="px-3 py-3">Status</th>
              </tr>
            </thead>
            <tbody>
              {deliveries.map((delivery) => (
                <tr key={delivery.supplier + delivery.material} className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="px-3 py-3 font-medium text-slate-900">{delivery.supplier}</td>
                  <td className="px-3 py-3">{delivery.material}</td>
                  <td className="px-3 py-3">{delivery.quantity}</td>
                  <td className="px-3 py-3">{delivery.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

export default GoodsInward;
