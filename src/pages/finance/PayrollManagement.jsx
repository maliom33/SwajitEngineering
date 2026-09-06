import { useEffect, useMemo, useState } from 'react';
import client from '../../api/client';

function formatCurrency(value) {
  return value === null || value === undefined ? 'Not available' : `₹${Number(value).toLocaleString('en-IN')}`;
}

function formatStatus(status) {
  return status ? status.toLowerCase().replace(/_/g, ' ').replace(/\b\w/g, (letter) => letter.toUpperCase()) : 'Not available';
}

function PayrollManagement() {
  const [payrollItems, setPayrollItems] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [payrollRuns, setPayrollRuns] = useState([]);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const loadPayroll = async () => {
    setIsLoading(true);
    setErrorMessage('');
    try {
      const [itemsResponse, employeesResponse, runsResponse] = await Promise.all([
        client.get('workforce/payroll-items/'),
        client.get('workforce/employees/'),
        client.get('workforce/payroll-runs/'),
      ]);
      const getResults = (response) => (Array.isArray(response.data) ? response.data : response.data?.results) || [];
      setPayrollItems(getResults(itemsResponse));
      setEmployees(getResults(employeesResponse));
      setPayrollRuns(getResults(runsResponse));
    } catch (error) {
      if (error.response?.status === 403) {
        setErrorMessage('You do not have permission to view payroll records.');
      } else if (error.response?.status >= 500) {
        setErrorMessage('The payroll service is temporarily unavailable. Please try again shortly.');
      } else if (!error.response) {
        setErrorMessage('The backend is unavailable. Please check the server and try again.');
      } else {
        setErrorMessage('We could not load payroll records. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadPayroll();
  }, []);

  const employeeMap = useMemo(() => new Map(employees.map((employee) => [employee.employee_id, employee])), [employees]);
  const runMap = useMemo(() => new Map(payrollRuns.map((run) => [run.payroll_run_id, run])), [payrollRuns]);
  const rows = useMemo(() => payrollItems.map((item) => {
    const employee = employeeMap.get(item.employee);
    const run = runMap.get(item.payroll_run);
    return {
      ...item,
      employeeId: employee?.employee_code || `Employee #${item.employee}`,
      employeeName: employee ? `${employee.first_name} ${employee.last_name}` : 'Unknown employee',
      department: employee?.department_name || 'Not available',
      payrollStatus: formatStatus(run?.status),
    };
  }), [payrollItems, employeeMap, runMap]);

  const visibleRows = useMemo(() => {
    const query = search.trim().toLowerCase();
    return rows.filter((row) => {
      const matchesStatus = statusFilter === 'ALL' || row.payment_status === statusFilter;
      const matchesSearch = !query || [row.employeeId, row.employeeName, row.department, row.payrollStatus].some((value) => String(value).toLowerCase().includes(query));
      return matchesStatus && matchesSearch;
    });
  }, [rows, search, statusFilter]);

  return (
    <div className="space-y-6">
      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Payroll Management</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">Employee Payroll & Monthly Payroll Status</h1>
      </section>

      {successMessage && <p role="status" className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-700">{successMessage}</p>}
      {errorMessage && <div role="alert" className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"><p>{errorMessage}</p><button type="button" onClick={loadPayroll} className="mt-3 rounded-2xl bg-red-700 px-4 py-2 font-medium text-white">Try again</button></div>}

      {!isLoading && !errorMessage && <div className="flex flex-wrap items-center gap-3 rounded-2xl border border-slate-200 bg-white/90 p-4 shadow-sm"><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search payroll..." className="rounded-2xl border border-slate-200 px-4 py-2" /><select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)} className="rounded-2xl border border-slate-200 px-4 py-2"><option value="ALL">All payment statuses</option><option value="PENDING">Pending</option><option value="PAID">Paid</option><option value="FAILED">Failed</option><option value="CANCELLED">Cancelled</option></select></div>}

      <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm">
        {isLoading && <div role="status" className="p-6 text-sm text-slate-600">Loading payroll records...</div>}
        {!isLoading && !errorMessage && visibleRows.length === 0 && <div className="p-6 text-sm text-slate-600">{rows.length === 0 ? 'No payroll records have been created yet.' : 'No payroll records match your search or filter.'}</div>}
        {!isLoading && !errorMessage && visibleRows.length > 0 && <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500">
                <th className="px-3 py-3">Employee ID</th>
                <th className="px-3 py-3">Employee Name</th>
                <th className="px-3 py-3">Department</th>
                <th className="px-3 py-3">Basic Salary</th>
                <th className="px-3 py-3">Overtime</th>
                <th className="px-3 py-3">Allowances</th>
                <th className="px-3 py-3">Deductions</th>
                <th className="px-3 py-3">Net Salary</th>
                <th className="px-3 py-3">Status</th>
              </tr>
            </thead>
            <tbody>
              {visibleRows.map((entry) => (
                <tr key={entry.payroll_item_id} className="border-b border-slate-100 hover:bg-slate-50">
                  <td className="px-3 py-3 font-medium text-slate-900">{entry.employeeId}</td>
                  <td className="px-3 py-3">{entry.employeeName}</td>
                  <td className="px-3 py-3">{entry.department}</td>
                  <td className="px-3 py-3">{formatCurrency(entry.basic_salary)}</td>
                  <td className="px-3 py-3">{formatCurrency(entry.overtime)}</td>
                  <td className="px-3 py-3">{formatCurrency(entry.allowances)}</td>
                  <td className="px-3 py-3">{formatCurrency(entry.deductions)}</td>
                  <td className="px-3 py-3">{formatCurrency(entry.net_salary)}</td>
                  <td className="px-3 py-3">{entry.payrollStatus}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>}
      </section>
    </div>
  );
}

export default PayrollManagement;
