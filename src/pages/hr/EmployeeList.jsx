import { useEffect, useMemo, useState } from 'react';
import EmployeeTable from '../../components/EmployeeTable';
import client from '../../api/client';

function formatStatus(status) {
  return status
    ? status.toLowerCase().replace(/_/g, ' ').replace(/\b\w/g, (letter) => letter.toUpperCase())
    : 'Not available';
}

function getValidationMessage(error) {
  const data = error.response?.data;
  if (!data || typeof data !== 'object') return 'Please check the employee details and try again.';
  const firstError = Object.values(data).flat()[0];
  return typeof firstError === 'string' ? firstError : 'Please check the employee details and try again.';
}

const frontendBaseUrl = (import.meta.env.VITE_APP_BASE_URL || 'https://swajit-engineering-frontend.onrender.com').replace(/\/$/, '');

function mapEmployee(employee, departments, designations) {
  const department = employee.department_name || (employee.department ? departments.find((item) => item.department_id === employee.department)?.department_name : null);
  const designation = employee.designation_name || (employee.designation ? designations.find((item) => item.designation_id === employee.designation)?.designation_name : null);

  return {
    id: employee.employee_code || employee.employee_id,
    employeeId: employee.employee_id,
    record: employee,
    name: `${employee.first_name || ''} ${employee.last_name || ''}`.trim() || 'Unnamed employee',
    department: department || 'Not available',
    designation: designation || 'Not available',
    gender: employee.gender || 'Not available',
    attendance: 'Not available',
    status: formatStatus(employee.status),
    emailVerified: employee.email_verified,
    phoneVerified: employee.phone_verified,
    profileComplete: employee.profile_complete,
  };
}

function EmployeeList() {
  const [employees, setEmployees] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [designations, setDesignations] = useState([]);
  const [selectedDepartment, setSelectedDepartment] = useState('');
  const [isLookupLoading, setIsLookupLoading] = useState(false);
  const [lookupError, setLookupError] = useState('');
  const [search, setSearch] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [deletingId, setDeletingId] = useState(null);
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingEmployee, setEditingEmployee] = useState(null);
  const [formError, setFormError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [activationLink, setActivationLink] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const loadEmployees = async () => {
    setIsLoading(true);
    setErrorMessage('');

    try {
      const response = await client.get('workforce/employees/');
      const results = Array.isArray(response.data) ? response.data : response.data?.results;
      setEmployees(Array.isArray(results) ? results : []);
    } catch (error) {
      if (error.response?.status === 403) {
        setErrorMessage('You do not have permission to view employees.');
      } else if (error.response?.status >= 500) {
        setErrorMessage('The employee service is temporarily unavailable. Please try again shortly.');
      } else if (!error.response) {
        setErrorMessage('The backend is unavailable. Please check the server and try again.');
      } else {
        setErrorMessage('We could not load the employee list. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadEmployees();
  }, []);

  const openCreateForm = () => {
    setEditingEmployee(null);
    setSelectedDepartment('');
    setDesignations([]);
    setFormError('');
    setLookupError('');
    setSuccessMessage('');
    setActivationLink('');
    setIsFormOpen(true);
  };

  const openEditForm = (employee) => {
    setEditingEmployee(employee.record);
    setSelectedDepartment(String(employee.record.department || ''));
    setFormError('');
    setLookupError('');
    setSuccessMessage('');
    setActivationLink('');
    setIsFormOpen(true);
  };

  useEffect(() => {
    if (!isFormOpen) return undefined;

    let isCancelled = false;
    const getResults = (response) => (Array.isArray(response.data) ? response.data : response.data?.results) || [];
    setIsLookupLoading(true);
    setLookupError('');
    Promise.all([
      departments.length ? Promise.resolve({ data: departments }) : client.get('workforce/departments/'),
      selectedDepartment ? client.get(`workforce/designations/?department=${selectedDepartment}`) : Promise.resolve({ data: [] }),
    ])
      .then(([departmentResponse, designationResponse]) => {
        if (isCancelled) return;
        setDepartments(getResults(departmentResponse));
        setDesignations(getResults(designationResponse));
      })
      .catch(() => {
        if (!isCancelled) setLookupError('Departments or designations could not be loaded. Please try again.');
      })
      .finally(() => {
        if (!isCancelled) setIsLookupLoading(false);
      });

    return () => { isCancelled = true; };
  }, [isFormOpen, selectedDepartment]);

  const handleDepartmentChange = (event) => {
    const departmentId = event.target.value;
    setSelectedDepartment(departmentId);
    setDesignations([]);
    event.currentTarget.form.elements.designation.value = '';
  };

  const closeForm = () => {
    if (!isSaving) {
      setIsFormOpen(false);
      setEditingEmployee(null);
      setFormError('');
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setFormError('');
    setSuccessMessage('');
    setIsSaving(true);

    const formData = new FormData(event.currentTarget);
    const payload = Object.fromEntries(formData.entries());
    delete payload.employee_code;
    payload.department = Number(payload.department);
    payload.designation = Number(payload.designation);
    payload.base_salary = Number(payload.base_salary);

    try {
      if (editingEmployee?.employee_id) {
        await client.patch(`workforce/employees/${editingEmployee.employee_id}/`, payload);
        setSuccessMessage('Employee updated successfully.');
      } else {
        const response = await client.post('workforce/employees/', payload);
        if (response.data?.activation_token) {
          const query = new URLSearchParams({ email: payload.email, activation_token: response.data.activation_token });
          setActivationLink(`${frontendBaseUrl}/activate?${query.toString()}`);
          setSuccessMessage('Employee added. Share the activation link with the employee.');
        } else {
          setSuccessMessage('Employee added successfully.');
        }
      }
      setIsFormOpen(false);
      setEditingEmployee(null);
      await loadEmployees();
    } catch (error) {
      if (error.response?.status === 403) {
        setFormError('You do not have permission to manage employees.');
      } else if (error.response?.status === 400) {
        setFormError(getValidationMessage(error));
      } else if (!error.response) {
        setFormError('The backend is unavailable. Please try again.');
      } else {
        setFormError('We could not save this employee. Please try again.');
      }
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async (employee) => {
    if (!employee.employeeId || !window.confirm(`Delete ${employee.name}?`)) return;

    setDeletingId(employee.employeeId);
    setErrorMessage('');
    setSuccessMessage('');
    try {
      await client.delete(`workforce/employees/${employee.employeeId}/`);
      setSuccessMessage('Employee deleted successfully.');
      await loadEmployees();
    } catch (error) {
      if (error.response?.status === 403) {
        setErrorMessage('You do not have permission to delete employees.');
      } else if (!error.response) {
        setErrorMessage('The backend is unavailable. Please try again.');
      } else {
        setErrorMessage('We could not delete this employee. Please try again.');
      }
    } finally {
      setDeletingId(null);
    }
  };

  const getFieldValue = (field) => editingEmployee?.[field] ?? '';

  const visibleEmployees = useMemo(() => {
    const query = search.trim().toLowerCase();
    const mappedEmployees = employees
      .map((employee) => mapEmployee(employee, departments, designations))
    if (!query) return mappedEmployees;

    return mappedEmployees.filter((employee) => Object.values(employee).some((value) => String(value).toLowerCase().includes(query)));
  }, [departments, designations, employees, search]);

  return (
    <div>
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Employee List</h2>
        <div className="flex items-center gap-2">
          <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search employees..." className="rounded-2xl border border-slate-200 px-4 py-2" />
          <button type="button" onClick={openCreateForm} className="rounded-2xl bg-brand-900 px-4 py-2 text-white">Add Employee</button>
        </div>
      </div>

      {successMessage && <div role="status" className="mb-4 rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-700"><p>{successMessage}</p>{activationLink && <a href={activationLink} target="_blank" rel="noreferrer" className="mt-2 block break-all font-medium underline">Open employee activation link</a>}</div>}
      {errorMessage && <p role="alert" className="mb-4 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{errorMessage}</p>}

      {isLoading && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-600" role="status">
          Loading employees...
        </div>
      )}

      {!isLoading && errorMessage && (
        <div className="rounded-2xl border border-red-200 bg-red-50 p-6 text-sm text-red-700" role="alert">
          <p>{errorMessage}</p>
          <button type="button" onClick={loadEmployees} className="mt-4 rounded-2xl bg-red-700 px-4 py-2 font-medium text-white">
            Try again
          </button>
        </div>
      )}

      {!isLoading && !errorMessage && employees.length === 0 && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-600">
          No employees have been registered yet.
        </div>
      )}

      {!isLoading && !errorMessage && employees.length > 0 && visibleEmployees.length === 0 && (
        <div className="rounded-2xl border border-slate-200 bg-white p-6 text-sm text-slate-600">
          No employees match your search.
        </div>
      )}

      {!isLoading && !errorMessage && visibleEmployees.length > 0 && <EmployeeTable employees={visibleEmployees} onEdit={openEditForm} onDelete={handleDelete} deletingId={deletingId} />}

      {isFormOpen && (
        <div className="fixed inset-0 z-30 flex items-start justify-center overflow-y-auto bg-slate-950/40 px-4 py-10" role="dialog" aria-modal="true" aria-labelledby="employee-form-title">
          <form onSubmit={handleSubmit} className="w-full max-w-3xl rounded-3xl bg-white p-6 shadow-2xl">
            <div className="flex items-center justify-between gap-4">
              <h3 id="employee-form-title" className="text-xl font-semibold text-slate-950">{editingEmployee ? 'Edit Employee' : 'Add Employee'}</h3>
              <button type="button" onClick={closeForm} className="rounded-2xl border border-slate-200 px-3 py-2 text-sm text-slate-600">Close</button>
            </div>

            {(formError || lookupError) && <p role="alert" className="mt-4 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{formError || lookupError}</p>}

            <div className="mt-6 grid gap-4 sm:grid-cols-2">
              <div className="text-sm text-slate-700">Employee code<div className="mt-1 flex h-11 items-center rounded-2xl border border-slate-200 bg-slate-50 px-3 text-slate-500">{editingEmployee?.employee_code || 'Auto-generated by backend'}</div></div>
              <label className="text-sm text-slate-700">Email<input name="email" type="email" required defaultValue={getFieldValue('email')} className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3" /></label>
              <label className="text-sm text-slate-700">First name<input name="first_name" required defaultValue={getFieldValue('first_name')} className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3" /></label>
              <label className="text-sm text-slate-700">Last name<input name="last_name" required defaultValue={getFieldValue('last_name')} className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3" /></label>
              <label className="text-sm text-slate-700">Phone<input name="phone" required defaultValue={getFieldValue('phone')} className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3" /></label>
              <label className="text-sm text-slate-700">Joining date<input name="joining_date" type="date" required defaultValue={getFieldValue('joining_date')} className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3" /></label>
              <label className="text-sm text-slate-700">Department<select name="department" required defaultValue={getFieldValue('department')} onChange={handleDepartmentChange} disabled={isLookupLoading} className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3"><option value="">{isLookupLoading ? 'Loading departments...' : 'Select department'}</option>{departments.filter((department) => department.is_active).map((department) => <option key={department.department_id} value={department.department_id}>{department.department_name}</option>)}</select></label>
              <label className="text-sm text-slate-700">Designation<select name="designation" required defaultValue={getFieldValue('designation')} disabled={!selectedDepartment || isLookupLoading} className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3"><option value="">{!selectedDepartment ? 'Select department first' : isLookupLoading ? 'Loading designations...' : designations.length ? 'Select designation' : 'No designations available'}</option>{designations.filter((designation) => designation.is_active).map((designation) => <option key={designation.designation_id} value={designation.designation_id}>{designation.designation_name}</option>)}</select></label>
              <label className="text-sm text-slate-700">Employment type<select name="employment_type" required defaultValue={getFieldValue('employment_type') || 'FULL_TIME'} className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3"><option value="FULL_TIME">Full Time</option><option value="PART_TIME">Part Time</option><option value="CONTRACT">Contract</option><option value="INTERN">Intern</option></select></label>
              <label className="text-sm text-slate-700">Base salary<input name="base_salary" type="number" min="0" step="0.01" required defaultValue={getFieldValue('base_salary')} className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3" /></label>
              <label className="text-sm text-slate-700">Status<select name="status" defaultValue={getFieldValue('status') || 'ACTIVE'} className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3"><option value="ACTIVE">Active</option><option value="INACTIVE">Inactive</option><option value="ON_LEAVE">On Leave</option><option value="RESIGNED">Resigned</option><option value="TERMINATED">Terminated</option></select></label>
              <label className="text-sm text-slate-700">Gender<select name="gender" required defaultValue={getFieldValue('gender')} className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3"><option value="">Select gender</option><option value="Male">Male</option><option value="Female">Female</option><option value="Other">Other</option><option value="Prefer not to say">Prefer not to say</option></select></label>
              <label className="text-sm text-slate-700">Date of birth<input name="date_of_birth" type="date" defaultValue={getFieldValue('date_of_birth')} className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3" /></label>
              <label className="text-sm text-slate-700 sm:col-span-2">Address<textarea name="address" defaultValue={getFieldValue('address')} className="mt-1 w-full rounded-2xl border border-slate-200 px-3 py-2" rows="2" /></label>
              <label className="text-sm text-slate-700">City<input name="city" defaultValue={getFieldValue('city')} className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3" /></label>
              <label className="text-sm text-slate-700">State<input name="state" defaultValue={getFieldValue('state')} className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3" /></label>
              <label className="text-sm text-slate-700">Pincode<input name="pincode" defaultValue={getFieldValue('pincode')} className="mt-1 h-11 w-full rounded-2xl border border-slate-200 px-3" /></label>
            </div>

            <div className="mt-6 flex justify-end gap-3">
              <button type="button" onClick={closeForm} disabled={isSaving} className="rounded-2xl border border-slate-200 px-4 py-2 text-sm text-slate-700">Cancel</button>
              <button type="submit" disabled={isSaving} className="rounded-2xl bg-brand-900 px-4 py-2 text-sm font-medium text-white disabled:opacity-60">{isSaving ? 'Saving...' : editingEmployee ? 'Update Employee' : 'Save Employee'}</button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}

export default EmployeeList;
