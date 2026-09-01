class Employee {
  Employee.fromJson(Map<String, dynamic> json)
    : employeeId = json['employee_id'] as int,
      employeeCode = json['employee_code'] as String,
      firstName = json['first_name'] as String,
      lastName = json['last_name'] as String,
      email = json['email'] as String? ?? '',
      phone = json['phone'] as String? ?? '',
      departmentName = json['department_name'] as String? ?? '',
      designationName = json['designation_name'] as String? ?? '',
      joiningDate = json['joining_date'] as String? ?? '',
      employmentType = json['employment_type'] as String? ?? '',
      gender = json['gender'] as String? ?? '',
      status = json['status'] as String? ?? '',
      profilePhotoUrl = json['profile_photo'] as String? ?? '',
      profileComplete = json['profile_complete'] as bool? ?? false;
  final int employeeId;
  final String employeeCode,
      firstName,
      lastName,
      email,
      phone,
      departmentName,
      designationName,
      joiningDate,
      employmentType,
      gender,
      status,
      profilePhotoUrl;
  final bool profileComplete;
  String get fullName => '$firstName $lastName';
}

class AttendanceRecord {
  AttendanceRecord.fromJson(Map<String, dynamic> json)
    : id = json['attendance_id'] as int,
      date = json['attendance_date'] as String,
      status = json['status'] as String,
      checkIn = json['check_in'] as String?,
      checkOut = json['check_out'] as String?,
      photo = json['photo'] as String?,
      latitude = json['latitude']?.toString(),
      longitude = json['longitude']?.toString();
  final int id;
  final String date, status;
  final String? checkIn, checkOut;
  final String? photo, latitude, longitude;
}

class PayrollItem {
  PayrollItem.fromJson(Map<String, dynamic> json)
    : id = json['payroll_item_id'] as int,
      payrollRunId = json['payroll_run'] as int,
      basicSalary = json['basic_salary'].toString(),
      overtime = json['overtime'].toString(),
      allowances = json['allowances'].toString(),
      deductions = json['deductions'].toString(),
      grossSalary = json['gross_salary'].toString(),
      netSalary = json['net_salary'].toString(),
      paymentStatus = json['payment_status'] as String;
  final int id, payrollRunId;
  final String basicSalary,
      overtime,
      allowances,
      deductions,
      grossSalary,
      netSalary,
      paymentStatus;
}

class PayrollRun {
  PayrollRun.fromJson(Map<String, dynamic> json)
    : id = json['payroll_run_id'] as int,
      periodStart = json['period_start'] as String,
      periodEnd = json['period_end'] as String,
      status = json['status'] as String;
  final int id;
  final String periodStart, periodEnd, status;
}

class LeaveType {
  LeaveType.fromJson(Map<String, dynamic> json)
    : id = json['leave_type_id'] as int,
      name = json['leave_name'] as String,
      maximumDays = json['maximum_days'] as int;
  final int id, maximumDays;
  final String name;
}

class LeaveRequest {
  LeaveRequest.fromJson(Map<String, dynamic> json)
    : id = json['leave_request_id'] as int,
      startDate = json['start_date'] as String,
      endDate = json['end_date'] as String,
      totalDays = json['total_days'].toString(),
      status = json['status'] as String,
      reason = json['reason'] as String;
  final int id;
  final String startDate, endDate, totalDays, status, reason;
}

class UserSession {
  UserSession.fromJson(Map<String, dynamic> json)
    : roleCode = json['role_code'] as String? ?? '',
      isFirstLogin = json['is_first_login'] as bool? ?? false,
      emailVerified = json['email_verified'] as bool? ?? false,
      employee = json['employee'] == null
          ? null
          : Employee.fromJson(json['employee'] as Map<String, dynamic>);
  final String roleCode;
  final bool isFirstLogin, emailVerified;
  final Employee? employee;
  bool get profileComplete => employee?.profileComplete ?? false;
}
