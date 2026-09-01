import { Database, CheckCircle2 } from 'lucide-react';

function DatabaseManagementPanel() {
  const databases = [
    {
      name: 'PostgreSQL',
      status: 'Connected',
      size: '4.8 GB',
      connections: '12/100',
      lastBackup: '2 hours ago',
    },
    {
      name: 'MongoDB',
      status: 'Connected',
      size: '2.3 GB',
      collections: '28 collections',
      lastBackup: '4 hours ago',
    },
  ];

  return (
    <section className="card-glass rounded-3xl border border-slate-200/80 bg-white/90 p-6 shadow-sm">
      <div className="flex items-center justify-between gap-4 mb-6">
        <div>
          <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Database Management</p>
          <h2 className="mt-3 text-2xl font-semibold text-slate-950">Data Infrastructure</h2>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {databases.map((db) => (
          <div key={db.name} className="rounded-2xl border border-slate-200/80 bg-slate-50 p-6 shadow-sm">
            <div className="flex items-center gap-3 mb-4">
              <div className="inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-brand-900 text-white shadow-md">
                <Database className="h-6 w-6" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-slate-950">{db.name}</h3>
                <div className="flex items-center gap-2 mt-1">
                  <CheckCircle2 className="h-4 w-4 text-emerald-600" />
                  <span className="text-sm text-emerald-700 font-medium">{db.status}</span>
                </div>
              </div>
            </div>

            <div className="space-y-3 mb-5">
              <div className="flex items-center justify-between text-sm">
                <span className="text-slate-600">Database Size</span>
                <span className="font-semibold text-slate-950">{db.size}</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-slate-600">{db.name === 'PostgreSQL' ? 'Active Connections' : 'Collections'}</span>
                <span className="font-semibold text-slate-950">{db.connections || db.collections}</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-slate-600">Last Backup</span>
                <span className="font-semibold text-slate-950">{db.lastBackup}</span>
              </div>
            </div>

            <div className="flex gap-2">
              <button className="flex-1 rounded-full border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-900 transition hover:bg-slate-50">
                Test Connection
              </button>
              <button className="flex-1 rounded-full border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-900 transition hover:bg-slate-50">
                Backup Status
              </button>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

export default DatabaseManagementPanel;
