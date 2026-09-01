import ApiResourceTable from '../../components/ApiResourceTable';

function Receivables() {
  return <ApiResourceTable title="Customer Receivables" description="Live invoice balances from the finance API." endpoint="finance/invoices/" columns={[{ key: 'invoice_number', label: 'Invoice' }, { key: 'customer', label: 'Customer' }, { key: 'invoice_date', label: 'Date' }, { key: 'amount_due', label: 'Amount due' }, { key: 'status', label: 'Status' }]} searchKeys={['invoice_number', 'customer', 'status']} />;
}

export default Receivables;
