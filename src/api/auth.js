import client from './client';

export function login(email, password) {
  return client.post('auth/login/', { email, password });
}

export function requestPasswordReset(email) {
  return client.post('auth/password-reset/request/', { email });
}

export function confirmPasswordReset(payload) {
  return client.post('auth/password-reset/confirm/', payload);
}

export function refreshToken(refresh) {
  return client.post('auth/refresh/', { refresh });
}

export function getCurrentUser() {
  return client.get('auth/me/');
}

export function verifyEmail(token) {
  return client.get('auth/verification/email/verify/', { params: { token } });
}