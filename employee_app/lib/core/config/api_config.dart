import 'package:flutter/foundation.dart';

class ApiConfig {
  static const configuredBaseUrl = String.fromEnvironment('API_BASE_URL');

  static String get baseUrl => configuredBaseUrl.isNotEmpty
      ? configuredBaseUrl
      : kIsWeb
          ? 'http://127.0.0.1:8000/api/'
          : 'http://10.0.2.2:8000/api/';
}
