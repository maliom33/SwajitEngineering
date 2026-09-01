import ApiResourceTable from '../../components/ApiResourceTable';

function Alerts() {
  return <ApiResourceTable title="Critical Inventory Alerts" description="Live low-stock inventory from the warehouse API. Reorder action is not currently exposed by the backend." endpoint="warehouse/inventory/low-stock/" columns={[{ key: 'inventory_id', label: 'ID' }, { key: 'product', label: 'Product' }, { key: 'quantity_available', label: 'Available' }, { key: 'reorder_level', label: 'Reorder level' }]} searchKeys={['product']} />;
}

export default Alerts;
