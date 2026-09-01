function DispatchProfile() {
  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Profile</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Dispatch Executive Profile</h1>
      </section>

      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
          <div className="flex items-center gap-4">
            <div className="flex h-16 w-16 items-center justify-center rounded-3xl bg-slate-900 text-xl font-semibold text-white">DE</div>
            <div>
              <h3 className="text-xl font-semibold text-slate-950">Aarav Sharma</h3>
              <p className="text-sm text-slate-500">Dispatch Executive</p>
            </div>
          </div>
          <div className="rounded-2xl border border-slate-100 bg-slate-50 px-4 py-3 text-sm text-slate-600">
            Shift: Morning Dispatch Operations
          </div>
        </div>
      </section>
    </div>
  );
}

export default DispatchProfile;
