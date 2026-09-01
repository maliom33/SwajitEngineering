import { useMemo, useState } from 'react';

const initialPurchaseOrders = [
  { id: 'PO-2001', customer: 'SteelWorks Pvt. Ltd.', date: '2026-07-01', status: 'Uploaded', document: 'PO-2001.pdf' },
  { id: 'PO-2002', customer: 'Metro Infrastructure', date: '2026-06-30', status: 'Pending', document: 'PO-2002.pdf' },
];

function PurchaseOrders() {
  const [purchaseOrders, setPurchaseOrders] = useState(initialPurchaseOrders);
  const [search, setSearch] = useState('');

  const visiblePurchaseOrders = useMemo(() => purchaseOrders.filter((order) => [order.id, order.customer, order.status].some((value) => value.toLowerCase().includes(search.toLowerCase()))), [purchaseOrders, search]);

  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Purchase Orders</p>
            <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Upload & Review Orders</h1>
            <p className="mt-2 text-sm text-slate-600">Manage purchase order documents, status, and retrieval.</p>
          </div>
          <button type="button" className="rounded-2xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white">Upload Purchase Order</button>
        </div>
      </section>

      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <div className="mb-4 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
          <h3 className="text-lg font-semibold text-slate-950">Purchase Order List</h3>
          <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search purchase orders" className="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 lg:max-w-xs" />
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500">
                <th className="px-3 py-3">PO Number</th>
                <th className="px-3 py-3">Customer</th>
                <th className="px-3 py-3">Date</th>
                <th className="px-3 py-3">Status</th>
                <th className="px-3 py-3">Document</th>
              </tr>
            </thead>
            <tbody>
              {visiblePurchaseOrders.map((order) => (
                <tr key={order.id} className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="px-3 py-3 font-medium text-slate-900">{order.id}</td>
                  <td className="px-3 py-3">{order.customer}</td>
                  <td className="px-3 py-3">{order.date}</td>
                  <td className="px-3 py-3">{order.status}</td>
                  <td className="px-3 py-3">{order.document}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

export default PurchaseOrders;
