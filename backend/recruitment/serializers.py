from rest_framework import serializers
from workforce.models import Employee

from .models import (
    Candidate,
    CandidateResume,
    CandidateSkill,
    Interview,
    JobApplication,
    JobPosition,
    RecruitmentScreening,
)


class JobPositionSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = JobPosition
        fields = '__all__'

    def validate(self, attrs):
        if attrs.get('salary_range_min') is not None and attrs.get('salary_range_max') is not None and attrs['salary_range_max'] < attrs['salary_range_min']:
            raise serializers.ValidationError({'salary_range_max': 'Maximum salary cannot be lower than minimum salary.'})
        return attrs


class CandidateSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Candidate
        fields = '__all__'


class CandidateResumeSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = CandidateResume
        fields = '__all__'
        read_only_fields = ['resume_id', 'original_filename', 'file_type', 'file_size', 'uploaded_at', 'parsing_status']

    def validate_file(self, value):
        allowed_types = {
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        }
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError('Resume files must be 10 MB or smaller.')
        extension = value.name.rsplit('.', 1)[-1].lower() if '.' in value.name else ''
        if extension not in {'pdf', 'doc', 'docx'}:
            raise serializers.ValidationError('Only PDF, DOC, and DOCX resumes are supported.')
        if value.content_type and value.content_type not in allowed_types:
            raise serializers.ValidationError('The uploaded content type is not supported.')
        return value

    def create(self, validated_data):
        uploaded_file = validated_data['file']
        validated_data.update({
            'original_filename': uploaded_file.name,
            'file_type': uploaded_file.content_type or 'application/octet-stream',
            'file_size': uploaded_file.size,
        })
        return super().create(validated_data)


class CandidateSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateSkill
        fields = '__all__'


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ['application_id', 'application_date', 'created_at', 'updated_at']

    def validate(self, attrs):
        candidate = attrs.get('candidate', getattr(self.instance, 'candidate', None))
        resume = attrs.get('resume', getattr(self.instance, 'resume', None))
        if resume and candidate and resume.candidate_id != candidate.candidate_id:
            raise serializers.ValidationError({'resume': 'Resume must belong to the selected candidate.'})
        return attrs


class RecruitmentScreeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruitmentScreening
        fields = '__all__'
        read_only_fields = ['screening_id', 'created_at']

    def validate(self, attrs):
        for field in ['skills_score', 'education_score', 'experience_score', 'overall_score']:
            if not 0 <= attrs[field] <= 100:
                raise serializers.ValidationError({field: 'Score must be between 0 and 100.'})
        return attrs


class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = '__all__'
        read_only_fields = ['interview_id', 'created_at', 'updated_at']

    def validate_score(self, value):
        if value is not None and not 0 <= value <= 100:
            raise serializers.ValidationError('Score must be between 0 and 100.')
        return value


class CandidateConversionSerializer(serializers.Serializer):
    department = serializers.IntegerField()
    designation = serializers.IntegerField()
    joining_date = serializers.DateField()
    employment_type = serializers.ChoiceField(choices=Employee.EmploymentType.choices)
    base_salary = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=0)