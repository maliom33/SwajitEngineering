import { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import client from '../api/client';

function getErrorMessage(requestError) {
  const data = requestError.response?.data;
  if (data?.detail) return data.detail;
  return 'We could not verify your email. The link may be expired or invalid.';
}

function VerifyEmail() {
  const [searchParams] = useSearchParams();
  const [status, setStatus] = useState('loading'); // 'loading', 'success', 'error'
  const [message, setMessage] = useState('');
  const token = searchParams.get('token') || '';

  useEffect(() => {
    const verify = async () => {
      if (!token) {
        setStatus('error');
        setMessage('Email verification link is missing or invalid.');
        return;
      }

      try {
        await client.get('auth/verification/email/verify/', { params: { token } });
        setStatus('success');
        setMessage('Email verified successfully. You can now log in.');
      } catch (error) {
        setStatus('error');
        setMessage(getErrorMessage(error));
      }
    };

    verify();
  }, [token]);

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-50 px-4 py-10">
      <div className="w-full max-w-md rounded-3xl border border-slate-200 bg-white p-8 shadow-xl">
        <p className="text-sm font-semibold uppercase tracking-[0.2em] text-brand-700">Swajit Engineering</p>
        <h1 className="mt-3 text-2xl font-semibold text-slate-950">Email Verification</h1>
        <p className="mt-2 text-sm text-slate-600">Verifying your email address...</p>

        <div className="mt-6">
          {status === 'loading' && (
            <div className="rounded-2xl bg-blue-50 p-4 text-center">
              <div className="flex justify-center">
                <div className="h-6 w-6 animate-spin rounded-full border-2 border-blue-200 border-t-blue-600" />
              </div>
              <p className="mt-3 text-sm text-blue-700">Verifying your email...</p>
            </div>
          )}

          {status === 'success' && (
            <div>
              <div role="status" className="rounded-2xl bg-emerald-50 p-4 text-center">
                <p className="text-sm font-semibold text-emerald-700">✓ {message}</p>
              </div>
              <Link
                to="/login"
                className="mt-6 block w-full rounded-2xl bg-brand-900 px-4 py-3 text-center font-medium text-white transition hover:bg-brand-800"
              >
                Return to Login
              </Link>
            </div>
          )}

          {status === 'error' && (
            <div>
              <div role="alert" className="rounded-2xl bg-red-50 p-4 text-center">
                <p className="text-sm font-semibold text-red-700">✗ {message}</p>
              </div>
              <div className="mt-6 space-y-3">
                <Link
                  to="/login"
                  className="block w-full rounded-2xl bg-brand-900 px-4 py-3 text-center font-medium text-white transition hover:bg-brand-800"
                >
                  Back to Login
                </Link>
                <p className="text-center text-xs text-slate-600">
                  If you need a new verification link, you can request one during the login process.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}

export default VerifyEmail;
