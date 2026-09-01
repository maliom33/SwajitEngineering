const materials = [
  { name: 'Hot Rolled Coil', supplier: 'Suryametal', quantity: '480 Tons', purchaseDate: '2026-06-20', stock: '430 Tons' },
  { name: 'Scrap Steel', supplier: 'Metro Supply', quantity: '260 Tons', purchaseDate: '2026-06-18', stock: '210 Tons' },
];

function RawMaterials() {
  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Raw Materials</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Material Inventory</h1>
        <p className="mt-2 text-sm text-slate-600">Manage inbound raw materials, supplier details, and stock levels.</p>
      </section>

      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500">
                <th className="px-3 py-3">Material Name</th>
                <th className="px-3 py-3">Supplier</th>
                <th className="px-3 py-3">Quantity</th>
                <th className="px-3 py-3">Purchase Date</th>
                <th className="px-3 py-3">Current Stock</th>
              </tr>
            </thead>
            <tbody>
              {materials.map((material) => (
                <tr key={material.name} className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="px-3 py-3 font-medium text-slate-900">{material.name}</td>
                  <td className="px-3 py-3">{material.supplier}</td>
                  <td className="px-3 py-3">{material.quantity}</td>
                  <td className="px-3 py-3">{material.purchaseDate}</td>
                  <td className="px-3 py-3">{material.stock}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

export default RawMaterials;
