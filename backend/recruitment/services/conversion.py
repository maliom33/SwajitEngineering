from django.db import transaction

from workforce.models import Employee

from recruitment.models import Candidate, JobApplication


@transaction.atomic
def convert_selected_candidate_to_employee(candidate, *, department, designation, joining_date, employment_type, base_salary):
    candidate = Candidate.objects.select_for_update().get(pk=candidate.pk)
    if candidate.employee_id:
        return candidate.employee

    selected_application = candidate.applications.filter(
        application_status=JobApplication.Status.SELECTED,
    ).first()
    if not selected_application:
        raise ValueError('Candidate must have a selected application before conversion.')

    employee = Employee.objects.create(
        employee_code=candidate.candidate_code,
        first_name=candidate.first_name,
        last_name=candidate.last_name,
        email=candidate.email,
        phone=candidate.phone,
        date_of_birth=candidate.date_of_birth,
        address=candidate.address,
        city=candidate.city,
        state=candidate.state,
        pincode=candidate.pincode,
        department=department,
        designation=designation,
        joining_date=joining_date,
        employment_type=employment_type,
        base_salary=base_salary,
    )
    candidate.employee = employee
    candidate.save(update_fields=['employee', 'updated_at'])
    return employee