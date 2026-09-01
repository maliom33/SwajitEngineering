import { MapPin, Circle } from 'lucide-react';

const markers = [
  { label: 'Port Hub', position: 'NE', status: 'On time' },
  { label: 'Warehouse 2', position: 'SW', status: 'Checkpoint' },
  { label: 'Factory Gate', position: 'C', status: 'Live' },
];

function MapSection() {
  return (
    <section className="card-glass rounded-3xl border border-slate-200/80 p-6 shadow-glass">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Live logistics</p>
          <h2 className="mt-3 text-2xl font-semibold text-slate-950">Live Truck Tracking</h2>
        </div>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-700">Future GPS-ready</span>
      </div>
      <div className="mt-6 relative h-80 overflow-hidden rounded-[2rem] border border-slate-200 bg-gradient-to-br from-slate-100 via-slate-50 to-slate-200 shadow-inner">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(59,130,246,0.18),transparent_25%),radial-gradient(circle_at_bottom_right,_rgba(100,116,139,0.18),transparent_20%)]" />
        <div className="absolute inset-0 p-6">
          <div className="h-full rounded-[2rem] border border-slate-200/80 bg-slate-950/5 p-6">
            <div className="flex h-full flex-col justify-between">
              <div className="flex items-center justify-between">
                <div className="space-y-2">
                  <p className="text-sm font-medium uppercase tracking-[0.24em] text-slate-500">Map placeholder</p>
                  <h3 className="text-xl font-semibold text-slate-950">Geospatial view</h3>
                </div>
                <div className="flex items-center gap-2 rounded-full bg-white/90 px-4 py-2 text-sm text-slate-700 shadow-sm">
                  <Circle className="h-3 w-3 text-emerald-500" /> Live update
                </div>
              </div>

              <div className="relative flex h-full items-center justify-center rounded-[1.75rem] border border-slate-200/70 bg-slate-50/75">
                {markers.map((marker) => (
                  <div key={marker.label} className={`absolute ${marker.position === 'NE' ? 'right-8 top-8' : marker.position === 'SW' ? 'bottom-10 left-10' : 'top-1/3 left-1/2 -translate-x-1/2'} text-slate-950`}>
                    <div className="flex flex-col items-center gap-2 rounded-3xl bg-white/90 px-3 py-3 shadow-lg shadow-slate-950/5 backdrop-blur-sm">
                      <MapPin className="h-5 w-5 text-slate-900" />
                      <p className="text-sm font-semibold">{marker.label}</p>
                      <p className="text-xs text-slate-500">{marker.status}</p>
                    </div>
                  </div>
                ))}
                <div className="absolute inset-0 rounded-[1.75rem] bg-[linear-gradient(90deg,rgba(59,130,246,0.08),transparent_30%),linear-gradient(180deg,rgba(100,116,139,0.06),transparent_30%)]" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default MapSection;
