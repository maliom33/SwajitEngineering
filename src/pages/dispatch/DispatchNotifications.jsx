const notifications = [
  { title: 'Shipment Ready', message: 'Order ORD-2048 is prepared and ready for dispatch.', time: '10 mins ago' },
  { title: 'Loading Completed', message: 'Truck MH 12 AB 1234 loading verification is complete.', time: '24 mins ago' },
  { title: 'Challan Generated', message: 'Delivery challan CH-301 has been generated for dispatch.', time: '1 hr ago' },
];

function DispatchNotifications() {
  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Notifications</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Dispatch Alerts & Updates</h1>
      </section>

      <section className="space-y-4">
        {notifications.map((item) => (
          <div key={item.title} className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
            <div className="flex items-center justify-between gap-3">
              <h3 className="text-lg font-semibold text-slate-950">{item.title}</h3>
              <span className="text-sm text-slate-500">{item.time}</span>
            </div>
            <p className="mt-3 text-sm text-slate-600">{item.message}</p>
          </div>
        ))}
      </section>
    </div>
  );
}

export default DispatchNotifications;
