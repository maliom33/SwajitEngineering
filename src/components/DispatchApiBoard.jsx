import { useEffect, useState } from 'react';
import client from '../api/client';

const statusLabel = (value) => value ? value.toLowerCase().replace(/_/g, ' ').replace(/\b\w/g, (letter) => letter.toUpperCase()) : 'Not available';

function DispatchApiBoard({ title, description, endpoint = 'dispatch/dispatches/', actionButtons = false }) {
  const [records, setRecords] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [busyId, setBusyId] = useState(null);

  const loadRecords = async () => {
    setIsLoading(true);
    setErrorMessage('');
    try {
      const response = await client.get(`dispatch/${endpoint}`);
      setRecords(Array.isArray(response.data) ? response.data : response.data?.results || []);
    } catch (error) {
      if (error.response?.status === 403) setErrorMessage('You do not have permission to view dispatch records.');
      else if (!error.response) setErrorMessage('The backend is unavailable. Please check the server and try again.');
      else setErrorMessage('We could not load dispatch records. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => { loadRecords(); }, [endpoint]);

  const runAction = async (record, action) => {
    setBusyId(record.dispatch_id);
    setErrorMessage('');
    setSuccessMessage('');
    try {
      await client.post(`dispatch/dispatches/${record.dispatch_id}/${action}/`, {});
      setSuccessMessage(`Dispatch ${action.replace(/-/g, ' ')} completed successfully.`);
      await loadRecords();
    } catch (error) {
      setErrorMessage(error.response?.status === 403 ? 'You do not have permission to perform this dispatch action.' : 'The dispatch action could not be completed.');
    } finally {
      setBusyId(null);
    }
  };

  return <div className="space-y-6"><section className="rounded-[2rem] border border-slate-200/80 bg-white/90 p-6 shadow-glass"><div className="flex items-start justify-between gap-4"><div><p className="text-sm uppercase tracking-[0.24em] text-slate-400">Dispatch Operations</p><h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950">{title}</h1><p className="mt-2 text-sm text-slate-600">{description}</p></div><button type="button" onClick={loadRecords} className="rounded-2xl border border-slate-200 px-3 py-2 text-sm text-slate-700">Refresh</button></div></section>{successMessage && <p role="status" className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-700">{successMessage}</p>}{errorMessage && <div role="alert" className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"><p>{errorMessage}</p><button type="button" onClick={loadRecords} className="mt-3 rounded-2xl bg-red-700 px-4 py-2 text-white">Try again</button></div>}{isLoading && <div role="status" className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-600">Loading dispatch records...</div>}{!isLoading && !errorMessage && records.length === 0 && <div className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-600">No dispatch records are available.</div>}{!isLoading && !errorMessage && records.length > 0 && <div className="overflow-x-auto rounded-2xl border border-slate-200 bg-white p-4 shadow-sm"><table className="w-full min-w-[850px] text-left text-sm text-slate-700"><thead><tr className="text-slate-500"><th className="px-3 py-3">Dispatch</th><th className="px-3 py-3">Order</th><th className="px-3 py-3">Delivery</th><th className="px-3 py-3">Warehouse</th><th className="px-3 py-3">Scheduled date</th><th className="px-3 py-3">Status</th>{actionButtons && <th className="px-3 py-3">Actions</th>}</tr></thead><tbody className="divide-y divide-slate-100">{records.map((record) => <tr key={record.dispatch_id}><td className="px-3 py-3 font-medium text-slate-900">{record.dispatch_number || `#${record.dispatch_id}`}</td><td className="px-3 py-3">#{record.order}</td><td className="px-3 py-3">#{record.delivery}</td><td className="px-3 py-3">#{record.warehouse}</td><td className="px-3 py-3">{record.scheduled_dispatch_date}</td><td className="px-3 py-3">{statusLabel(record.dispatch_status)}</td>{actionButtons && <td className="px-3 py-3"><div className="flex flex-wrap gap-2">{record.dispatch_status === 'SCHEDULED' && <button type="button" disabled={busyId === record.dispatch_id} onClick={() => runAction(record, 'prepare')} className="rounded-2xl bg-blue-600 px-3 py-2 text-xs text-white disabled:opacity-60">Prepare</button>}{record.dispatch_status === 'READY' && <><button type="button" disabled={busyId === record.dispatch_id} onClick={() => runAction(record, 'generate-challan')} className="rounded-2xl bg-violet-600 px-3 py-2 text-xs text-white disabled:opacity-60">Challan</button><button type="button" disabled={busyId === record.dispatch_id} onClick={() => runAction(record, 'handover')} className="rounded-2xl bg-amber-600 px-3 py-2 text-xs text-white disabled:opacity-60">Handover</button></>}{record.dispatch_status === 'HANDED_OVER' && <button type="button" disabled={busyId === record.dispatch_id} onClick={() => runAction(record, 'confirm')} className="rounded-2xl bg-emerald-600 px-3 py-2 text-xs text-white disabled:opacity-60">Confirm</button>}</div></td>}</tr>)}</tbody></table></div>}</div>;
}

export default DispatchApiBoard;
