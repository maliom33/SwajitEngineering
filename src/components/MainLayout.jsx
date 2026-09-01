import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import AdminNavbar from './AdminNavbar';
import DashboardSidebar from './DashboardSidebar';
import { clearAuth } from '../api/storage';

function MainLayout({ title, links, children, userProfile, defaultSidebarOpen = true }) {
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(defaultSidebarOpen);

  const handleLogout = () => {
    clearAuth();
    navigate('/login');
  };

  return (
    <div className="min-h-screen transition-colors duration-300" style={{ backgroundColor: 'var(--bg-page)', color: 'var(--text-primary)' }}>
      <div className="lg:flex lg:min-h-screen">
        <DashboardSidebar
          links={links}
          title={title}
          isOpen={sidebarOpen}
          toggleSidebar={() => setSidebarOpen((open) => !open)}
          onLogout={handleLogout}
        />
        <div className="flex-1">
          <AdminNavbar userProfile={userProfile} onLogout={handleLogout} />
          <main className="mx-auto max-w-7xl px-4 pb-10 pt-6 sm:px-6 lg:px-8">
            {children}
          </main>
        </div>
      </div>
    </div>
  );
}

export default MainLayout;
