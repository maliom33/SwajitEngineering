import { Outlet } from 'react-router-dom';
import MainLayout from '../../components/MainLayout';

const financeLinks = [
  { label: 'Dashboard', to: '/finance', icon: 'LayoutGrid' },
  { label: 'Invoice Management', to: '/finance/invoices', icon: 'FileText' },
  { label: 'Billing Management', to: '/finance/billing', icon: 'Receipt' },
  { label: 'Payment Management', to: '/finance/payments', icon: 'CreditCard' },
  { label: 'Accounts Receivable', to: '/finance/receivables', icon: 'Wallet' },
  { label: 'Accounts Payable', to: '/finance/payables', icon: 'Banknote' },
  { label: 'Payroll Management', to: '/finance/payroll', icon: 'Users' },
  { label: 'Salary Processing', to: '/finance/salary', icon: 'BadgeDollarSign' },
  { label: 'Payslip Management', to: '/finance/payslips', icon: 'ReceiptText' },
  { label: 'GST & Tax Management', to: '/finance/tax', icon: 'Percent' },
  { label: 'Revenue Analysis', to: '/finance/revenue', icon: 'BarChart3' },
  { label: 'Expense Analysis', to: '/finance/expenses', icon: 'TrendingDown' },
  { label: 'Profit & Loss', to: '/finance/profit-loss', icon: 'ChartNoAxesCombined' },
  { label: 'Financial Reports', to: '/finance/reports', icon: 'FileBarChart2' },
  { label: 'Notifications', to: '/finance/notifications', icon: 'Bell' },
  { label: 'Profile', to: '/finance/profile', icon: 'User' },
  { label: 'Logout', to: '/login', icon: 'LogOut' },
];

function FinanceLayout() {
  return (
    <MainLayout title="Finance" links={financeLinks} userProfile={{ name: 'Finance Manager', role: 'Finance' }}>
      <Outlet />
    </MainLayout>
  );
}

export default FinanceLayout;
