const stages = [
  { title: 'Draft', detail: 'Order drafted and saved' },
  { title: 'Submitted', detail: 'Order submitted for review' },
  { title: 'Warehouse Verification', detail: 'Pending stock verification' },
  { title: 'Approved', detail: 'Approved by operations' },
  { title: 'Dispatch Planned', detail: 'Dispatch schedule prepared' },
  { title: 'Truck Assigned', detail: 'Load assigned to truck' },
  { title: 'In Transit', detail: 'En route to customer' },
  { title: 'Delivered', detail: 'Delivery completed' },
  { title: 'Completed', detail: 'Invoice and closeout ready' },
];

function Tracking() {
  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Order Tracking</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Order Status Timeline</h1>
        <p className="mt-2 text-sm text-slate-600">Follow every order from draft to delivery with a clear progress timeline.</p>
      </section>

      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <div className="grid gap-4 lg:grid-cols-2">
          {stages.map((stage, index) => (
            <div key={stage.title} className="rounded-3xl border border-slate-200/80 bg-slate-50 p-5">
              <div className="flex items-center gap-3">
                <span className="flex h-9 w-9 items-center justify-center rounded-full bg-slate-900 text-sm font-semibold text-white">{index + 1}</span>
                <div>
                  <h3 className="font-semibold text-slate-950">{stage.title}</h3>
                  <p className="text-sm text-slate-500">{stage.detail}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default Tracking;
