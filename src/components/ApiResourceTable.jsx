import { useEffect, useMemo, useState } from 'react';
import client from '../api/client';

function formatLabel(value) {
  return String(value).replace(/_/g, ' ').replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function formatValue(value) {
  if (value === null || value === undefined || value === '') return 'Not available';
  if (typeof value === 'object') return JSON.stringify(value);
  return String(value);
}

function ApiResourceTable({ title, description, endpoint, columns = [], searchKeys = [] }) {
  const [records, setRecords] = useState([]);
  const [search, setSearch] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');

  const loadRecords = async () => {
    setIsLoading(true);
    setErrorMessage('');
    try {
      const response = await client.get(endpoint);
      setRecords(Array.isArray(response.data) ? response.data : response.data?.results || []);
    } catch (error) {
      if (error.response?.status === 403) setErrorMessage('You do not have permission to view these records.');
      else if (!error.response) setErrorMessage('The backend is unavailable. Please check the server and try again.');
      else setErrorMessage('We could not load these records. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => { loadRecords(); }, [endpoint]);

  const visibleRecords = useMemo(() => {
    const query = search.trim().toLowerCase();
    if (!query) return records;
    return records.filter((record) => (searchKeys.length ? searchKeys : columns.map((column) => column.key)).some((key) => formatValue(record[key]).toLowerCase().includes(query)));
  }, [records, search, searchKeys, columns]);

  return <div className="space-y-6"><section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass"><div className="flex flex-wrap items-start justify-between gap-4"><div><h2 className="text-2xl font-semibold text-slate-950">{title}</h2><p className="mt-2 text-sm text-slate-600">{description}</p></div><button type="button" onClick={loadRecords} className="rounded-2xl border border-slate-200 px-3 py-2 text-sm text-slate-700">Refresh</button></div></section>{errorMessage && <div role="alert" className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"><p>{errorMessage}</p><button type="button" onClick={loadRecords} className="mt-3 rounded-2xl bg-red-700 px-4 py-2 text-white">Try again</button></div>}{isLoading && <div role="status" className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-600">Loading records...</div>}{!isLoading && !errorMessage && <section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-sm"><div className="mb-4 flex flex-wrap items-center justify-between gap-3"><h3 className="text-lg font-semibold text-slate-950">{visibleRecords.length} records</h3><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search records..." className="rounded-2xl border border-slate-200 px-4 py-2 text-sm" /></div>{visibleRecords.length === 0 ? <p className="p-4 text-sm text-slate-600">No records are available.</p> : <div className="overflow-x-auto"><table className="w-full min-w-[700px] text-left text-sm text-slate-700"><thead><tr className="text-slate-500">{columns.map((column) => <th key={column.key} className="px-3 py-3">{column.label || formatLabel(column.key)}</th>)}</tr></thead><tbody className="divide-y divide-slate-100">{visibleRecords.map((record, index) => <tr key={record.id || record[columns[0]?.key] || index}>{columns.map((column) => <td key={column.key} className="px-3 py-3">{column.render ? column.render(record[column.key], record) : formatValue(record[column.key])}</td>)}</tr>)}</tbody></table></div>}</section>}</div>;
}

export default ApiResourceTable;
