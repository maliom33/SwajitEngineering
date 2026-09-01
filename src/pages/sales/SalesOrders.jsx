import { useMemo, useState } from 'react';

const initialOrders = [
  { id: 'SO-1001', customer: 'SteelWorks Pvt. Ltd.', product: 'MS Plate', quantity: '50', unit: 'Ton', amount: '₹8,50,000', priority: 'High', status: 'Approved' },
  { id: 'SO-1002', customer: 'Metro Infrastructure', product: 'Angle Iron', quantity: '20', unit: 'Ton', amount: '₹3,20,000', priority: 'Medium', status: 'Pending' },
];

function SalesOrders() {
  const [orders, setOrders] = useState(initialOrders);
  const [search, setSearch] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ customer: '', company: '', category: '', product: '', grade: '', quantity: '', unit: '', price: '', total: '', deliveryDate: '', address: '', priority: 'Medium', remarks: '' });

  const visibleOrders = useMemo(() => orders.filter((order) => [order.id, order.customer, order.product].some((value) => value.toLowerCase().includes(search.toLowerCase()))), [orders, search]);

  const handleSave = (e) => {
    e.preventDefault();
    const newOrder = { id: `SO-${1003 + orders.length}`, customer: form.customer, product: form.product, quantity: form.quantity, unit: form.unit, amount: form.total, priority: form.priority, status: 'Draft' };
    setOrders((prev) => [newOrder, ...prev]);
    setShowForm(false);
    setForm({ customer: '', company: '', category: '', product: '', grade: '', quantity: '', unit: '', price: '', total: '', deliveryDate: '', address: '', priority: 'Medium', remarks: '' });
  };

  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Sales Orders</p>
            <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Create & Manage Orders</h1>
            <p className="mt-2 text-sm text-slate-600">Create sales orders, review them, and track their approval path.</p>
          </div>
          <button type="button" onClick={() => setShowForm((prev) => !prev)} className="rounded-2xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white">{showForm ? 'Close Form' : 'Create Sales Order'}</button>
        </div>
      </section>

      {showForm && (
        <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-950">Sales Order Form</h3>
          <form onSubmit={handleSave} className="mt-5 grid gap-4 md:grid-cols-2">
            <input required value={form.customer} onChange={(e) => setForm({ ...form, customer: e.target.value })} placeholder="Customer Name" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3" />
            <input value={form.company} onChange={(e) => setForm({ ...form, company: e.target.value })} placeholder="Company Name" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3" />
            <input value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} placeholder="Product Category" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3" />
            <input required value={form.product} onChange={(e) => setForm({ ...form, product: e.target.value })} placeholder="Product Name" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3" />
            <input value={form.grade} onChange={(e) => setForm({ ...form, grade: e.target.value })} placeholder="Steel Grade" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3" />
            <input required value={form.quantity} onChange={(e) => setForm({ ...form, quantity: e.target.value })} placeholder="Quantity" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3" />
            <input value={form.unit} onChange={(e) => setForm({ ...form, unit: e.target.value })} placeholder="Unit" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3" />
            <input value={form.price} onChange={(e) => setForm({ ...form, price: e.target.value })} placeholder="Unit Price" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3" />
            <input value={form.total} onChange={(e) => setForm({ ...form, total: e.target.value })} placeholder="Total Amount" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3" />
            <input type="date" value={form.deliveryDate} onChange={(e) => setForm({ ...form, deliveryDate: e.target.value })} className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3" />
            <input value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} placeholder="Delivery Address" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3" />
            <select value={form.priority} onChange={(e) => setForm({ ...form, priority: e.target.value })} className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
            </select>
            <textarea value={form.remarks} onChange={(e) => setForm({ ...form, remarks: e.target.value })} rows="3" placeholder="Remarks" className="md:col-span-2 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3" />
            <div className="md:col-span-2 flex justify-end gap-3">
              <button type="button" onClick={() => setShowForm(false)} className="rounded-2xl border border-slate-200 px-4 py-3">Cancel</button>
              <button type="submit" className="rounded-2xl bg-brand-900 px-4 py-3 text-white">Submit Order</button>
            </div>
          </form>
        </section>
      )}

      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <div className="mb-4 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
          <h3 className="text-lg font-semibold text-slate-950">Sales Order List</h3>
          <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search orders" className="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 lg:max-w-xs" />
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500">
                <th className="px-3 py-3">Order ID</th>
                <th className="px-3 py-3">Customer</th>
                <th className="px-3 py-3">Product</th>
                <th className="px-3 py-3">Qty</th>
                <th className="px-3 py-3">Amount</th>
                <th className="px-3 py-3">Priority</th>
                <th className="px-3 py-3">Status</th>
              </tr>
            </thead>
            <tbody>
              {visibleOrders.map((order) => (
                <tr key={order.id} className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="px-3 py-3 font-medium text-slate-900">{order.id}</td>
                  <td className="px-3 py-3">{order.customer}</td>
                  <td className="px-3 py-3">{order.product}</td>
                  <td className="px-3 py-3">{order.quantity} {order.unit}</td>
                  <td className="px-3 py-3">{order.amount}</td>
                  <td className="px-3 py-3">{order.priority}</td>
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

export default SalesOrders;
