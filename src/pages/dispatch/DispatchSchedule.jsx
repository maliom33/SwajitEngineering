import DispatchApiBoard from '../../components/DispatchApiBoard';

function DispatchSchedule() {
  return <DispatchApiBoard title="Today's Dispatch Schedule" description="Dispatch records scheduled for today." endpoint="dispatches/today/" />;
}

export default DispatchSchedule;
