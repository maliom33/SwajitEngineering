import 'package:flutter/material.dart';

import 'core/network/api_client.dart';
import 'core/storage/secure_token_storage.dart';
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
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xff0d5c63)),
        scaffoldBackgroundColor: const Color(0xfff4f7f6),
        useMaterial3: true,
        cardTheme: const CardThemeData(
          margin: EdgeInsets.zero,
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.all(Radius.circular(18)),
          ),
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: Colors.white,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(14),
            borderSide: BorderSide.none,
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(14),
            borderSide: const BorderSide(color: Color(0xffd9e5e2)),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(14),
            borderSide: const BorderSide(color: Color(0xff0d5c63), width: 2),
          ),
          contentPadding: const EdgeInsets.symmetric(
            horizontal: 16,
            vertical: 16,
          ),
        ),
        filledButtonTheme: FilledButtonThemeData(
          style: FilledButton.styleFrom(
            minimumSize: const Size.fromHeight(52),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(14),
            ),
          ),
        ),
      ),
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
              : LoginScreen(
                  authRepository: authRepository,
                  employeeRepository: employeeRepository,
                  attendanceRepository: attendanceRepository,
                  leaveRepository: leaveRepository,
                  payrollRepository: payrollRepository,
                );
        },
      ),
    );
  }
}
