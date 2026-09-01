import DispatchApiBoard from '../../components/DispatchApiBoard';

function DispatchPlanning() {
  return <DispatchApiBoard title="Pending Dispatch Orders & Scheduling" description="Live dispatch queue and supported dispatch workflow actions." actionButtons endpoint="dispatches/" />;
}

export default DispatchPlanning;
