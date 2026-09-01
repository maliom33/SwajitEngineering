import { AlertTriangle, Clock3, Wallet, CreditCard } from 'lucide-react';

const iconMap = {
  'Low Stock Alert': AlertTriangle,
  'Delayed Truck': Clock3,
  'Pending Payroll': Wallet,
  'Invoice Due': CreditCard,
};

function AlertsPanel({ alerts }) {
  return (
    <section className="card-glass rounded-3xl border border-slate-200/80 p-6 shadow-glass">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Alerts & notifications</p>
          <h2 className="mt-3 text-2xl font-semibold text-slate-950">Operational warnings</h2>
        </div>
      </div>
      <div className="mt-6 space-y-4">
        {alerts.map((alert) => {
          const Icon = iconMap[alert.title] || AlertTriangle;
          return (
            <div key={alert.title} className={`flex items-start gap-4 rounded-3xl border border-slate-200/80 ${alert.color} p-4 shadow-sm`}>
              <div className="mt-1 inline-flex h-12 w-12 items-center justify-center rounded-3xl bg-white/85 text-slate-900 shadow-sm">
                <Icon className="h-6 w-6" />
              </div>
              <div>
                <h3 className="text-base font-semibold text-slate-950">{alert.title}</h3>
                <p className="mt-1 text-sm text-slate-600">{alert.description}</p>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

export default AlertsPanel;
