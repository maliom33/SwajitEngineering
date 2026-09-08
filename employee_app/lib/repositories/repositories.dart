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
    if (employee == null) {
      throw StateError('Authenticated user is not linked to an employee.');
    }
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

  Future<void> requestEmailVerification({String? email, String? employeeCode, String? password}) {
    final payload = <String, String>{};
    if (email != null && email.trim().isNotEmpty) {
      payload['email'] = email.trim();
    }
    if (employeeCode != null && employeeCode.trim().isNotEmpty) {
      payload['employee_code'] = employeeCode.trim();
    }
    if (password != null && password.isNotEmpty) {
      payload['password'] = password;
    }
    if (payload.isEmpty) {
      throw StateError(
        'Enter your email and Employee ID to resend the verification link.',
      );
    }
    return _api.dio.post('auth/verification/email/request/', data: payload);
  }
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

  Future<AttendanceRecord> checkOut({
    required int attendanceId,
    required String photoPath,
    required double latitude,
    required double longitude,
  }) async {
    final response = await _api.dio.post(
      'workforce/attendance/$attendanceId/check-out/',
      data: FormData.fromMap({
        'photo': await MultipartFile.fromFile(
          photoPath,
          filename: File(photoPath).uri.pathSegments.last,
        ),
        'latitude': double.parse(latitude.toStringAsFixed(6)),
        'longitude': double.parse(longitude.toStringAsFixed(6)),
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

String _extractErrorMessage(dynamic data) {
  if (data is Map) {
    final detail = data['detail'];
    if (detail is String && detail.trim().isNotEmpty) return detail.trim();
    final message = data['message'];
    if (message is String && message.trim().isNotEmpty) return message.trim();
    for (final value in data.values) {
      if (value is List && value.isNotEmpty) {
        final first = value.first;
        if (first is String && first.trim().isNotEmpty) return first.trim();
      }
      if (value is String && value.trim().isNotEmpty) return value.trim();
    }
  }
  if (data is String && data.trim().isNotEmpty) return data.trim();
  return '';
}

String userMessage(Object error) {
  if (error is StateError) return error.message.toString();
  if (error is DioException) {
    final status = error.response?.statusCode;
    final data = error.response?.data;
    final responseMessage = _extractErrorMessage(data);
    if (status == 401) return 'Your session has expired. Please login again.';
    if (status == 503) {
      if (responseMessage.isNotEmpty) return responseMessage;
      return 'Verification is temporarily unavailable. Please try again later.';
    }
    if (status == 400) {
      if (responseMessage.isNotEmpty) return responseMessage;
      return 'The request could not be completed. Please check your details and try again.';
    }
    if (status == 413) {
      return 'The photo is too large. Please retake the photo.';
    }
    if (status == 403) {
      if (responseMessage.isNotEmpty) return responseMessage;
      return 'You do not have permission to access this feature.';
    }
    if (status != null && status >= 400 && status < 600) {
      if (responseMessage.isNotEmpty) return responseMessage;
      return 'The server rejected the request. Please try again later.';
    }
    if (error.type == DioExceptionType.connectionError ||
        error.type == DioExceptionType.connectionTimeout) {
      return 'Unable to connect to server. Please check your internet connection.';
    }
    if (responseMessage.isNotEmpty) return responseMessage;
  }
  return 'Something went wrong. Please try again later.';
}
