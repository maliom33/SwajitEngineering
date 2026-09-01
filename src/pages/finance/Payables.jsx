import ApiResourceTable from '../../components/ApiResourceTable';

function Payables() {
  return <ApiResourceTable title="Supplier Payables" description="Recorded expenses used as payable obligations." endpoint="finance/expenses/" columns={[{ key: 'expense_number', label: 'Expense' }, { key: 'category', label: 'Category' }, { key: 'amount', label: 'Amount' }, { key: 'expense_date', label: 'Date' }, { key: 'status', label: 'Status' }]} searchKeys={['expense_number', 'status']} />;
}

export default Payables;
