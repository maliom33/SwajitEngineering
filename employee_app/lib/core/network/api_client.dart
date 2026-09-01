import 'package:dio/dio.dart';
import '../config/api_config.dart';
import '../storage/secure_token_storage.dart';

class ApiClient {
  ApiClient({required SecureTokenStorage storage}) : _storage = storage {
    dio = Dio(BaseOptions(baseUrl: ApiConfig.baseUrl, connectTimeout: const Duration(seconds: 10), receiveTimeout: const Duration(seconds: 15), headers: {'Content-Type': 'application/json'}));
    dio.interceptors.add(InterceptorsWrapper(onRequest: (options, handler) async { final token = await _storage.accessToken; if (token != null) options.headers['Authorization'] = 'Bearer $token'; handler.next(options); }, onError: _handleError));
  }
  final SecureTokenStorage _storage;
  late final Dio dio;
  Future<void>? _refreshing;

  Future<void> _handleError(DioException error, ErrorInterceptorHandler handler) async {
    final request = error.requestOptions;
    final isAuthRequest = request.path.contains('auth/login') || request.path.contains('auth/refresh');
    if (error.response?.statusCode != 401 || request.extra['retried'] == true || isAuthRequest) { handler.next(error); return; }
    final refresh = await _storage.refreshToken;
    if (refresh == null) { await _storage.clear(); handler.next(error); return; }
    try {
      _refreshing ??= _refresh(refresh).whenComplete(() => _refreshing = null);
      await _refreshing;
      request.extra['retried'] = true;
      request.headers['Authorization'] = 'Bearer ${await _storage.accessToken}';
      handler.resolve(await dio.fetch(request));
    } catch (_) { await _storage.clear(); handler.next(error); }
  }

  Future<void> _refresh(String refresh) async {
    final response = await Dio().post('${ApiConfig.baseUrl}auth/refresh/', data: {'refresh': refresh});
    await _storage.saveAccess(response.data['access'] as String);
  }
}
