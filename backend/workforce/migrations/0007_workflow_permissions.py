from django.db import migrations


def seed_workflow_permissions(apps, schema_editor):
	Permission = apps.get_model('accounts', 'Permission')
	Role = apps.get_model('accounts', 'Role')
	RolePermission = apps.get_model('accounts', 'RolePermission')

	definitions = {
		'VIEW_ATTENDANCE': ('View attendance', 'View attendance records without modifying them.'),
		'VIEW_PAYROLL': ('View payroll', 'View payroll records.'),
		'MANAGE_PAYROLL': ('Manage payroll', 'Create and manage payroll records.'),
	}
	permissions = {}
	for code, (name, description) in definitions.items():
		permissions[code], _ = Permission.objects.get_or_create(
			permission_code=code,
			defaults={
				'permission_name': name,
				'module': 'workforce',
				'description': description,
			},
		)

	for role_code in ('SYSTEM_ADMIN', 'HR_MANAGER', 'FINANCE_MANAGER'):
		role = Role.objects.filter(role_code=role_code).first()
		if role:
			for permission_code in ('VIEW_PAYROLL', 'MANAGE_PAYROLL'):
				RolePermission.objects.get_or_create(role=role, permission=permissions[permission_code])

	for role_code in ('SYSTEM_ADMIN', 'HR_MANAGER'):
		role = Role.objects.filter(role_code=role_code).first()
		if role:
			RolePermission.objects.get_or_create(role=role, permission=permissions['VIEW_ATTENDANCE'])

	RolePermission.objects.filter(
		role__role_code='HR_MANAGER',
		permission__permission_code='MANAGE_ATTENDANCE',
	).delete()


class Migration(migrations.Migration):
	dependencies = [
		('workforce', '0006_seed_hr_workforce_data'),
	]

	operations = [
		migrations.RunPython(seed_workflow_permissions, migrations.RunPython.noop),
	]