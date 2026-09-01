import { CheckCircle2, AlertCircle, XCircle } from 'lucide-react';

function SystemHealthPanel() {
  const systemStatus = [
    { name: 'Server Status', status: 'online', uptime: '99.9%' },
    { name: 'API Gateway', status: 'online', uptime: '99.8%' },
    { name: 'PostgreSQL Connection', status: 'online', ping: '2ms' },
    { name: 'MongoDB Connection', status: 'online', ping: '3ms' },
    { name: 'Redis Cache', status: 'online', memory: '512MB' },
    { name: 'Network Status', status: 'online', bandwidth: '1Gbps' },
  ];

  const getStatusIcon = (status) => {
    if (status === 'online') return <CheckCircle2 className="h-5 w-5 text-emerald-600" />;
    if (status === 'warning') return <AlertCircle className="h-5 w-5 text-amber-600" />;
    return <XCircle className="h-5 w-5 text-rose-600" />;
  };

  const getStatusColor = (status) => {
    if (status === 'online') return 'bg-emerald-50 text-emerald-900';
    if (status === 'warning') return 'bg-amber-50 text-amber-900';
    return 'bg-rose-50 text-rose-900';
  };

  return (
    <section className="card-glass rounded-3xl border border-slate-200/80 bg-white/90 p-6 shadow-sm">
      <div className="flex items-center justify-between gap-4 mb-6">
        <div>
          <p className="text-sm uppercase tracking-[0.24em] text-slate-400">System Health</p>
          <h2 className="mt-3 text-2xl font-semibold text-slate-950">Real-time Monitoring</h2>
        </div>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-700">Live</span>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {systemStatus.map((item) => (
          <div key={item.name} className={`rounded-2xl border border-slate-200/80 ${getStatusColor(item.status)} p-4 shadow-sm`}>
            <div className="flex items-center gap-3">
              {getStatusIcon(item.status)}
              <div className="flex-1">
                <p className="text-sm font-semibold">{item.name}</p>
                <p className="text-xs mt-1 opacity-75">
                  {item.uptime || item.ping || item.memory || item.bandwidth || 'Operational'}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default SystemHealthPanel;
