import DispatchApiBoard from '../../components/DispatchApiBoard';

function VehicleDispatch() {
  return <DispatchApiBoard title="Vehicle Dispatch Queue & Status" description="Live dispatch records and supported handover/confirmation actions." endpoint="dispatches/" actionButtons />;
}

export default VehicleDispatch;
