import { useMemo, useState } from 'react';

const initialInventory = [
  { code: 'P-101', name: 'MS Plate 8mm', category: 'Steel', grade: 'E250', quantity: '1200', unit: 'Tons', location: 'WH-A1', status: 'Available' },
  { code: 'P-102', name: 'Angle Iron 50x50', category: 'Steel', grade: 'E350', quantity: '430', unit: 'Tons', location: 'WH-B2', status: 'Low Stock' },
];

function Inventory() {
  const [inventory, setInventory] = useState(initialInventory);
  const [search, setSearch] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ code: '', name: '', category: '', grade: '', quantity: '', unit: '', location: '', status: 'Available' });

  const visibleInventory = useMemo(() => inventory.filter((item) => [item.code, item.name, item.category, item.location].some((value) => value.toLowerCase().includes(search.toLowerCase()))), [inventory, search]);

  const handleAdd = (e) => {
    e.preventDefault();
    setInventory((prev) => [{ code: form.code, name: form.name, category: form.category, grade: form.grade, quantity: form.quantity, unit: form.unit, location: form.location, status: form.status }, ...prev]);
    setShowForm(false);
    setForm({ code: '', name: '', category: '', grade: '', quantity: '', unit: '', location: '', status: 'Available' });
  };

  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Inventory Management</p>
            <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Inventory List</h1>
            <p className="mt-2 text-sm text-slate-600">Add, search, and review inventory items across warehouse zones.</p>
          </div>
          <button type="button" onClick={() => setShowForm((prev) => !prev)} className="rounded-2xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white">{showForm ? 'Close Form' : 'Add Product'}</button>
        </div>
      </section>

      {showForm && (
        <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-950">Add Product</h3>
          <form onSubmit={handleAdd} className="mt-5 grid gap-4 md:grid-cols-2">
            <input required value={form.code} onChange={(e) => setForm({ ...form, code: e.target.value })} placeholder="Product Code" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3" />
            <input required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="Product Name" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3" />
            <input required value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} placeholder="Category" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3" />
            <input required value={form.grade} onChange={(e) => setForm({ ...form, grade: e.target.value })} placeholder="Steel Grade" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3" />
            <input required value={form.quantity} onChange={(e) => setForm({ ...form, quantity: e.target.value })} placeholder="Quantity" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3" />
            <input required value={form.unit} onChange={(e) => setForm({ ...form, unit: e.target.value })} placeholder="Unit" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3" />
            <input required value={form.location} onChange={(e) => setForm({ ...form, location: e.target.value })} placeholder="Warehouse Location" className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3" />
            <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })} className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
              <option value="Available">Available</option>
              <option value="Low Stock">Low Stock</option>
              <option value="Reserved">Reserved</option>
            </select>
            <div className="md:col-span-2 flex justify-end gap-3">
              <button type="button" onClick={() => setShowForm(false)} className="rounded-2xl border border-slate-200 px-4 py-3">Cancel</button>
              <button type="submit" className="rounded-2xl bg-brand-900 px-4 py-3 text-white">Save Product</button>
            </div>
          </form>
        </section>
      )}

      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <div className="mb-4 flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
          <h3 className="text-lg font-semibold text-slate-950">Inventory Records</h3>
          <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search products" className="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 lg:max-w-xs" />
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500">
                <th className="px-3 py-3">Code</th>
                <th className="px-3 py-3">Product</th>
                <th className="px-3 py-3">Category</th>
                <th className="px-3 py-3">Grade</th>
                <th className="px-3 py-3">Qty</th>
                <th className="px-3 py-3">Location</th>
                <th className="px-3 py-3">Status</th>
              </tr>
            </thead>
            <tbody>
              {visibleInventory.map((item) => (
                <tr key={item.code} className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="px-3 py-3 font-medium text-slate-900">{item.code}</td>
                  <td className="px-3 py-3">{item.name}</td>
                  <td className="px-3 py-3">{item.category}</td>
                  <td className="px-3 py-3">{item.grade}</td>
                  <td className="px-3 py-3">{item.quantity} {item.unit}</td>
                  <td className="px-3 py-3">{item.location}</td>
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

export default Inventory;
