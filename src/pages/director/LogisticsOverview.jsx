import ApiAnalyticsSummary from '../../components/ApiAnalyticsSummary';

function LogisticsOverview() {
  return <ApiAnalyticsSummary title="Logistics Overview" description="Fleet performance, delivery lifecycle, and route monitoring." endpoint="analytics/logistics/" />;
}

export default LogisticsOverview;
