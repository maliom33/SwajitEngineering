import ApiAnalyticsSummary from '../../components/ApiAnalyticsSummary';

function WarehouseOverview() {
  return <ApiAnalyticsSummary title="Warehouse Overview" description="Inventory health, capacity, and material flow monitoring." endpoint="analytics/warehouse/" />;
}

export default WarehouseOverview;
