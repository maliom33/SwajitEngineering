import DispatchApiBoard from '../../components/DispatchApiBoard';

function LoadingVerification() {
  return <DispatchApiBoard title="Vehicle Loading & QA Verification" description="Live dispatch records and supported confirmation workflow." endpoint="dispatches/" actionButtons />;
}

export default LoadingVerification;
