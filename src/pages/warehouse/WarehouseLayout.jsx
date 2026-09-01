import { Outlet } from 'react-router-dom';
import MainLayout from '../../components/MainLayout';

const warehouseLinks = [
  { label: 'Dashboard', to: '/warehouse', icon: 'LayoutGrid' },
  { label: 'Inventory Management', to: '/warehouse/inventory', icon: 'Boxes' },
  { label: 'Stock Verification', to: '/warehouse/verification', icon: 'CheckCircle2' },
  { label: 'Products', to: '/warehouse/products', icon: 'Package' },
  { label: 'Raw Materials', to: '/warehouse/raw-materials', icon: 'Package2' },
  { label: 'Finished Goods', to: '/warehouse/finished-goods', icon: 'Warehouse' },
  { label: 'Goods Inward', to: '/warehouse/goods-inward', icon: 'ArrowDownLeft' },
  { label: 'Goods Outward', to: '/warehouse/goods-outward', icon: 'ArrowUpRight' },
  { label: 'Material Allocation', to: '/warehouse/allocation', icon: 'Shuffle' },
  { label: 'Warehouse Capacity', to: '/warehouse/capacity', icon: 'HardDrive' },
  { label: 'Low Stock Alerts', to: '/warehouse/alerts', icon: 'AlertTriangle' },
  { label: 'Supplier Management', to: '/warehouse/suppliers', icon: 'Factory' },
  { label: 'Reports', to: '/warehouse/reports', icon: 'BarChart3' },
  { label: 'Notifications', to: '/warehouse/notifications', icon: 'Bell' },
  { label: 'Profile', to: '/warehouse/profile', icon: 'User' },
  { label: 'Logout', to: '/login', icon: 'LogOut' },
];

function WarehouseLayout() {
  return (
    <MainLayout title="Warehouse" links={warehouseLinks} userProfile={{ name: 'Warehouse Manager', role: 'Warehouse' }}>
      <Outlet />
    </MainLayout>
  );
}

export default WarehouseLayout;
