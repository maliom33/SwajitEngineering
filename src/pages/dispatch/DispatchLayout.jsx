import { Outlet } from 'react-router-dom';
import MainLayout from '../../components/MainLayout';

const dispatchLinks = [
  { label: 'Dashboard', to: '/dispatch', icon: 'LayoutGrid' },
  { label: 'Dispatch Planning', to: '/dispatch/planning', icon: 'Calendar' },
  { label: 'Ready for Dispatch', to: '/dispatch/ready', icon: 'PackageCheck' },
  { label: 'Shipment Preparation', to: '/dispatch/shipment', icon: 'Package' },
  { label: 'Loading Verification', to: '/dispatch/loading', icon: 'ShieldCheck' },
  { label: 'Delivery Challans', to: '/dispatch/challans', icon: 'FileText' },
  { label: 'Vehicle Dispatch', to: '/dispatch/vehicles', icon: 'Truck' },
  { label: 'Dispatch Schedule', to: '/dispatch/schedule', icon: 'Clock3' },
  { label: 'Dispatch History', to: '/dispatch/history', icon: 'History' },
  { label: 'Reports', to: '/dispatch/reports', icon: 'BarChart3' },
  { label: 'Notifications', to: '/dispatch/notifications', icon: 'Bell' },
  { label: 'Profile', to: '/dispatch/profile', icon: 'User' },
  { label: 'Logout', to: '/login', icon: 'LogOut' },
];

function DispatchLayout() {
  return (
    <MainLayout title="Dispatch" links={dispatchLinks} userProfile={{ name: 'Dispatch Executive', role: 'Dispatch' }}>
      <Outlet />
    </MainLayout>
  );
}

export default DispatchLayout;
