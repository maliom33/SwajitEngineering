const allocations = [
  { order: 'SO-1001', customer: 'SteelWorks Pvt. Ltd.', product: 'MS Plate', quantity: '50 Tons', reserved: 'Reserved', status: 'Ready for Dispatch' },
  { order: 'SO-1002', customer: 'Metro Infrastructure', product: 'Angle Iron', quantity: '20 Tons', reserved: 'Pending', status: 'Awaiting Allocation' },
];

function Allocation() {
  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Material Allocation</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Pending Orders & Reserved Inventory</h1>
        <p className="mt-2 text-sm text-slate-600">Reserve stock for approved orders and prepare it for dispatch.</p>
      </section>

      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500">
                <th className="px-3 py-3">Order</th>
                <th className="px-3 py-3">Customer</th>
                <th className="px-3 py-3">Product</th>
                <th className="px-3 py-3">Quantity</th>
                <th className="px-3 py-3">Reserved</th>
                <th className="px-3 py-3">Status</th>
              </tr>
            </thead>
            <tbody>
              {allocations.map((item) => (
                <tr key={item.order} className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="px-3 py-3 font-medium text-slate-900">{item.order}</td>
                  <td className="px-3 py-3">{item.customer}</td>
                  <td className="px-3 py-3">{item.product}</td>
                  <td className="px-3 py-3">{item.quantity}</td>
                  <td className="px-3 py-3">{item.reserved}</td>
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

export default Allocation;
