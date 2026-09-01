import { useEffect, useMemo, useState } from 'react';
import client from '../../api/client';

function formatStatus(status) {
  return status ? status.toLowerCase().replace(/_/g, ' ').replace(/\b\w/g, (letter) => letter.toUpperCase()) : 'Not available';
}

function Recruitment() {
  const [jobs, setJobs] = useState([]);
  const [candidates, setCandidates] = useState([]);
  const [applications, setApplications] = useState([]);
  const [interviews, setInterviews] = useState([]);
  const [search, setSearch] = useState('');
  const [candidateStatus, setCandidateStatus] = useState('ALL');
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');

  const loadRecruitment = async () => {
    setIsLoading(true);
    setErrorMessage('');
    try {
      const responses = await Promise.all([
        client.get('recruitment/jobs/'),
        client.get('recruitment/candidates/'),
        client.get('recruitment/applications/'),
        client.get('recruitment/interviews/'),
      ]);
      const getResults = (response) => (Array.isArray(response.data) ? response.data : response.data?.results) || [];
      setJobs(getResults(responses[0]));
      setCandidates(getResults(responses[1]));
      setApplications(getResults(responses[2]));
      setInterviews(getResults(responses[3]));
    } catch (error) {
      if (error.response?.status === 403) setErrorMessage('You do not have permission to view recruitment records.');
      else if (!error.response) setErrorMessage('The backend is unavailable. Please check the server and try again.');
      else setErrorMessage('We could not load recruitment data. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadRecruitment();
  }, []);

  const visibleCandidates = useMemo(() => candidates.filter((candidate) => {
    const query = search.trim().toLowerCase();
    const name = `${candidate.candidate_code} ${candidate.first_name} ${candidate.last_name} ${candidate.email}`.toLowerCase();
    return (candidateStatus === 'ALL' || candidate.candidate_status === candidateStatus) && (!query || name.includes(query));
  }), [candidates, search, candidateStatus]);

  return (
    <div>
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"><div><h2 className="text-2xl font-semibold">Recruitment</h2><p className="mt-2 text-sm text-slate-600">Job openings, candidates, applications, and interviews.</p></div><button type="button" onClick={loadRecruitment} className="rounded-2xl border border-slate-200 px-4 py-2 text-sm text-slate-700">Refresh</button></div>
      {errorMessage && <div role="alert" className="mb-6 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"><p>{errorMessage}</p><button type="button" onClick={loadRecruitment} className="mt-3 rounded-2xl bg-red-700 px-4 py-2 text-white">Try again</button></div>}
      {isLoading && <div role="status" className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-600">Loading recruitment data...</div>}
      {!isLoading && !errorMessage && <><div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4"><div className="rounded-2xl border border-slate-200 bg-white p-5"><p className="text-sm text-slate-500">Open jobs</p><p className="mt-2 text-2xl font-semibold">{jobs.filter((job) => job.status === 'OPEN').length}</p></div><div className="rounded-2xl border border-slate-200 bg-white p-5"><p className="text-sm text-slate-500">Candidates</p><p className="mt-2 text-2xl font-semibold">{candidates.length}</p></div><div className="rounded-2xl border border-slate-200 bg-white p-5"><p className="text-sm text-slate-500">Applications</p><p className="mt-2 text-2xl font-semibold">{applications.length}</p></div><div className="rounded-2xl border border-slate-200 bg-white p-5"><p className="text-sm text-slate-500">Interviews</p><p className="mt-2 text-2xl font-semibold">{interviews.length}</p></div></div><section className="mb-6 rounded-2xl border border-slate-200 bg-white p-5"><h3 className="text-lg font-semibold text-slate-950">Job openings</h3>{jobs.length === 0 ? <p className="mt-4 text-sm text-slate-600">No job openings have been created.</p> : <div className="mt-4 overflow-x-auto"><table className="w-full min-w-[700px] text-left text-sm text-slate-700"><thead><tr className="text-slate-500"><th className="px-3 py-2">Code</th><th className="px-3 py-2">Title</th><th className="px-3 py-2">Openings</th><th className="px-3 py-2">Status</th><th className="px-3 py-2">Closing date</th></tr></thead><tbody className="divide-y divide-slate-100">{jobs.map((job) => <tr key={job.job_id}><td className="px-3 py-3">{job.job_code}</td><td className="px-3 py-3 font-medium text-slate-900">{job.job_title}</td><td className="px-3 py-3">{job.number_of_openings}</td><td className="px-3 py-3">{formatStatus(job.status)}</td><td className="px-3 py-3">{job.closing_date || 'Open'}</td></tr>)}</tbody></table></div>}</section><section className="rounded-2xl border border-slate-200 bg-white p-5"><div className="flex flex-wrap items-center justify-between gap-3"><h3 className="text-lg font-semibold text-slate-950">Candidates</h3><div className="flex gap-2"><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search candidates..." className="rounded-2xl border border-slate-200 px-4 py-2 text-sm" /><select value={candidateStatus} onChange={(event) => setCandidateStatus(event.target.value)} className="rounded-2xl border border-slate-200 px-3 py-2 text-sm"><option value="ALL">All statuses</option><option value="NEW">New</option><option value="SCREENING">Screening</option><option value="SHORTLISTED">Shortlisted</option><option value="INTERVIEW">Interview</option><option value="SELECTED">Selected</option><option value="REJECTED">Rejected</option></select></div></div>{visibleCandidates.length === 0 ? <p className="mt-4 text-sm text-slate-600">No candidates match the current filters.</p> : <div className="mt-4 overflow-x-auto"><table className="w-full min-w-[800px] text-left text-sm text-slate-700"><thead><tr className="text-slate-500"><th className="px-3 py-2">Code</th><th className="px-3 py-2">Candidate</th><th className="px-3 py-2">Email</th><th className="px-3 py-2">Experience</th><th className="px-3 py-2">Status</th></tr></thead><tbody className="divide-y divide-slate-100">{visibleCandidates.map((candidate) => <tr key={candidate.candidate_id}><td className="px-3 py-3">{candidate.candidate_code}</td><td className="px-3 py-3 font-medium text-slate-900">{candidate.first_name} {candidate.last_name}</td><td className="px-3 py-3">{candidate.email}</td><td className="px-3 py-3">{candidate.total_experience_years} years</td><td className="px-3 py-3">{formatStatus(candidate.candidate_status)}</td></tr>)}</tbody></table></div>}</section></>}
    </div>
  );
}

export default Recruitment;
