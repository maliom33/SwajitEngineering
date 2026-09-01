from django.contrib import admin

from .models import Candidate, CandidateResume, CandidateSkill, Interview, JobApplication, JobPosition, RecruitmentScreening


@admin.register(JobPosition)
class JobPositionAdmin(admin.ModelAdmin):
	list_display = ['job_code', 'job_title', 'department', 'status', 'opening_date', 'closing_date']
	list_filter = ['status', 'department', 'designation', 'opening_date']
	search_fields = ['job_code', 'job_title']


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
	list_display = ['candidate_code', 'first_name', 'last_name', 'email', 'candidate_status', 'created_at']
	list_filter = ['candidate_status', 'created_at']
	search_fields = ['candidate_code', 'first_name', 'last_name', 'email']


@admin.register(CandidateResume)
class CandidateResumeAdmin(admin.ModelAdmin):
	list_display = ['candidate', 'original_filename', 'file_type', 'parsing_status', 'is_primary', 'uploaded_at']
	list_filter = ['parsing_status', 'is_primary', 'file_type']
	search_fields = ['candidate__candidate_code', 'original_filename']
	exclude = ['parsed_text']


@admin.register(CandidateSkill)
class CandidateSkillAdmin(admin.ModelAdmin):
	list_display = ['candidate', 'skill_name', 'proficiency_level', 'source', 'years_of_experience']
	list_filter = ['source', 'proficiency_level']
	search_fields = ['candidate__candidate_code', 'skill_name']


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
	list_display = ['application_number', 'candidate', 'job', 'application_status', 'screening_score', 'application_date']
	list_filter = ['application_status', 'application_date']
	search_fields = ['application_number', 'candidate__candidate_code', 'job__job_code']


@admin.register(RecruitmentScreening)
class RecruitmentScreeningAdmin(admin.ModelAdmin):
	list_display = ['application', 'model_version', 'overall_score', 'recommendation', 'screened_at']
	list_filter = ['recommendation', 'model_version', 'screened_at']
	search_fields = ['application__application_number']
	exclude = ['explanation']


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
	list_display = ['application', 'interview_round', 'interview_type', 'scheduled_at', 'status', 'score', 'interviewer']
	list_filter = ['interview_type', 'status', 'scheduled_at']
	search_fields = ['application__application_number', 'interviewer__email']
