import { useEffect, useState } from 'react';
import { getCurrentUser } from '../../api/auth';

function Profile() {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');

  const loadProfile = async () => {
    setIsLoading(true);
    setErrorMessage('');
    try {
      const response = await getCurrentUser();
      setUser(response.data);
    } catch {
      setErrorMessage('We could not load your profile. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadProfile();
  }, []);

  return (
    <div>
      <h2 className="text-2xl font-semibold">Profile</h2>
      <p className="mt-2 text-sm text-slate-600">View your authenticated account details and permissions.</p>
      {isLoading && <div role="status" className="mt-6 rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-600">Loading profile...</div>}
      {!isLoading && errorMessage && <div role="alert" className="mt-6 rounded-2xl border border-red-200 bg-red-50 p-6 text-sm text-red-700"><p>{errorMessage}</p><button type="button" onClick={loadProfile} className="mt-3 rounded-2xl bg-red-700 px-4 py-2 text-white">Try again</button></div>}
      {!isLoading && !errorMessage && user && <section className="mt-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><div className="grid gap-4 sm:grid-cols-2"><div><p className="text-sm text-slate-500">Name</p><p className="mt-1 font-medium text-slate-900">{user.first_name} {user.last_name}</p></div><div><p className="text-sm text-slate-500">Email</p><p className="mt-1 font-medium text-slate-900">{user.email}</p></div><div><p className="text-sm text-slate-500">Role</p><p className="mt-1 font-medium text-slate-900">{user.role || 'Not assigned'}</p></div><div><p className="text-sm text-slate-500">Role code</p><p className="mt-1 font-medium text-slate-900">{user.role_code || 'Not assigned'}</p></div></div><div className="mt-6"><p className="text-sm text-slate-500">Permissions</p><div className="mt-2 flex flex-wrap gap-2">{user.permissions?.length ? user.permissions.map((permission) => <span key={permission} className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-700">{permission}</span>) : <span className="text-sm text-slate-600">No permissions assigned.</span>}</div></div></section>}
    </div>
  );
}

export default Profile;
