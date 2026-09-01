const finishedGoods = [
  { name: 'MS Plate 8mm', quantity: '1200 Tons', dispatchStatus: 'Ready', location: 'WH-A1' },
  { name: 'Angle Iron 50x50', quantity: '430 Tons', dispatchStatus: 'Reserved', location: 'WH-B2' },
];

function FinishedGoods() {
  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Finished Goods</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Dispatch Ready Inventory</h1>
        <p className="mt-2 text-sm text-slate-600">Track finished products, readiness for dispatch, and storage location.</p>
      </section>

      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500">
                <th className="px-3 py-3">Product Name</th>
                <th className="px-3 py-3">Quantity Ready</th>
                <th className="px-3 py-3">Dispatch Status</th>
                <th className="px-3 py-3">Storage Location</th>
              </tr>
            </thead>
            <tbody>
              {finishedGoods.map((item) => (
                <tr key={item.name} className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="px-3 py-3 font-medium text-slate-900">{item.name}</td>
                  <td className="px-3 py-3">{item.quantity}</td>
                  <td className="px-3 py-3">{item.dispatchStatus}</td>
                  <td className="px-3 py-3">{item.location}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

export default FinishedGoods;
