import ApiResourceTable from '../../components/ApiResourceTable';

function PayslipManagement() {
  return <ApiResourceTable title="Payroll Items" description="The backend has no dedicated payslip resource; payroll items are shown as the closest available source." endpoint="workforce/payroll-items/" columns={[{ key: 'payroll_item_id', label: 'ID' }, { key: 'employee', label: 'Employee' }, { key: 'payroll_run', label: 'Payroll run' }, { key: 'net_salary', label: 'Net salary' }, { key: 'payment_status', label: 'Payment status' }]} searchKeys={['employee', 'payroll_run', 'payment_status']} />;
}

export default PayslipManagement;
