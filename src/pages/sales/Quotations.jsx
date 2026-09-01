import ApiResourceTable from '../../components/ApiResourceTable';

function Quotations() {
  return <ApiResourceTable title="Quotation List" description="Live quotations from the sales API. The previous form did not contain the required customer/date financial fields for a safe create request." endpoint="sales/quotations/" columns={[{ key: 'quotation_id', label: 'ID' }, { key: 'quotation_number', label: 'Quotation' }, { key: 'customer', label: 'Customer' }, { key: 'total_amount', label: 'Total' }, { key: 'status', label: 'Status' }, { key: 'quotation_date', label: 'Date' }]} searchKeys={['quotation_number', 'customer', 'status']} />;
}

export default Quotations;
