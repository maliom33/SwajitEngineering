import ApiResourceTable from '../../components/ApiResourceTable';

function PaymentManagement() {
  return <ApiResourceTable title="Payments, Receipts & Status Tracking" description="Payments are read-only here; the backend supports recording payments through invoices and refund actions." endpoint="finance/payments/" columns={[{ key: 'payment_id', label: 'ID' }, { key: 'invoice', label: 'Invoice' }, { key: 'payment_date', label: 'Date' }, { key: 'amount', label: 'Amount' }, { key: 'payment_method', label: 'Method' }, { key: 'payment_status', label: 'Status' }]} searchKeys={['invoice', 'payment_method', 'payment_status']} />;
}

export default PaymentManagement;
