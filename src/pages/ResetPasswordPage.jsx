import { ShieldCheck } from 'lucide-react';
import { useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';

import { confirmPasswordReset } from '../api/auth';

function ResetPasswordPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const uidb64 = searchParams.get('uidb64') || '';
  const token = searchParams.get('token') || '';
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    setErrorMessage('');
    setSuccessMessage('');

    if (!uidb64 || !token) {
      setErrorMessage('This password reset link is invalid or expired.');
      return;
    }

    if (password !== confirmPassword) {
      setErrorMessage('Passwords do not match.');
      return;
    }

    setIsLoading(true);

    try {
      await confirmPasswordReset({
        uidb64,
        token,
        password,
        confirm_password: confirmPassword,
      });

      setSuccessMessage('Password reset successfully. Redirecting to login...');
      setTimeout(() => navigate('/login', { replace: true }), 1200);
    } catch (error) {
      const detail = error.response?.data?.detail || 'We could not reset your password. Please request a new reset link.';
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
            <span>←</span>
            Back to login
          </Link>
        </div>

        <div className="rounded-[2rem] border border-slate-200 bg-white p-7 shadow-xl">
          <div className="flex justify-center">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-emerald-50 text-emerald-600">
              <ShieldCheck className="h-7 w-7" />
            </div>
          </div>

          <div className="mt-6 text-center">
            <p className="text-xs uppercase tracking-[0.3em] text-slate-500">Account security</p>
            <h2 className="mt-3 text-3xl font-semibold text-slate-950">Set a new password</h2>
            <p className="mt-2 text-sm leading-6 text-slate-600">
              Create a strong password to secure your account.
            </p>
          </div>

          <form onSubmit={handleSubmit} className="mt-8 space-y-5">
            {errorMessage && (
              <p role="alert" className="rounded-2xl border border-red-200 bg-red-50 p-3 text-sm text-red-700">
                {errorMessage}
              </p>
            )}

            {successMessage && (
              <p className="rounded-2xl border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">
                {successMessage}
              </p>
            )}

            <div>
              <label htmlFor="new-password" className="block text-sm font-medium text-slate-700">
                New password
              </label>
              <input
                id="new-password"
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                className="mt-2 h-12 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 text-sm text-slate-900 outline-none transition focus:border-blue-500/60 focus:ring-2 focus:ring-blue-500/20"
                required
              />
            </div>

            <div>
              <label htmlFor="confirm-password" className="block text-sm font-medium text-slate-700">
                Confirm password
              </label>
              <input
                id="confirm-password"
                type="password"
                value={confirmPassword}
                onChange={(event) => setConfirmPassword(event.target.value)}
                className="mt-2 h-12 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 text-sm text-slate-900 outline-none transition focus:border-blue-500/60 focus:ring-2 focus:ring-blue-500/20"
                required
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="flex w-full items-center justify-center rounded-full bg-gradient-to-r from-emerald-600 to-emerald-500 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-emerald-600/20 transition hover:shadow-xl hover:shadow-emerald-600/30 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {isLoading ? 'Resetting...' : 'Reset password'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default ResetPasswordPage;
