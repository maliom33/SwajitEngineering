import ApiResourceTable from '../../components/ApiResourceTable';

function BillingManagement() {
  return <ApiResourceTable title="Customer Billing & Bill Status" description="Live invoice records used for billing. Invoice generation is not a separate frontend action here." endpoint="finance/invoices/" columns={[{ key: 'invoice_number', label: 'Invoice' }, { key: 'customer', label: 'Customer' }, { key: 'total_amount', label: 'Total' }, { key: 'amount_due', label: 'Due' }, { key: 'status', label: 'Status' }]} searchKeys={['invoice_number', 'customer', 'status']} />;
}

export default BillingManagement;
