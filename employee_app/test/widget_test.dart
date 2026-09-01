import 'package:flutter_test/flutter_test.dart';

import 'package:employee_app/main.dart';

void main() {
  testWidgets('shows the employee app loading state', (tester) async {
    await tester.pumpWidget(const EmployeeApp());
    expect(find.byType(EmployeeApp), findsOneWidget);
  });
}
