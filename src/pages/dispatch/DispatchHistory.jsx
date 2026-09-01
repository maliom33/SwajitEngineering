import DispatchApiBoard from '../../components/DispatchApiBoard';

function DispatchHistory() {
  return <DispatchApiBoard title="Completed Dispatch History" description="Status history records supplied by the dispatch API." endpoint="dispatches/history/" />;
}

export default DispatchHistory;
