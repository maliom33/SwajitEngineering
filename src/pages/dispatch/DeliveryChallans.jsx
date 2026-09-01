import ApiResourceTable from '../../components/ApiResourceTable';

function DeliveryChallans() {
  return <ApiResourceTable title="Generate & Review Delivery Challans" description="Live challans. Generation is available through the dispatch action endpoint." endpoint="dispatch/challans/" columns={[{ key: 'challan_id', label: 'ID' }, { key: 'challan_number', label: 'Challan' }, { key: 'dispatch', label: 'Dispatch' }, { key: 'challan_date', label: 'Date' }, { key: 'total_items', label: 'Items' }, { key: 'status', label: 'Status' }]} searchKeys={['challan_number', 'dispatch', 'status']} />;
}

export default DeliveryChallans;
