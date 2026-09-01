import ApiAnalyticsSummary from '../../components/ApiAnalyticsSummary';

function CompanyOverview() {
  return <ApiAnalyticsSummary title="Company Overview" description="Executive snapshot of operations, departments, and overall health." endpoint="analytics/executive-dashboard/" groups={[{ label: 'Workforce', key: 'workforce' }, { label: 'Sales', key: 'sales' }, { label: 'Operations', key: 'logistics' }, { label: 'Finance', key: 'finance' }]} />;
}

export default CompanyOverview;
