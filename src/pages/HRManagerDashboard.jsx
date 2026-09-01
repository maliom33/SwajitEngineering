import { useMemo, useState } from 'react';
import AdminNavbar from '../components/AdminNavbar';
import DashboardSidebar from '../components/DashboardSidebar';
import AdminKpiCard from '../components/AdminKpiCard';
import HRQuickActions from '../components/HRQuickActions';
import EmployeeTable from '../components/EmployeeTable';

const hrLinks = [
  { label: 'Dashboard', icon: 'LayoutGrid' },
  { label: 'Employee Management', icon: 'Users' },
  { label: 'Attendance Management', icon: 'Clock' },
  { label: 'Leave Management', icon: 'Calendar' },
  { label: 'Recruitment', icon: 'UserPlus' },
  { label: 'Shift Management', icon: 'Repeat' },
  { label: 'Payroll', icon: 'DollarSign' },
  { label: 'Employee Performance', icon: 'BarChart3' },
  { label: 'Reports', icon: 'FileText' },
  { label: 'Notifications', icon: 'Bell' },
  { label: 'Profile', icon: 'User' },
  { label: 'Logout', icon: 'LogOut' },
];

const kpis = [
  { title: 'Total Employees', value: '1,250', icon: 'Users', trend: 'up', trendValue: '+1.8%', description: 'All employees' },
  { title: 'Present Today', value: '987', icon: 'UserCheck', trend: 'up', trendValue: '+0.6%', description: 'Checked-in' },
  { title: 'Absent Today', value: '38', icon: 'UserMinus', trend: 'down', trendValue: '-0.4%', description: 'Not present' },
  { title: 'On Leave', value: '45', icon: 'Calendar', trend: 'down', trendValue: '-1', description: 'Approved leave' },
  { title: 'Open Positions', value: '6', icon: 'Briefcase', trend: 'up', trendValue: '+2', description: 'Vacancies' },
  { title: 'Candidates Pending', value: '18', icon: 'FileText', trend: 'up', trendValue: '+4', description: 'Screening queue' },
  { title: 'Pending Leaves', value: '9', icon: 'Clock', trend: 'down', trendValue: '-1', description: 'Awaiting approval' },
  { title: 'Payroll Status', value: 'Processing', icon: 'CreditCard', trend: 'up', trendValue: '72%', description: 'This cycle' },
];

const sampleEmployees = [
  { id: 'EMP-0001', name: 'Rajesh Nair', department: 'Manufacturing', designation: 'Director', attendance: 'Present', status: 'Active' },
  { id: 'EMP-0012', name: 'Priya Sharma', department: 'Human Resources', designation: 'HR Manager', attendance: 'Present', status: 'Active' },
  { id: 'EMP-0045', name: 'Amit Kumar', department: 'Logistics', designation: 'Logistics Manager', attendance: 'Absent', status: 'Active' },
  { id: 'EMP-0033', name: 'Sneha Desai', department: 'Warehouse', designation: 'Warehouse Manager', attendance: 'On Leave', status: 'Active' },
  { id: 'EMP-0028', name: 'Vikram Singh', department: 'Finance', designation: 'Finance Manager', attendance: 'Present', status: 'Active' },
];

function HRManagerDashboard({ onNavigateToLogin = () => {} }) {
  const [activeItem, setActiveItem] = useState('Dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const currentDate = useMemo(() => new Date().toLocaleString(), []);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="lg:flex lg:min-h-screen">
        <DashboardSidebar isOpen={sidebarOpen} activeItem={activeItem} onSelect={(label) => {
          if (label === 'Logout') return onNavigateToLogin();
          setActiveItem(label);
        }} toggleSidebar={() => setSidebarOpen((s) => !s)} links={hrLinks} title="HR" />

        <div className="flex-1">
          <AdminNavbar />

          <main className="mx-auto max-w-7xl px-4 pb-10 pt-6 sm:px-6 lg:px-8">
            {activeItem === 'Dashboard' && (
              <>
                <section className="mb-6 rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
                  <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                    <div>
                      <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Human Resources</p>
                      <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">Welcome, HR Manager</h1>
                      <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-600">Manage employees, recruitment, attendance, leave, shifts, payroll coordination and employee performance from one centralized HR dashboard.</p>
                    </div>
                    <div className="rounded-3xl border border-slate-200/80 bg-white/80 px-5 py-4 shadow-sm backdrop-blur-sm">
                      <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Current Date & Time</p>
                      <p className="mt-2 text-lg font-semibold text-slate-950">{currentDate}</p>
                      <p className="mt-1 inline-flex items-center gap-2 text-sm text-slate-600">Department: Human Resources</p>
                    </div>
                  </div>
                </section>

                <section className="mb-6 grid gap-6 lg:grid-cols-2 xl:grid-cols-4">
                  {kpis.map((metric) => (
                    <AdminKpiCard key={metric.title} title={metric.title} value={metric.value} icon={metric.icon} trend={metric.trend} trendValue={metric.trendValue} description={metric.description} />
                  ))}
                </section>

                <section className="mb-6 grid gap-6 lg:grid-cols-3">
                  <div className="col-span-2">
                    <div className="card-glass rounded-2xl border border-slate-200/80 bg-white/90 p-6 shadow-sm">
                      <h3 className="text-lg font-semibold text-slate-950">Attendance Summary</h3>
                      <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                        <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
                          <p className="text-sm text-slate-500">Today's Attendance</p>
                          <p className="mt-2 text-2xl font-semibold">987</p>
                        </div>
                        <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
                          <p className="text-sm text-slate-500">Late Arrivals</p>
                          <p className="mt-2 text-2xl font-semibold">12</p>
                        </div>
                        <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
                          <p className="text-sm text-slate-500">Overtime</p>
                          <p className="mt-2 text-2xl font-semibold">24</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div>
                    <HRQuickActions />
                  </div>
                </section>

                <section className="mb-6 grid gap-6 lg:grid-cols-2">
                  <div className="rounded-2xl border border-slate-200 bg-white p-6">
                    <h4 className="text-lg font-semibold text-slate-950">Leave Management</h4>
                    <div className="mt-4 grid gap-4 sm:grid-cols-2">
                      <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
                        <p className="text-sm text-slate-500">Pending Requests</p>
                        <p className="mt-2 text-2xl font-semibold">9</p>
                        <div className="mt-3 flex gap-2">
                          <button className="rounded-2xl bg-emerald-600 px-4 py-2 text-sm text-white">Approve</button>
                          <button className="rounded-2xl bg-rose-600 px-4 py-2 text-sm text-white">Reject</button>
                        </div>
                      </div>
                      <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
                        <p className="text-sm text-slate-500">Approved Leaves</p>
                        <p className="mt-2 text-2xl font-semibold">45</p>
                      </div>
                    </div>
                  </div>

                  <div className="rounded-2xl border border-slate-200 bg-white p-6">
                    <h4 className="text-lg font-semibold text-slate-950">Recruitment</h4>
                    <div className="mt-4 space-y-3">
                      <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">
                        <p className="text-sm text-slate-500">Open Vacancies</p>
                        <p className="mt-2 text-2xl font-semibold">6</p>
                      </div>
                      <div className="flex gap-2">
                        <button className="rounded-2xl bg-brand-900 px-4 py-2 text-sm text-white">Add Job</button>
                        <button className="rounded-2xl border border-slate-200 px-4 py-2 text-sm">View Candidates</button>
                        <button className="rounded-2xl border border-slate-200 px-4 py-2 text-sm">Schedule Interview</button>
                      </div>
                    </div>
                  </div>
                </section>

                <section className="mb-6">
                  <EmployeeTable employees={sampleEmployees} />
                </section>
              </>
            )}

            {/* Simple placeholder pages for other sidebar items */}
            {activeItem === 'Employee Management' && (
              <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
                <h2 className="text-2xl font-semibold">Employee Management</h2>
                <div className="mt-6"><EmployeeTable employees={sampleEmployees} /></div>
              </section>
            )}

            {activeItem === 'Attendance Management' && (
              <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
                <h2 className="text-2xl font-semibold">Attendance Management</h2>
                <p className="mt-2 text-sm text-slate-600">Today's attendance overview and reports.</p>
              </section>
            )}

            {activeItem === 'Leave Management' && (
              <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
                <h2 className="text-2xl font-semibold">Leave Management</h2>
                <p className="mt-2 text-sm text-slate-600">Manage leave requests and approvals.</p>
              </section>
            )}

            {activeItem === 'Payroll' && (
              <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
                <h2 className="text-2xl font-semibold">Payroll Overview</h2>
                <p className="mt-2 text-sm text-slate-600">Salary processing and payroll status.</p>
              </section>
            )}

            {activeItem === 'Reports' && (
              <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
                <h2 className="text-2xl font-semibold">Reports</h2>
                <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                  <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">Attendance Report</div>
                  <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">Leave Report</div>
                  <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4">Recruitment Report</div>
                </div>
              </section>
            )}

          </main>

          <footer className="border-t border-slate-200/80 bg-white/90 py-6">
            <div className="mx-auto flex max-w-7xl flex-col gap-6 px-4 text-sm text-slate-600 sm:flex-row sm:items-center sm:justify-between sm:px-6 lg:px-8">
              <div>
                <p className="font-semibold text-slate-950">Swajit Engineering Pvt. Ltd.</p>
                <p>Smart Workforce & E-Logistics ERP System</p>
              </div>
              <div className="space-y-1">
                <p>Version 1.0</p>
                <p>© 2026 All Rights Reserved</p>
              </div>
            </div>
          </footer>
        </div>
      </div>
    </div>
  );
}

export default HRManagerDashboard;
