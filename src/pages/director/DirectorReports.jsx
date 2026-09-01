import ApiAnalyticsSummary from '../../components/ApiAnalyticsSummary';

function DirectorReports() {
  return <ApiAnalyticsSummary title="Reports" description="Live executive analytics. Report export is not currently provided by the backend." endpoint="analytics/executive-dashboard/" />;
}

export default DirectorReports;
