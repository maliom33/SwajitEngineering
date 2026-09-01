import { Outlet } from 'react-router-dom';
import MainLayout from '../../components/MainLayout';

const directorLinks = [
  { label: 'Dashboard', to: '/director', icon: 'LayoutGrid' },
  { label: 'Company Overview', to: '/director/company', icon: 'Building2' },
  { label: 'Workforce Analytics', to: '/director/workforce', icon: 'Users' },
  { label: 'Logistics Overview', to: '/director/logistics', icon: 'Truck' },
  { label: 'Warehouse Overview', to: '/director/warehouse', icon: 'Package' },
  { label: 'Financial Overview', to: '/director/finance', icon: 'DollarSign' },
  { label: 'AI Business Insights', to: '/director/insights', icon: 'Sparkles' },
  { label: 'Reports', to: '/director/reports', icon: 'FileText' },
  { label: 'Notifications', to: '/director/notifications', icon: 'Bell' },
  { label: 'Profile', to: '/director/profile', icon: 'User' },
  { label: 'Logout', to: '/login', icon: 'LogOut' },
];

function DirectorLayout() {
  return (
    <MainLayout title="Director" links={directorLinks} userProfile={{ name: 'Director', role: 'Executive' }}>
      <Outlet />
    </MainLayout>
  );
}

export default DirectorLayout;
