from rest_framework.routers import DefaultRouter

from .views import (
    CandidateResumeViewSet,
    CandidateSkillViewSet,
    CandidateViewSet,
    InterviewViewSet,
    JobApplicationViewSet,
    JobPositionViewSet,
    RecruitmentScreeningViewSet,
)

router = DefaultRouter()
router.register('jobs', JobPositionViewSet, basename='recruitment-job')
router.register('candidates', CandidateViewSet, basename='recruitment-candidate')
router.register('resumes', CandidateResumeViewSet, basename='recruitment-resume')
router.register('skills', CandidateSkillViewSet, basename='recruitment-skill')
router.register('applications', JobApplicationViewSet, basename='recruitment-application')
router.register('screenings', RecruitmentScreeningViewSet, basename='recruitment-screening')
router.register('interviews', InterviewViewSet, basename='recruitment-interview')

urlpatterns = router.urls