import ApiResourceTable from '../../components/ApiResourceTable';

function SalaryProcessing() {
  return <ApiResourceTable title="Salary Structures" description="Live employee salary structures from the workforce API." endpoint="workforce/salary-structures/" columns={[{ key: 'salary_structure_id', label: 'ID' }, { key: 'employee', label: 'Employee' }, { key: 'effective_from', label: 'Effective from' }, { key: 'basic_salary', label: 'Basic salary' }, { key: 'hra', label: 'HRA' }, { key: 'other_deductions', label: 'Deductions' }]} searchKeys={['employee', 'effective_from']} />;
}

export default SalaryProcessing;
