import { useEffect, useState } from 'react';
import { Navigate, Outlet, useLocation, useOutletContext } from 'react-router-dom';
import MainLayout from '../components/MainLayout';
import { getCurrentUser } from '../api/auth';
import { clearAuth, getStoredUser } from '../api/storage';
import client from '../api/client';

const employeeLinks = [
  { label: 'Dashboard', to: '/employee', icon: 'LayoutGrid' },
  { label: 'My Profile', to: '/employee/profile', icon: 'User' },
  { label: 'Attendance', to: '/employee/attendance', icon: 'Clock' },
  { label: 'Leave', to: '/employee/leave', icon: 'Calendar' },
  { label: 'Logout', to: '/employee/logout', icon: 'LogOut' },
];

function EmployeePortal() {
  const location = useLocation();
  const [user, setUser] = useState(getStoredUser());
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    getCurrentUser().then((response) => setUser(response.data)).finally(() => setIsLoading(false));
  }, []);

  if (isLoading) return <div className="min-h-screen bg-slate-50 p-8 text-slate-600">Loading your portal...</div>;
  if (!user || user.role_code !== 'EMPLOYEE' || !user.employee) return <Navigate to="/login" replace state={{ from: location }} />;

  const employee = user.employee;
  return (
    <MainLayout title="Employee Portal" links={employeeLinks} userProfile={{ name: `${employee.first_name} ${employee.last_name}`, role: 'Employee' }}>
      <Outlet context={{ user, employee }} />
    </MainLayout>
  );
}

export function EmployeeDashboard() {
  const { employee } = useOutletContext();
  return <div><h2 className="text-2xl font-semibold">Welcome, {employee.first_name} {employee.last_name}</h2><p className="mt-2 text-sm text-slate-600">Your employee workspace.</p><section className="mt-6 grid gap-4 sm:grid-cols-3"><div className="rounded-2xl border border-slate-200 bg-white p-5"><p className="text-sm text-slate-500">Employee ID</p><p className="mt-2 font-semibold text-slate-950">{employee.employee_code}</p></div><div className="rounded-2xl border border-slate-200 bg-white p-5"><p className="text-sm text-slate-500">Department</p><p className="mt-2 font-semibold text-slate-950">{employee.department_name}</p></div><div className="rounded-2xl border border-slate-200 bg-white p-5"><p className="text-sm text-slate-500">Designation</p><p className="mt-2 font-semibold text-slate-950">{employee.designation_name}</p></div></section></div>;
}

export function EmployeeProfile() {
  const { user, employee } = useOutletContext();
  return <div><h2 className="text-2xl font-semibold">My Profile</h2><section className="mt-6 rounded-2xl border border-slate-200 bg-white p-6"><div className="grid gap-4 sm:grid-cols-2"><p>Name: {employee.first_name} {employee.last_name}</p><p>Email: {user.email}</p><p>Department: {employee.department_name}</p><p>Designation: {employee.designation_name}</p></div></section></div>;
}

export function EmployeeAttendance() {
  const [records, setRecords] = useState([]);
  useEffect(() => { client.get('workforce/attendance/').then((response) => setRecords(response.data?.results || response.data || [])); }, []);
  return <div><h2 className="text-2xl font-semibold">My Attendance</h2><div className="mt-6 overflow-x-auto rounded-2xl border border-slate-200 bg-white p-4"><table className="w-full text-left text-sm"><thead><tr><th className="px-3 py-2">Date</th><th className="px-3 py-2">Status</th><th className="px-3 py-2">Method</th></tr></thead><tbody>{records.map((record) => <tr key={record.attendance_id} className="border-t border-slate-100"><td className="px-3 py-2">{record.attendance_date}</td><td className="px-3 py-2">{record.status}</td><td className="px-3 py-2">{record.attendance_method}</td></tr>)}</tbody></table></div></div>;
}

export function EmployeeLeave() {
  const [requests, setRequests] = useState([]);
  const [leaveTypes, setLeaveTypes] = useState([]);
  const [message, setMessage] = useState('');
  const [form, setForm] = useState({ leave_type: '', start_date: '', end_date: '', total_days: '', reason: '' });
  const load = () => Promise.all([client.get('workforce/leave-requests/'), client.get('workforce/leave-types/')]).then(([requestsResponse, typesResponse]) => { setRequests(requestsResponse.data?.results || requestsResponse.data || []); setLeaveTypes((typesResponse.data?.results || typesResponse.data || []).filter((type) => type.is_active)); });
  useEffect(() => { load(); }, []);
  const submit = async (event) => { event.preventDefault(); setMessage(''); try { await client.post('workforce/leave-requests/', { ...form, leave_type: Number(form.leave_type), total_days: Number(form.total_days) }); setForm({ leave_type: '', start_date: '', end_date: '', total_days: '', reason: '' }); setMessage('Leave request submitted.'); await load(); } catch { setMessage('The leave request could not be submitted.'); } };
  return <div><h2 className="text-2xl font-semibold">My Leave</h2>{message && <p className="mt-4 rounded-2xl bg-slate-100 p-3 text-sm text-slate-700">{message}</p>}<form onSubmit={submit} className="mt-6 grid gap-3 rounded-2xl border border-slate-200 bg-white p-5 sm:grid-cols-2"><select required value={form.leave_type} onChange={(event) => setForm({ ...form, leave_type: event.target.value })} className="h-11 rounded-2xl border border-slate-200 px-3"><option value="">Leave type</option>{leaveTypes.map((type) => <option key={type.leave_type_id} value={type.leave_type_id}>{type.leave_name}</option>)}</select><input required type="number" min="0.5" step="0.5" placeholder="Total days" value={form.total_days} onChange={(event) => setForm({ ...form, total_days: event.target.value })} className="h-11 rounded-2xl border border-slate-200 px-3" /><input required type="date" value={form.start_date} onChange={(event) => setForm({ ...form, start_date: event.target.value })} className="h-11 rounded-2xl border border-slate-200 px-3" /><input required type="date" value={form.end_date} onChange={(event) => setForm({ ...form, end_date: event.target.value })} className="h-11 rounded-2xl border border-slate-200 px-3" /><textarea required placeholder="Reason" value={form.reason} onChange={(event) => setForm({ ...form, reason: event.target.value })} className="rounded-2xl border border-slate-200 px-3 py-2 sm:col-span-2" /><button className="rounded-2xl bg-brand-900 px-4 py-2 text-white sm:col-span-2">Submit leave request</button></form><div className="mt-6 overflow-x-auto rounded-2xl border border-slate-200 bg-white p-4"><table className="w-full text-left text-sm"><thead><tr><th className="px-3 py-2">Dates</th><th className="px-3 py-2">Days</th><th className="px-3 py-2">Status</th></tr></thead><tbody>{requests.map((request) => <tr key={request.leave_request_id} className="border-t border-slate-100"><td className="px-3 py-2">{request.start_date} to {request.end_date}</td><td className="px-3 py-2">{request.total_days}</td><td className="px-3 py-2">{request.status}</td></tr>)}</tbody></table></div></div>;
}

export function EmployeeLogout() {
  clearAuth();
  return <Navigate to="/login" replace />;
}

export default EmployeePortal;