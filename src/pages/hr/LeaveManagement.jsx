import { useEffect, useMemo, useState } from 'react';
import client from '../../api/client';

function formatStatus(status) {
  return status.toLowerCase().replace(/_/g, ' ').replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function LeaveManagement() {
  const [leaveTypes, setLeaveTypes] = useState([]);
  const [requests, setRequests] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [updatingId, setUpdatingId] = useState(null);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [formError, setFormError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const loadLeaveData = async () => {
    setIsLoading(true);
    setErrorMessage('');
    try {
      const [typeResponse, requestResponse, employeeResponse] = await Promise.all([
        client.get('workforce/leave-types/'),
        client.get('workforce/leave-requests/'),
        client.get('workforce/employees/'),
      ]);
      const getResults = (response) => (Array.isArray(response.data) ? response.data : response.data?.results) || [];
      setLeaveTypes(getResults(typeResponse));
      setRequests(getResults(requestResponse));
      setEmployees(getResults(employeeResponse));
    } catch (error) {
      if (error.response?.status === 403) {
        setErrorMessage('You do not have permission to view leave records.');
      } else if (error.response?.status >= 500) {
        setErrorMessage('The leave service is temporarily unavailable. Please try again shortly.');
      } else if (!error.response) {
        setErrorMessage('The backend is unavailable. Please check the server and try again.');
      } else {
        setErrorMessage('We could not load leave data. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadLeaveData();
  }, []);

  const employeeNames = useMemo(() => new Map(employees.map((employee) => [employee.employee_id, `${employee.employee_code} - ${employee.first_name} ${employee.last_name}`])), [employees]);
  const leaveTypeNames = useMemo(() => new Map(leaveTypes.map((leaveType) => [leaveType.leave_type_id, leaveType.leave_name])), [leaveTypes]);
  const visibleRequests = useMemo(() => requests.filter((request) => statusFilter === 'ALL' || request.status === statusFilter), [requests, statusFilter]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setFormError('');
    setSuccessMessage('');
    setIsSaving(true);
    const payload = Object.fromEntries(new FormData(event.currentTarget).entries());
    payload.employee = Number(payload.employee);
    payload.leave_type = Number(payload.leave_type);
    payload.total_days = Number(payload.total_days);

    if (payload.end_date < payload.start_date) {
      setFormError('The end date cannot be before the start date.');
      setIsSaving(false);
      return;
    }

    try {
      await client.post('workforce/leave-requests/', payload);
      setIsFormOpen(false);
      setSuccessMessage('Leave request submitted successfully.');
      await loadLeaveData();
    } catch (error) {
      if (error.response?.status === 403) {
        setFormError('You do not have permission to submit leave requests.');
      } else if (error.response?.status === 400) {
        setFormError('Please check the leave request details and try again.');
      } else if (!error.response) {
        setFormError('The backend is unavailable. Please try again.');
      } else {
        setFormError('We could not submit this leave request. Please try again.');
      }
    } finally {
      setIsSaving(false);
    }
  };

  const updateRequestStatus = async (request, status) => {
    setUpdatingId(request.leave_request_id);
    setErrorMessage('');
    setSuccessMessage('');
    try {
      await client.patch(`workforce/leave-requests/${request.leave_request_id}/`, { status });
      setSuccessMessage(`Leave request ${status.toLowerCase()} successfully.`);
      await loadLeaveData();
    } catch (error) {
      if (error.response?.status === 403) {
        setErrorMessage('You do not have permission to update leave requests.');
      } else if (error.response?.status === 400) {
        setErrorMessage('The leave request could not be updated with that status.');
      } else if (!error.response) {
        setErrorMessage('The backend is unavailable. Please try again.');
      } else {
        setErrorMessage('We could not update this leave request. Please try again.');
      }
    } finally {
      setUpdatingId(null);
    }
  };

  return (
    <div>
      <div className="mb-4 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-2xl font-semibold">Leave Management</h2>
          <p className="mt-2 text-sm text-slate-600">Manage leave requests, configured leave limits, and request history.</p>
        </div>
        <button type="button" onClick={() => { setFormError(''); setIsFormOpen(true); }} className="rounded-2xl bg-brand-900 px-4 py-2 text-white">Request Leave</button>
      </div>

      {successMessage && <p role="status" className="mb-4 rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-700">{successMessage}</p>}
      {errorMessage && <div role="alert" className="mb-4 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"><p>{errorMessage}</p><button type="button" onClick={loadLeaveData} className="mt-3 rounded-2xl bg-red-700 px-4 py-2 font-medium text-white">Try again</button></div>}

      {isLoading && <div role="status" className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-600">Loading leave data...</div>}

      {!isLoading && !errorMessage && <>
        <section className="mb-6 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <div className="flex items-center justify-between"><h3 className="text-lg font-semibold text-slate-950">Leave Types and Limits</h3><span className="text-sm text-slate-500">Configured allowances</span></div>
          {leaveTypes.length === 0 ? <p className="mt-4 text-sm text-slate-600">No leave types have been configured.</p> : <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">{leaveTypes.map((leaveType) => <div key={leaveType.leave_type_id} className="rounded-2xl border border-slate-100 bg-slate-50 p-4"><p className="font-medium text-slate-950">{leaveType.leave_name}</p><p className="mt-1 text-sm text-slate-600">{leaveType.maximum_days} days · {leaveType.is_paid ? 'Paid' : 'Unpaid'}</p></div>)}</div>}
        </section>

        <div className="mb-4 flex flex-wrap items-center gap-3 rounded-2xl border border-slate-200 bg-white p-4"><label className="text-sm text-slate-700">Status<select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)} className="ml-2 rounded-2xl border border-slate-200 px-3 py-2"><option value="ALL">All statuses</option><option value="PENDING">Pending</option><option value="APPROVED">Approved</option><option value="REJECTED">Rejected</option><option value="CANCELLED">Cancelled</option></select></label></div>

        {visibleRequests.length === 0 ? <div className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-600">No leave requests match the selected status.</div> : <div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white p-4 shadow-sm"><table className="w-full min-w-[900px] text-left text-sm text-slate-700"><thead><tr className="text-slate-600"><th className="px-3 py-3">Employee</th><th className="px-3 py-3">Leave type</th><th className="px-3 py-3">Dates</th><th className="px-3 py-3">Days</th><th className="px-3 py-3">Status</th><th className="px-3 py-3">Reason</th><th className="px-3 py-3">Actions</th></tr></thead><tbody className="divide-y divide-slate-100">{visibleRequests.map((request) => <tr key={request.leave_request_id}><td className="px-3 py-3 font-medium text-slate-900">{employeeNames.get(request.employee) || `Employee #${request.employee}`}</td><td className="px-3 py-3">{leaveTypeNames.get(request.leave_type) || `Leave type #${request.leave_type}`}</td><td className="px-3 py-3">{request.start_date} to {request.end_date}</td><td className="px-3 py-3">{request.total_days}</td><td className="px-3 py-3">{formatStatus(request.status)}</td><td className="max-w-xs px-3 py-3">{request.reason}</td><td className="px-3 py-3">{request.status === 'PENDING' && <div className="flex gap-2"><button type="button" onClick={() => updateRequestStatus(request, 'APPROVED')} disabled={updatingId === request.leave_request_id} className="rounded-2xl bg-emerald-600 px-3 py-2 text-xs text-white disabled:opacity-60">Approve</button><button type="button" onClick={() => updateRequestStatus(request, 'REJECTED')} disabled={updatingId === request.leave_request_id} className="rounded-2xl bg-rose-600 px-3 py-2 text-xs text-white disabled:opacity-60">Reject</button></div>}</td></tr>)}</tbody></table></div>}
      </>}

      {isFormOpen && <div className="fixed inset-0 z-30 flex items-start justify-center overflow-y-auto bg-slate-950/40 px-4 py-10" role="dialog" aria-modal="true" aria-labelledby="leave-form-title"><form onSubmit={handleSubmit} className="w-full max-w-2xl rounded-3xl bg-white p-6 shadow-2xl"><div className="flex items-center justify-between"><h3 id="leave-form-title" className="text-xl font-semibold text-slate-950">Request Leave</h3><button type="button" onClick={() => !isSaving && setIsFormOpen(false)} className="rounded-2xl border border-slate-200 px-3 py-2 text-sm text-slate-600">Close</button></div>{formError && <p role="alert" className="mt-4 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{formError}</p>}<div className="mt-6 grid gap-4 sm:grid-cols-2"><label className="text-sm text-slate-700 sm:col-span-2">Employee<select name="employee" required className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3"><option value="">Select employee</option>{employees.map((employee) => <option key={employee.employee_id} value={employee.employee_id}>{employee.employee_code} - {employee.first_name} {employee.last_name}</option>)}</select></label><label className="text-sm text-slate-700">Leave type<select name="leave_type" required className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3"><option value="">Select leave type</option>{leaveTypes.filter((leaveType) => leaveType.is_active).map((leaveType) => <option key={leaveType.leave_type_id} value={leaveType.leave_type_id}>{leaveType.leave_name}</option>)}</select></label><label className="text-sm text-slate-700">Total days<input name="total_days" type="number" min="0.5" step="0.5" required className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3" /></label><label className="text-sm text-slate-700">Start date<input name="start_date" type="date" required className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3" /></label><label className="text-sm text-slate-700">End date<input name="end_date" type="date" required className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3" /></label><label className="text-sm text-slate-700 sm:col-span-2">Reason<textarea name="reason" required rows="3" className="mt-1 w-full rounded-2xl border border-slate-200 px-3 py-2" /></label></div><div className="mt-6 flex justify-end gap-3"><button type="button" onClick={() => !isSaving && setIsFormOpen(false)} disabled={isSaving} className="rounded-2xl border border-slate-200 px-4 py-2 text-sm text-slate-700">Cancel</button><button type="submit" disabled={isSaving || employees.length === 0 || leaveTypes.length === 0} className="rounded-2xl bg-brand-900 px-4 py-2 text-sm font-medium text-white disabled:opacity-60">{isSaving ? 'Submitting...' : 'Submit Request'}</button></div></form></div>}
    </div>
  );
}

export default LeaveManagement;
