const STORAGE_KEY = "lifeguard_token";

export function getToken() {
  return localStorage.getItem(STORAGE_KEY);
}

export function setToken(token) {
  localStorage.setItem(STORAGE_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(STORAGE_KEY);
}

export function authHeaders() {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}
