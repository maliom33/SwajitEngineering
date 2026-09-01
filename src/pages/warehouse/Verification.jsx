const verificationItems = [
  { order: 'SO-1001', customer: 'SteelWorks Pvt. Ltd.', product: 'MS Plate', required: '50 Tons', available: '60 Tons', status: 'Pending', action: 'Approve' },
  { order: 'SO-1002', customer: 'Metro Infrastructure', product: 'Angle Iron', required: '20 Tons', available: '12 Tons', status: 'Pending', action: 'Reject' },
];

function Verification() {
  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Stock Verification</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Pending Sales Orders</h1>
        <p className="mt-2 text-sm text-slate-600">Verify stock availability and approve or reject orders for dispatch readiness.</p>
      </section>

      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500">
                <th className="px-3 py-3">Order</th>
                <th className="px-3 py-3">Customer</th>
                <th className="px-3 py-3">Product</th>
                <th className="px-3 py-3">Required</th>
                <th className="px-3 py-3">Available</th>
                <th className="px-3 py-3">Status</th>
                <th className="px-3 py-3">Action</th>
              </tr>
            </thead>
            <tbody>
              {verificationItems.map((item) => (
                <tr key={item.order} className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="px-3 py-3 font-medium text-slate-900">{item.order}</td>
                  <td className="px-3 py-3">{item.customer}</td>
                  <td className="px-3 py-3">{item.product}</td>
                  <td className="px-3 py-3">{item.required}</td>
                  <td className="px-3 py-3">{item.available}</td>
                  <td className="px-3 py-3">{item.status}</td>
                  <td className="px-3 py-3">
                    <div className="flex gap-2">
                      <button className="rounded-2xl bg-emerald-600 px-3 py-2 text-white">Approve</button>
                      <button className="rounded-2xl bg-rose-600 px-3 py-2 text-white">Reject</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

export default Verification;
