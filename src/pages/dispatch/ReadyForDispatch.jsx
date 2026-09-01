import DispatchApiBoard from '../../components/DispatchApiBoard';

function ReadyForDispatch() {
  return <DispatchApiBoard title="Approved Orders Ready for Vehicle Dispatch" description="Dispatch records currently marked ready by the backend." endpoint="dispatches/ready-for-dispatch/" actionButtons />;
}

export default ReadyForDispatch;
