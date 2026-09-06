
class ApiConfig {
  static const configuredBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'https://swajit-engineering-backend.onrender.com/api/',
  );

  static String get baseUrl => configuredBaseUrl.isNotEmpty
      ? configuredBaseUrl
      : 'https://swajit-engineering-backend.onrender.com/api/';
}
