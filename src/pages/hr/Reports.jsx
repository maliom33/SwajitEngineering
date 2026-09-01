import { useEffect, useState } from 'react';
import client from '../../api/client';

function Reports() {
  const [reports, setReports] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');

  const loadReports = async () => {
    setIsLoading(true);
    setErrorMessage('');
    try {
      const [workforceResponse, recruitmentResponse] = await Promise.all([client.get('analytics/workforce/'), client.get('analytics/recruitment/')]);
      setReports({ workforce: workforceResponse.data?.data || {}, recruitment: recruitmentResponse.data?.data || {} });
    } catch {
      setErrorMessage('We could not load HR report data. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadReports();
  }, []);

  return (
    <div>
      <div className="flex items-center justify-between gap-3"><div><h2 className="text-2xl font-semibold">Reports</h2><p className="mt-2 text-sm text-slate-600">Live workforce and recruitment summaries from the analytics API.</p></div><button type="button" onClick={loadReports} className="rounded-2xl border border-slate-200 px-4 py-2 text-sm text-slate-700">Refresh</button></div>
      {isLoading && <div role="status" className="mt-6 rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-600">Loading reports...</div>}
      {!isLoading && errorMessage && <div role="alert" className="mt-6 rounded-2xl border border-red-200 bg-red-50 p-6 text-sm text-red-700"><p>{errorMessage}</p><button type="button" onClick={loadReports} className="mt-3 rounded-2xl bg-red-700 px-4 py-2 text-white">Try again</button></div>}
      {!isLoading && !errorMessage && reports && <div className="mt-6 grid gap-6 md:grid-cols-2"><section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><h3 className="text-lg font-semibold text-slate-950">Workforce</h3><div className="mt-4 space-y-3 text-sm text-slate-700"><p>Total employees: <strong>{reports.workforce.total_employees}</strong></p><p>Active employees: <strong>{reports.workforce.active_employees}</strong></p><p>Attendance percentage: <strong>{reports.workforce.attendance_percentage}%</strong></p><p>Average work hours: <strong>{reports.workforce.average_work_hours}</strong></p><p>Performance reviews: <strong>{reports.workforce.performance_summary?.reviews ?? 0}</strong></p></div></section><section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><h3 className="text-lg font-semibold text-slate-950">Recruitment</h3><div className="mt-4 space-y-3 text-sm text-slate-700"><p>Open jobs: <strong>{reports.recruitment.open_jobs}</strong></p><p>Candidates: <strong>{reports.recruitment.candidates}</strong></p><p>Applications: <strong>{reports.recruitment.applications}</strong></p><p>Shortlisted: <strong>{reports.recruitment.shortlisted_candidates}</strong></p><p>Interviews: <strong>{reports.recruitment.interviews}</strong></p></div></section></div>}
    </div>
  );
}

export default Reports;
