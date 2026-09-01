import ApiAnalyticsSummary from '../../components/ApiAnalyticsSummary';

function FinancialOverview() {
  return <ApiAnalyticsSummary title="Financial Overview" description="Revenue, expenses, profit, payments, and payroll-related financial metrics." endpoint="analytics/finance/" />;
}

export default FinancialOverview;
