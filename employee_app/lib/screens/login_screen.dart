import 'package:flutter/material.dart';

import '../core/theme/app_theme.dart';
import '../repositories/repositories.dart';
import 'app_shell.dart';

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({super.key, required this.onGetStarted});
  final VoidCallback onGetStarted;

  @override
  Widget build(BuildContext context) {
    final wide = MediaQuery.sizeOf(context).width >= 600;
    return Scaffold(
      body: PageBackground(
        child: SafeArea(
          child: SingleChildScrollView(
            padding: EdgeInsets.symmetric(
              horizontal: wide ? 56 : 22,
              vertical: 28,
            ),
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 860),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const BrandLogo(size: 50, showWordmark: true),
                  const SizedBox(height: 26),
                  Container(
                    constraints: const BoxConstraints(minHeight: 360),
                    padding: const EdgeInsets.all(28),
                    decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(28),
                      gradient: const LinearGradient(
                        colors: [Color(0xff173b4a), Color(0xff0b1b25)],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      ),
                      border: Border.all(color: AppColors.line),
                    ),
                    child: SizedBox(
                      height: 360,
                      child: Stack(
                        children: [
                          const Positioned(
                            right: -18,
                            top: -18,
                            child: Icon(
                              Icons.route_rounded,
                              size: 220,
                              color: Color(0x24169db3),
                            ),
                          ),
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            mainAxisAlignment: MainAxisAlignment.end,
                            children: [
                              const Eyebrow('E-LOGISTICS  /  EMPLOYEE WORKSPACE'),
                              const SizedBox(height: 12),
                              Text(
                                'Move the workday\nforward.',
                                style: Theme.of(context).textTheme.displaySmall
                                    ?.copyWith(
                                      color: Colors.white,
                                      fontWeight: FontWeight.w900,
                                      height: .98,
                                    ),
                              ),
                              const SizedBox(height: 14),
                              const Text(
                                'Verified attendance, employee services,\nand a clearer route through every shift.',
                                style: TextStyle(
                                  color: AppColors.muted,
                                  fontSize: 16,
                                  height: 1.4,
                                ),
                              ),
                              const SizedBox(height: 24),
                              FilledButton.icon(
                                onPressed: onGetStarted,
                                icon: const Icon(Icons.arrow_forward_rounded),
                                label: const Text('CONTINUE TO WORKSPACE'),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(height: 18),
                  const Row(
                    children: [
                      Expanded(
                        child: WelcomeFeature(
                          icon: Icons.gps_fixed_rounded,
                          title: 'VERIFIED',
                          detail: 'Photo + location attendance',
                        ),
                      ),
                      SizedBox(width: 10),
                      Expanded(
                        child: WelcomeFeature(
                          icon: Icons.bolt_rounded,
                          title: 'CONNECTED',
                          detail: 'Your workday in one place',
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class WelcomeFeature extends StatelessWidget {
  const WelcomeFeature({
    super.key,
    required this.icon,
    required this.title,
    required this.detail,
  });
  final IconData icon;
  final String title;
  final String detail;
  @override
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: const EdgeInsets.all(15),
      child: Row(
        children: [
          Icon(icon, color: AppColors.cyan, size: 24),
          const SizedBox(width: 10),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    fontWeight: FontWeight.w900,
                    fontSize: 11,
                    letterSpacing: 1,
                  ),
                ),
                const SizedBox(height: 3),
                Text(
                  detail,
                  style: const TextStyle(color: AppColors.muted, fontSize: 11),
                ),
              ],
            ),
          ),
        ],
      ),
    ),
  );
}

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
              accountPassword: _password.text,
            )
          : AppShell(
              authRepository: widget.authRepository,
              employeeRepository: widget.employeeRepository,
              attendanceRepository: widget.attendanceRepository,
              leaveRepository: widget.leaveRepository,
              payrollRepository: widget.payrollRepository,
              initialSession: session,
              accountPassword: _password.text,
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: PageBackground(
        child: SafeArea(
          child: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(22),
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 500),
                child: Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      const BrandLogo(size: 58, showWordmark: true),
                      const SizedBox(height: 36),
                      const Eyebrow('SECURE EMPLOYEE ACCESS'),
                      const SizedBox(height: 8),
                      Text(
                        'Welcome back.',
                        style: Theme.of(context).textTheme.headlineLarge,
                      ),
                      const SizedBox(height: 6),
                      const Text(
                        'Sign in to manage your shift, attendance, and employee services.',
                      ),
                      const SizedBox(height: 28),
                      Card(
                        child: Padding(
                          padding: const EdgeInsets.all(18),
                          child: Column(
                            children: [
                              if (_error != null) _ErrorBanner(_error!),
                              TextFormField(
                                controller: _employeeCode,
                                textCapitalization:
                                    TextCapitalization.characters,
                                decoration: const InputDecoration(
                                  labelText: 'Employee ID (optional)',
                                  prefixIcon: Icon(Icons.badge_outlined),
                                ),
                              ),
                              const SizedBox(height: 12),
                              TextFormField(
                                controller: _email,
                                keyboardType: TextInputType.emailAddress,
                                decoration: const InputDecoration(
                                  labelText: 'Work email',
                                  prefixIcon: Icon(
                                    Icons.alternate_email_rounded,
                                  ),
                                ),
                                validator: (value) =>
                                    value == null ||
                                        !RegExp(
                                          r'^[^@\s]+@[^@\s]+\.[^@\s]+$',
                                        ).hasMatch(value.trim())
                                    ? 'Enter a valid email address'
                                    : null,
                              ),
                              const SizedBox(height: 12),
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
                                      () =>
                                          _obscurePassword = !_obscurePassword,
                                    ),
                                    icon: Icon(
                                      _obscurePassword
                                          ? Icons.visibility_outlined
                                          : Icons.visibility_off_outlined,
                                    ),
                                  ),
                                ),
                                validator: (value) =>
                                    value == null || value.isEmpty
                                    ? 'Enter your password'
                                    : null,
                              ),
                              const SizedBox(height: 20),
                              FilledButton.icon(
                                onPressed: _loading ? null : _login,
                                icon: _loading
                                    ? const SizedBox(
                                        height: 20,
                                        width: 20,
                                        child: CircularProgressIndicator(
                                          strokeWidth: 2,
                                        ),
                                      )
                                    : const Icon(Icons.arrow_forward_rounded),
                                label: Text(
                                  _loading
                                      ? 'Connecting...'
                                      : 'Continue to workspace',
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                      const SizedBox(height: 18),
                      const Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.shield_outlined,
                            size: 16,
                            color: AppColors.success,
                          ),
                          SizedBox(width: 6),
                          Text(
                            'Protected employee workspace',
                            style: TextStyle(
                              color: AppColors.muted,
                              fontSize: 12,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
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
    decoration: BoxDecoration(
      color: AppColors.danger.withValues(alpha: .14),
      borderRadius: BorderRadius.circular(12),
      border: Border.all(color: AppColors.danger.withValues(alpha: .35)),
    ),
    child: Text(message, style: const TextStyle(color: Color(0xffffa4a4))),
  );
}
