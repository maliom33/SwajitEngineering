import { useMemo, useState } from 'react';
import AdminNavbar from '../components/AdminNavbar';
import DashboardSidebar from '../components/DashboardSidebar';
import AdminKpiCard from '../components/AdminKpiCard';
import SystemHealthPanel from '../components/SystemHealthPanel';
import DatabaseManagementPanel from '../components/DatabaseManagementPanel';
import SecurityAlertsPanel from '../components/SecurityAlertsPanel';
import AdminQuickActions from '../components/AdminQuickActions';
import UserManagementTable from '../components/UserManagementTable';
import HRManagerDashboard from './HRManagerDashboard';
import { clearAuth } from '../api/storage';

const kpiMetrics = [
  { title: 'Total Employees', value: '1,250', icon: 'Users2', trend: 'up', trendValue: '+3.2%', description: 'Active workforce', color: 'bg-sky-100 text-sky-600' },
  { title: 'Active Users', value: '987', icon: 'UserCheck', trend: 'up', trendValue: '+2.1%', description: 'Logged in today', color: 'bg-emerald-100 text-emerald-600' },
  { title: 'Departments', value: '18', icon: 'Building2', trend: 'up', trendValue: '+1', description: 'Total divisions', color: 'bg-indigo-100 text-indigo-600' },
  { title: 'Active Sessions', value: '342', icon: 'Activity', trend: 'up', trendValue: '+8.3%', description: 'Currently online', color: 'bg-violet-100 text-violet-600' },
  { title: 'Failed Logins', value: '3', icon: 'AlertCircle', trend: 'down', trendValue: '-2', description: 'Last 24 hours', color: 'bg-rose-100 text-rose-600' },
  { title: 'DB Status', value: 'Online', icon: 'Database', trend: 'up', trendValue: '99.9%', description: 'Uptime', color: 'bg-teal-100 text-teal-600' },
  { title: 'Storage Used', value: '7.1 TB', icon: 'HardDrive', trend: 'up', trendValue: '+2.5%', description: 'Total capacity', color: 'bg-orange-100 text-orange-600' },
  { title: 'Server Uptime', value: '45d', icon: 'Clock', trend: 'up', trendValue: '99.98%', description: 'Without restart', color: 'bg-cyan-100 text-cyan-600' },
];

function SystemAdminDashboard() {
  const [activeItem, setActiveItem] = useState('Dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const currentDate = useMemo(() => new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit' }), []);
  const handleLogout = () => {
    clearAuth();
    window.location.assign('/login');
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="lg:flex lg:min-h-screen">
        <DashboardSidebar isOpen={sidebarOpen} activeItem={activeItem} onSelect={setActiveItem} toggleSidebar={() => setSidebarOpen((prev) => !prev)} onLogout={handleLogout} />

        <div className="flex-1">
          <AdminNavbar onLogout={handleLogout} />

          <main className="mx-auto max-w-7xl px-4 pb-10 pt-6 sm:px-6 lg:px-8">
            {/* Render based on activeItem */}
            {activeItem === 'Dashboard' && (
              <>
                {/* Welcome Section */}
                <section className="mb-6 rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
                  <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
                    <div>
                      <p className="text-sm uppercase tracking-[0.24em] text-slate-400">System Administration</p>
                      <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">Welcome, System Administrator</h1>
                      <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-600">
                        You have complete administrative access to manage users, security, permissions, departments and overall system configuration.
                      </p>
                    </div>
                    <div className="rounded-3xl border border-slate-200/80 bg-white/80 px-5 py-4 shadow-sm backdrop-blur-sm">
                      <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Current Date & Time</p>
                      <p className="mt-2 text-lg font-semibold text-slate-950">{currentDate}</p>
                      <p className="mt-1 inline-flex items-center gap-2 text-sm text-emerald-700">
                        <span className="h-2.5 w-2.5 rounded-full bg-emerald-500" />
                        Server Status: Online
                      </p>
                    </div>
                  </div>
                </section>

                {/* KPI Cards */}
                <section className="mb-6 grid gap-6 lg:grid-cols-2 xl:grid-cols-4">
                  {kpiMetrics.map((metric) => (
                    <AdminKpiCard
                      key={metric.title}
                      title={metric.title}
                      value={metric.value}
                      icon={metric.icon}
                      trend={metric.trend}
                      trendValue={metric.trendValue}
                      description={metric.description}
                      color={metric.color}
                    />
                  ))}
                </section>

                {/* System Health & Database Management */}
                <section className="mb-6 space-y-6">
                  <SystemHealthPanel />
                  <DatabaseManagementPanel />
                </section>

                {/* Security Alerts & Quick Actions */}
                <section className="mb-6 grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
                  <SecurityAlertsPanel />
                  <AdminQuickActions />
                </section>

                {/* User Management Table */}
                <section className="mb-6">
                  <UserManagementTable />
                </section>
              </>
            )}

            {activeItem === 'User Management' && (
              <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
                <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Administration</p>
                <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">User Management</h1>
                <p className="mt-2 text-sm text-slate-600">Manage employee accounts, roles, and access permissions.</p>
                <div className="mt-8">
                  <UserManagementTable />
                </div>
              </section>
            )}

            {activeItem === 'Role & Permission' && (
              <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
                <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Administration</p>
                <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">Role & Permission Management</h1>
                <p className="mt-2 text-sm text-slate-600">Configure roles, permissions, and access control policies.</p>
                <div className="mt-8 grid gap-4">
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <p className="font-semibold text-slate-950">System Administrator</p>
                    <p className="mt-1 text-sm text-slate-600">Full system access - 45 permissions enabled</p>
                  </div>
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <p className="font-semibold text-slate-950">HR Manager</p>
                    <p className="mt-1 text-sm text-slate-600">Employee & attendance management - 28 permissions enabled</p>
                  </div>
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <p className="font-semibold text-slate-950">Logistics Manager</p>
                    <p className="mt-1 text-sm text-slate-600">Shipment & fleet management - 32 permissions enabled</p>
                  </div>
                </div>
              </section>
            )}

            {activeItem === 'Department Management' && (
              <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
                <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Administration</p>
                <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">Department Management</h1>
                <p className="mt-2 text-sm text-slate-600">Create, edit, and manage company departments and divisions.</p>
                <div className="mt-8 grid gap-4 lg:grid-cols-2">
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <p className="font-semibold text-slate-950">Human Resources</p>
                    <p className="mt-1 text-sm text-slate-600">45 employees • Manager: Priya Sharma</p>
                  </div>
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <p className="font-semibold text-slate-950">Logistics & Supply Chain</p>
                    <p className="mt-1 text-sm text-slate-600">62 employees • Manager: Amit Kumar</p>
                  </div>
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <p className="font-semibold text-slate-950">Manufacturing</p>
                    <p className="mt-1 text-sm text-slate-600">128 employees • Manager: Rajesh Nair</p>
                  </div>
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <p className="font-semibold text-slate-950">Finance & Accounting</p>
                    <p className="mt-1 text-sm text-slate-600">35 employees • Manager: Vikram Singh</p>
                  </div>
                </div>
              </section>
            )}

            {activeItem === 'Attendance Config' && (
              <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
                <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Administration</p>
                <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">Attendance Configuration</h1>
                <p className="mt-2 text-sm text-slate-600">Configure attendance settings, working hours, and policies.</p>
                <div className="mt-8 space-y-4">
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <p className="font-semibold text-slate-950">Working Hours</p>
                    <p className="mt-1 text-sm text-slate-600">Monday - Friday: 9:00 AM - 6:00 PM • Saturday: 9:00 AM - 1:00 PM</p>
                  </div>
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <p className="font-semibold text-slate-950">Grace Period</p>
                    <p className="mt-1 text-sm text-slate-600">15 minutes • Applied to all employees by default</p>
                  </div>
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <p className="font-semibold text-slate-950">Late Mark Policy</p>
                    <p className="mt-1 text-sm text-slate-600">After 15 mins: Half day • After 4 hours: Full day absence</p>
                  </div>
                </div>
              </section>
            )}

            {activeItem === 'System Monitoring' && (
              <section className="space-y-6">
                <div className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
                  <p className="text-sm uppercase tracking-[0.24em] text-slate-400">System Administration</p>
                  <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">System Monitoring</h1>
                  <p className="mt-2 text-sm text-slate-600">Real-time monitoring of system health and performance metrics.</p>
                </div>
                <SystemHealthPanel />
              </section>
            )}

            {activeItem === 'Database Management' && (
              <section className="space-y-6">
                <div className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
                  <p className="text-sm uppercase tracking-[0.24em] text-slate-400">System Administration</p>
                  <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">Database Management</h1>
                  <p className="mt-2 text-sm text-slate-600">Monitor database connectivity, performance, and status.</p>
                </div>
                <DatabaseManagementPanel />
              </section>
            )}

            {activeItem === 'Backup & Restore' && (
              <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
                <p className="text-sm uppercase tracking-[0.24em] text-slate-400">System Administration</p>
                <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">Backup & Restore</h1>
                <p className="mt-2 text-sm text-slate-600">Manage database backups and system recovery options.</p>
                <div className="mt-8 space-y-4">
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <p className="font-semibold text-slate-950">Last Backup</p>
                    <p className="mt-1 text-sm text-slate-600">Today at 2:30 AM • Size: 12.4 GB • Status: Successful</p>
                  </div>
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <p className="font-semibold text-slate-950">Backup Schedule</p>
                    <p className="mt-1 text-sm text-slate-600">Daily at 2:00 AM • Retention: 30 days</p>
                  </div>
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <p className="font-semibold text-slate-950">Storage</p>
                    <p className="mt-1 text-sm text-slate-600">Used: 125 GB • Available: 375 GB</p>
                  </div>
                </div>
              </section>
            )}

            {activeItem === 'Activity Logs' && (
              <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
                <p className="text-sm uppercase tracking-[0.24em] text-slate-400">System Administration</p>
                <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">Activity Logs</h1>
                <p className="mt-2 text-sm text-slate-600">View detailed system activity and audit logs.</p>
                <div className="mt-8 space-y-2 divide-y divide-slate-200">
                  <div className="py-3">
                    <p className="text-sm font-semibold text-slate-950">User Login: Rajesh Nair</p>
                    <p className="text-xs text-slate-600">2026-06-27 10:45:32 AM • IP: 192.168.1.100</p>
                  </div>
                  <div className="py-3">
                    <p className="text-sm font-semibold text-slate-950">Database Backup Completed</p>
                    <p className="text-xs text-slate-600">2026-06-27 02:30:15 AM • Size: 12.4 GB</p>
                  </div>
                  <div className="py-3">
                    <p className="text-sm font-semibold text-slate-950">User Created: Sneha Desai</p>
                    <p className="text-xs text-slate-600">2026-06-26 03:15:42 PM • Department: Warehouse</p>
                  </div>
                  <div className="py-3">
                    <p className="text-sm font-semibold text-slate-950">Password Reset: Amit Kumar</p>
                    <p className="text-xs text-slate-600">2026-06-26 11:22:10 AM • Success</p>
                  </div>
                </div>
              </section>
            )}

            {activeItem === 'Notifications' && (
              <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
                <p className="text-sm uppercase tracking-[0.24em] text-slate-400">System Administration</p>
                <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">Notifications</h1>
                <p className="mt-2 text-sm text-slate-600">Manage system notifications and alert settings.</p>
                <div className="mt-8 space-y-3">
                  <div className="rounded-2xl border border-blue-200 bg-blue-50 p-4">
                    <p className="text-sm font-semibold text-blue-950">ⓘ Info: System Update Available</p>
                    <p className="mt-1 text-xs text-blue-700">Version 1.1.0 is ready to install</p>
                  </div>
                  <div className="rounded-2xl border border-amber-200 bg-amber-50 p-4">
                    <p className="text-sm font-semibold text-amber-950">⚠ Warning: Storage Usage High</p>
                    <p className="mt-1 text-xs text-amber-700">77% of storage capacity is being used</p>
                  </div>
                  <div className="rounded-2xl border border-rose-200 bg-rose-50 p-4">
                    <p className="text-sm font-semibold text-rose-950">✕ Alert: Failed Login Attempts</p>
                    <p className="mt-1 text-xs text-rose-700">3 failed attempts detected in last hour</p>
                  </div>
                </div>
              </section>
            )}

            {activeItem === 'System Settings' && (
              <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
                <p className="text-sm uppercase tracking-[0.24em] text-slate-400">System Administration</p>
                <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">System Settings</h1>
                <p className="mt-2 text-sm text-slate-600">Configure core system settings and preferences.</p>
                <div className="mt-8 space-y-4">
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <p className="font-semibold text-slate-950">Company Name</p>
                    <p className="mt-1 text-sm text-slate-600">Swajit Engineering Pvt. Ltd.</p>
                  </div>
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <p className="font-semibold text-slate-950">System Version</p>
                    <p className="mt-1 text-sm text-slate-600">v1.0.0 • Last Updated: 2026-06-01</p>
                  </div>
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <p className="font-semibold text-slate-950">Session Timeout</p>
                    <p className="mt-1 text-sm text-slate-600">30 minutes of inactivity</p>
                  </div>
                  <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                    <p className="font-semibold text-slate-950">API Endpoint</p>
                    <p className="mt-1 text-sm text-slate-600">https://api.swajit.local/v1</p>
                  </div>
                </div>
              </section>
            )}
          </main>

          {/* Footer */}
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

export default SystemAdminDashboard;
