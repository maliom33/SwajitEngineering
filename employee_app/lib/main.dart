import 'package:flutter/material.dart';

import 'core/network/api_client.dart';
import 'core/storage/secure_token_storage.dart';
import 'core/theme/app_theme.dart';
import 'repositories/repositories.dart';
import 'screens/app_shell.dart';
import 'screens/login_screen.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const EmployeeApp());
}

class EmployeeApp extends StatefulWidget {
  const EmployeeApp({super.key});

  @override
  State<EmployeeApp> createState() => _EmployeeAppState();
}

class _EmployeeAppState extends State<EmployeeApp> {
  late final SecureTokenStorage storage = SecureTokenStorage();
  late final ApiClient apiClient = ApiClient(storage: storage);
  late final AuthRepository authRepository = AuthRepository(
    apiClient: apiClient,
    storage: storage,
  );
  late final EmployeeRepository employeeRepository = EmployeeRepository(
    apiClient,
  );
  late final AttendanceRepository attendanceRepository = AttendanceRepository(
    apiClient,
  );
  late final LeaveRepository leaveRepository = LeaveRepository(apiClient);
  late final PayrollRepository payrollRepository = PayrollRepository(apiClient);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Swajit Engineering Employee',
      debugShowCheckedModeBanner: false,
      theme: buildAppTheme(),
      home: FutureBuilder<bool>(
        future: storage.hasSession(),
        builder: (context, snapshot) {
          if (snapshot.connectionState != ConnectionState.done) {
            return const Scaffold(
              body: Center(child: CircularProgressIndicator()),
            );
          }
          return snapshot.data == true
              ? AppShell(
                  authRepository: authRepository,
                  employeeRepository: employeeRepository,
                  attendanceRepository: attendanceRepository,
                  leaveRepository: leaveRepository,
                  payrollRepository: payrollRepository,
                )
              : WelcomeScreen(
                  onGetStarted: () {
                    Navigator.of(context).push(
                      MaterialPageRoute(
                        builder: (_) => LoginScreen(
                          authRepository: authRepository,
                          employeeRepository: employeeRepository,
                          attendanceRepository: attendanceRepository,
                          leaveRepository: leaveRepository,
                          payrollRepository: payrollRepository,
                        ),
                      ),
                    );
                  },
                );
        },
      ),
    );
  }
}
