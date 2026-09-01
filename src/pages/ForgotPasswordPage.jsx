import { ArrowLeft, MailCheck } from 'lucide-react';
import { useState } from 'react';
import { Link } from 'react-router-dom';

import { requestPasswordReset } from '../api/auth';

function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    setErrorMessage('');
    setMessage('');
    setIsLoading(true);

    try {
      await requestPasswordReset(email.trim());
      setMessage('If an account exists for this email, a password reset link has been sent.');
      setEmail('');
    } catch (error) {
      const detail = error.response?.data?.detail || 'Unable to send the reset link right now. Please try again.';
      setErrorMessage(detail);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 px-4 py-12 text-slate-900">
      <div className="mx-auto max-w-md">
        <div className="mb-6 flex items-center justify-between">
          <Link to="/login" className="inline-flex items-center gap-2 text-sm font-medium text-slate-600 transition hover:text-slate-900">
            <ArrowLeft className="h-4 w-4" />
            Back to login
          </Link>
        </div>

        <div className="rounded-[2rem] border border-slate-200 bg-white p-7 shadow-xl">
          <div className="flex justify-center">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-blue-50 text-blue-600">
              <MailCheck className="h-7 w-7" />
            </div>
          </div>

          <div className="mt-6 text-center">
            <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Security</p>
            <h2 className="mt-3 text-3xl font-semibold text-slate-950">Forgot password?</h2>
            <p className="mt-2 text-sm leading-6 text-slate-600">
              Enter the email linked to your account and we’ll send a secure reset link.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="mt-8 space-y-5">
            {errorMessage && (
              <p role="alert" className="rounded-2xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">
                {errorMessage}
              </p>
            )}

            {message && (
              <p className="rounded-2xl border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">
                {message}
              </p>
            )}

            <div>
              <label htmlFor="forgot-email" className="block text-sm font-medium text-slate-700">
                Email address
              </label>
              <input
                id="forgot-email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                className="mt-2 h-12 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 text-sm text-slate-900 placeholder-slate-400 outline-none transition focus:border-blue-500/60 focus:ring-2 focus:ring-blue-500/20"
                required
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="flex w-full items-center justify-center rounded-full bg-gradient-to-r from-blue-600 to-blue-500 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-600/20 transition hover:shadow-xl hover:shadow-blue-600/30 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {isLoading ? 'Sending link...' : 'Send reset link'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default ForgotPasswordPage;
