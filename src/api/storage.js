const ACCESS_TOKEN_KEY = 'auth_access_token';
const REFRESH_TOKEN_KEY = 'auth_refresh_token';
const USER_KEY = 'auth_user';

export function getAccessToken() {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function getRefreshToken() {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
}

export function getStoredUser() {
  const user = localStorage.getItem(USER_KEY);
  if (!user) return null;

  try {
    return JSON.parse(user);
  } catch {
    return null;
  }
}

export function storeAuth({ access, refresh, user }) {
  if (!access || !refresh || !user) {
    throw new Error('Incomplete authentication response');
  }

  localStorage.setItem(ACCESS_TOKEN_KEY, access);
  localStorage.setItem(REFRESH_TOKEN_KEY, refresh);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function storeAccessToken(access) {
  if (access) {
    localStorage.setItem(ACCESS_TOKEN_KEY, access);
  }
}

export function clearAuth() {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}