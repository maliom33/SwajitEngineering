import 'dart:io';
import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';
import 'package:image_picker/image_picker.dart';

import '../core/config/api_config.dart';
import '../core/theme/app_theme.dart';
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
    this.accountPassword,
  });

  final AuthRepository authRepository;
  final EmployeeRepository employeeRepository;
  final AttendanceRepository attendanceRepository;
  final LeaveRepository leaveRepository;
  final PayrollRepository payrollRepository;
  final UserSession? initialSession;
  final String? accountPassword;

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
    this.accountPassword,
  });
  final AuthRepository authRepository;
  final EmployeeRepository employeeRepository;
  final AttendanceRepository attendanceRepository;
  final LeaveRepository leaveRepository;
  final PayrollRepository payrollRepository;
  final UserSession initialSession;
  final String? accountPassword;
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
  final imagePicker = ImagePicker();
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
        final missing = _missingProfileFields(employee);
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

  Future<void> pickProfilePhoto([
    ImageSource source = ImageSource.gallery,
  ]) async {
    setState(() {
      loading = true;
      message = null;
    });
    try {
      final image = await imagePicker.pickImage(
        source: source,
        imageQuality: 85,
        maxWidth: 1600,
      );
      if (image == null) return;
      await widget.employeeRepository.uploadPhoto(
        widget.initialSession.employee!.employeeId,
        image.path,
      );
      final refreshed = await widget.authRepository.me();
      if (mounted) {
        final employee = refreshed.employee;
        setState(() {
          localPhotoPath = image.path;
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
      if (mounted) setState(() => loading = false);
    }
  }

  Future<void> chooseProfilePhoto() async {
    final source = await showModalBottomSheet<ImageSource>(
      context: context,
      showDragHandle: true,
      builder: (context) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              leading: const Icon(Icons.camera_alt_outlined),
              title: const Text('Take a profile photo'),
              onTap: () => Navigator.pop(context, ImageSource.camera),
            ),
            ListTile(
              leading: const Icon(Icons.photo_library_outlined),
              title: const Text('Choose from gallery'),
              onTap: () => Navigator.pop(context, ImageSource.gallery),
            ),
          ],
        ),
      ),
    );
    if (source != null && mounted) await pickProfilePhoto(source);
  }

  List<String> _missingProfileFields(Employee? employee) {
    if (employee == null) return const ['profile info'];
    final missing = <String>[];
    if (employee.firstName.trim().isEmpty) missing.add('First name');
    if (employee.lastName.trim().isEmpty) missing.add('Last name');
    if (employee.email.trim().isEmpty) missing.add('Email');
    if (employee.phone.trim().isEmpty) missing.add('Phone');
    if (employee.gender.trim().isEmpty) missing.add('Gender');
    if (employee.departmentName.trim().isEmpty) missing.add('Department');
    if (employee.designationName.trim().isEmpty) missing.add('Designation');
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
    final password = widget.accountPassword ?? await _requestVerificationPassword();
    if (password == null || password.isEmpty) return;
    setState(() {
      loading = true;
      message = null;
    });
    try {
      await widget.employeeRepository.requestEmailVerification(
        password: password,
      );
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

  Future<String?> _requestVerificationPassword() async {
    final controller = TextEditingController();
    final password = await showDialog<String>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Confirm your password'),
        content: TextField(
          controller: controller,
          obscureText: true,
          autofocus: true,
          decoration: const InputDecoration(labelText: 'Password'),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(context, controller.text),
            child: const Text('Send verification'),
          ),
        ],
      ),
    );
    controller.dispose();
    return password;
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
                    onPressed: loading ? null : chooseProfilePhoto,
                    icon: const Icon(Icons.photo_library_outlined),
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
          const SizedBox(height: 18),
          FilledButton.icon(
            onPressed: loading ? null : saveProfile,
            icon: const Icon(Icons.save_outlined),
            label: Text(loading ? 'Saving profile...' : 'Save profile'),
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
          accountPassword: widget.accountPassword,
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
        onOpenAttendance: () => setState(() => selectedTab = 1),
        onOpenLeave: () => setState(() => selectedTab = 2),
        onOpenPayroll: () => setState(() => selectedTab = 3),
        onOpenProfile: () => setState(() => selectedTab = 4),
      ),
      AttendancePage(
        employee: employee,
        repository: widget.attendanceRepository,
        faceRecognitionService: PendingFaceRecognitionService(),
        onAttendanceRecorded: _refreshSession,
        employeeStatus: employee.status,
        profileComplete: employee.profileComplete,
        onCompleteProfile: _openProfileSetup,
      ),
      LeavePage(employee: employee, repository: widget.leaveRepository),
      PayrollPage(employee: employee, repository: widget.payrollRepository),
      ProfilePage(
        employee: employee,
        emailVerified: session?.emailVerified ?? false,
        onEditProfile: _openProfileSetup,
        onLogout: _logout,
      ),
    ];
    return Scaffold(
      appBar: PreferredSize(
        preferredSize: const Size.fromHeight(82),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(20, 12, 16, 10),
            child: Row(
              children: [
                const Expanded(child: BrandLogo(size: 40, showWordmark: true)),
                EmployeeAvatar(employee: employee, radius: 20),
                IconButton(
                  onPressed: () => showInfoSheet(
                    context,
                    'Notifications',
                    'You are all caught up. Attendance and leave updates will appear here.',
                  ),
                  tooltip: 'Notifications',
                  icon: const Icon(Icons.notifications_none_rounded),
                ),
                IconButton(
                  onPressed: _logout,
                  tooltip: 'Sign out',
                  icon: const Icon(Icons.logout_rounded),
                ),
              ],
            ),
          ),
        ),
      ),
      body: LayoutBuilder(
        builder: (context, constraints) {
          final wide = constraints.maxWidth >= 760;
          final navigation = NavigationRail(
            selectedIndex: selectedTab,
            onDestinationSelected: (value) =>
                setState(() => selectedTab = value),
            labelType: NavigationRailLabelType.all,
            backgroundColor: const Color(0xff0d1b25),
            destinations: const [
              NavigationRailDestination(
                icon: Icon(Icons.grid_view_rounded),
                label: Text('Home'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.fingerprint_rounded),
                label: Text('Attendance'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.event_note_rounded),
                label: Text('Leave'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.account_balance_wallet_rounded),
                label: Text('Payroll'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.person_rounded),
                label: Text('Profile'),
              ),
            ],
          );
          return Row(
            children: [
              if (wide) navigation,
              Expanded(child: pages[selectedTab]),
            ],
          );
        },
      ),
      bottomNavigationBar: MediaQuery.sizeOf(context).width >= 760
          ? null
          : NavigationBar(
              selectedIndex: selectedTab,
              onDestinationSelected: (value) =>
                  setState(() => selectedTab = value),
              destinations: const [
                NavigationDestination(
                  icon: Icon(Icons.grid_view_rounded),
                  label: 'Home',
                ),
                NavigationDestination(
                  icon: Icon(Icons.fingerprint_rounded),
                  label: 'Attendance',
                ),
                NavigationDestination(
                  icon: Icon(Icons.event_note_rounded),
                  label: 'Leave',
                ),
                NavigationDestination(
                  icon: Icon(Icons.account_balance_wallet_rounded),
                  label: 'Payroll',
                ),
                NavigationDestination(
                  icon: Icon(Icons.person_rounded),
                  label: 'Profile',
                ),
              ],
            ),
    );
  }
}

class SwajeetMark extends StatelessWidget {
  const SwajeetMark({super.key, this.size = 48});
  final double size;

  @override
  Widget build(BuildContext context) => BrandLogo(size: size);
}

class EmployeeAvatar extends StatelessWidget {
  const EmployeeAvatar({super.key, required this.employee, this.radius = 26});
  final Employee employee;
  final double radius;

  @override
  Widget build(BuildContext context) {
    final photo = _photoUrl(employee.profilePhotoUrl);
    final initials =
        '${employee.firstName.isNotEmpty ? employee.firstName[0] : ''}${employee.lastName.isNotEmpty ? employee.lastName[0] : ''}'
            .toUpperCase();
    return Container(
      width: (radius + 2) * 2,
      height: (radius + 2) * 2,
      padding: const EdgeInsets.all(2),
      decoration: const BoxDecoration(
        shape: BoxShape.circle,
        color: AppColors.accent,
      ),
      child: ClipOval(
        child: photo.isEmpty
            ? _initials(initials)
            : Image.network(
                photo,
                fit: BoxFit.cover,
                errorBuilder: (context, error, stackTrace) =>
                    _initials(initials),
              ),
      ),
    );
  }

  String _photoUrl(String value) {
    final photo = value.trim();
    if (photo.isEmpty) return '';

    final parsed = Uri.tryParse(photo);
    final apiUri = Uri.parse(ApiConfig.baseUrl);
    if (parsed == null || parsed.path.isEmpty) return photo;

    final usesLocalHost = parsed.host == 'localhost' ||
        parsed.host == '127.0.0.1' ||
        parsed.host == '0.0.0.0';
    if (!parsed.hasScheme || usesLocalHost) {
      return apiUri.replace(
        path: parsed.path.startsWith('/') ? parsed.path : '/${parsed.path}',
        query: parsed.query,
        fragment: parsed.fragment,
      ).toString();
    }
    return photo;
  }

  Widget _initials(String initials) => Container(
    color: AppColors.secondarySurface,
    alignment: Alignment.center,
    child: Text(
      initials.isEmpty ? '?' : initials,
      style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900),
    ),
  );
}

class EmployeePageHeader extends StatelessWidget {
  const EmployeePageHeader({
    super.key,
    required this.employee,
    required this.title,
    this.subtitle,
  });
  final Employee employee;
  final String title;
  final String? subtitle;

  @override
  Widget build(BuildContext context) => Padding(
    padding: const EdgeInsets.only(bottom: 14),
    child: Row(
      children: [
        EmployeeAvatar(employee: employee, radius: 24),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                  fontWeight: FontWeight.w900,
                ),
              ),
              Text(
                subtitle ?? '${employee.fullName}  •  ${employee.employeeCode}',
                style: const TextStyle(color: Color(0xff9db0bb)),
              ),
            ],
          ),
        ),
      ],
    ),
  );
}

class DashboardPage extends StatefulWidget {
  const DashboardPage({
    super.key,
    required this.employee,
    required this.emailVerified,
    required this.attendanceRepository,
    required this.leaveRepository,
    required this.onOpenAttendance,
    required this.onOpenLeave,
    required this.onOpenPayroll,
    required this.onOpenProfile,
  });
  final Employee employee;
  final bool emailVerified;
  final AttendanceRepository attendanceRepository;
  final LeaveRepository leaveRepository;
  final VoidCallback onOpenAttendance;
  final VoidCallback onOpenLeave;
  final VoidCallback onOpenPayroll;
  final VoidCallback onOpenProfile;

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
    padding: const EdgeInsets.fromLTRB(18, 10, 18, 28),
    children: [
      Container(
        padding: const EdgeInsets.all(22),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(24),
          gradient: const LinearGradient(
            colors: [Color(0xff173b4a), Color(0xff0d1c25)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          border: Border.all(color: AppColors.line),
        ),
        child: Stack(
          children: [
            const Positioned(
              right: -16,
              top: -24,
              child: Icon(
                Icons.route_rounded,
                size: 170,
                color: Color(0x24169db3),
              ),
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    EmployeeAvatar(employee: widget.employee, radius: 25),
                    const SizedBox(width: 12),
                    const Expanded(child: Eyebrow('EMPLOYEE WORKSPACE')),
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 9,
                        vertical: 6,
                      ),
                      decoration: BoxDecoration(
                        color: AppColors.success.withValues(alpha: .14),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: const Text(
                        'CONNECTED',
                        style: TextStyle(
                          color: AppColors.success,
                          fontSize: 10,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 22),
                const Text(
                  'GOOD MORNING',
                  style: TextStyle(
                    color: Color(0xffffb79e),
                    fontSize: 11,
                    fontWeight: FontWeight.w900,
                    letterSpacing: 1.5,
                  ),
                ),
                const SizedBox(height: 5),
                Text(
                  widget.employee.fullName,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 28,
                    fontWeight: FontWeight.w900,
                  ),
                ),
                const SizedBox(height: 5),
                Text(
                  '${widget.employee.designationName}  /  ${widget.employee.employeeCode}',
                  style: const TextStyle(color: AppColors.muted),
                ),
              ],
            ),
          ],
        ),
      ),
      const SizedBox(height: 20),
      const Eyebrow('TODAY\'S OPERATIONS', color: AppColors.muted),
      const SizedBox(height: 10),
      FutureBuilder<(List<AttendanceRecord>, List<LeaveRequest>)>(
        future: summary,
        builder: (context, snapshot) {
          if (snapshot.hasError) {
            return _DashboardError(
              onRetry: () => setState(() => summary = _loadSummary()),
            );
          }
          if (!snapshot.hasData) return const _DashboardLoading();
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
          final today = DateTime.now().toIso8601String().substring(0, 10);
          final todayRecord = attendance
              .where((record) => record.date == today)
              .firstOrNull;
          return Column(
            children: [
              TodayWorkCard(
                record: todayRecord,
                onOpenAttendance: widget.onOpenAttendance,
              ),
              const SizedBox(height: 12),
              Row(
                children: [
                  Expanded(
                    child: MetricTile(
                      value: '$present',
                      label: 'PRESENT',
                      icon: Icons.check_circle_outline,
                      color: AppColors.success,
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: MetricTile(
                      value: '$pending',
                      label: 'PENDING LEAVE',
                      icon: Icons.pending_actions_rounded,
                      color: AppColors.warning,
                    ),
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: MetricTile(
                      value: '${attendance.length}',
                      label: 'RECORDS',
                      icon: Icons.timeline_rounded,
                      color: AppColors.cyan,
                    ),
                  ),
                ],
              ),
            ],
          );
        },
      ),
      const SizedBox(height: 20),
      const Eyebrow('QUICK ACCESS', color: AppColors.muted),
      const SizedBox(height: 10),
      Row(
        children: [
          Expanded(
            child: QuickActionTile(
              icon: Icons.fingerprint_rounded,
              label: 'Attendance',
              color: AppColors.accent,
              onTap: widget.onOpenAttendance,
            ),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: QuickActionTile(
              icon: Icons.event_note_rounded,
              label: 'Leave',
              color: AppColors.warning,
              onTap: widget.onOpenLeave,
            ),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: QuickActionTile(
              icon: Icons.payments_outlined,
              label: 'Payroll',
              color: AppColors.success,
              onTap: widget.onOpenPayroll,
            ),
          ),
          const SizedBox(width: 10),
          Expanded(
            child: QuickActionTile(
              icon: Icons.person_outline_rounded,
              label: 'Profile',
              color: AppColors.cyan,
              onTap: widget.onOpenProfile,
            ),
          ),
        ],
      ),
      const SizedBox(height: 20),
      LifecycleStatusCard(employmentStatus: widget.employee.status),
    ],
  );

  Future<(List<AttendanceRecord>, List<LeaveRequest>)> _loadSummary() =>
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

class _DashboardLoading extends StatelessWidget {
  const _DashboardLoading();

  @override
  Widget build(BuildContext context) => const Card(
    child: Padding(
      padding: EdgeInsets.all(24),
      child: Center(child: CircularProgressIndicator()),
    ),
  );
}

class _DashboardError extends StatelessWidget {
  const _DashboardError({required this.onRetry});
  final VoidCallback onRetry;

  @override
  Widget build(BuildContext context) => Card(
    child: ListTile(
      leading: const Icon(Icons.cloud_off_rounded, color: AppColors.danger),
      title: const Text('Unable to load today\'s operations'),
      trailing: IconButton(
        onPressed: onRetry,
        icon: const Icon(Icons.refresh_rounded),
      ),
    ),
  );
}

class MetricTile extends StatelessWidget {
  const MetricTile({
    super.key,
    required this.value,
    required this.label,
    required this.icon,
    required this.color,
  });
  final String value;
  final String label;
  final IconData icon;
  final Color color;

  @override
  Widget build(BuildContext context) => Card(
    child: Padding(
      padding: const EdgeInsets.all(13),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: color, size: 20),
          const SizedBox(height: 10),
          Text(
            value,
            style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w900),
          ),
          const SizedBox(height: 3),
          Text(
            label,
            style: const TextStyle(
              color: AppColors.muted,
              fontSize: 9,
              fontWeight: FontWeight.w900,
              letterSpacing: .6,
            ),
          ),
        ],
      ),
    ),
  );
}

class QuickActionTile extends StatelessWidget {
  const QuickActionTile({
    super.key,
    required this.icon,
    required this.label,
    required this.color,
    required this.onTap,
  });
  final IconData icon;
  final String label;
  final Color color;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) => InkWell(
    onTap: onTap,
    borderRadius: BorderRadius.circular(16),
    child: Card(
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 4),
        child: Column(
          children: [
            Icon(icon, color: color, size: 23),
            const SizedBox(height: 8),
            Text(
              label,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 10, fontWeight: FontWeight.w800),
            ),
          ],
        ),
      ),
    ),
  );
}

class StatusChip extends StatelessWidget {
  const StatusChip({super.key, required this.label, required this.color});
  final String label;
  final Color color;

  @override
  Widget build(BuildContext context) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 6),
    decoration: BoxDecoration(
      color: color.withValues(alpha: .14),
      borderRadius: BorderRadius.circular(8),
    ),
    child: Text(
      label,
      style: TextStyle(
        color: color,
        fontSize: 10,
        fontWeight: FontWeight.w900,
        letterSpacing: .6,
      ),
    ),
  );
}

class TodayWorkCard extends StatelessWidget {
  const TodayWorkCard({
    super.key,
    required this.record,
    required this.onOpenAttendance,
  });
  final AttendanceRecord? record;
  final VoidCallback onOpenAttendance;

  @override
  Widget build(BuildContext context) {
    final active = record?.checkIn != null && record?.checkOut == null;
    final completed = record?.checkOut != null;
    final title = completed
        ? 'SHIFT COMPLETED'
        : active
        ? 'ON DUTY'
        : 'READY TO START';
    final detail = completed
        ? '${record!.checkIn}  →  ${record!.checkOut}'
        : active
        ? 'Checked in at ${record!.checkIn}'
        : 'Capture your live photo and location to begin.';
    return Card(
      color: const Color(0xff102733),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(
                  Icons.access_time_filled_rounded,
                  color: Color(0xffff8d68),
                ),
                const SizedBox(width: 8),
                const Expanded(
                  child: Text(
                    "TODAY'S WORK",
                    style: TextStyle(
                      color: Color(0xff9db0bb),
                      fontWeight: FontWeight.w800,
                      letterSpacing: 1.2,
                    ),
                  ),
                ),
                Text(
                  title,
                  style: TextStyle(
                    color: completed
                        ? const Color(0xff31c48d)
                        : const Color(0xffff8d68),
                    fontWeight: FontWeight.w900,
                    fontSize: 12,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 14),
            Text(
              detail,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 18,
                fontWeight: FontWeight.w800,
              ),
            ),
            if (record?.totalWorkMinutes != null) ...[
              const SizedBox(height: 6),
              Text(
                '${record!.totalWorkMinutes} minutes worked',
                style: const TextStyle(color: Color(0xff9db0bb)),
              ),
            ],
            const SizedBox(height: 16),
            if (!completed)
              FilledButton.icon(
                onPressed: onOpenAttendance,
                icon: Icon(
                  active ? Icons.logout_rounded : Icons.fingerprint_rounded,
                ),
                label: Text(active ? 'CHECK OUT' : 'CHECK IN'),
              )
            else
              const Text(
                'Attendance completed for today.',
                style: TextStyle(
                  color: Color(0xff31c48d),
                  fontWeight: FontWeight.w700,
                ),
              ),
          ],
        ),
      ),
    );
  }
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
    child: Padding(
      padding: const EdgeInsets.all(18),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(11),
            decoration: BoxDecoration(
              color: const Color(0xff173e52),
              borderRadius: BorderRadius.circular(14),
            ),
            child: Icon(icon, color: const Color(0xffff8d68)),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  label,
                  style: const TextStyle(
                    color: Color(0xff9db0bb),
                    fontSize: 12,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  value,
                  style: const TextStyle(
                    fontWeight: FontWeight.w800,
                    fontSize: 16,
                  ),
                ),
              ],
            ),
          ),
        ],
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
  const LifecycleStatusCard({super.key, required this.employmentStatus});
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
            leading: const Icon(Icons.work_outline),
            title: const Text('Employment status'),
            subtitle: Text(employmentStatus),
          ),
          if (employmentStatus == 'INACTIVE')
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
    required this.employee,
    required this.faceRecognitionService,
    this.onAttendanceRecorded,
    required this.employeeStatus,
    required this.profileComplete,
    required this.onCompleteProfile,
  });
  final AttendanceRepository repository;
  final Employee employee;
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
  AttendanceRecord? openAttendance;
  @override
  void initState() {
    super.initState();
    future = _loadAttendance();
  }

  Future<List<AttendanceRecord>> _loadAttendance() async {
    final records = await widget.repository.list();
    final openRecords = records
        .where((record) => record.checkIn != null && record.checkOut == null)
        .toList();
    openAttendance = openRecords.isEmpty ? null : openRecords.first;
    if (mounted) setState(() {});
    return records;
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

  Future<void> startCheckout(AttendanceRecord record) async {
    setState(() {
      openAttendance = record;
      capturedPhotoPath = null;
      capturedPosition = null;
      captureMessage = null;
    });
    await captureFace();
  }

  Future<void> captureAndSubmitCheckout(AttendanceRecord record) async {
    await startCheckout(record);
    if (!mounted || capturedPhotoPath == null || capturedPosition == null) {
      return;
    }
    await submitAttendance();
  }

  Future<void> submitAttendance() async {
    final photoPath = capturedPhotoPath;
    final position = capturedPosition;
    if (photoPath == null || position == null) return;
    final checkingOut = openAttendance != null;
    setState(() {
      processing = true;
      captureMessage = null;
      capturedPhotoPath = null;
      capturedPosition = null;
    });
    try {
      if (openAttendance == null) {
        await widget.repository.submit(
          photoPath: photoPath,
          latitude: position.latitude,
          longitude: position.longitude,
        );
      } else {
        await widget.repository.checkOut(
          attendanceId: openAttendance!.id,
          photoPath: photoPath,
          latitude: position.latitude,
          longitude: position.longitude,
        );
      }
      final refreshedStatus = await widget.onAttendanceRecorded?.call();
      if (mounted) {
        setState(() {
          capturedPhotoPath = null;
          capturedPosition = null;
          captureMessage = refreshedStatus == 'ACTIVE'
              ? 'Attendance marked successfully. Your employee account is now ACTIVE.'
              : checkingOut
              ? 'Check-out recorded successfully. Have a great day.'
              : 'Check-in recorded successfully.';
          openAttendance = null;
          future = _loadAttendance();
        });
      }
    } catch (exception) {
      if (mounted) {
        setState(() {
          capturedPhotoPath = null;
          capturedPosition = null;
          captureMessage = userMessage(exception);
        });
      }
    } finally {
      if (mounted) setState(() => processing = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return DataPage(
      title: 'My Attendance',
      header: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          EmployeePageHeader(
            employee: widget.employee,
            title: 'My Attendance',
            subtitle: 'Live attendance and work hours',
          ),
          _attendanceHeaderContent(),
        ],
      ),
      future: future,
      empty: 'No attendance records found.',
      item: (record) => _attendanceRecordCard(record),
    );
  }

  Widget _attendanceHeaderContent() => Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      const Text(
        'Capture a live photo and your current location to record your work time.',
        style: TextStyle(color: AppColors.muted),
      ),
      if (openAttendance != null)
        Card(
          color: AppColors.elevated,
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const Row(
                  children: [
                    Icon(Icons.timer_outlined, color: AppColors.accent),
                    SizedBox(width: 10),
                    Expanded(child: Eyebrow('SHIFT IN PROGRESS')),
                    StatusChip(label: 'ON DUTY', color: AppColors.success),
                  ],
                ),
                const SizedBox(height: 10),
                Text(
                  'Checked in at ${openAttendance!.checkIn}',
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                const SizedBox(height: 12),
                FilledButton.icon(
                  onPressed: processing || !widget.profileComplete
                      ? null
                      : () => captureAndSubmitCheckout(openAttendance!),
                  style: FilledButton.styleFrom(
                    backgroundColor: AppColors.accent,
                  ),
                  icon: const Icon(Icons.logout_rounded),
                  label: const Text('CAPTURE & CHECK OUT'),
                ),
              ],
            ),
          ),
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
          color: AppColors.danger.withValues(alpha: .12),
          child: ListTile(
            leading: const Icon(
              Icons.warning_amber_outlined,
              color: AppColors.warning,
            ),
            title: const Text(
              'Complete your profile before marking attendance.',
            ),
            trailing: TextButton(
              onPressed: widget.onCompleteProfile,
              child: const Text('Complete'),
            ),
          ),
        ),
      const SizedBox(height: 12),
      if (capturedPhotoPath != null)
        ClipRRect(
          borderRadius: BorderRadius.circular(16),
          child: Image.file(
            File(capturedPhotoPath!),
            height: 220,
            fit: BoxFit.cover,
          ),
        ),
      if (capturedPosition != null)
        Card(
          color: AppColors.secondarySurface,
          child: ListTile(
            leading: const Icon(
              Icons.location_on_outlined,
              color: AppColors.success,
            ),
            title: const Text(
              'LOCATION VERIFIED',
              style: TextStyle(fontWeight: FontWeight.w900, fontSize: 12),
            ),
            subtitle: Text(
              '${capturedPosition!.latitude.toStringAsFixed(6)}, ${capturedPosition!.longitude.toStringAsFixed(6)}',
            ),
          ),
        ),
      Row(
        children: [
          Expanded(
            child: FilledButton.icon(
              onPressed: processing || !widget.profileComplete
                  ? null
                  : openAttendance != null
                  ? () => captureAndSubmitCheckout(openAttendance!)
                  : captureFace,
              icon: const Icon(Icons.camera_alt_outlined),
              label: Text(
                capturedPhotoPath == null
                    ? openAttendance == null
                          ? 'CHECK IN'
                          : 'CHECK OUT'
                    : 'RETAKE PHOTO',
              ),
            ),
          ),
          if (capturedPhotoPath != null) const SizedBox(width: 8),
          if (capturedPhotoPath != null)
            Expanded(
              child: OutlinedButton.icon(
                onPressed: processing || capturedPosition == null
                    ? null
                    : submitAttendance,
                icon: const Icon(Icons.check),
                label: Text(processing ? 'SAVING...' : 'CONFIRM'),
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
  );
  Widget _attendanceRecordCard(AttendanceRecord record) => Card(
    margin: const EdgeInsets.only(bottom: 12),
    child: Padding(
      padding: const EdgeInsets.all(14),
      child: Column(
        children: [
          ListTile(
            contentPadding: EdgeInsets.zero,
            leading: const Icon(Icons.fingerprint_rounded, size: 30),
            title: Text(record.date),
            subtitle: Text(
              '${record.status} | Check-in: ${record.checkIn ?? 'Not recorded'} | Check-out: ${record.checkOut ?? 'Not recorded'}${record.totalWorkMinutes == null ? '' : ' | ${record.totalWorkMinutes} min worked'}${record.latitude == null ? '' : ' | Location captured'}',
            ),
            trailing: record.photo == null && record.checkOutPhoto == null
                ? null
                : const Icon(Icons.verified_user_outlined),
          ),
          if (record.checkIn != null && record.checkOut == null)
            SizedBox(
              width: double.infinity,
              child: FilledButton.icon(
                onPressed: processing || !widget.profileComplete
                    ? null
                    : () => captureAndSubmitCheckout(record),
                style: FilledButton.styleFrom(
                  backgroundColor: const Color(0xffff5b2e),
                ),
                icon: const Icon(Icons.logout_rounded),
                label: const Text('CHECK OUT'),
              ),
            ),
        ],
      ),
    ),
  );
}

class PayrollPage extends StatefulWidget {
  const PayrollPage({
    super.key,
    required this.employee,
    required this.repository,
  });
  final Employee employee;
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
        padding: const EdgeInsets.fromLTRB(18, 10, 18, 28),
        children: [
          EmployeePageHeader(
            employee: widget.employee,
            title: 'My Payroll',
            subtitle: 'Salary, payslips and payment history',
          ),
          const Eyebrow('COMPENSATION OVERVIEW', color: AppColors.muted),
          const SizedBox(height: 10),
          if (items.isEmpty)
            const Card(
              child: Padding(
                padding: EdgeInsets.all(22),
                child: Text('No payroll records found.'),
              ),
            ),
          ...items.map((item) {
            final run = runs[item.payrollRunId];
            return Card(
              margin: const EdgeInsets.only(bottom: 12),
              child: Padding(
                padding: const EdgeInsets.all(18),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Expanded(child: Eyebrow('NET PAY')),
                        StatusChip(
                          label: item.paymentStatus,
                          color: AppColors.success,
                        ),
                      ],
                    ),
                    const SizedBox(height: 6),
                    Text(
                      item.netSalary,
                      style: const TextStyle(
                        fontSize: 30,
                        fontWeight: FontWeight.w900,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      '${run?.periodStart ?? 'Unknown period'}  →  ${run?.periodEnd ?? 'Unknown period'}',
                      style: const TextStyle(color: AppColors.muted),
                    ),
                    const SizedBox(height: 18),
                    Row(
                      children: [
                        Expanded(
                          child: PayrollValue(
                            label: 'GROSS',
                            value: item.grossSalary,
                            color: AppColors.cyan,
                          ),
                        ),
                        Expanded(
                          child: PayrollValue(
                            label: 'OVERTIME',
                            value: item.overtime,
                            color: AppColors.warning,
                          ),
                        ),
                        Expanded(
                          child: PayrollValue(
                            label: 'DEDUCTIONS',
                            value: item.deductions,
                            color: AppColors.danger,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            );
          }),
        ],
      );
    },
  );
}

class PayrollValue extends StatelessWidget {
  const PayrollValue({
    super.key,
    required this.label,
    required this.value,
    required this.color,
  });
  final String label;
  final String value;
  final Color color;

  @override
  Widget build(BuildContext context) => Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Text(
        label,
        style: TextStyle(
          color: color,
          fontSize: 9,
          fontWeight: FontWeight.w900,
          letterSpacing: .7,
        ),
      ),
      const SizedBox(height: 4),
      Text(
        value,
        style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 12),
      ),
    ],
  );
}

class LeavePage extends StatefulWidget {
  const LeavePage({
    super.key,
    required this.employee,
    required this.repository,
  });
  final Employee employee;
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
  bool submitting = false;

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
    setState(() => submitting = true);
    try {
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
    } catch (error) {
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text(userMessage(error))));
      }
    } finally {
      if (mounted) setState(() => submitting = false);
    }
  }

  @override
  Widget build(BuildContext context) => ListView(
    padding: const EdgeInsets.fromLTRB(18, 10, 18, 28),
    children: [
      EmployeePageHeader(
        employee: widget.employee,
        title: 'My Leave',
        subtitle: 'Balances, requests and approvals',
      ),
      const Eyebrow('REQUEST TIME AWAY', color: AppColors.muted),
      const SizedBox(height: 10),
      Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Form(
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
                  onPressed: submitting ? null : submit,
                  child: Text(
                    submitting ? 'Submitting...' : 'Submit leave request',
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
      const SizedBox(height: 24),
      const Eyebrow('RECENT REQUESTS', color: AppColors.muted),
      const SizedBox(height: 10),
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
    required this.onEditProfile,
    required this.onLogout,
  });
  final Employee employee;
  final bool emailVerified;
  final Future<void> Function() onEditProfile;
  final Future<void> Function() onLogout;
  @override
  Widget build(BuildContext context) => ListView(
    padding: const EdgeInsets.fromLTRB(18, 10, 18, 28),
    children: [
      const Eyebrow('EMPLOYEE IDENTITY', color: AppColors.muted),
      const SizedBox(height: 16),
      Card(
        color: AppColors.elevated,
        child: Padding(
          padding: const EdgeInsets.all(22),
          child: Row(
            children: [
              EmployeeAvatar(employee: employee, radius: 38),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      employee.fullName,
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 22,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                    const SizedBox(height: 5),
                    Text(
                      employee.employeeCode,
                      style: const TextStyle(
                        color: AppColors.accent,
                        fontWeight: FontWeight.w700,
                      ),
                    ),
                    const SizedBox(height: 3),
                    Text(
                      employee.email,
                      style: const TextStyle(color: Color(0xffb6c5cb)),
                    ),
                    const SizedBox(height: 10),
                    TextButton.icon(
                      onPressed: () {
                        onEditProfile();
                      },
                      icon: const Icon(Icons.camera_alt_outlined, size: 17),
                      label: const Text('Change photo'),
                      style: TextButton.styleFrom(
                        foregroundColor: const Color(0xffff8d68),
                        padding: EdgeInsets.zero,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
      const SizedBox(height: 12),
      Card(
        child: Column(
          children: [
            MoreMenuTile(
              icon: Icons.person_outline_rounded,
              title: 'My Profile',
              onTap: () {
                onEditProfile();
              },
            ),
            MoreMenuTile(
              icon: Icons.notifications_none_rounded,
              title: 'Notifications',
              trailing: const NotificationDot(),
              onTap: () => showInfoSheet(
                context,
                'Notifications',
                'You are all caught up. New attendance and leave updates will appear here.',
              ),
            ),
            MoreMenuTile(
              icon: Icons.photo_library_outlined,
              title: 'Profile picture',
              subtitle: 'Choose a photo from your gallery',
              onTap: () {
                onEditProfile();
              },
            ),
          ],
        ),
      ),
      const SizedBox(height: 12),
      Card(
        child: Column(
          children: [
            MoreMenuTile(
              icon: Icons.badge_outlined,
              title: 'Employee details',
              onTap: () => showInfoSheet(
                context,
                'Employee details',
                '${employee.departmentName}\n${employee.designationName}\n${employee.employmentType.replaceAll('_', ' ')}',
              ),
            ),
            MoreMenuTile(
              icon: Icons.settings_outlined,
              title: 'Settings',
              onTap: () => showInfoSheet(
                context,
                'Settings',
                'Your local employee workspace is ready.',
              ),
            ),
            MoreMenuTile(
              icon: Icons.help_outline_rounded,
              title: 'Help & support',
              onTap: () => showInfoSheet(
                context,
                'Help & support',
                'Contact your HR administrator for account and attendance support.',
              ),
            ),
          ],
        ),
      ),
      const SizedBox(height: 12),
      Card(
        color: const Color(0xff281923),
        child: MoreMenuTile(
          icon: Icons.logout_rounded,
          title: 'Logout',
          onTap: () {
            onLogout();
          },
          color: const Color(0xffff6b58),
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
      const Eyebrow('WORK IDENTITY', color: AppColors.muted),
      const SizedBox(height: 8),
      Card(
        child: Column(
          children: [
            MoreMenuTile(
              icon: Icons.apartment_outlined,
              title: 'Department',
              subtitle: employee.departmentName,
              onTap: () =>
                  showInfoSheet(context, 'Department', employee.departmentName),
            ),
            MoreMenuTile(
              icon: Icons.badge_outlined,
              title: 'Designation',
              subtitle: employee.designationName,
              onTap: () => showInfoSheet(
                context,
                'Designation',
                employee.designationName,
              ),
            ),
            MoreMenuTile(
              icon: Icons.work_history_outlined,
              title: 'Employment',
              subtitle: employee.employmentType.replaceAll('_', ' '),
              onTap: () => showInfoSheet(
                context,
                'Employment',
                employee.employmentType.replaceAll('_', ' '),
              ),
            ),
          ],
        ),
      ),
      const SizedBox(height: 12),
      const Eyebrow('CONTACT', color: AppColors.muted),
      const SizedBox(height: 8),
      Card(
        child: Column(
          children: [
            MoreMenuTile(
              icon: Icons.email_outlined,
              title: 'Email',
              subtitle: employee.email,
              onTap: () => showInfoSheet(context, 'Email', employee.email),
            ),
            MoreMenuTile(
              icon: Icons.phone_outlined,
              title: 'Phone',
              subtitle: employee.phone,
              onTap: () => showInfoSheet(context, 'Phone', employee.phone),
            ),
          ],
        ),
      ),
    ],
  );
}

class MoreMenuTile extends StatelessWidget {
  const MoreMenuTile({
    super.key,
    required this.icon,
    required this.title,
    required this.onTap,
    this.subtitle,
    this.trailing,
    this.color,
  });
  final IconData icon;
  final String title;
  final String? subtitle;
  final Widget? trailing;
  final VoidCallback onTap;
  final Color? color;
  @override
  Widget build(BuildContext context) => ListTile(
    onTap: onTap,
    leading: Icon(icon, color: color ?? const Color(0xffd6e0e4)),
    title: Text(
      title,
      style: TextStyle(color: color, fontWeight: FontWeight.w700),
    ),
    subtitle: subtitle == null
        ? null
        : Text(subtitle!, style: const TextStyle(color: Color(0xff9db0bb))),
    trailing:
        trailing ??
        const Icon(Icons.chevron_right_rounded, color: Color(0xff6e818b)),
  );
}

class NotificationDot extends StatelessWidget {
  const NotificationDot({super.key});
  @override
  Widget build(BuildContext context) => Container(
    width: 22,
    height: 22,
    alignment: Alignment.center,
    decoration: const BoxDecoration(
      color: Color(0xfff15b35),
      shape: BoxShape.circle,
    ),
    child: const Text(
      '3',
      style: TextStyle(
        color: Colors.white,
        fontSize: 11,
        fontWeight: FontWeight.w800,
      ),
    ),
  );
}

void showInfoSheet(BuildContext context, String title, String message) {
  showModalBottomSheet<void>(
    context: context,
    showDragHandle: true,
    builder: (_) => Padding(
      padding: const EdgeInsets.fromLTRB(24, 0, 24, 32),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: Theme.of(
              context,
            ).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 12),
          Text(message),
          const SizedBox(height: 18),
        ],
      ),
    ),
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
