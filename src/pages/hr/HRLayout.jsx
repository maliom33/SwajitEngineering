import { Outlet } from 'react-router-dom';
import MainLayout from '../../components/MainLayout';

const hrLinks = [
  { label: 'Dashboard', to: '/hr', icon: 'LayoutGrid' },
  { label: 'Employee Management', to: '/hr/employees', icon: 'Users' },
  { label: 'Attendance Management', to: '/hr/attendance', icon: 'Clock' },
  { label: 'Leave Management', to: '/hr/leave', icon: 'Calendar' },
  { label: 'Recruitment', to: '/hr/recruitment', icon: 'UserPlus' },
  { label: 'Shift Management', to: '/hr/shifts', icon: 'Repeat' },
  { label: 'Payroll', to: '/hr/payroll', icon: 'DollarSign' },
  { label: 'Employee Performance', to: '/hr/performance', icon: 'BarChart3' },
  { label: 'Reports', to: '/hr/reports', icon: 'FileText' },
  { label: 'Notifications', to: '/hr/notifications', icon: 'Bell' },
  { label: 'Profile', to: '/hr/profile', icon: 'User' },
  { label: 'Logout', to: '/login', icon: 'LogOut' },
];

function HRLayout() {
  return (
    <MainLayout title="HR" links={hrLinks} userProfile={{ name: 'HR Manager', role: 'Human Resources' }}>
      <Outlet />
    </MainLayout>
  );
}

export default HRLayout;
