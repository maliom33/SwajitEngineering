function Profile() {
  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Profile</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Sales Executive Profile</h1>
      </section>

      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        <div className="grid gap-6 md:grid-cols-[0.8fr_1.2fr]">
          <div className="rounded-3xl border border-slate-200/80 bg-slate-50 p-6">
            <div className="flex h-20 w-20 items-center justify-center rounded-full bg-slate-900 text-xl font-semibold text-white">SE</div>
            <h3 className="mt-4 text-xl font-semibold text-slate-950">Aarav Patel</h3>
            <p className="mt-1 text-sm text-slate-600">Sales Executive</p>
          </div>
          <div className="grid gap-4 md:grid-cols-2">
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4"><p className="text-sm text-slate-500">Employee ID</p><p className="mt-2 font-semibold text-slate-950">EMP-2045</p></div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4"><p className="text-sm text-slate-500">Department</p><p className="mt-2 font-semibold text-slate-950">Sales</p></div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4"><p className="text-sm text-slate-500">Email</p><p className="mt-2 font-semibold text-slate-950">aarav@swajit.com</p></div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4"><p className="text-sm text-slate-500">Phone</p><p className="mt-2 font-semibold text-slate-950">+91 98765 00000</p></div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Profile;
