import ApiResourceTable from '../../components/ApiResourceTable';

function Customers() {
  return <ApiResourceTable title="Customer List" description="Live customers from the sales API. Customer creation requires backend fields not present in the previous mock form." endpoint="sales/customers/" columns={[{ key: 'customer_id', label: 'ID' }, { key: 'customer_code', label: 'Code' }, { key: 'company_name', label: 'Company' }, { key: 'contact_person', label: 'Contact' }, { key: 'phone', label: 'Phone' }, { key: 'email', label: 'Email' }, { key: 'city', label: 'City' }, { key: 'status', label: 'Status' }]} searchKeys={['customer_code', 'company_name', 'contact_person', 'email', 'city']} />;
}

export default Customers;
