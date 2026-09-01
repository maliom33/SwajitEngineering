export const ROLE_ROUTES = {
  SYSTEM_ADMIN: '/admin',
  DIRECTOR: '/director',
  HR_MANAGER: '/hr',
  SALES_EXECUTIVE: '/sales',
  WAREHOUSE_MANAGER: '/warehouse',
  LOGISTICS_MANAGER: '/logistics',
  DISPATCH_EXECUTIVE: '/dispatch',
  FINANCE_MANAGER: '/finance',
  DRIVER: '/logistics',
  EMPLOYEE: '/employee',
};

export function getRoleRoute(roleCode) {
  return ROLE_ROUTES[roleCode] || null;
}