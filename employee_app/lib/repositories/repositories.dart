import 'dart:io';
import 'package:dio/dio.dart';
import '../core/network/api_client.dart';
import '../core/storage/secure_token_storage.dart';
import '../models/models.dart';

class AuthRepository {
  AuthRepository({
    required ApiClient apiClient,
    required SecureTokenStorage storage,
  }) : _api = apiClient,
       _storage = storage;
  final ApiClient _api;
  final SecureTokenStorage _storage;
  Future<UserSession> login(String email, String password) async {
    final response = await _api.dio.post(
      'auth/login/',
      data: {'email': email, 'password': password},
    );
    await _storage.save(
      access: response.data['access'] as String,
      refresh: response.data['refresh'] as String,
    );
    return me();
  }

  Future<UserSession> me() async => UserSession.fromJson(
    (await _api.dio.get('auth/me/')).data as Map<String, dynamic>,
  );
  Future<void> logout() => _storage.clear();
}

class EmployeeRepository {
  EmployeeRepository(this._api);
  final ApiClient _api;
  Future<Employee> getMe() async {
    final response = await _api.dio.get('auth/me/');
    final employee =
        (response.data as Map<String, dynamic>)['employee']
            as Map<String, dynamic>?;
    if (employee == null)
      throw StateError('Authenticated user is not linked to an employee.');
    return Employee.fromJson(employee);
  }

  Future<void> changePassword({
    required String currentPassword,
    required String newPassword,
    required String confirmPassword,
  }) => _api.dio.post(
    'auth/change-password/',
    data: {
      'current_password': currentPassword,
      'new_password': newPassword,
      'confirm_password': confirmPassword,
    },
  );
  Future<void> uploadPhoto(int employeeId, String path) async {
    await _api.dio.patch(
      'workforce/employees/$employeeId/',
      data: FormData.fromMap({
        'profile_photo': await MultipartFile.fromFile(path),
      }),
    );
  }

  Future<void> updateProfile({
    required int employeeId,
    required String firstName,
    required String lastName,
    required String email,
    required String phone,
    required String gender,
    required String address,
    required String city,
    required String state,
    required String pincode,
  }) => _api.dio.patch(
    'workforce/employees/$employeeId/',
    data: {
      'first_name': firstName,
      'last_name': lastName,
      'email': email,
      'phone': phone,
      'gender': gender,
      'address': address,
      'city': city,
      'state': state,
      'pincode': pincode,
    },
  );

  Future<void> requestEmailVerification({
    String? email,
    String? employeeCode,
  }) => _api.dio.post(
    'auth/verification/email/request/',
    data: {
      if (email case final value?) 'email': value,
      if (employeeCode case final value?) 'employee_code': value,
    },
  );
}

class AttendanceRepository {
  AttendanceRepository(this._api);
  final ApiClient _api;
  Future<List<AttendanceRecord>> list() async {
    final data = (await _api.dio.get('workforce/attendance/')).data;
    final rows = data is List ? data : data['results'];
    return rows
        .map<AttendanceRecord>(
          (row) => AttendanceRecord.fromJson(row as Map<String, dynamic>),
        )
        .toList();
  }

  Future<AttendanceRecord> submit({
    required String photoPath,
    required double latitude,
    required double longitude,
  }) async {
    final normalizedLatitude = double.parse(latitude.toStringAsFixed(6));
    final normalizedLongitude = double.parse(longitude.toStringAsFixed(6));
    final response = await _api.dio.post(
      'workforce/attendance/',
      data: FormData.fromMap({
        'photo': await MultipartFile.fromFile(
          photoPath,
          filename: File(photoPath).uri.pathSegments.last,
        ),
        'latitude': normalizedLatitude,
        'longitude': normalizedLongitude,
      }),
    );
    return AttendanceRecord.fromJson(response.data as Map<String, dynamic>);
  }
}

class PayrollRepository {
  PayrollRepository(this._api);
  final ApiClient _api;
  Future<List<PayrollItem>> items() async {
    final data = (await _api.dio.get('workforce/payroll-items/')).data;
    final rows = data is List ? data : data['results'];
    return rows
        .map<PayrollItem>(
          (row) => PayrollItem.fromJson(row as Map<String, dynamic>),
        )
        .toList();
  }

  Future<List<PayrollRun>> runs() async {
    final data = (await _api.dio.get('workforce/payroll-runs/')).data;
    final rows = data is List ? data : data['results'];
    return rows
        .map<PayrollRun>(
          (row) => PayrollRun.fromJson(row as Map<String, dynamic>),
        )
        .toList();
  }
}

class LeaveRepository {
  LeaveRepository(this._api);
  final ApiClient _api;
  Future<List<LeaveType>> types() async {
    final data = (await _api.dio.get('workforce/leave-types/')).data;
    final rows = data is List ? data : data['results'];
    return rows
        .map<LeaveType>(
          (row) => LeaveType.fromJson(row as Map<String, dynamic>),
        )
        .toList();
  }

  Future<List<LeaveRequest>> requests() async {
    final data = (await _api.dio.get('workforce/leave-requests/')).data;
    final rows = data is List ? data : data['results'];
    return rows
        .map<LeaveRequest>(
          (row) => LeaveRequest.fromJson(row as Map<String, dynamic>),
        )
        .toList();
  }

  Future<void> submit({
    required int leaveType,
    required String startDate,
    required String endDate,
    required double totalDays,
    required String reason,
  }) => _api.dio.post(
    'workforce/leave-requests/',
    data: {
      'leave_type': leaveType,
      'start_date': startDate,
      'end_date': endDate,
      'total_days': totalDays,
      'reason': reason,
    },
  );
}

String userMessage(Object error) {
  if (error is StateError) return error.message.toString();
  if (error is DioException) {
    final status = error.response?.statusCode;
    final data = error.response?.data;
    if (status == 401) return 'Your session has expired. Please login again.';
    if (status == 503)
      return 'Verification is temporarily unavailable. Please try again later.';
    if (status == 400) {
      if (data is Map && data['detail'] is String)
        return data['detail'] as String;
      if (data is Map &&
          data['non_field_errors'] is List &&
          (data['non_field_errors'] as List).isNotEmpty)
        return (data['non_field_errors'] as List).first.toString();
      if (data is Map && data['attendance_date'] is List)
        return data['attendance_date'].first.toString();
      if (data is Map && data['photo'] is List)
        return data['photo'].first.toString();
      if (data is Map && data['location'] is List)
        return data['location'].first.toString();
      if (data is Map) {
        for (final value in data.values) {
          if (value is List && value.isNotEmpty) return value.first.toString();
          if (value is String && value.isNotEmpty) return value;
        }
      }
      return 'The request could not be completed. Please check your details and try again.';
    }
    if (status == 413)
      return 'The photo is too large. Please retake the photo.';
    if (status == 403) {
      if (data is Map && data['detail'] is String)
        return data['detail'] as String;
      return 'You do not have permission to access this feature.';
    }
    if (error.type == DioExceptionType.connectionError ||
        error.type == DioExceptionType.connectionTimeout)
      return 'Unable to connect to server. Please check your internet connection.';
  }
  return 'Something went wrong. Please try again later.';
}
