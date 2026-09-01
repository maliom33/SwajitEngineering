import { Outlet } from 'react-router-dom';
import MainLayout from '../../components/MainLayout';

const salesLinks = [
  { label: 'Dashboard', to: '/sales', icon: 'LayoutGrid' },
  { label: 'Customer Management', to: '/sales/customers', icon: 'Users' },
  { label: 'Sales Orders', to: '/sales/orders', icon: 'ShoppingCart' },
  { label: 'Purchase Orders', to: '/sales/purchase-orders', icon: 'Package' },
  { label: 'Quotations', to: '/sales/quotations', icon: 'FileText' },
  { label: 'Order Tracking', to: '/sales/tracking', icon: 'Truck' },
  { label: 'Customer History', to: '/sales/history', icon: 'History' },
  { label: 'Reports', to: '/sales/reports', icon: 'BarChart3' },
  { label: 'Notifications', to: '/sales/notifications', icon: 'Bell' },
  { label: 'Profile', to: '/sales/profile', icon: 'User' },
  { label: 'Logout', to: '/login', icon: 'LogOut' },
];

function SalesLayout() {
  return (
    <MainLayout title="Sales" links={salesLinks} userProfile={{ name: 'Sales Executive', role: 'Sales' }}>
      <Outlet />
    </MainLayout>
  );
}

export default SalesLayout;
