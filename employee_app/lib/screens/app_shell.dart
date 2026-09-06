import 'dart:io';
import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';

import '../models/models.dart';
import '../repositories/repositories.dart';
import '../services/face_recognition_service.dart';
import 'login_screen.dart';

class AppShell extends StatefulWidget {
  const AppShell({
    super.key,
    required this.authRepository,
    required this.employeeRepository,
    required this.attendanceRepository,
    required this.leaveRepository,
    required this.payrollRepository,
    this.initialSession,
  });

  final AuthRepository authRepository;
  final EmployeeRepository employeeRepository;
  final AttendanceRepository attendanceRepository;
  final LeaveRepository leaveRepository;
  final PayrollRepository payrollRepository;
  final UserSession? initialSession;

  @override
  State<AppShell> createState() => _AppShellState();
}

class ProfileSetupPage extends StatefulWidget {
  const ProfileSetupPage({
    super.key,
    required this.authRepository,
    required this.employeeRepository,
    required this.attendanceRepository,
    required this.leaveRepository,
    required this.payrollRepository,
    required this.initialSession,
  });
  final AuthRepository authRepository;
  final EmployeeRepository employeeRepository;
  final AttendanceRepository attendanceRepository;
  final LeaveRepository leaveRepository;
  final PayrollRepository payrollRepository;
  final UserSession initialSession;
  @override
  State<ProfileSetupPage> createState() => _ProfileSetupPageState();
}

class _ProfileSetupPageState extends State<ProfileSetupPage> {
  final form = GlobalKey<FormState>();
  final profileForm = GlobalKey<FormState>();
  final current = TextEditingController();
  final next = TextEditingController();
  final confirm = TextEditingController();
  final firstName = TextEditingController();
  final lastName = TextEditingController();
  final email = TextEditingController();
  final phone = TextEditingController();
  final gender = TextEditingController();
  final address = TextEditingController();
  final city = TextEditingController();
  final state = TextEditingController();
  final pincode = TextEditingController();
  String? message;
  bool loading = false;
  final cameraService = FaceCameraService();
  String? localPhotoPath;
  String? currentPhotoUrl;
  bool emailVerified = false;

  @override
  void initState() {
    super.initState();
    emailVerified = widget.initialSession.emailVerified;
    final employee = widget.initialSession.employee!;
    firstName.text = employee.firstName;
    lastName.text = employee.lastName;
    email.text = employee.email;
    phone.text = employee.phone;
    gender.text = employee.gender;
    currentPhotoUrl = employee.profilePhotoUrl.isNotEmpty
        ? employee.profilePhotoUrl
        : null;
  }

  @override
  void dispose() {
    cameraService.close();
    current.dispose();
    next.dispose();
    confirm.dispose();
    firstName.dispose();
    lastName.dispose();
    email.dispose();
    phone.dispose();
    gender.dispose();
    address.dispose();
    city.dispose();
    state.dispose();
    pincode.dispose();
    super.dispose();
  }

  Future<void> savePassword() async {
    if (!form.currentState!.validate()) return;
    setState(() {
      loading = true;
      message = null;
    });
    try {
      await widget.employeeRepository.changePassword(
        currentPassword: current.text,
        newPassword: next.text,
        confirmPassword: confirm.text,
      );
      if (mounted) {
        setState(
          () => message =
              'Password changed. Check your email and open the verification link before logging in.',
        );
      }
    } catch (error) {
      if (mounted) setState(() => message = userMessage(error));
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  Future<void> saveProfile() async {
    if (!profileForm.currentState!.validate()) return;
    setState(() {
      loading = true;
      message = null;
    });
    try {
      await widget.employeeRepository.updateProfile(
        employeeId: widget.initialSession.employee!.employeeId,
        firstName: firstName.text.trim(),
        lastName: lastName.text.trim(),
        email: email.text.trim(),
        phone: phone.text.trim(),
        gender: gender.text.trim(),
        address: address.text.trim(),
        city: city.text.trim(),
        state: state.text.trim(),
        pincode: pincode.text.trim(),
      );
      final refreshed = await widget.authRepository.me();
      if (mounted) {
        final employee = refreshed.employee;
        final missing = _missingProfileFields(
          employee,
          refreshed.emailVerified,
        );
        setState(() {
          emailVerified = refreshed.emailVerified;
          currentPhotoUrl = employee?.profilePhotoUrl.isNotEmpty == true
              ? employee!.profilePhotoUrl
              : currentPhotoUrl;
          message = refreshed.profileComplete
              ? 'Profile completed. You can now mark attendance.'
              : 'Profile saved. Complete all required fields before marking attendance.';
          if (missing.isNotEmpty) {
            message = '${message!}\nMissing: ${missing.join(', ')}';
          }
        });
      }
    } catch (error) {
      if (mounted) setState(() => message = userMessage(error));
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  Future<void> capturePhoto() async {
    setState(() {
      loading = true;
      message = null;
    });
    try {
      await cameraService.initialize();
      final result = await cameraService.captureAndDetect();
      if (!result.isSuitable) {
        if (mounted) setState(() => message = result.message);
        return;
      }
      await widget.employeeRepository.uploadPhoto(
        widget.initialSession.employee!.employeeId,
        result.imagePath,
      );
      final refreshed = await widget.authRepository.me();
      if (mounted) {
        final employee = refreshed.employee;
        setState(() {
          localPhotoPath = result.imagePath;
          currentPhotoUrl = employee?.profilePhotoUrl.isNotEmpty == true
              ? employee!.profilePhotoUrl
              : null;
          message = refreshed.profileComplete
              ? 'Profile photo saved. Profile completed. You can now mark attendance.'
              : 'Profile photo saved. Complete all required fields before marking attendance.';
        });
      }
    } catch (error) {
      if (mounted) setState(() => message = userMessage(error));
    } finally {
      await cameraService.dispose();
      if (mounted) setState(() => loading = false);
    }
  }

  List<String> _missingProfileFields(Employee? employee, bool emailVerified) {
    if (employee == null) return const ['profile info'];
    final missing = <String>[];
    if (employee.firstName.trim().isEmpty) missing.add('First name');
    if (employee.lastName.trim().isEmpty) missing.add('Last name');
    if (employee.email.trim().isEmpty) missing.add('Email');
    if (employee.phone.trim().isEmpty) missing.add('Phone');
    if (employee.gender.trim().isEmpty) missing.add('Gender');
    if (employee.departmentName.trim().isEmpty) missing.add('Department');
    if (employee.designationName.trim().isEmpty) missing.add('Designation');
    if (!emailVerified) missing.add('Email verification');
    if (employee.profilePhotoUrl.trim().isEmpty &&
        (localPhotoPath == null || localPhotoPath!.trim().isEmpty)) {
      missing.add('Profile photo');
    }
    return missing;
  }

  Widget _requirementRow(String title, bool complete) => Row(
    children: [
      Icon(
        complete ? Icons.check_circle : Icons.warning_amber_rounded,
        color: complete ? Colors.green : Colors.orange,
      ),
      const SizedBox(width: 12),
      Expanded(
        child: Text(
          title,
          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
            color: complete ? Colors.green : Colors.orange,
            fontWeight: FontWeight.w600,
          ),
        ),
      ),
      Text(
        complete ? '✓ Completed' : '⚠ Required',
        style: Theme.of(context).textTheme.labelMedium?.copyWith(
          color: complete ? Colors.green : Colors.orange,
        ),
      ),
    ],
  );

  Future<void> requestEmailVerification() async {
    setState(() {
      loading = true;
      message = null;
    });
    try {
      await widget.employeeRepository.requestEmailVerification();
      if (mounted) {
        setState(
          () => message =
              'Verification link sent. Please check your email and open the link to verify your account.',
        );
      }
    } catch (error) {
      if (mounted) setState(() => message = userMessage(error));
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  Future<void> refreshVerificationStatus() async {
    setState(() {
      loading = true;
      message = null;
    });
    try {
      final session = await widget.authRepository.me();
      if (mounted) {
        setState(() {
          emailVerified = session.emailVerified;
          message = emailVerified
              ? 'Email verified successfully. You can now log in.'
              : 'Your email is still pending verification.';
        });
      }
    } catch (error) {
      if (mounted) setState(() => message = userMessage(error));
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final requiredFields = _missingProfileFields(
      widget.initialSession.employee,
      emailVerified,
    );
    final employee = widget.initialSession.employee!;
    return Scaffold(
      appBar: AppBar(title: const Text('Complete Your Profile')),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Text(
            'Your account was created by HR. Complete the required steps before using employee services.',
            style: Theme.of(context).textTheme.bodyLarge,
          ),
          const SizedBox(height: 20),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Profile completion status',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 12),
                  ...[
                    _requirementRow(
                      'First name',
                      employee.firstName.trim().isNotEmpty,
                    ),
                    _requirementRow(
                      'Last name',
                      employee.lastName.trim().isNotEmpty,
                    ),
                    _requirementRow('Email', employee.email.trim().isNotEmpty),
                    _requirementRow('Phone', employee.phone.trim().isNotEmpty),
                    _requirementRow(
                      'Gender',
                      employee.gender.trim().isNotEmpty,
                    ),
                    _requirementRow(
                      'Department',
                      employee.departmentName.trim().isNotEmpty,
                    ),
                    _requirementRow(
                      'Designation',
                      employee.designationName.trim().isNotEmpty,
                    ),
                    _requirementRow('Email verification', emailVerified),
                    _requirementRow(
                      'Profile photo',
                      (currentPhotoUrl != null &&
                              currentPhotoUrl!.trim().isNotEmpty) ||
                          (localPhotoPath != null &&
                              localPhotoPath!.trim().isNotEmpty),
                    ),
                  ].expand((widget) => [widget, const SizedBox(height: 10)]),
                ],
              ),
            ),
          ),
          const SizedBox(height: 20),
          StatusPanel(
            title: 'Account verification',
            value: emailVerified ? 'Email Verified' : 'Pending',
            icon: emailVerified
                ? Icons.verified
                : Icons.mark_email_unread_outlined,
            color: emailVerified ? Colors.green : Colors.orange,
            detail: emailVerified
                ? 'Your email has been successfully verified.'
                : 'Please check your email and click the verification link to verify your account.',
          ),
          if (!emailVerified)
            Row(
              children: [
                Expanded(
                  child: FilledButton.icon(
                    onPressed: loading ? null : requestEmailVerification,
                    icon: const Icon(Icons.email_outlined),
                    label: const Text('Resend link'),
                  ),
                ),
                const SizedBox(width: 10),
                IconButton.filledTonal(
                  tooltip: 'Check verification status',
                  onPressed: loading ? null : refreshVerificationStatus,
                  icon: const Icon(Icons.refresh),
                ),
              ],
            ),
          StatusPanel(
            title: 'Employment status',
            value: widget.initialSession.employee!.status,
            icon: Icons.work_outline,
            color: statusColor(widget.initialSession.employee!.status),
            detail: statusDescription(widget.initialSession.employee!.status),
          ),
          ListTile(
            leading: const Icon(Icons.phone_android_outlined),
            title: const Text('Mobile number'),
            subtitle: Text(
              widget.initialSession.employee!.phone.isEmpty
                  ? 'No mobile number is registered.'
                  : widget.initialSession.employee!.phone,
            ),
          ),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Form(
                key: profileForm,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Text(
                      'Profile information',
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 4),
                    const Text(
                      'Complete the required fields before marking attendance.',
                    ),
                    const SizedBox(height: 16),
                    TextFormField(
                      controller: firstName,
                      decoration: const InputDecoration(
                        labelText: 'First name',
                      ),
                      validator: requiredField,
                    ),
                    const SizedBox(height: 12),
                    TextFormField(
                      controller: lastName,
                      decoration: const InputDecoration(labelText: 'Last name'),
                      validator: requiredField,
                    ),
                    const SizedBox(height: 12),
                    TextFormField(
                      controller: email,
                      keyboardType: TextInputType.emailAddress,
                      decoration: const InputDecoration(labelText: 'Email'),
                      validator: emailField,
                    ),
                    const SizedBox(height: 12),
                    TextFormField(
                      controller: phone,
                      keyboardType: TextInputType.phone,
                      decoration: const InputDecoration(
                        labelText: 'Mobile number',
                        helperText:
                            '+91XXXXXXXXXX or 10-digit Indian mobile number',
                      ),
                      validator: phoneField,
                    ),
                    const SizedBox(height: 12),
                    DropdownButtonFormField<String>(
                      initialValue:
                          const [
                            'Male',
                            'Female',
                            'Other',
                            'Prefer not to say',
                          ].contains(gender.text)
                          ? gender.text
                          : null,
                      decoration: const InputDecoration(labelText: 'Gender'),
                      items:
                          const ['Male', 'Female', 'Other', 'Prefer not to say']
                              .map(
                                (value) => DropdownMenuItem(
                                  value: value,
                                  child: Text(value),
                                ),
                              )
                              .toList(),
                      onChanged: (value) => gender.text = value ?? '',
                      validator: requiredField,
                    ),
                    const SizedBox(height: 12),
                    TextFormField(
                      controller: address,
                      decoration: const InputDecoration(
                        labelText: 'Address (optional)',
                      ),
                      maxLines: 2,
                    ),
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        Expanded(
                          child: TextFormField(
                            controller: city,
                            decoration: const InputDecoration(
                              labelText: 'City (optional)',
                            ),
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: TextFormField(
                            controller: state,
                            decoration: const InputDecoration(
                              labelText: 'State (optional)',
                            ),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    TextFormField(
                      controller: pincode,
                      keyboardType: TextInputType.number,
                      decoration: const InputDecoration(
                        labelText: 'Pincode (optional)',
                      ),
                    ),
                    const SizedBox(height: 16),
                    FilledButton.icon(
                      onPressed: loading ? null : saveProfile,
                      icon: const Icon(Icons.save_outlined),
                      label: const Text('Save profile'),
                    ),
                  ],
                ),
              ),
            ),
          ),
          const SizedBox(height: 16),
          Form(
            key: form,
            child: Column(
              children: [
                TextFormField(
                  controller: current,
                  obscureText: true,
                  decoration: const InputDecoration(
                    labelText: 'Current password',
                  ),
                  validator: (value) => value == null || value.isEmpty
                      ? 'Enter current password'
                      : null,
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: next,
                  obscureText: true,
                  decoration: const InputDecoration(labelText: 'New password'),
                  validator: (value) => value == null || value.length < 8
                      ? 'Use at least 8 characters'
                      : null,
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: confirm,
                  obscureText: true,
                  decoration: const InputDecoration(
                    labelText: 'Confirm new password',
                  ),
                  validator: (value) =>
                      value != next.text ? 'Passwords do not match' : null,
                ),
                const SizedBox(height: 16),
                FilledButton(
                  onPressed: loading ? null : savePassword,
                  child: Text(loading ? 'Saving...' : 'Change password'),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Text(
                    'Profile photo',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 12),
                  if ((currentPhotoUrl != null &&
                          currentPhotoUrl!.trim().isNotEmpty) ||
                      (localPhotoPath != null &&
                          localPhotoPath!.trim().isNotEmpty))
                    ClipRRect(
                      borderRadius: BorderRadius.circular(12),
                      child:
                          (localPhotoPath != null &&
                              localPhotoPath!.trim().isNotEmpty)
                          ? Image.file(
                              File(localPhotoPath!),
                              height: 220,
                              fit: BoxFit.cover,
                            )
                          : Image.network(
                              currentPhotoUrl!,
                              height: 220,
                              fit: BoxFit.cover,
                              errorBuilder: (context, error, stackTrace) =>
                                  const SizedBox(
                                    height: 220,
                                    child: Center(
                                      child: Icon(
                                        Icons.image_not_supported_outlined,
                                      ),
                                    ),
                                  ),
                            ),
                    )
                  else
                    Container(
                      height: 220,
                      decoration: BoxDecoration(
                        color: Theme.of(
                          context,
                        ).colorScheme.surfaceContainerHighest,
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: const Center(
                        child: Icon(Icons.person_outline, size: 56),
                      ),
                    ),
                  const SizedBox(height: 12),
                  FilledButton.icon(
                    onPressed: loading ? null : capturePhoto,
                    icon: const Icon(Icons.camera_alt_outlined),
                    label: Text(
                      (currentPhotoUrl != null &&
                                  currentPhotoUrl!.trim().isNotEmpty) ||
                              (localPhotoPath != null &&
                                  localPhotoPath!.trim().isNotEmpty)
                          ? 'Replace profile photo'
                          : 'Register profile photo',
                    ),
                  ),
                ],
              ),
            ),
          ),
          if (message != null)
            Padding(
              padding: const EdgeInsets.only(top: 16),
              child: Text(message!),
            ),
          if (requiredFields.isNotEmpty)
            Padding(
              padding: const EdgeInsets.only(top: 16),
              child: Text(
                'Missing required fields: ${requiredFields.join(', ')}',
                style: Theme.of(
                  context,
                ).textTheme.bodyMedium?.copyWith(color: Colors.orange.shade900),
              ),
            ),
        ],
      ),
    );
  }
}

class _AppShellState extends State<AppShell> {
  int selectedTab = 0;
  UserSession? session;
  String? error;

  Future<String> _refreshSession() async {
    final refreshed = await widget.authRepository.me();
    if (mounted) setState(() => session = refreshed);
    return refreshed.employee?.status ?? '';
  }

  Future<void> _openProfileSetup() async {
    final currentSession = await widget.authRepository.me();
    if (!mounted || currentSession.employee == null) return;
    await Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => ProfileSetupPage(
          authRepository: widget.authRepository,
          employeeRepository: widget.employeeRepository,
          attendanceRepository: widget.attendanceRepository,
          leaveRepository: widget.leaveRepository,
          payrollRepository: widget.payrollRepository,
          initialSession: currentSession,
        ),
      ),
    );
    await _refreshSession();
  }

  @override
  void initState() {
    super.initState();
    session = widget.initialSession;
    if (session == null) _loadSession();
  }

  Future<void> _loadSession() async {
    try {
      final value = await widget.authRepository.me();
      if (!mounted) return;
      if (value.roleCode != 'EMPLOYEE' || value.employee == null) {
        await widget.authRepository.logout();
        setState(
          () => error = 'This application is available for employees only.',
        );
      } else {
        setState(() => session = value);
      }
    } catch (exception) {
      if (mounted) setState(() => error = userMessage(exception));
    }
  }

  Future<void> _logout() async {
    await widget.authRepository.logout();
    if (!mounted) return;
    Navigator.of(context).pushAndRemoveUntil(
      MaterialPageRoute(
        builder: (_) => LoginScreen(
          authRepository: widget.authRepository,
          employeeRepository: widget.employeeRepository,
          attendanceRepository: widget.attendanceRepository,
          leaveRepository: widget.leaveRepository,
          payrollRepository: widget.payrollRepository,
        ),
      ),
      (_) => false,
    );
  }

  @override
  Widget build(BuildContext context) {
    if (error != null) return Scaffold(body: Center(child: Text(error!)));
    final employee = session?.employee;
    if (employee == null) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }
    final pages = <Widget>[
      DashboardPage(
        employee: employee,
        emailVerified: session?.emailVerified ?? false,
        attendanceRepository: widget.attendanceRepository,
        leaveRepository: widget.leaveRepository,
      ),
      AttendancePage(
        repository: widget.attendanceRepository,
        faceRecognitionService: PendingFaceRecognitionService(),
        onAttendanceRecorded: _refreshSession,
        employeeStatus: employee.status,
        profileComplete: employee.profileComplete,
        onCompleteProfile: _openProfileSetup,
      ),
      LeavePage(repository: widget.leaveRepository),
      PayrollPage(repository: widget.payrollRepository),
      ProfilePage(
        employee: employee,
        emailVerified: session?.emailVerified ?? false,
      ),
    ];
    return Scaffold(
      appBar: AppBar(
        title: const Text('Employee Portal'),
        actions: [
          IconButton(onPressed: _logout, icon: const Icon(Icons.logout)),
        ],
      ),
      body: pages[selectedTab],
      bottomNavigationBar: NavigationBar(
        selectedIndex: selectedTab,
        onDestinationSelected: (value) => setState(() => selectedTab = value),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), label: 'Home'),
          NavigationDestination(
            icon: Icon(Icons.schedule_outlined),
            label: 'Attendance',
          ),
          NavigationDestination(
            icon: Icon(Icons.event_note_outlined),
            label: 'Leave',
          ),
          NavigationDestination(
            icon: Icon(Icons.payments_outlined),
            label: 'Payroll',
          ),
          NavigationDestination(
            icon: Icon(Icons.person_outline),
            label: 'Profile',
          ),
        ],
      ),
    );
  }
}

class DashboardPage extends StatefulWidget {
  const DashboardPage({
    super.key,
    required this.employee,
    required this.emailVerified,
    required this.attendanceRepository,
    required this.leaveRepository,
  });
  final Employee employee;
  final bool emailVerified;
  final AttendanceRepository attendanceRepository;
  final LeaveRepository leaveRepository;

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  late Future<(List<AttendanceRecord>, List<LeaveRequest>)> summary;

  @override
  void initState() {
    super.initState();
    summary =
        Future.wait<Object>([
          widget.attendanceRepository.list(),
          widget.leaveRepository.requests(),
        ]).then(
          (values) => (
            values[0] as List<AttendanceRecord>,
            values[1] as List<LeaveRequest>,
          ),
        );
  }

  @override
  Widget build(BuildContext context) => ListView(
    padding: const EdgeInsets.all(20),
    children: [
      Text(
        'Welcome, ${widget.employee.firstName}',
        style: Theme.of(
          context,
        ).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
      ),
      const SizedBox(height: 8),
      const Text('Your employee workspace'),
      const SizedBox(height: 24),
      LifecycleStatusCard(
        emailVerified: widget.emailVerified,
        employmentStatus: widget.employee.status,
      ),
      const SizedBox(height: 12),
      InfoCard(
        label: 'Employee ID',
        value: widget.employee.employeeCode,
        icon: Icons.badge_outlined,
      ),
      InfoCard(
        label: 'Department',
        value: widget.employee.departmentName,
        icon: Icons.apartment_outlined,
      ),
      InfoCard(
        label: 'Designation',
        value: widget.employee.designationName,
        icon: Icons.work_outline,
      ),
      FutureBuilder<(List<AttendanceRecord>, List<LeaveRequest>)>(
        future: summary,
        builder: (context, snapshot) {
          if (snapshot.hasError) return Text(userMessage(snapshot.error!));
          if (!snapshot.hasData) {
            return const Padding(
              padding: EdgeInsets.all(16),
              child: Center(child: CircularProgressIndicator()),
            );
          }
          final attendance = snapshot.data!.$1;
          final leaves = snapshot.data!.$2;
          final present = attendance
              .where(
                (record) =>
                    record.status == 'PRESENT' ||
                    record.status == 'LATE' ||
                    record.status == 'HALF_DAY',
              )
              .length;
          final pending = leaves
              .where((request) => request.status == 'PENDING')
              .length;
          return Column(
            children: [
              InfoCard(
                label: 'Attendance records',
                value: '$present present of ${attendance.length}',
                icon: Icons.schedule_outlined,
              ),
              InfoCard(
                label: 'Pending leave requests',
                value: '$pending',
                icon: Icons.event_note_outlined,
              ),
            ],
          );
        },
      ),
    ],
  );
}

class InfoCard extends StatelessWidget {
  const InfoCard({
    super.key,
    required this.label,
    required this.value,
    required this.icon,
  });
  final String label;
  final String value;
  final IconData icon;

  @override
  Widget build(BuildContext context) => Card(
    child: ListTile(
      leading: Icon(icon, color: const Color(0xff0d5c63)),
      title: Text(label),
      subtitle: Text(
        value,
        style: const TextStyle(fontWeight: FontWeight.bold),
      ),
    ),
  );
}

class StatusPanel extends StatelessWidget {
  const StatusPanel({
    super.key,
    required this.title,
    required this.value,
    required this.icon,
    required this.color,
    required this.detail,
  });
  final String title;
  final String value;
  final IconData icon;
  final Color color;
  final String detail;

  @override
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: const EdgeInsets.all(16),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: color, size: 28),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: Theme.of(context).textTheme.labelLarge),
                const SizedBox(height: 4),
                Text(
                  value,
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    color: color,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 4),
                Text(detail, style: Theme.of(context).textTheme.bodySmall),
              ],
            ),
          ),
        ],
      ),
    ),
  );
}

String? requiredField(String? value) =>
    value == null || value.trim().isEmpty ? 'This field is required' : null;

String? emailField(String? value) =>
    value == null ||
        !RegExp(r'^[^@\s]+@[^@\s]+\.[^@\s]+$').hasMatch(value.trim())
    ? 'Enter a valid email address'
    : null;

String? phoneField(String? value) {
  final digits = value?.replaceAll(RegExp(r'\D'), '') ?? '';
  final normalized = digits.startsWith('91') && digits.length == 12
      ? digits.substring(2)
      : digits;
  return normalized.length == 10 && '6789'.contains(normalized[0])
      ? null
      : 'Enter a valid Indian mobile number';
}

Color statusColor(String status) => switch (status) {
  'ACTIVE' => Colors.green,
  'ON_LEAVE' => Colors.orange,
  'RESIGNED' || 'TERMINATED' => Colors.red,
  _ => Colors.blueGrey,
};

String statusDescription(String status) => switch (status) {
  'ACTIVE' => 'Your employee account is active and attendance has started.',
  'ON_LEAVE' => 'Your employment record is currently marked as on leave.',
  'RESIGNED' => 'Your employment record is marked as resigned.',
  'TERMINATED' => 'Your employment record is marked as terminated.',
  _ => 'Your first successful attendance will activate your employee status.',
};

class LifecycleStatusCard extends StatelessWidget {
  const LifecycleStatusCard({
    super.key,
    required this.emailVerified,
    required this.employmentStatus,
  });
  final bool emailVerified;
  final String employmentStatus;

  @override
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text(
            'Account lifecycle',
            style: Theme.of(
              context,
            ).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 12),
          ListTile(
            contentPadding: EdgeInsets.zero,
            leading: Icon(
              emailVerified ? Icons.verified : Icons.mark_email_unread_outlined,
              color: emailVerified ? Colors.green : Colors.orange,
            ),
            title: const Text('Email verification'),
            subtitle: Text(emailVerified ? 'Verified' : 'Not verified'),
          ),
          ListTile(
            contentPadding: EdgeInsets.zero,
            leading: const Icon(Icons.work_outline),
            title: const Text('Employment status'),
            subtitle: Text(employmentStatus),
          ),
          if (emailVerified && employmentStatus == 'INACTIVE')
            const Text(
              'Your account is verified. Your first successful attendance will activate your employee status.',
            ),
        ],
      ),
    ),
  );
}

class AttendancePage extends StatefulWidget {
  const AttendancePage({
    super.key,
    required this.repository,
    required this.faceRecognitionService,
    this.onAttendanceRecorded,
    required this.employeeStatus,
    required this.profileComplete,
    required this.onCompleteProfile,
  });
  final AttendanceRepository repository;
  final FaceRecognitionService faceRecognitionService;
  final Future<String> Function()? onAttendanceRecorded;
  final String employeeStatus;
  final bool profileComplete;
  final Future<void> Function() onCompleteProfile;
  @override
  State<AttendancePage> createState() => _AttendancePageState();
}

class _AttendancePageState extends State<AttendancePage> {
  late Future<List<AttendanceRecord>> future;
  final cameraService = FaceCameraService();
  final locationService = AttendanceLocationService();
  bool processing = false;
  String? captureMessage;
  String? capturedPhotoPath;
  Position? capturedPosition;
  @override
  void initState() {
    super.initState();
    future = widget.repository.list();
  }

  @override
  void dispose() {
    cameraService.close();
    super.dispose();
  }

  Future<void> captureFace() async {
    setState(() {
      processing = true;
      captureMessage = null;
      capturedPhotoPath = null;
      capturedPosition = null;
    });
    try {
      await cameraService.initialize();
      final result = await cameraService.captureAndDetect();
      if (!result.isSuitable) {
        if (mounted) setState(() => captureMessage = result.message);
        return;
      }
      if (mounted) {
        setState(() {
          capturedPhotoPath = result.imagePath;
          captureMessage = 'Photo captured. Getting your current location...';
        });
      }
      final position = await locationService.currentPosition();
      if (mounted) {
        setState(() {
          capturedPosition = position;
          captureMessage = 'Photo and location captured successfully.';
        });
      }
    } catch (exception) {
      if (mounted) setState(() => captureMessage = userMessage(exception));
    } finally {
      await cameraService.dispose();
      if (mounted) setState(() => processing = false);
    }
  }

  Future<void> submitAttendance() async {
    final photoPath = capturedPhotoPath;
    final position = capturedPosition;
    if (photoPath == null || position == null) return;
    setState(() {
      processing = true;
      captureMessage = null;
    });
    try {
      await widget.repository.submit(
        photoPath: photoPath,
        latitude: position.latitude,
        longitude: position.longitude,
      );
      final refreshedStatus = await widget.onAttendanceRecorded?.call();
      if (mounted) {
        setState(() {
          capturedPhotoPath = null;
          capturedPosition = null;
          captureMessage = refreshedStatus == 'ACTIVE'
              ? 'Attendance marked successfully. Your employee account is now ACTIVE.'
              : 'Attendance submitted successfully.';
          future = widget.repository.list();
        });
      }
    } catch (exception) {
      if (mounted) setState(() => captureMessage = userMessage(exception));
    } finally {
      if (mounted) setState(() => processing = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return DataPage(
      title: 'My Attendance',
      future: future,
      empty: 'No attendance records found.',
      header: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const Text(
            'Capture a photo and your current location before confirming attendance.',
          ),
          if (widget.employeeStatus == 'INACTIVE')
            const Padding(
              padding: EdgeInsets.only(top: 8),
              child: Text(
                'Your first successful attendance will activate your employee status.',
              ),
            ),
          if (!widget.profileComplete)
            Card(
              color: Theme.of(context).colorScheme.errorContainer,
              child: ListTile(
                leading: const Icon(Icons.warning_amber_outlined),
                title: const Text(
                  'Complete your profile before marking attendance.',
                ),
                trailing: TextButton(
                  onPressed: widget.onCompleteProfile,
                  child: const Text('Complete Profile'),
                ),
              ),
            ),
          const SizedBox(height: 12),
          if (capturedPhotoPath != null)
            Image.file(
              File(capturedPhotoPath!),
              height: 220,
              fit: BoxFit.cover,
            ),
          if (capturedPosition != null)
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 8),
              child: Text(
                'Location: ${capturedPosition!.latitude.toStringAsFixed(6)}, ${capturedPosition!.longitude.toStringAsFixed(6)}',
              ),
            ),
          Row(
            children: [
              Expanded(
                child: FilledButton.icon(
                  onPressed: processing || !widget.profileComplete
                      ? null
                      : captureFace,
                  icon: const Icon(Icons.camera_alt_outlined),
                  label: Text(
                    capturedPhotoPath == null
                        ? 'Mark Attendance'
                        : 'Retake Photo',
                  ),
                ),
              ),
              if (capturedPhotoPath != null) const SizedBox(width: 8),
              if (capturedPhotoPath != null)
                Expanded(
                  child: FilledButton.icon(
                    onPressed: processing || capturedPosition == null
                        ? null
                        : submitAttendance,
                    icon: const Icon(Icons.check),
                    label: Text(
                      processing ? 'Submitting...' : 'Submit Attendance',
                    ),
                  ),
                ),
            ],
          ),
          if (captureMessage != null)
            Padding(
              padding: const EdgeInsets.only(top: 12),
              child: Text(captureMessage!),
            ),
        ],
      ),
      item: (record) => ListTile(
        leading: const Icon(Icons.schedule),
        title: Text(record.date),
        subtitle: Text(
          '${record.status} | Check-in: ${record.checkIn ?? 'Not recorded'} | Check-out: ${record.checkOut ?? 'Not recorded'}${record.latitude == null ? '' : ' | Location captured'}',
        ),
        trailing: record.photo == null
            ? null
            : const Icon(Icons.photo_outlined),
      ),
    );
  }
}

class PayrollPage extends StatefulWidget {
  const PayrollPage({super.key, required this.repository});
  final PayrollRepository repository;
  @override
  State<PayrollPage> createState() => _PayrollPageState();
}

class _PayrollPageState extends State<PayrollPage> {
  late Future<(List<PayrollItem>, List<PayrollRun>)> future;
  @override
  void initState() {
    super.initState();
    future =
        Future.wait<Object>([
          widget.repository.items(),
          widget.repository.runs(),
        ]).then(
          (values) =>
              (values[0] as List<PayrollItem>, values[1] as List<PayrollRun>),
        );
  }

  @override
  Widget build(
    BuildContext context,
  ) => FutureBuilder<(List<PayrollItem>, List<PayrollRun>)>(
    future: future,
    builder: (context, snapshot) {
      if (snapshot.hasError) {
        return ListView(
          padding: const EdgeInsets.all(20),
          children: [Text(userMessage(snapshot.error!))],
        );
      }
      if (!snapshot.hasData) {
        return const Center(child: CircularProgressIndicator());
      }
      final runs = {for (final run in snapshot.data!.$2) run.id: run};
      final items = snapshot.data!.$1;
      return ListView(
        padding: const EdgeInsets.all(20),
        children: [
          Text(
            'My Payroll',
            style: Theme.of(
              context,
            ).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 16),
          if (items.isEmpty) const Text('No payroll records found.'),
          ...items.map((item) {
            final run = runs[item.payrollRunId];
            return Card(
              child: ListTile(
                title: Text('Net salary: ${item.netSalary}'),
                subtitle: Text(
                  '${run?.periodStart ?? 'Unknown period'} to ${run?.periodEnd ?? 'Unknown period'}\nGross: ${item.grossSalary} | Deductions: ${item.deductions}',
                ),
                trailing: Text(item.paymentStatus),
              ),
            );
          }),
        ],
      );
    },
  );
}

class LeavePage extends StatefulWidget {
  const LeavePage({super.key, required this.repository});
  final LeaveRepository repository;
  @override
  State<LeavePage> createState() => _LeavePageState();
}

class _LeavePageState extends State<LeavePage> {
  late Future<List<LeaveRequest>> requests;
  List<LeaveType> types = [];
  final form = GlobalKey<FormState>();
  int? leaveType;
  final start = TextEditingController();
  final end = TextEditingController();
  final days = TextEditingController();
  final reason = TextEditingController();

  @override
  void initState() {
    super.initState();
    requests = widget.repository.requests();
    widget.repository
        .types()
        .then((value) {
          if (mounted) setState(() => types = value);
        })
        .catchError((_) {
          if (mounted) setState(() => types = []);
        });
  }

  Future<void> submit() async {
    if (!form.currentState!.validate()) return;
    await widget.repository.submit(
      leaveType: leaveType!,
      startDate: start.text,
      endDate: end.text,
      totalDays: double.parse(days.text),
      reason: reason.text,
    );
    if (!mounted) return;
    final refreshedRequests = widget.repository.requests();
    setState(() => requests = refreshedRequests);
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(const SnackBar(content: Text('Leave request submitted.')));
  }

  @override
  Widget build(BuildContext context) => ListView(
    padding: const EdgeInsets.all(20),
    children: [
      Text(
        'My Leave',
        style: Theme.of(
          context,
        ).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
      ),
      Form(
        key: form,
        child: Column(
          children: [
            DropdownButtonFormField<int>(
              initialValue: leaveType,
              decoration: const InputDecoration(labelText: 'Leave type'),
              items: types
                  .map(
                    (type) => DropdownMenuItem(
                      value: type.id,
                      child: Text(type.name),
                    ),
                  )
                  .toList(),
              onChanged: (value) => setState(() => leaveType = value),
              validator: (value) =>
                  value == null ? 'Select a leave type' : null,
            ),
            const SizedBox(height: 12),
            dateField(start, 'Start date'),
            const SizedBox(height: 12),
            dateField(end, 'End date'),
            const SizedBox(height: 12),
            TextFormField(
              controller: days,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(labelText: 'Total days'),
              validator: (value) => double.tryParse(value ?? '') == null
                  ? 'Enter total days'
                  : null,
            ),
            const SizedBox(height: 12),
            TextFormField(
              controller: reason,
              maxLines: 2,
              decoration: const InputDecoration(labelText: 'Reason'),
              validator: (value) =>
                  value == null || value.isEmpty ? 'Enter a reason' : null,
            ),
            const SizedBox(height: 12),
            FilledButton(
              onPressed: submit,
              child: const Text('Submit leave request'),
            ),
          ],
        ),
      ),
      const SizedBox(height: 24),
      FutureBuilder<List<LeaveRequest>>(
        future: requests,
        builder: (context, snapshot) {
          if (snapshot.hasError) return Text(userMessage(snapshot.error!));
          if (!snapshot.hasData) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.data!.isEmpty) {
            return const Text('No leave requests found.');
          }
          return Column(
            children: snapshot.data!
                .map(
                  (request) => Card(
                    child: ListTile(
                      title: Text('${request.startDate} to ${request.endDate}'),
                      subtitle: Text(request.reason),
                      trailing: Text(request.status),
                    ),
                  ),
                )
                .toList(),
          );
        },
      ),
    ],
  );

  Widget dateField(TextEditingController controller, String label) =>
      TextFormField(
        controller: controller,
        readOnly: true,
        decoration: InputDecoration(labelText: label),
        onTap: () async {
          final value = await showDatePicker(
            context: context,
            firstDate: DateTime(2020),
            lastDate: DateTime(2100),
            initialDate: DateTime.now(),
          );
          if (value != null) {
            controller.text = value.toIso8601String().substring(0, 10);
          }
        },
        validator: (value) =>
            value == null || value.isEmpty ? 'Select a date' : null,
      );
}

class ProfilePage extends StatelessWidget {
  const ProfilePage({
    super.key,
    required this.employee,
    required this.emailVerified,
  });
  final Employee employee;
  final bool emailVerified;
  @override
  Widget build(BuildContext context) => ListView(
    padding: const EdgeInsets.all(20),
    children: [
      Text(
        'My Profile',
        style: Theme.of(
          context,
        ).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
      ),
      const SizedBox(height: 16),
      Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Account verification',
                style: Theme.of(
                  context,
                ).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 12),
              Row(
                children: [
                  Icon(
                    emailVerified
                        ? Icons.verified
                        : Icons.mark_email_unread_outlined,
                    color: emailVerified ? Colors.green : Colors.orange,
                  ),
                  const SizedBox(width: 12),
                  Text(
                    'Email: ${emailVerified ? '✓ Verified' : '⚠ Not verified'}',
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
      const SizedBox(height: 12),
      Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Employment status',
                style: Theme.of(
                  context,
                ).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 12),
              Row(
                children: [
                  Icon(Icons.work_outline, color: statusColor(employee.status)),
                  const SizedBox(width: 12),
                  Text('Status: ${employee.status}'),
                ],
              ),
              const SizedBox(height: 4),
              Text(statusDescription(employee.status)),
            ],
          ),
        ),
      ),
      const SizedBox(height: 12),
      if (employee.profilePhotoUrl.isNotEmpty)
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: ClipRRect(
              borderRadius: BorderRadius.circular(12),
              child: Image.network(
                employee.profilePhotoUrl,
                height: 220,
                fit: BoxFit.cover,
                errorBuilder: (context, error, stackTrace) => const SizedBox(
                  height: 220,
                  child: Center(
                    child: Icon(Icons.image_not_supported_outlined),
                  ),
                ),
              ),
            ),
          ),
        ),
      ...{
        'Employee code': employee.employeeCode,
        'First name': employee.firstName,
        'Last name': employee.lastName,
        'Email': employee.email,
        'Phone': employee.phone,
        'Department': employee.departmentName,
        'Designation': employee.designationName,
        'Joining date': employee.joiningDate,
        'Employment type': employee.employmentType,
        'Gender': employee.gender,
      }.entries.map(
        (item) => ListTile(title: Text(item.key), subtitle: Text(item.value)),
      ),
    ],
  );
}

class DataPage<T> extends StatelessWidget {
  const DataPage({
    super.key,
    required this.title,
    required this.future,
    required this.empty,
    required this.item,
    this.header,
  });
  final String title;
  final Future<List<T>> future;
  final String empty;
  final Widget Function(T) item;
  final Widget? header;
  @override
  Widget build(BuildContext context) => ListView(
    padding: const EdgeInsets.all(20),
    children: [
      Text(
        title,
        style: Theme.of(
          context,
        ).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
      ),
      if (header != null)
        Padding(
          padding: const EdgeInsets.symmetric(vertical: 16),
          child: header,
        ),
      const SizedBox(height: 16),
      FutureBuilder<List<T>>(
        future: future,
        builder: (context, snapshot) {
          if (snapshot.hasError) return Text(userMessage(snapshot.error!));
          if (!snapshot.hasData) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.data!.isEmpty) return Text(empty);
          return Column(children: snapshot.data!.map(item).toList());
        },
      ),
    ],
  );
}
