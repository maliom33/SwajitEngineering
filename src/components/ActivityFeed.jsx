import { Clock3, CheckCircle2, Truck, FileText, UserCheck, Archive } from 'lucide-react';

const iconMap = {
  Attendance: CheckCircle2,
  Logistics: Truck,
  Finance: FileText,
  Recruitment: UserCheck,
  Warehouse: Archive,
};

function ActivityFeed({ items }) {
  return (
    <section className="card-glass rounded-3xl border border-slate-200/80 p-6 shadow-glass">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Recent activities</p>
          <h2 className="mt-3 text-2xl font-semibold text-slate-950">Activity feed</h2>
        </div>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-700">Today</span>
      </div>
      <div className="mt-6 space-y-4">
        {items.map((item) => {
          const Icon = iconMap[item.tag] || Clock3;
          return (
            <div key={item.time} className="flex flex-col gap-3 rounded-3xl border border-slate-200/80 bg-white/90 p-4 shadow-sm sm:flex-row sm:items-center sm:justify-between">
              <div className="flex items-center gap-4">
                <div className="inline-flex h-12 w-12 items-center justify-center rounded-3xl bg-slate-100 text-slate-700">
                  <Icon className="h-5 w-5" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-slate-950">{item.title}</p>
                  <p className="mt-1 text-sm text-slate-500">{item.description}</p>
                </div>
              </div>
              <div className="flex items-center justify-between gap-3 text-sm text-slate-500 sm:w-44 sm:flex-col sm:items-end">
                <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-700">{item.tag}</span>
                <span>{item.time}</span>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

export default ActivityFeed;
