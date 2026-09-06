import { UserCircle2, ArrowRight } from 'lucide-react';
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { login } from '../api/auth';
import { clearAuth, storeAuth } from '../api/storage';
import { getRoleRoute } from '../auth/roleRoutes';
import logo from '../images/logo.png';

function LoginPage({ onNavigateToHome = () => {} }) {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    setErrorMessage('');
    setIsLoading(true);

    try {
      const response = await login(email.trim(), password);
      const { access, refresh, user } = response.data ?? {};
      const route = getRoleRoute(user?.role_code);

      if (!access || !refresh || !user || !route) {
        clearAuth();
        setErrorMessage('Your account has no configured dashboard. Please contact an administrator.');
        return;
      }

      storeAuth({ access, refresh, user });
      navigate(route, { replace: true });
    } catch (error) {
      clearAuth();
      if (error.response?.status === 400 || error.response?.status === 401) {
        setErrorMessage('The email or password is incorrect.');
      } else if (error.response?.status === 422) {
        setErrorMessage('Please enter a valid email address and password.');
      } else if (error.response?.status >= 500) {
        setErrorMessage('The sign-in service is temporarily unavailable. Please try again shortly.');
      } else if (!error.response) {
        setErrorMessage('The backend is unavailable. Please try again shortly.');
      } else {
        setErrorMessage('We could not sign you in. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen light-page transition-colors duration-300 bg-slate-50 text-slate-900">
      {/* Navbar */}
      <header className="sticky top-0 z-10 border-b border-slate-200 bg-white backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <img src={logo} alt="Swajit Engineering logo" className='h-12 w-15 object-contain'/>
            <div>
              <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Swajit Engineering</p>
              <p className="text-sm font-semibold text-slate-950">ERP & Operations Platform</p>
            </div>
          </div>

          <nav className="hidden items-center gap-8 lg:flex">
            {/*<button onClick={onNavigateToHome} className="text-sm font-medium text-slate-600 transition hover:text-slate-950">Home</button>
            <a href="/#about" className="text-sm font-medium text-slate-600 transition hover:text-slate-950">About</a>
            <a href="/#features" className="text-sm font-medium text-slate-600 transition hover:text-slate-950">Services</a>
            <a href="/#contact" className="text-sm font-medium text-slate-600 transition hover:text-slate-950">Contact</a>
            <span className="text-sm font-medium text-brand-900">Login</span>*/}
          </nav>

        <div className="flex items-center gap-3">
              <button type="button" onClick={onNavigateToHome} className="flex h-16 w-16 flex-col items-center justify-center rounded-2xl border border-slate-200 bg-white text-slate-900 transition hover:border-slate-300 hover:text-slate-950">
                <UserCircle2 className="h-5 w-5" />
                  <span className="text-xs">Home</span>
              </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="mx-auto max-w-8xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="flex justify-center">
          {/* Login Card - Centered */}
          <motion.section initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.35 }} className="w-full max-w-xl">
            <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-xl">
              <div>
                <p className="text-sm uppercase tracking-[0.28em] text-slate-500">Secure access</p>
                <h2 className="mt-3 text-3xl font-semibold text-slate-950">Welcome Back</h2>
                <p className="mt-2 text-sm leading-6 text-slate-600">
                  Please sign in using your email and password. Your role-based dashboard will load automatically.
                </p>
              </div>

              <form onSubmit={handleLogin} className="mt-8 space-y-5">
                
                {errorMessage && (
                  <p role="alert" className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
                    {errorMessage}
                  </p>
                )}

                {/* Email */}
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-slate-700">
                    Email
                  </label>
                  <input
                    id="email"
                    type="email"
                    placeholder="you@example.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="mt-2 h-12 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 text-sm text-slate-900 placeholder-slate-400 outline-none transition focus:border-blue-500/60 focus:ring-2 focus:ring-blue-500/20"
                    required
                  />
                </div>
                
                {/* Password */}
                <div>
                  <label htmlFor="password" className="block text-sm font-medium text-slate-700">
                    Password
                  </label>
                  <div className="relative mt-2">
                    <input
                      id="password"
                      type={showPassword ? 'text' : 'password'}
                      placeholder="••••••••"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="h-12 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 text-sm text-slate-900 placeholder-slate-400 outline-none transition focus:border-blue-500/60 focus:ring-2 focus:ring-blue-500/20"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 transition hover:text-slate-200"
                    >
                      {showPassword ? '🙈' : '👁️'}
                    </button>
                  </div>
                </div>

                {/* Remember Me & Forgot Password */}
                <div className="flex items-center justify-between">
                  <label className="flex items-center gap-2 text-sm text-slate-700">
                    <input
                      type="checkbox"
                      checked={rememberMe}
                      onChange={(e) => setRememberMe(e.target.checked)}
                      className="h-4 w-4 rounded border-slate-300 bg-white text-blue-500 outline-none transition focus:ring-2 focus:ring-blue-500/20"
                    />
                    Remember me
                  </label>
                  <Link to="/forgot-password" className="text-sm font-medium text-blue-600 transition hover:text-blue-700">
                    Forgot Password?
                  </Link>
                </div>

                {/* Login Button */}
                <button
                  type="submit"
                  disabled={isLoading}
                  aria-busy={isLoading}
                  className="mt-6 flex w-full items-center justify-center gap-2 rounded-full bg-gradient-to-r from-blue-600 to-blue-500 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-blue-600/20 transition hover:shadow-xl hover:shadow-blue-600/30 active:scale-95"
                >
                  {isLoading ? 'Signing In...' : 'Sign In to Dashboard'}
                  <ArrowRight className="h-4 w-4" />
                </button>

                {/* Security Notice */}
                <p className="rounded-2xl border border-slate-200 bg-slate-50 p-4 text-center text-xs text-slate-600">
                  Only authorized employees of Swajit Engineering Pvt. Ltd. can access this system. Verify your credentials are accurate.
                </p>
              </form>
            </div>
          </motion.section>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-16 border-t border-slate-200 bg-white/95 py-6">
        <div className="mx-auto flex max-w-7xl flex-col gap-6 px-4 text-sm text-slate-600 sm:flex-row sm:items-center sm:justify-between sm:px-6 lg:px-8">
          <div>
            <p className="font-semibold text-slate-950">Swajit Engineering Pvt. Ltd.</p>
            <p>Industrial Estate, K-9 M.I.D.C. Waluj, Ch.Sambhajinagar, Maharashtra, India</p>
          </div>
          <div className="space-y-1">
            <p>Phone: +91 240 2555031 / 2554531</p>
            <p>Email: marketing@swajit.com</p>
            <p>Website: www.swajitengineering.com</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default LoginPage;
