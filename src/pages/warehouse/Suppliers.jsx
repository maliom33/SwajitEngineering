import ApiResourceTable from '../../components/ApiResourceTable';

function Suppliers() {
  return <ApiResourceTable title="Supplier Directory" description="Live suppliers from the warehouse API." endpoint="warehouse/suppliers/" columns={[{ key: 'supplier_id', label: 'ID' }, { key: 'supplier_code', label: 'Code' }, { key: 'supplier_name', label: 'Supplier' }, { key: 'contact_person', label: 'Contact' }, { key: 'phone', label: 'Phone' }, { key: 'status', label: 'Status' }]} searchKeys={['supplier_code', 'supplier_name', 'contact_person']} />;
}

export default Suppliers;
