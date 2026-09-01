import { AlertTriangle, AlertCircle, Clock, HardDrive, Lock } from 'lucide-react';

function SecurityAlertsPanel() {
  const alerts = [
    { type: 'danger', icon: AlertTriangle, title: 'Failed Login Attempts', message: '3 failed attempts from IP 192.168.1.100', time: '5 mins ago' },
    { type: 'warning', icon: Clock, title: 'Database Backup Reminder', message: 'Schedule next backup for today at 8 PM', time: '1 hour ago' },
    { type: 'warning', icon: HardDrive, title: 'Storage Threshold', message: 'Database storage at 85% capacity', time: '2 hours ago' },
    { type: 'info', icon: Lock, title: 'Weak Password Warning', message: 'User "john_doe" has weak password', time: '3 hours ago' },
  ];

  const getAlertColor = (type) => {
    if (type === 'danger') return 'bg-rose-50 text-rose-900 border-rose-200';
    if (type === 'warning') return 'bg-amber-50 text-amber-900 border-amber-200';
    return 'bg-blue-50 text-blue-900 border-blue-200';
  };

  return (
    <section className="card-glass rounded-3xl border border-slate-200/80 bg-white/90 p-6 shadow-sm">
      <div className="flex items-center justify-between gap-4 mb-6">
        <div>
          <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Security & Alerts</p>
          <h2 className="mt-3 text-2xl font-semibold text-slate-950">System Notifications</h2>
        </div>
        <span className="rounded-full bg-rose-100 px-3 py-1 text-sm font-medium text-rose-700">4 Active</span>
      </div>

      <div className="space-y-3">
        {alerts.map((alert, idx) => {
          const Icon = alert.icon;
          return (
            <div key={idx} className={`rounded-2xl border ${getAlertColor(alert.type)} p-4 flex items-start gap-4`}>
              <Icon className="h-5 w-5 mt-1 flex-shrink-0" />
              <div className="flex-1">
                <h3 className="font-semibold text-sm">{alert.title}</h3>
                <p className="text-xs mt-1 opacity-75">{alert.message}</p>
                <p className="text-xs mt-2 opacity-60">{alert.time}</p>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

export default SecurityAlertsPanel;
