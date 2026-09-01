import { useMemo, useState } from 'react';

const initialOrders = [
  { id: 'LD-101', customer: 'SteelWorks Pvt. Ltd.', product: 'MS Plate', quantity: '50 Tons', destination: 'Mumbai', priority: 'High', deliveryDate: '2026-07-06', status: 'Pending' },
  { id: 'LD-102', customer: 'Metro Infrastructure', product: 'Angle Iron', quantity: '20 Tons', destination: 'Pune', priority: 'Medium', deliveryDate: '2026-07-07', status: 'Approved' },
];

function Orders() {
  const [orders] = useState(initialOrders);
  const [search, setSearch] = useState('');

  const visibleOrders = useMemo(() => orders.filter((order) => [order.id, order.customer, order.destination, order.status].some((value) => value.toLowerCase().includes(search.toLowerCase()))), [orders, search]);

  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Order Management</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Pending & Approved Orders</h1>
        <p className="mt-2 text-sm text-slate-600">View approved orders and assign trucks and drivers for dispatch.</p>
      </section>

      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <div className="mb-4 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
          <h3 className="text-lg font-semibold text-slate-950">Order List</h3>
          <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search orders" className="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 lg:max-w-xs" />
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500">
                <th className="px-3 py-3">Order No.</th>
                <th className="px-3 py-3">Customer</th>
                <th className="px-3 py-3">Product</th>
                <th className="px-3 py-3">Quantity</th>
                <th className="px-3 py-3">Destination</th>
                <th className="px-3 py-3">Priority</th>
                <th className="px-3 py-3">Delivery Date</th>
                <th className="px-3 py-3">Status</th>
              </tr>
            </thead>
            <tbody>
              {visibleOrders.map((order) => (
                <tr key={order.id} className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="px-3 py-3 font-medium text-slate-900">{order.id}</td>
                  <td className="px-3 py-3">{order.customer}</td>
                  <td className="px-3 py-3">{order.product}</td>
                  <td className="px-3 py-3">{order.quantity}</td>
                  <td className="px-3 py-3">{order.destination}</td>
                  <td className="px-3 py-3">{order.priority}</td>
                  <td className="px-3 py-3">{order.deliveryDate}</td>
                  <td className="px-3 py-3">{order.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

export default Orders;
