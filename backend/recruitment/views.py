from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from accounts.permissions import HasPermission
from workforce.models import Department, Designation

from .models import Candidate, CandidateResume, CandidateSkill, Interview, JobApplication, JobPosition, RecruitmentScreening
from .serializers import (
    CandidateConversionSerializer,
    CandidateResumeSerializer,
    CandidateSerializer,
    CandidateSkillSerializer,
    InterviewSerializer,
    JobApplicationSerializer,
    JobPositionSerializer,
    RecruitmentScreeningSerializer,
)
from .services.conversion import convert_selected_candidate_to_employee


class RecruitmentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    write_permissions = {}

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        required_permission = self.write_permissions.get(self.action)
        if required_permission:
            self.required_permission = required_permission
            permission_classes.append(HasPermission)
        return [permission() for permission in permission_classes]


class JobPositionViewSet(RecruitmentViewSet):
    queryset = JobPosition.objects.select_related('department', 'designation', 'created_by').all()
    serializer_class = JobPositionSerializer
    write_permissions = {'create': 'MANAGE_JOB_POSITIONS', 'update': 'MANAGE_JOB_POSITIONS', 'partial_update': 'MANAGE_JOB_POSITIONS', 'destroy': 'MANAGE_JOB_POSITIONS'}

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CandidateViewSet(RecruitmentViewSet):
    queryset = Candidate.objects.select_related('employee').all()
    serializer_class = CandidateSerializer
    write_permissions = {'create': 'MANAGE_CANDIDATES', 'update': 'MANAGE_CANDIDATES', 'partial_update': 'MANAGE_CANDIDATES', 'destroy': 'MANAGE_CANDIDATES', 'convert_to_employee': 'MANAGE_CANDIDATES'}

    @action(detail=True, methods=['post'], url_path='convert-to-employee')
    def convert_to_employee(self, request, pk=None):
        serializer = CandidateConversionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            department = Department.objects.get(pk=serializer.validated_data['department'])
            designation = Designation.objects.get(pk=serializer.validated_data['designation'])
        except (Department.DoesNotExist, Designation.DoesNotExist) as error:
            raise ValidationError('A valid department and designation are required.') from error
        try:
            employee = convert_selected_candidate_to_employee(
                self.get_object(),
                department=department,
                designation=designation,
                joining_date=serializer.validated_data['joining_date'],
                employment_type=serializer.validated_data['employment_type'],
                base_salary=serializer.validated_data['base_salary'],
            )
        except ValueError as error:
            raise ValidationError(str(error)) from error
        return Response({'employee_id': employee.employee_id, 'employee_code': employee.employee_code}, status=status.HTTP_201_CREATED)


class CandidateResumeViewSet(RecruitmentViewSet):
    queryset = CandidateResume.objects.select_related('candidate').all()
    serializer_class = CandidateResumeSerializer
    write_permissions = {'create': 'MANAGE_CANDIDATES', 'update': 'MANAGE_CANDIDATES', 'partial_update': 'MANAGE_CANDIDATES', 'destroy': 'MANAGE_CANDIDATES'}


class CandidateSkillViewSet(RecruitmentViewSet):
    queryset = CandidateSkill.objects.select_related('candidate').all()
    serializer_class = CandidateSkillSerializer
    write_permissions = {'create': 'MANAGE_CANDIDATES', 'update': 'MANAGE_CANDIDATES', 'partial_update': 'MANAGE_CANDIDATES', 'destroy': 'MANAGE_CANDIDATES'}


class JobApplicationViewSet(RecruitmentViewSet):
    queryset = JobApplication.objects.select_related('candidate', 'job', 'resume').all()
    serializer_class = JobApplicationSerializer
    write_permissions = {'create': 'MANAGE_CANDIDATES', 'update': 'MANAGE_CANDIDATES', 'partial_update': 'MANAGE_CANDIDATES', 'destroy': 'MANAGE_CANDIDATES'}


class RecruitmentScreeningViewSet(RecruitmentViewSet):
    queryset = RecruitmentScreening.objects.select_related('application', 'screened_by').all()
    serializer_class = RecruitmentScreeningSerializer
    write_permissions = {'create': 'SCREEN_RESUMES', 'update': 'SCREEN_RESUMES', 'partial_update': 'SCREEN_RESUMES', 'destroy': 'SCREEN_RESUMES'}


class InterviewViewSet(RecruitmentViewSet):
    queryset = Interview.objects.select_related('application', 'interviewer').all()
    serializer_class = InterviewSerializer
    write_permissions = {'create': 'MANAGE_INTERVIEWS', 'update': 'MANAGE_INTERVIEWS', 'partial_update': 'MANAGE_INTERVIEWS', 'destroy': 'MANAGE_INTERVIEWS'}
