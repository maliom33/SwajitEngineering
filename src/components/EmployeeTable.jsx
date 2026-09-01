import { Eye, Edit, User, Users } from 'lucide-react';

function EmployeeTable({ employees = [], onEdit = () => {}, onDelete = () => {}, deletingId = null }) {
  return (
    <div className="card-glass rounded-2xl border border-slate-200/80 bg-white/90 p-4 shadow-sm">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-slate-950">Employee Management</h3>
        <p className="text-sm text-slate-500">{employees.length} employees</p>
      </div>

      <div className="mt-4 overflow-x-auto">
        <table className="w-full table-auto text-left">
          <thead>
            <tr className="text-sm text-slate-600">
              <th className="px-4 py-3">Employee ID</th>
              <th className="px-4 py-3">Name</th>
              <th className="px-4 py-3">Department</th>
              <th className="px-4 py-3">Designation</th>
              <th className="px-4 py-3">Gender</th>
              <th className="px-4 py-3">Attendance</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3">Verification</th>
              <th className="px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody className="mt-2 divide-y divide-slate-100">
            {employees.map((emp) => (
              <tr key={emp.id} className="text-sm text-slate-700">
                <td className="px-4 py-3 font-mono text-slate-900">{emp.id}</td>
                <td className="px-4 py-3">{emp.name}</td>
                <td className="px-4 py-3">{emp.department}</td>
                <td className="px-4 py-3">{emp.designation}</td>
                <td className="px-4 py-3">{emp.gender}</td>
                <td className="px-4 py-3">{emp.attendance}</td>
                <td className="px-4 py-3">{emp.status}</td>
                <td className="px-4 py-3 text-xs">Email: {emp.emailVerified ? 'Verified' : 'Pending'}<br />Mobile: {emp.phoneVerified ? 'Verified' : 'Pending'}<br />Profile: {emp.profileComplete ? 'Complete' : 'Incomplete'}</td>
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <button type="button" onClick={() => onEdit(emp)} className="inline-flex items-center gap-2 rounded-2xl border border-slate-200 bg-white px-3 py-2 text-xs text-slate-700 transition hover:bg-slate-50">
                      <Eye className="h-4 w-4" /> View
                    </button>
                    <button type="button" onClick={() => onEdit(emp)} className="inline-flex items-center gap-2 rounded-2xl border border-slate-200 bg-white px-3 py-2 text-xs text-slate-700 transition hover:bg-slate-50">
                      <Edit className="h-4 w-4" /> Edit
                    </button>
                    <button type="button" onClick={() => onDelete(emp)} disabled={deletingId === emp.employeeId} className="inline-flex items-center gap-2 rounded-2xl border border-red-200 bg-white px-3 py-2 text-xs text-red-700 transition hover:bg-red-50 disabled:cursor-wait disabled:opacity-60">
                      {deletingId === emp.employeeId ? 'Deleting...' : 'Delete'}
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default EmployeeTable;
