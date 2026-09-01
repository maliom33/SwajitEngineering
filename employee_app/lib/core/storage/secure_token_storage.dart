import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class SecureTokenStorage {
  static const _accessKey = 'access_token';
  static const _refreshKey = 'refresh_token';
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  Future<String?> get accessToken => _storage.read(key: _accessKey);
  Future<String?> get refreshToken => _storage.read(key: _refreshKey);
  Future<bool> hasSession() async => (await accessToken)?.isNotEmpty == true;
  Future<void> save({required String access, required String refresh}) async { await _storage.write(key: _accessKey, value: access); await _storage.write(key: _refreshKey, value: refresh); }
  Future<void> saveAccess(String access) => _storage.write(key: _accessKey, value: access);
  Future<void> clear() => _storage.deleteAll();
}
