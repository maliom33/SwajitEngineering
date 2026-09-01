import ApiResourceTable from '../../components/ApiResourceTable';

function Deliveries() {
  return <ApiResourceTable title="Active & Delayed Deliveries" description="Live deliveries from the logistics API." endpoint="logistics/deliveries/active/" columns={[{ key: 'delivery_id', label: 'ID' }, { key: 'delivery_number', label: 'Delivery' }, { key: 'order', label: 'Order' }, { key: 'driver', label: 'Driver' }, { key: 'vehicle', label: 'Vehicle' }, { key: 'delivery_status', label: 'Status' }, { key: 'expected_delivery_at', label: 'ETA' }]} searchKeys={['delivery_number', 'delivery_status']} />;
}

export default Deliveries;
