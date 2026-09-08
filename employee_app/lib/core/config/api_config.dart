
import 'package:flutter/foundation.dart';

class ApiConfig {
  static const configuredBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: '',
  );

  static String get baseUrl {
    if (configuredBaseUrl.isNotEmpty) return configuredBaseUrl;

    // Android emulator uses 10.0.2.2 to reach the host machine.
    // Physical devices and deployed HTTPS APIs must override this via
    // --dart-define=API_BASE_URL=https://<your-render-domain>/api/.
    if (!kIsWeb && defaultTargetPlatform == TargetPlatform.android) {
      return 'http://10.0.2.2:8000/api/';
    }

    return 'http://127.0.0.1:8000/api/';
  }
}
