import 'package:dio/dio.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:employee_app/main.dart';
import 'package:employee_app/repositories/repositories.dart';

void main() {
  testWidgets('shows the employee app loading state', (tester) async {
    await tester.pumpWidget(const EmployeeApp());
    expect(find.byType(EmployeeApp), findsOneWidget);
  });

  test('returns the backend validation message for a 400 list error', () {
    final exception = DioException(
      requestOptions: RequestOptions(path: 'auth/login/'),
      response: Response(
        requestOptions: RequestOptions(path: 'auth/login/'),
        statusCode: 400,
        data: {
          'non_field_errors': ['Please verify your email before logging in.'],
        },
      ),
    );

    expect(userMessage(exception), 'Please verify your email before logging in.');
  });

  test('returns the backend detail message for non-standard error payloads', () {
    final exception = DioException(
      requestOptions: RequestOptions(path: 'auth/login/'),
      response: Response(
        requestOptions: RequestOptions(path: 'auth/login/'),
        statusCode: 500,
        data: {'detail': 'Server is temporarily busy. Try again.'},
      ),
    );

    expect(userMessage(exception), 'Server is temporarily busy. Try again.');
  });
}
