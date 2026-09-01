import ApiResourceTable from '../../components/ApiResourceTable';

function InvoiceManagement() {
  return <ApiResourceTable title="Invoice List & Generation" description="Live invoices. The backend supports invoice actions, but no create form was fabricated from the previous mock fields." endpoint="finance/invoices/" columns={[{ key: 'invoice_id', label: 'ID' }, { key: 'invoice_number', label: 'Invoice' }, { key: 'customer', label: 'Customer' }, { key: 'total_amount', label: 'Total' }, { key: 'amount_due', label: 'Due' }, { key: 'status', label: 'Status' }]} searchKeys={['invoice_number', 'customer', 'status']} />;
}

export default InvoiceManagement;
