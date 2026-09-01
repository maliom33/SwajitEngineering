import { Eye, Edit, Ban } from 'lucide-react';

function UserManagementTable() {
  const users = [
    { id: 'EMP-001', name: 'Rajesh Nair', department: 'Operations', designation: 'Director', status: 'Active', lastLogin: '10:30 AM Today' },
    { id: 'EMP-002', name: 'Priya Sharma', department: 'HR', designation: 'HR Manager', status: 'Active', lastLogin: '09:15 AM Today' },
    { id: 'EMP-003', name: 'Amit Kumar', department: 'Logistics', designation: 'Logistics Manager', status: 'Active', lastLogin: 'Yesterday' },
    { id: 'EMP-004', name: 'Sneha Desai', department: 'Warehouse', designation: 'Warehouse Manager', status: 'Active', lastLogin: '2 days ago' },
    { id: 'EMP-005', name: 'Vikram Singh', department: 'Finance', designation: 'Finance Manager', status: 'Inactive', lastLogin: 'Last week' },
  ];

  const getStatusBadge = (status) => {
    return status === 'Active' ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-700';
  };

  return (
    <section className="card-glass rounded-3xl border border-slate-200/80 bg-white/90 p-6 shadow-sm">
      <div className="flex items-center justify-between gap-4 mb-6">
        <div>
          <p className="text-sm uppercase tracking-[0.24em] text-slate-400">User Management</p>
          <h2 className="mt-3 text-2xl font-semibold text-slate-950">Active Users</h2>
        </div>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-700">{users.length} Users</span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-200">
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">Employee ID</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">Name</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">Department</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">Designation</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">Status</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">Last Login</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-[0.24em] text-slate-400">Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id} className="border-b border-slate-200/50 hover:bg-slate-50/50">
                <td className="px-4 py-3 text-sm font-medium text-slate-950">{user.id}</td>
                <td className="px-4 py-3 text-sm text-slate-700">{user.name}</td>
                <td className="px-4 py-3 text-sm text-slate-600">{user.department}</td>
                <td className="px-4 py-3 text-sm text-slate-600">{user.designation}</td>
                <td className="px-4 py-3">
                  <span className={`inline-flex rounded-full px-3 py-1 text-xs font-medium ${getStatusBadge(user.status)}`}>
                    {user.status}
                  </span>
                </td>
                <td className="px-4 py-3 text-sm text-slate-600">{user.lastLogin}</td>
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <button className="inline-flex h-8 w-8 items-center justify-center rounded-2xl bg-slate-100 text-slate-700 transition hover:bg-slate-200">
                      <Eye className="h-4 w-4" />
                    </button>
                    <button className="inline-flex h-8 w-8 items-center justify-center rounded-2xl bg-slate-100 text-slate-700 transition hover:bg-slate-200">
                      <Edit className="h-4 w-4" />
                    </button>
                    <button className="inline-flex h-8 w-8 items-center justify-center rounded-2xl bg-slate-100 text-slate-700 transition hover:bg-rose-100 hover:text-rose-700">
                      <Ban className="h-4 w-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default UserManagementTable;
