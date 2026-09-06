import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import SystemAdminDashboard from './pages/SystemAdminDashboard';
import HRLayout from './pages/hr/HRLayout';
import HRHome from './pages/hr/HRHome';
import EmployeeList from './pages/hr/EmployeeList';
import Attendance from './pages/hr/Attendance';
import LeaveManagement from './pages/hr/LeaveManagement';
import Recruitment from './pages/hr/Recruitment';
import Shifts from './pages/hr/Shifts';
import Payroll from './pages/hr/Payroll';
import Performance from './pages/hr/Performance';
import Reports from './pages/hr/Reports';
import Notifications from './pages/hr/Notifications';
import Profile from './pages/hr/Profile';
import DirectorLayout from './pages/director/DirectorLayout';
import DirectorDashboard from './pages/director/DirectorDashboard';
import CompanyOverview from './pages/director/CompanyOverview';
import WorkforceAnalytics from './pages/director/WorkforceAnalytics';
import LogisticsOverview from './pages/director/LogisticsOverview';
import WarehouseOverview from './pages/director/WarehouseOverview';
import FinancialOverview from './pages/director/FinancialOverview';
import AIInsights from './pages/director/AIInsights';
import DirectorReports from './pages/director/DirectorReports';
import DirectorNotifications from './pages/director/DirectorNotifications';
import DirectorProfile from './pages/director/DirectorProfile';
import SalesLayout from './pages/sales/SalesLayout';
import SalesHome from './pages/sales/SalesHome';
import Customers from './pages/sales/Customers';
import SalesOrders from './pages/sales/SalesOrders';
import PurchaseOrders from './pages/sales/PurchaseOrders';
import Quotations from './pages/sales/Quotations';
import Tracking from './pages/sales/Tracking';
import History from './pages/sales/History';
import SalesReports from './pages/sales/Reports';
import SalesNotifications from './pages/sales/Notifications';
import SalesProfile from './pages/sales/Profile';
import WarehouseLayout from './pages/warehouse/WarehouseLayout';
import WarehouseHome from './pages/warehouse/WarehouseHome';
import Inventory from './pages/warehouse/Inventory';
import Verification from './pages/warehouse/Verification';
import Products from './pages/warehouse/Products';
import RawMaterials from './pages/warehouse/RawMaterials';
import FinishedGoods from './pages/warehouse/FinishedGoods';
import GoodsInward from './pages/warehouse/GoodsInward';
import GoodsOutward from './pages/warehouse/GoodsOutward';
import Allocation from './pages/warehouse/Allocation';
import Capacity from './pages/warehouse/Capacity';
import Alerts from './pages/warehouse/Alerts';
import Suppliers from './pages/warehouse/Suppliers';
import WarehouseReports from './pages/warehouse/Reports';
import WarehouseNotifications from './pages/warehouse/Notifications';
import WarehouseProfile from './pages/warehouse/Profile';
import LogisticsLayout from './pages/logistics/LogisticsLayout';
import LogisticsHome from './pages/logistics/LogisticsHome';
import Orders from './pages/logistics/Orders';
import Deliveries from './pages/logistics/Deliveries';
import Fleet from './pages/logistics/Fleet';
import LogisticsSectionPage from './pages/logistics/LogisticsSectionPage';
import DispatchLayout from './pages/dispatch/DispatchLayout';
import DispatchHome from './pages/dispatch/DispatchHome';
import DispatchPlanning from './pages/dispatch/DispatchPlanning';
import ReadyForDispatch from './pages/dispatch/ReadyForDispatch';
import ShipmentPreparation from './pages/dispatch/ShipmentPreparation';
import LoadingVerification from './pages/dispatch/LoadingVerification';
import DeliveryChallans from './pages/dispatch/DeliveryChallans';
import VehicleDispatch from './pages/dispatch/VehicleDispatch';
import DispatchSchedule from './pages/dispatch/DispatchSchedule';
import DispatchHistory from './pages/dispatch/DispatchHistory';
import DispatchReports from './pages/dispatch/DispatchReports';
import DispatchNotifications from './pages/dispatch/DispatchNotifications';
import DispatchProfile from './pages/dispatch/DispatchProfile';
import FinanceLayout from './pages/finance/FinanceLayout';
import FinanceHome from './pages/finance/FinanceHome';
import InvoiceManagement from './pages/finance/InvoiceManagement';
import BillingManagement from './pages/finance/BillingManagement';
import PaymentManagement from './pages/finance/PaymentManagement';
import Receivables from './pages/finance/Receivables';
import Payables from './pages/finance/Payables';
import PayrollManagement from './pages/finance/PayrollManagement';
import SalaryProcessing from './pages/finance/SalaryProcessing';
import PayslipManagement from './pages/finance/PayslipManagement';
import TaxManagement from './pages/finance/TaxManagement';
import RevenueAnalysis from './pages/finance/RevenueAnalysis';
import ExpenseAnalysis from './pages/finance/ExpenseAnalysis';
import ProfitLoss from './pages/finance/ProfitLoss';
import FinancialReports from './pages/finance/FinancialReports';
import FinanceNotifications from './pages/finance/FinanceNotifications';
import FinanceProfile from './pages/finance/FinanceProfile';
import ProtectedRoute from './auth/ProtectedRoute';
import EmployeePortal, { EmployeeAttendance, EmployeeDashboard, EmployeeLeave, EmployeeLogout, EmployeeProfile } from './pages/EmployeePortal';
import ActivateAccount from './pages/ActivateAccount';
import VerifyEmail from './pages/VerifyEmail';
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import ResetPasswordPage from './pages/ResetPasswordPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage onNavigateToLogin={() => { window.location.href = '/login'; }} />} />
        <Route path="/login" element={<LoginPage onNavigateToHome={() => (window.location.href = '/')} />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/reset-password" element={<ResetPasswordPage />} />
        <Route path="/activate" element={<ActivateAccount />} />
        <Route path="/verify-email" element={<VerifyEmail />} />

        <Route path="/employee" element={<ProtectedRoute><EmployeePortal /></ProtectedRoute>}>
          <Route index element={<EmployeeDashboard />} />
          <Route path="profile" element={<EmployeeProfile />} />
          <Route path="attendance" element={<EmployeeAttendance />} />
          <Route path="leave" element={<EmployeeLeave />} />
          <Route path="logout" element={<EmployeeLogout />} />
        </Route>

        <Route path="/admin" element={<ProtectedRoute><SystemAdminDashboard /></ProtectedRoute>} />

        <Route path="/hr" element={<ProtectedRoute><HRLayout /></ProtectedRoute>}>
          <Route index element={<HRHome />} />
          <Route path="employees" element={<EmployeeList />} />
          <Route path="attendance" element={<Attendance />} />
          <Route path="leave" element={<LeaveManagement />} />
          <Route path="recruitment" element={<Recruitment />} />
          <Route path="shifts" element={<Shifts />} />
          <Route path="payroll" element={<Payroll />} />
          <Route path="performance" element={<Performance />} />
          <Route path="reports" element={<Reports />} />
          <Route path="notifications" element={<Notifications />} />
          <Route path="profile" element={<Profile />} />
        </Route>

        <Route path="/director" element={<ProtectedRoute><DirectorLayout /></ProtectedRoute>}>
          <Route index element={<DirectorDashboard />} />
          <Route path="company" element={<CompanyOverview />} />
          <Route path="workforce" element={<WorkforceAnalytics />} />
          <Route path="logistics" element={<LogisticsOverview />} />
          <Route path="warehouse" element={<WarehouseOverview />} />
          <Route path="finance" element={<FinancialOverview />} />
          <Route path="insights" element={<AIInsights />} />
          <Route path="reports" element={<DirectorReports />} />
          <Route path="notifications" element={<DirectorNotifications />} />
          <Route path="profile" element={<DirectorProfile />} />
        </Route>

        <Route path="/sales" element={<ProtectedRoute><SalesLayout /></ProtectedRoute>}>
          <Route index element={<SalesHome />} />
          <Route path="customers" element={<Customers />} />
          <Route path="orders" element={<SalesOrders />} />
          <Route path="purchase-orders" element={<PurchaseOrders />} />
          <Route path="quotations" element={<Quotations />} />
          <Route path="tracking" element={<Tracking />} />
          <Route path="history" element={<History />} />
          <Route path="reports" element={<SalesReports />} />
          <Route path="notifications" element={<SalesNotifications />} />
          <Route path="profile" element={<SalesProfile />} />
        </Route>

        <Route path="/warehouse" element={<ProtectedRoute><WarehouseLayout /></ProtectedRoute>}>
          <Route index element={<WarehouseHome />} />
          <Route path="inventory" element={<Inventory />} />
          <Route path="verification" element={<Verification />} />
          <Route path="products" element={<Products />} />
          <Route path="raw-materials" element={<RawMaterials />} />
          <Route path="finished-goods" element={<FinishedGoods />} />
          <Route path="goods-inward" element={<GoodsInward />} />
          <Route path="goods-outward" element={<GoodsOutward />} />
          <Route path="allocation" element={<Allocation />} />
          <Route path="capacity" element={<Capacity />} />
          <Route path="alerts" element={<Alerts />} />
          <Route path="suppliers" element={<Suppliers />} />
          <Route path="reports" element={<WarehouseReports />} />
          <Route path="notifications" element={<WarehouseNotifications />} />
          <Route path="profile" element={<WarehouseProfile />} />
        </Route>

        <Route path="/logistics" element={<ProtectedRoute><LogisticsLayout /></ProtectedRoute>}>
          <Route index element={<LogisticsHome />} />
          <Route path="orders" element={<Orders />} />
          <Route path="deliveries" element={<Deliveries />} />
          <Route path="trucks" element={<Fleet />} />
          <Route path="drivers" element={<LogisticsSectionPage title="Driver Management" description="Coordinate drivers, shift availability, compliance, and dispatch readiness across the fleet." highlights={['Shift allocation', 'Driver compliance', 'Safety readiness']} />} />
          <Route path="fleet" element={<Fleet />} />
          <Route path="routes" element={<LogisticsSectionPage title="Route Optimization" description="Plan cost-efficient routes and reduce transit delays with AI-backed recommendations." highlights={['Optimized delivery routes', 'Traffic-aware planning', 'Fuel savings forecasts']} />} />
          <Route path="gps" element={<LogisticsSectionPage title="Live GPS Tracking" description="Track vehicles in real time to maintain visibility across every active dispatch." highlights={['Live vehicle position', 'ETA updates', 'Route deviation alerts']} />} />
          <Route path="timeline" element={<LogisticsSectionPage title="Delivery Timeline" description="Monitor a chronological view of dispatches, handoffs, and expected deliveries." highlights={['Delivery stage visibility', 'Milestone updates', 'Priority exceptions']} />} />
          <Route path="fuel" element={<LogisticsSectionPage title="Fuel & Cost Analysis" description="Control fleet spending and review fuel, toll, and maintenance costs across the month." highlights={['Fuel cost trends', 'Maintenance spend', 'Cost optimization insights']} />} />
          <Route path="reports" element={<LogisticsSectionPage title="Reports" description="Review logistics performance, dispatch breadth, and fleet productivity in one place." highlights={['Performance reports', 'Service level tracking', 'Executive summaries']} />} />
          <Route path="notifications" element={<LogisticsSectionPage title="Notifications" description="Stay current with dispatch alerts, service issues, and operational escalations." highlights={['Critical alerts', 'Truck updates', 'Manager reminders']} />} />
          <Route path="profile" element={<LogisticsSectionPage title="Profile" description="Maintain personal role details, access settings, and operational preferences." highlights={['Profile details', 'Preferences', 'Security settings']} />} />
        </Route>

        <Route path="/dispatch" element={<ProtectedRoute><DispatchLayout /></ProtectedRoute>}>
          <Route index element={<DispatchHome />} />
          <Route path="planning" element={<DispatchPlanning />} />
          <Route path="ready" element={<ReadyForDispatch />} />
          <Route path="shipment" element={<ShipmentPreparation />} />
          <Route path="loading" element={<LoadingVerification />} />
          <Route path="challans" element={<DeliveryChallans />} />
          <Route path="vehicles" element={<VehicleDispatch />} />
          <Route path="schedule" element={<DispatchSchedule />} />
          <Route path="history" element={<DispatchHistory />} />
          <Route path="reports" element={<DispatchReports />} />
          <Route path="notifications" element={<DispatchNotifications />} />
          <Route path="profile" element={<DispatchProfile />} />
        </Route>

        <Route path="/finance" element={<ProtectedRoute><FinanceLayout /></ProtectedRoute>}>
          <Route index element={<FinanceHome />} />
          <Route path="invoices" element={<InvoiceManagement />} />
          <Route path="billing" element={<BillingManagement />} />
          <Route path="payments" element={<PaymentManagement />} />
          <Route path="receivables" element={<Receivables />} />
          <Route path="payables" element={<Payables />} />
          <Route path="payroll" element={<PayrollManagement />} />
          <Route path="salary" element={<SalaryProcessing />} />
          <Route path="payslips" element={<PayslipManagement />} />
          <Route path="tax" element={<TaxManagement />} />
          <Route path="revenue" element={<RevenueAnalysis />} />
          <Route path="expenses" element={<ExpenseAnalysis />} />
          <Route path="profit-loss" element={<ProfitLoss />} />
          <Route path="reports" element={<FinancialReports />} />
          <Route path="notifications" element={<FinanceNotifications />} />
          <Route path="profile" element={<FinanceProfile />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
