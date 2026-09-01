import 'package:flutter/material.dart';

import '../repositories/repositories.dart';
import 'app_shell.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({
    super.key,
    required this.authRepository,
    required this.employeeRepository,
    required this.attendanceRepository,
    required this.leaveRepository,
    required this.payrollRepository,
  });

  final AuthRepository authRepository;
  final EmployeeRepository employeeRepository;
  final AttendanceRepository attendanceRepository;
  final LeaveRepository leaveRepository;
  final PayrollRepository payrollRepository;

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _email = TextEditingController();
  final _employeeCode = TextEditingController();
  final _password = TextEditingController();
  bool _loading = false;
  bool _resending = false;
  bool _obscurePassword = true;
  String? _error;

  @override
  void dispose() {
    _email.dispose();
    _employeeCode.dispose();
    _password.dispose();
    super.dispose();
  }

  Future<void> _login() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final session = await widget.authRepository.login(
        _email.text.trim(),
        _password.text,
      );
      if (!mounted) return;
      if (session.roleCode != 'EMPLOYEE' || session.employee == null) {
        await widget.authRepository.logout();
        setState(
          () => _error = 'This application is available for employees only.',
        );
        return;
      }
      final destination = session.isFirstLogin || !session.profileComplete
          ? ProfileSetupPage(
              authRepository: widget.authRepository,
              employeeRepository: widget.employeeRepository,
              attendanceRepository: widget.attendanceRepository,
              leaveRepository: widget.leaveRepository,
              payrollRepository: widget.payrollRepository,
              initialSession: session,
            )
          : AppShell(
              authRepository: widget.authRepository,
              employeeRepository: widget.employeeRepository,
              attendanceRepository: widget.attendanceRepository,
              leaveRepository: widget.leaveRepository,
              payrollRepository: widget.payrollRepository,
              initialSession: session,
            );
      Navigator.of(
        context,
      ).pushReplacement(MaterialPageRoute(builder: (_) => destination));
    } catch (error) {
      if (mounted) setState(() => _error = userMessage(error));
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  Future<void> _resendVerification() async {
    if (_email.text.trim().isEmpty || _employeeCode.text.trim().isEmpty) {
      setState(
        () => _error =
            'Enter your email and Employee ID to resend the verification link.',
      );
      return;
    }
    setState(() {
      _resending = true;
      _error = null;
    });
    try {
      await widget.employeeRepository.requestEmailVerification(
        email: _email.text.trim(),
        employeeCode: _employeeCode.text.trim(),
      );
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text(
              'If the account is eligible, a verification link has been sent.',
            ),
          ),
        );
      }
    } catch (error) {
      if (mounted) setState(() => _error = userMessage(error));
    } finally {
      if (mounted) setState(() => _resending = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 430),
              child: Form(
                key: _formKey,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Container(
                      width: 76,
                      height: 76,
                      decoration: BoxDecoration(
                        color: theme.colorScheme.primaryContainer,
                        borderRadius: BorderRadius.circular(22),
                      ),
                      child: Icon(
                        Icons.badge_outlined,
                        size: 42,
                        color: theme.colorScheme.primary,
                      ),
                    ),
                    const SizedBox(height: 20),
                    Text(
                      'Swajit Engineering',
                      style: theme.textTheme.headlineSmall?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    Text(
                      'Employee workspace',
                      style: theme.textTheme.titleMedium?.copyWith(
                        color: theme.colorScheme.primary,
                      ),
                    ),
                    const SizedBox(height: 8),
                    const Text(
                      'Sign in securely with your Django employee account.',
                    ),
                    const SizedBox(height: 32),
                    if (_error != null) _ErrorBanner(_error!),
                    TextFormField(
                      controller: _employeeCode,
                      textCapitalization: TextCapitalization.characters,
                      decoration: const InputDecoration(
                        labelText: 'Employee ID (optional)',
                        prefixIcon: Icon(Icons.badge_outlined),
                      ),
                    ),
                    const SizedBox(height: 16),
                    TextFormField(
                      controller: _email,
                      keyboardType: TextInputType.emailAddress,
                      decoration: const InputDecoration(
                        labelText: 'Email',
                        prefixIcon: Icon(Icons.email_outlined),
                      ),
                      validator: (value) =>
                          value == null ||
                              !RegExp(
                                r'^[^@\s]+@[^@\s]+\.[^@\s]+$',
                              ).hasMatch(value.trim())
                          ? 'Enter a valid email address'
                          : null,
                    ),
                    const SizedBox(height: 16),
                    TextFormField(
                      controller: _password,
                      obscureText: _obscurePassword,
                      decoration: InputDecoration(
                        labelText: 'Password',
                        prefixIcon: const Icon(Icons.lock_outline),
                        suffixIcon: IconButton(
                          tooltip: _obscurePassword
                              ? 'Show password'
                              : 'Hide password',
                          onPressed: () => setState(
                            () => _obscurePassword = !_obscurePassword,
                          ),
                          icon: Icon(
                            _obscurePassword
                                ? Icons.visibility_outlined
                                : Icons.visibility_off_outlined,
                          ),
                        ),
                      ),
                      validator: (value) => value == null || value.isEmpty
                          ? 'Enter your password'
                          : null,
                    ),
                    const SizedBox(height: 24),
                    FilledButton.icon(
                      onPressed: _loading ? null : _login,
                      icon: _loading
                          ? const SizedBox(
                              height: 20,
                              width: 20,
                              child: CircularProgressIndicator(strokeWidth: 2),
                            )
                          : const Icon(Icons.login_outlined),
                      label: _loading
                          ? const Text('Signing in...')
                          : const Text('Sign in'),
                    ),
                    const SizedBox(height: 16),
                    OutlinedButton.icon(
                      onPressed: _resending ? null : _resendVerification,
                      icon: _resending
                          ? const SizedBox(
                              height: 18,
                              width: 18,
                              child: CircularProgressIndicator(strokeWidth: 2),
                            )
                          : const Icon(Icons.mark_email_unread_outlined),
                      label: const Text('Resend verification email'),
                    ),
                    const SizedBox(height: 12),
                    const Text(
                      'Email verification is required before employee login.',
                      textAlign: TextAlign.center,
                      style: TextStyle(color: Colors.black54),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _ErrorBanner extends StatelessWidget {
  const _ErrorBanner(this.message);
  final String message;
  @override
  Widget build(BuildContext context) => Container(
    margin: const EdgeInsets.only(bottom: 16),
    padding: const EdgeInsets.all(12),
    color: Colors.red.shade50,
    child: Text(message, style: TextStyle(color: Colors.red.shade800)),
  );
}
