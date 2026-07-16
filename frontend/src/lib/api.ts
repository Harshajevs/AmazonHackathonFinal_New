import { Movie } from '../types/Movie';

export const API_URL: string = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';
export const WS_URL: string = API_URL.replace(/^http/, 'ws');

const TOKEN_KEY = 'firetv_token';

export class ApiError extends Error {
  code: string;
  status: number;
  constructor(status: number, code: string, message: string) {
    super(message);
    this.status = status;
    this.code = code;
  }
}

export const getToken = (): string | null => localStorage.getItem(TOKEN_KEY);
export const setToken = (token: string) => localStorage.setItem(TOKEN_KEY, token);
export const clearToken = () => localStorage.removeItem(TOKEN_KEY);

export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });
  if (response.status === 204) return undefined as T;
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    const detail = body?.detail ?? {};
    throw new ApiError(response.status, detail.code ?? 'error', detail.message ?? 'Request failed');
  }
  return body as T;
}

/** Ensure we hold a session token, creating a guest session if needed. */
export async function ensureSession(): Promise<boolean> {
  try {
    if (getToken()) {
      await api('/api/users/me');
      return true;
    }
  } catch {
    clearToken(); // stale/expired token
  }
  try {
    const { access_token } = await api<{ access_token: string }>('/api/auth/guest', { method: 'POST' });
    setToken(access_token);
    return true;
  } catch {
    return false; // backend unreachable -> bundled-data demo mode
  }
}

export interface ApiMovie {
  id: number;
  title: string;
  description: string;
  genres: string[];
  duration: string;
  rating: number;
  year: number;
  image: string;
  platform: string;
  featured: boolean;
}

/** Map a backend movie onto the UI's existing Movie shape. */
export const toMovie = (m: ApiMovie): Movie => ({
  id: String(m.id),
  title: m.title,
  description: m.description,
  genre: m.genres,
  duration: m.duration,
  rating: m.rating.toFixed(1),
  year: m.year,
  image: m.image,
  platform: m.platform as Movie['platform'],
  featured: m.featured,
});
