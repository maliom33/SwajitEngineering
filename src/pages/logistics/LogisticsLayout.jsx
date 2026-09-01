import { Outlet } from 'react-router-dom';
import MainLayout from '../../components/MainLayout';

const logisticsLinks = [
  { label: 'Dashboard', to: '/logistics', icon: 'LayoutGrid' },
  { label: 'Order Management', to: '/logistics/orders', icon: 'Package' },
  { label: 'Delivery Management', to: '/logistics/deliveries', icon: 'Truck' },
  { label: 'Truck Management', to: '/logistics/trucks', icon: 'Car' },
  { label: 'Driver Management', to: '/logistics/drivers', icon: 'UserCircle2' },
  { label: 'Fleet Management', to: '/logistics/fleet', icon: 'BarChart3' },
  { label: 'Route Optimization', to: '/logistics/routes', icon: 'Map' },
  { label: 'Live GPS Tracking', to: '/logistics/gps', icon: 'MapPinned' },
  { label: 'Delivery Timeline', to: '/logistics/timeline', icon: 'Clock3' },
  { label: 'Fuel & Cost Analysis', to: '/logistics/fuel', icon: 'CircleDollarSign' },
  { label: 'Reports', to: '/logistics/reports', icon: 'FileText' },
  { label: 'Notifications', to: '/logistics/notifications', icon: 'Bell' },
  { label: 'Profile', to: '/logistics/profile', icon: 'User' },
  { label: 'Logout', to: '/login', icon: 'LogOut' },
];

function LogisticsLayout() {
  return (
    <MainLayout title="Logistics" links={logisticsLinks} userProfile={{ name: 'Logistics Manager', role: 'Logistics' }}>
      <Outlet />
    </MainLayout>
  );
}

export default LogisticsLayout;
