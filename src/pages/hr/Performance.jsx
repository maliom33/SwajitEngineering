import { useEffect, useMemo, useState } from 'react';
import client from '../../api/client';

function Performance() {
  const [records, setRecords] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [search, setSearch] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');

  const loadPerformance = async () => {
    setIsLoading(true);
    setErrorMessage('');
    try {
      const [performanceResponse, employeeResponse] = await Promise.all([
        client.get('workforce/performance/'),
        client.get('workforce/employees/'),
      ]);
      const getResults = (response) => (Array.isArray(response.data) ? response.data : response.data?.results) || [];
      setRecords(getResults(performanceResponse));
      setEmployees(getResults(employeeResponse));
    } catch {
      setErrorMessage('We could not load performance records. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadPerformance();
  }, []);

  const employeeMap = useMemo(() => new Map(employees.map((employee) => [employee.employee_id, employee])), [employees]);
  const visibleRecords = useMemo(() => records.filter((record) => {
    const employee = employeeMap.get(record.employee);
    const name = employee ? `${employee.employee_code} ${employee.first_name} ${employee.last_name}` : `Employee ${record.employee}`;
    return !search.trim() || name.toLowerCase().includes(search.trim().toLowerCase());
  }), [records, employeeMap, search]);

  return (
    <div>
      <div className="mb-4 flex flex-wrap items-center justify-between gap-3"><div><h2 className="text-2xl font-semibold">Employee Performance</h2><p className="mt-2 text-sm text-slate-600">Performance dashboard and evaluation records.</p></div><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search employees..." className="rounded-2xl border border-slate-200 px-4 py-2" /></div>
      {isLoading && <div role="status" className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-600">Loading performance records...</div>}
      {!isLoading && errorMessage && <div role="alert" className="rounded-2xl border border-red-200 bg-red-50 p-6 text-sm text-red-700"><p>{errorMessage}</p><button type="button" onClick={loadPerformance} className="mt-3 rounded-2xl bg-red-700 px-4 py-2 text-white">Try again</button></div>}
      {!isLoading && !errorMessage && visibleRecords.length === 0 && <div className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-600">No performance records match your search.</div>}
      {!isLoading && !errorMessage && visibleRecords.length > 0 && <div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white p-4 shadow-sm"><table className="w-full min-w-[800px] text-left text-sm text-slate-700"><thead><tr className="text-slate-600"><th className="px-3 py-3">Employee</th><th className="px-3 py-3">Evaluation period</th><th className="px-3 py-3">Attendance</th><th className="px-3 py-3">Task</th><th className="px-3 py-3">Delivery</th><th className="px-3 py-3">Overall</th><th className="px-3 py-3">Remarks</th></tr></thead><tbody className="divide-y divide-slate-100">{visibleRecords.map((record) => { const employee = employeeMap.get(record.employee); return <tr key={record.performance_id}><td className="px-3 py-3 font-medium text-slate-900">{employee ? `${employee.employee_code} - ${employee.first_name} ${employee.last_name}` : `Employee #${record.employee}`}</td><td className="px-3 py-3">{record.evaluation_period_start} to {record.evaluation_period_end}</td><td className="px-3 py-3">{record.attendance_score}</td><td className="px-3 py-3">{record.task_score}</td><td className="px-3 py-3">{record.delivery_score}</td><td className="px-3 py-3 font-semibold">{record.overall_score}</td><td className="px-3 py-3">{record.remarks || 'No remarks'}</td></tr>; })}</tbody></table></div>}
    </div>
  );
}

export default Performance;
