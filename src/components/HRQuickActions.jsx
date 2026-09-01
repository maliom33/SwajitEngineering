import * as Icons from 'lucide-react';

function HRQuickActions({ variant = 'hr' }) {
  const actions =
    variant === 'director'
      ? [
          { label: 'Review Board Metrics', icon: 'BarChart3', color: 'from-amber-500 to-orange-500' },
          { label: 'Approve Strategic Plan', icon: 'CheckCircle2', color: 'from-emerald-500 to-teal-500' },
          { label: 'Open Executive Report', icon: 'FileText', color: 'from-indigo-500 to-blue-500' },
          { label: 'Check Fleet Status', icon: 'Truck', color: 'from-sky-500 to-cyan-500' },
          { label: 'Review Warehouse KPI', icon: 'Package', color: 'from-violet-500 to-purple-500' },
          { label: 'Send Leadership Note', icon: 'Send', color: 'from-rose-500 to-red-500' },
        ]
      : variant === 'sales'
        ? [
            { label: 'Create Sales Order', icon: 'ShoppingCart', color: 'from-sky-500 to-cyan-500' },
            { label: 'Add Customer', icon: 'UserPlus', color: 'from-emerald-500 to-teal-500' },
            { label: 'Generate Quotation', icon: 'FileText', color: 'from-violet-500 to-purple-500' },
            { label: 'Upload Purchase Order', icon: 'Package', color: 'from-indigo-500 to-blue-500' },
            { label: 'Track Order', icon: 'Truck', color: 'from-amber-500 to-yellow-500' },
            { label: 'View Reports', icon: 'BarChart3', color: 'from-rose-500 to-red-500' },
          ]
        : variant === 'logistics'
          ? [
              { label: 'Create Dispatch', icon: 'Truck', color: 'from-sky-500 to-cyan-500' },
              { label: 'Assign Driver', icon: 'UserCircle2', color: 'from-emerald-500 to-teal-500' },
              { label: 'Optimize Route', icon: 'Map', color: 'from-violet-500 to-purple-500' },
              { label: 'Track Vehicle', icon: 'MapPinned', color: 'from-indigo-500 to-blue-500' },
              { label: 'Review Fuel Cost', icon: 'CircleDollarSign', color: 'from-amber-500 to-yellow-500' },
              { label: 'Open Report', icon: 'FileText', color: 'from-rose-500 to-red-500' },
            ]
          : variant === 'dispatch'
            ? [
                { label: 'Prepare Shipment', icon: 'Package', color: 'from-sky-500 to-cyan-500' },
                { label: 'Verify Loading', icon: 'ShieldCheck', color: 'from-emerald-500 to-teal-500' },
                { label: 'Generate Delivery Challan', icon: 'FileText', color: 'from-violet-500 to-purple-500' },
                { label: 'Dispatch Vehicle', icon: 'Truck', color: 'from-indigo-500 to-blue-500' },
                { label: 'View Dispatch Schedule', icon: 'Calendar', color: 'from-amber-500 to-yellow-500' },
                { label: 'Generate Dispatch Report', icon: 'BarChart3', color: 'from-rose-500 to-red-500' },
              ]
            : variant === 'finance'
              ? [
                  { label: 'Generate Invoice', icon: 'FileText', color: 'from-sky-500 to-cyan-500' },
                  { label: 'Record Payment', icon: 'CreditCard', color: 'from-emerald-500 to-teal-500' },
                  { label: 'Process Payroll', icon: 'Users', color: 'from-violet-500 to-purple-500' },
                  { label: 'Generate Payslip', icon: 'ReceiptText', color: 'from-indigo-500 to-blue-500' },
                  { label: 'View Financial Reports', icon: 'FileBarChart2', color: 'from-amber-500 to-yellow-500' },
                  { label: 'Export Revenue Report', icon: 'BarChart3', color: 'from-rose-500 to-red-500' },
                ]
              : [
              { label: 'Add Employee', icon: 'UserPlus', color: 'from-sky-500 to-cyan-500' },
              { label: 'Mark Attendance', icon: 'CheckSquare', color: 'from-emerald-500 to-teal-500' },
              { label: 'Approve Leave', icon: 'Check', color: 'from-amber-500 to-yellow-500' },
              { label: 'Add Job Opening', icon: 'Briefcase', color: 'from-violet-500 to-purple-500' },
              { label: 'Schedule Interview', icon: 'Calendar', color: 'from-indigo-500 to-blue-500' },
              { label: 'Generate Report', icon: 'FileText', color: 'from-rose-500 to-red-500' },
            ];

  const title = variant === 'director' ? 'Director Shortcuts' : variant === 'sales' ? 'Sales Shortcuts' : variant === 'logistics' ? 'Logistics Shortcuts' : variant === 'dispatch' ? 'Dispatch Shortcuts' : variant === 'finance' ? 'Finance Shortcuts' : 'HR Shortcuts';
  const subtitle = variant === 'director' ? 'Executive actions' : variant === 'sales' ? 'Sales operations' : variant === 'logistics' ? 'Dispatch operations' : variant === 'dispatch' ? 'Field execution tasks' : variant === 'finance' ? 'Financial operations' : 'HR operations';

  return (
    <section className="card-glass rounded-3xl border border-slate-200/80 bg-white/90 p-6 shadow-sm">
      <div className="mb-4">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Quick Actions</p>
        <h3 className="mt-2 text-lg font-semibold text-slate-950">{title}</h3>
        <p className="mt-1 text-sm text-slate-500">{subtitle}</p>
      </div>
      <div className="space-y-3">
        {actions.map((action) => {
          const Icon = Icons[action.icon] || Icons.ArrowRight;
          return (
            <button
              key={action.label}
              type="button"
              className={`w-full group flex items-center gap-4 rounded-3xl bg-gradient-to-r ${action.color} px-6 py-4 text-left text-white shadow-lg shadow-slate-950/10 transition hover:translate-y-0.5 hover:shadow-xl`}
            >
              <span className="inline-flex h-12 w-12 min-w-12 items-center justify-center rounded-3xl bg-white/15 text-white shadow-sm">
                <Icon className="h-5 w-5" />
              </span>
              <span className="text-base font-semibold">{action.label}</span>
            </button>
          );
        })}
      </div>
    </section>
  );
}

export default HRQuickActions;
