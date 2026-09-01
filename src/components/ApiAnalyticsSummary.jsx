import { useEffect, useState } from 'react';
import client from '../api/client';

function formatLabel(value) {
  return value.replace(/_/g, ' ').replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function formatValue(value) {
  if (value === null || value === undefined || value === '') return 'Not available';
  if (Array.isArray(value)) return `${value.length} records`;
  if (typeof value === 'object') return 'Available';
  return String(value);
}

function ApiAnalyticsSummary({ title, description, endpoint, groups = [] }) {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');

  const loadData = async () => {
    setIsLoading(true);
    setErrorMessage('');
    try {
      const response = await client.get(endpoint);
      setData(response.data?.data || response.data || null);
    } catch (error) {
      if (error.response?.status === 403) setErrorMessage('You do not have permission to view these analytics.');
      else if (!error.response) setErrorMessage('The backend is unavailable. Please check the server and try again.');
      else setErrorMessage('We could not load these analytics. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [endpoint]);

  return (
    <div className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass">
      <div className="flex items-start justify-between gap-4"><div><h2 className="text-2xl font-semibold text-slate-950">{title}</h2><p className="mt-2 text-sm text-slate-600">{description}</p></div><button type="button" onClick={loadData} className="rounded-2xl border border-slate-200 px-3 py-2 text-sm text-slate-700">Refresh</button></div>
      {isLoading && <div role="status" className="mt-6 rounded-2xl bg-slate-50 p-5 text-sm text-slate-600">Loading analytics...</div>}
      {!isLoading && errorMessage && <div role="alert" className="mt-6 rounded-2xl border border-red-200 bg-red-50 p-5 text-sm text-red-700"><p>{errorMessage}</p><button type="button" onClick={loadData} className="mt-3 rounded-2xl bg-red-700 px-4 py-2 text-white">Try again</button></div>}
      {!isLoading && !errorMessage && (!data || Object.keys(data).length === 0) && <div className="mt-6 rounded-2xl bg-slate-50 p-5 text-sm text-slate-600">No analytics data is available.</div>}
      {!isLoading && !errorMessage && data && <div className="mt-6 space-y-6">{(groups.length ? groups : [{ label: 'Summary', key: null }]).map((group) => { const source = group.key ? data[group.key] : data; const entries = source && typeof source === 'object' ? Object.entries(source).filter(([, value]) => typeof value !== 'object' || value === null) : []; return <section key={group.label}><h3 className="text-lg font-semibold text-slate-950">{group.label}</h3><div className="mt-3 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">{entries.map(([key, value]) => <div key={key} className="rounded-2xl border border-slate-100 bg-slate-50 p-4"><p className="text-sm text-slate-500">{formatLabel(key)}</p><p className="mt-2 text-xl font-semibold text-slate-900">{formatValue(value)}</p></div>)}</div></section>; })}</div>}
    </div>
  );
}

export default ApiAnalyticsSummary;
