import { useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import client from '../api/client';

function getErrorMessage(requestError) {
  const data = requestError.response?.data;
  if (data?.detail) return data.detail;
  if (data?.confirm_password?.[0]) return data.confirm_password[0];
  if (data?.password?.[0]) return data.password[0];
  return 'This activation link is invalid or expired.';
}

function ActivateAccount() {
  const [searchParams] = useSearchParams();
  const [form, setForm] = useState({
    email: searchParams.get('email') || '',
    activation_token: searchParams.get('activation_token') || searchParams.get('token') || '',
    password: '',
    confirm_password: '',
  });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const updateField = (field) => (event) => setForm((current) => ({ ...current, [field]: event.target.value }));

  const submit = async (event) => {
    event.preventDefault();
    setError('');
    setMessage('');
    if (form.password !== form.confirm_password) {
      setError('Passwords do not match.');
      return;
    }
    setIsSubmitting(true);
    try {
      await client.post('auth/activate/', form);
      setMessage('Account activated successfully. You can now login.');
      setForm((current) => ({ ...current, activation_token: '', password: '', confirm_password: '' }));
    } catch (requestError) {
      setError(getErrorMessage(requestError));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-50 px-4 py-10">
      <form onSubmit={submit} className="w-full max-w-md rounded-3xl border border-slate-200 bg-white p-8 shadow-xl">
        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-brand-700">Swajit Engineering</p>
        <h1 className="mt-3 text-2xl font-semibold text-slate-950">Employee Account Activation</h1>
        <p className="mt-2 text-sm text-slate-600">Set a secure password to access the employee application.</p>
        {message && <p role="status" className="mt-4 rounded-2xl bg-emerald-50 p-3 text-sm text-emerald-700">{message}</p>}
        {error && <p role="alert" className="mt-4 rounded-2xl bg-red-50 p-3 text-sm text-red-700">{error}</p>}
        <div className="mt-6 space-y-4">
          <label className="block text-sm font-medium text-slate-700">Employee email
            <input required type="email" value={form.email} onChange={updateField('email')} className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3" />
          </label>
          <label className="block text-sm font-medium text-slate-700">Activation token
            <input required value={form.activation_token} onChange={updateField('activation_token')} className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3" />
          </label>
          <label className="block text-sm font-medium text-slate-700">New password
            <input required minLength="8" type="password" value={form.password} onChange={updateField('password')} className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3" />
          </label>
          <label className="block text-sm font-medium text-slate-700">Confirm password
            <input required minLength="8" type="password" value={form.confirm_password} onChange={updateField('confirm_password')} className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3" />
          </label>
          <button type="submit" disabled={isSubmitting} className="w-full rounded-2xl bg-brand-900 px-4 py-3 font-medium text-white disabled:opacity-60">
            {isSubmitting ? 'Activating...' : 'Activate Account'}
          </button>
          {message && <Link to="/login" className="block text-center text-sm font-medium text-brand-700">Login</Link>}
        </div>
      </form>
    </main>
  );
}

export default ActivateAccount;