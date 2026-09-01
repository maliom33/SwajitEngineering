const notifications = [
  { title: 'New Sales Order Received', detail: 'SO-1002 created and needs verification', time: '2 mins ago' },
  { title: 'Low Stock Alert', detail: 'Angle Iron stock is nearing reorder level', time: '12 mins ago' },
  { title: 'Goods Received', detail: 'Supplier delivery recorded successfully', time: '1 hr ago' },
  { title: 'Material Allocated', detail: 'Material reserved for approved order', time: '2 hrs ago' },
  { title: 'Dispatch Ready', detail: 'Order ready for logistics handoff', time: 'Today' },
];

function Notifications() {
  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Notifications</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Warehouse Alerts</h1>
      </section>

      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <div className="space-y-3">
          {notifications.map((item) => (
            <div key={item.title} className="flex items-start justify-between rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <div>
                <h3 className="font-semibold text-slate-950">{item.title}</h3>
                <p className="mt-1 text-sm text-slate-600">{item.detail}</p>
              </div>
              <span className="text-sm text-slate-500">{item.time}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default Notifications;
