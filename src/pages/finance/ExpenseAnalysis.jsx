import ApiResourceTable from '../../components/ApiResourceTable';

function ExpenseAnalysis() {
  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Expense Analysis</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Operational, Payroll & Maintenance Expense Review</h1>
      </section>

      <ApiResourceTable title="Recorded Expenses" description="Live expenses from the finance API." endpoint="finance/expenses/" columns={[{ key: 'expense_number', label: 'Expense' }, { key: 'category', label: 'Category' }, { key: 'amount', label: 'Amount' }, { key: 'expense_date', label: 'Date' }, { key: 'status', label: 'Status' }]} searchKeys={['expense_number', 'status', 'description']} />
    </div>
  );
}

export default ExpenseAnalysis;
