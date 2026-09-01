import ApiResourceTable from '../../components/ApiResourceTable';

function Fleet() {
  return <ApiResourceTable title="Fleet Availability & Utilization" description="Live vehicles from the logistics API." endpoint="logistics/vehicles/" columns={[{ key: 'vehicle_id', label: 'ID' }, { key: 'vehicle_number', label: 'Vehicle' }, { key: 'vehicle_type', label: 'Type' }, { key: 'model', label: 'Model' }, { key: 'capacity', label: 'Capacity' }, { key: 'status', label: 'Status' }]} searchKeys={['vehicle_number', 'model', 'status']} />;
}

export default Fleet;
