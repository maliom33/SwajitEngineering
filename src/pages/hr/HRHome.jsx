import HRQuickActions from '../../components/HRQuickActions';
import AdminKpiCard from '../../components/AdminKpiCard';
import EmployeeTable from '../../components/EmployeeTable';
import { useEffect, useMemo, useState } from 'react';
import client from '../../api/client';

function HRHome() {
  const [dashboard, setDashboard] = useState(null);
  const [employees, setEmployees] = useState([]);
  const [pendingLeaveCount, setPendingLeaveCount] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');
  const currentDate = useMemo(() => new Date().toLocaleString(), []);

  const loadDashboard = async () => {
    setIsLoading(true);
    setErrorMessage('');
    try {
      const [workforceResponse, recruitmentResponse, employeeResponse, leaveResponse] = await Promise.all([
        client.get('analytics/workforce/'),
        client.get('analytics/recruitment/'),
        client.get('workforce/employees/'),
        client.get('workforce/leave-requests/?status=PENDING'),
      ]);
      setDashboard({
        workforce: workforceResponse.data?.data || {},
        recruitment: recruitmentResponse.data?.data || {},
      });
      const results = Array.isArray(employeeResponse.data) ? employeeResponse.data : employeeResponse.data?.results;
      setEmployees((results || []).map((employee) => ({
        id: employee.employee_code || employee.employee_id,
        name: `${employee.first_name || ''} ${employee.last_name || ''}`.trim() || 'Unnamed employee',
        department: employee.department ? `Department #${employee.department}` : 'Not available',
        designation: employee.designation ? `Designation #${employee.designation}` : 'Not available',
        attendance: 'Not available',
        status: employee.status || 'Not available',
        emailVerified: employee.email_verified,
        phoneVerified: employee.phone_verified,
        profileComplete: employee.profile_complete,
      })));
      const leaveResults = Array.isArray(leaveResponse.data) ? leaveResponse.data : leaveResponse.data?.results;
      setPendingLeaveCount((leaveResults || []).filter((request) => request.status === 'PENDING').length);
    } catch {
      setErrorMessage('We could not load the HR dashboard. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  const kpis = dashboard ? [
    { title: 'Total Employees', value: dashboard.workforce.total_employees ?? 0, icon: 'Users', trend: 'up', trendValue: '', description: 'Across all units' },
    { title: 'Present Today', value: dashboard.workforce.present_employees ?? 0, icon: 'UserCheck', trend: 'up', trendValue: '', description: 'Checked-in workforce' },
    { title: 'On Leave', value: dashboard.workforce.employees_on_leave ?? 0, icon: 'Calendar', trend: 'down', trendValue: '', description: 'Active employee records' },
    { title: 'Open Positions', value: dashboard.recruitment.open_jobs ?? 0, icon: 'Briefcase', trend: 'up', trendValue: '', description: 'Live vacancies' },
    { title: 'Pending Leave Requests', value: pendingLeaveCount, icon: 'Clock', trend: 'up', trendValue: '', description: 'Awaiting HR action' },
    { title: 'Interviews Scheduled', value: dashboard.recruitment.interviews ?? 0, icon: 'CalendarCheck', trend: 'up', trendValue: '', description: 'Recruitment interviews' },
    { title: 'Payroll Employees', value: dashboard.workforce.payroll_summary?.reviews ?? 'Available on Payroll', icon: 'CreditCard', trend: 'up', trendValue: '', description: 'Payroll data available' },
    { title: 'Performance Reviews', value: dashboard.workforce.performance_summary?.reviews ?? 0, icon: 'ShieldCheck', trend: 'up', trendValue: '', description: 'Recorded reviews' },
  ] : [];
  return (
    <>
      {isLoading && <div role="status" className="mb-6 rounded-2xl border border-slate-200 bg-white p-4 text-sm text-slate-600">Loading HR dashboard...</div>}
      {errorMessage && <div role="alert" className="mb-6 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"><p>{errorMessage}</p><button type="button" onClick={loadDashboard} className="mt-3 rounded-2xl bg-red-700 px-4 py-2 text-white">Try again</button></div>}
      <section className="mb-6 rounded-[2rem] border border-slate-200/80 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-700 p-6 text-white shadow-glass">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.24em] text-slate-300">Human Resources</p>
            <h1 className="mt-3 text-3xl font-semibold tracking-tight">People Operations Center</h1>
            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-300">Monitor attendance, recruitment, leave approvals, payroll readiness, and employee engagement from a single HR command center.</p>
          </div>
          <div className="rounded-3xl border border-white/15 bg-white/10 px-5 py-4 shadow-sm backdrop-blur-sm">
            <p className="text-sm uppercase tracking-[0.24em] text-slate-300">Current Date & Time</p>
            <p className="mt-2 text-lg font-semibold">{currentDate}</p>
          </div>
        </div>
      </section>

      <section className="mb-6 grid gap-6 lg:grid-cols-2 xl:grid-cols-4">
        {kpis.map((metric) => (
          <AdminKpiCard key={metric.title} title={metric.title} value={metric.value} icon={metric.icon} trend={metric.trend} trendValue={metric.trendValue} description={metric.description} />
        ))}
      </section>

      <section className="mb-6 grid gap-6 xl:grid-cols-[1.25fr_0.75fr]">
        <div className="rounded-2xl border border-slate-200/80 bg-white/90 p-6 shadow-sm">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-slate-950">Workforce Pulse</h3>
            <span className="rounded-full bg-emerald-100 px-3 py-1 text-sm font-medium text-emerald-700">Healthy</span>
          </div>
          <div className="mt-4 grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Attendance</p>
              <p className="mt-2 text-2xl font-semibold">{dashboard?.workforce.attendance_percentage ?? 0}%</p>
            </div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Absent Employees</p>
              <p className="mt-2 text-2xl font-semibold">{dashboard?.workforce.absent_employees ?? 0}</p>
            </div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Average Work Hours</p>
              <p className="mt-2 text-2xl font-semibold">{dashboard?.workforce.average_work_hours ?? 0}</p>
            </div>
          </div>
        </div>

        <div>
          <HRQuickActions />
        </div>
      </section>

      <section className="mb-6 grid gap-6 lg:grid-cols-2">
        <div className="rounded-2xl border border-slate-200/80 bg-white/90 p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-950">Recruitment Funnel</h3>
          <div className="mt-4 space-y-3">
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">Shortlisted: {dashboard?.recruitment.shortlisted_candidates ?? 'Not available'}</div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">Interviews: {dashboard?.recruitment.interviews ?? 'Not available'}</div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">Selected: {dashboard?.recruitment.selected_candidates ?? 'Not available'}</div>
          </div>
        </div>
        <div className="rounded-2xl border border-slate-200/80 bg-white/90 p-6 shadow-sm">
          <h3 className="text-lg font-semibold text-slate-950">Payroll & Compliance</h3>
          <div className="mt-4 space-y-3">
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">Gross payroll: {dashboard?.workforce.payroll_summary?.gross_salary ?? 'Not available'}</div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">Net payroll: {dashboard?.workforce.payroll_summary?.net_salary ?? 'Not available'}</div>
            <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">Performance reviews: {dashboard?.workforce.performance_summary?.reviews ?? 'Not available'}</div>
          </div>
        </div>
      </section>

      <section className="mb-6">
        {employees.length > 0 ? <EmployeeTable employees={employees} /> : <div className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-600">No employees have been registered yet.</div>}
      </section>
    </>
  );
}

export default HRHome;
