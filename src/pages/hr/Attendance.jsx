import { useEffect, useMemo, useState } from 'react';
import client from '../../api/client';

const today = new Date().toISOString().slice(0, 10);

function formatStatus(status) {
  return status.toLowerCase().replace(/_/g, ' ').replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function formatDateTime(value) {
  return value ? new Date(value).toLocaleString() : 'Not recorded';
}

function Attendance() {
  const [records, setRecords] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [selectedDate, setSelectedDate] = useState(today);
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [photoPreview, setPhotoPreview] = useState('');

  const loadAttendance = async () => {
    setIsLoading(true);
    setErrorMessage('');
    try {
      const [attendanceResponse, employeeResponse] = await Promise.all([
        client.get('workforce/attendance/'),
        client.get('workforce/employees/'),
      ]);
      const getResults = (response) => (Array.isArray(response.data) ? response.data : response.data?.results) || [];
      setRecords(getResults(attendanceResponse));
      setEmployees(getResults(employeeResponse));
    } catch (error) {
      if (error.response?.status === 403) setErrorMessage('You do not have permission to view attendance records.');
      else if (error.response?.status >= 500) setErrorMessage('The attendance service is temporarily unavailable. Please try again shortly.');
      else if (!error.response) setErrorMessage('The backend is unavailable. Please check the server and try again.');
      else setErrorMessage('We could not load attendance records. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => { loadAttendance(); }, []);

  const openDetails = async (record) => {
    setSelectedRecord(record);
    setPhotoPreview('');
    if (record.photo_available) {
      const response = await client.get(`workforce/attendance/${record.attendance_id}/photo/`, { responseType: 'blob' });
      setPhotoPreview(URL.createObjectURL(response.data));
    }
  };

  const employeeNames = useMemo(() => new Map(
    employees.map((employee) => [employee.employee_id, `${employee.employee_code} - ${employee.first_name} ${employee.last_name}`]),
  ), [employees]);

  const visibleRecords = useMemo(() => records.filter((record) => {
    const matchesDate = !selectedDate || record.attendance_date === selectedDate;
    const matchesStatus = statusFilter === 'ALL' || record.status === statusFilter;
    return matchesDate && matchesStatus;
  }), [records, selectedDate, statusFilter]);

  return (
    <div>
      <div className="mb-4 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-2xl font-semibold">Attendance</h2>
          <p className="mt-2 text-sm text-slate-600">Attendance records generated through the employee mobile application.</p>
        </div>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600">View only</span>
      </div>

      {errorMessage && <div role="alert" className="mb-4 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"><p>{errorMessage}</p><button type="button" onClick={loadAttendance} className="mt-3 rounded-2xl bg-red-700 px-4 py-2 font-medium text-white">Try again</button></div>}
      <div className="mb-4 flex flex-wrap items-center gap-3 rounded-2xl border border-slate-200 bg-white p-4"><label className="text-sm text-slate-700">Date<input type="date" value={selectedDate} onChange={(event) => setSelectedDate(event.target.value)} className="ml-2 rounded-2xl border border-slate-200 px-3 py-2" /></label><label className="text-sm text-slate-700">Status<select value={statusFilter} onChange={(event) => setStatusFilter(event.target.value)} className="ml-2 rounded-2xl border border-slate-200 px-3 py-2"><option value="ALL">All statuses</option><option value="PRESENT">Present</option><option value="ABSENT">Absent</option><option value="HALF_DAY">Half Day</option><option value="LATE">Late</option><option value="ON_LEAVE">On Leave</option></select></label><button type="button" onClick={() => { setSelectedDate(''); setStatusFilter('ALL'); }} className="rounded-2xl border border-slate-200 px-3 py-2 text-sm text-slate-700">Clear filters</button></div>
      {isLoading && <div role="status" className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-600">Loading attendance records...</div>}
      {!isLoading && !errorMessage && visibleRecords.length === 0 && <div className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-600">No attendance records match the selected filters.</div>}
      {!isLoading && !errorMessage && visibleRecords.length > 0 && <div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white p-4 shadow-sm"><table className="w-full min-w-[980px] text-left text-sm text-slate-700"><thead><tr className="text-slate-600"><th className="px-3 py-3">Employee</th><th className="px-3 py-3">Date</th><th className="px-3 py-3">Status</th><th className="px-3 py-3">Check in</th><th className="px-3 py-3">Check out</th><th className="px-3 py-3">Method</th><th className="px-3 py-3">Location</th><th className="px-3 py-3">Photo</th><th className="px-3 py-3">Details</th></tr></thead><tbody className="divide-y divide-slate-100">{visibleRecords.map((record) => <tr key={record.attendance_id}><td className="px-3 py-3 font-medium text-slate-900">{employeeNames.get(record.employee) || `Employee #${record.employee}`}</td><td className="px-3 py-3">{record.attendance_date}</td><td className="px-3 py-3">{formatStatus(record.status)}</td><td className="px-3 py-3">{formatDateTime(record.check_in)}</td><td className="px-3 py-3">{formatDateTime(record.check_out)}</td><td className="px-3 py-3">{formatStatus(record.attendance_method)}</td><td className="px-3 py-3">{record.latitude !== null && record.longitude !== null ? `${record.latitude}, ${record.longitude}` : 'Not captured'}</td><td className="px-3 py-3">{record.photo_available ? 'Available' : 'Not available'}</td><td className="px-3 py-3"><button type="button" onClick={() => openDetails(record)} className="rounded-2xl border border-slate-200 px-3 py-2 text-xs text-slate-700">View</button></td></tr>)}</tbody></table></div>}
      {selectedRecord && <div className="fixed inset-0 z-30 flex items-center justify-center bg-slate-950/40 px-4" role="dialog" aria-modal="true" aria-labelledby="attendance-details-title"><div className="w-full max-w-lg rounded-3xl bg-white p-6 shadow-2xl"><div className="flex items-center justify-between"><h3 id="attendance-details-title" className="text-xl font-semibold text-slate-950">Attendance details</h3><button type="button" onClick={() => { setSelectedRecord(null); setPhotoPreview(''); }} className="rounded-2xl border border-slate-200 px-3 py-2 text-sm text-slate-600">Close</button></div><dl className="mt-5 grid gap-3 text-sm text-slate-700"><div><dt className="font-medium text-slate-500">Employee</dt><dd>{employeeNames.get(selectedRecord.employee) || `Employee #${selectedRecord.employee}`}</dd></div><div><dt className="font-medium text-slate-500">Date and time</dt><dd>{selectedRecord.attendance_date} | {formatDateTime(selectedRecord.check_in)}</dd></div><div><dt className="font-medium text-slate-500">Status</dt><dd>{formatStatus(selectedRecord.status)}</dd></div><div><dt className="font-medium text-slate-500">Location</dt><dd>{selectedRecord.latitude !== null && selectedRecord.longitude !== null ? `${selectedRecord.latitude}, ${selectedRecord.longitude}` : 'Not captured'}</dd></div></dl>{photoPreview && <img src={photoPreview} alt="Attendance capture" className="mt-5 max-h-72 w-full rounded-2xl object-contain" />}</div></div>}
    </div>
  );
}

export default Attendance;