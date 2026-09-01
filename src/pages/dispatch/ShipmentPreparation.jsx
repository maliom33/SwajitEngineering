import ApiResourceTable from '../../components/ApiResourceTable';

function ShipmentPreparation() {
  return <ApiResourceTable title="Shipment Lists & Packaging Verification" description="Live dispatch items. Preparation mutations require the supported dispatch prepare action." endpoint="dispatch/dispatch-items/" columns={[{ key: 'dispatch_item_id', label: 'ID' }, { key: 'dispatch', label: 'Dispatch' }, { key: 'product', label: 'Product' }, { key: 'quantity', label: 'Quantity' }, { key: 'package_count', label: 'Packages' }, { key: 'remarks', label: 'Remarks' }]} searchKeys={['dispatch', 'product', 'remarks']} />;
}

export default ShipmentPreparation;
