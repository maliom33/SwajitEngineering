import { Navigate, useLocation } from 'react-router-dom';

import { getAccessToken, getStoredUser } from '../api/storage';

function ProtectedRoute({ children }) {
  const location = useLocation();

  if (!getAccessToken()) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  const roleCode = getStoredUser()?.role_code;
  const managementPrefixes = {
    '/admin': ['SYSTEM_ADMIN'],
    '/hr': ['SYSTEM_ADMIN', 'HR_MANAGER'],
    '/director': ['SYSTEM_ADMIN', 'DIRECTOR'],
    '/sales': ['SYSTEM_ADMIN', 'SALES_EXECUTIVE'],
    '/warehouse': ['SYSTEM_ADMIN', 'WAREHOUSE_MANAGER'],
    '/logistics': ['SYSTEM_ADMIN', 'LOGISTICS_MANAGER', 'DRIVER'],
    '/dispatch': ['SYSTEM_ADMIN', 'DISPATCH_EXECUTIVE'],
    '/finance': ['SYSTEM_ADMIN', 'FINANCE_MANAGER'],
    '/employee': ['EMPLOYEE'],
  };
  const prefix = Object.keys(managementPrefixes).find((path) => location.pathname === path || location.pathname.startsWith(`${path}/`));
  if (prefix && !managementPrefixes[prefix].includes(roleCode)) {
    return <Navigate to={roleCode === 'EMPLOYEE' ? '/employee' : '/login'} replace />;
  }

  return children;
}

export default ProtectedRoute;