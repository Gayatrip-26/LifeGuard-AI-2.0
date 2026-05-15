import { authHeaders } from "./auth";

const LOG = "[LifeGuard API]";

/** Trim trailing slash; empty string = same-origin (Vite proxy in Docker/dev). */
function normalizeBase(url) {
  const value = (url ?? "").trim();
  if (!value) return "";
  return value.replace(/\/$/, "");
}

export const API_URL = normalizeBase(
  import.meta.env.VITE_API_URL ||
    import.meta.env.VITE_BACKEND_URL ||
    import.meta.env.VITE_API_BASE_URL ||
    ""
);

export const INGESTION_URL = normalizeBase(import.meta.env.VITE_INGESTION_URL || "");

export const PREDICTION_URL = normalizeBase(import.meta.env.VITE_PREDICTION_URL || "");

export const AI_ENABLED = import.meta.env.VITE_AI_ENABLED !== "false";

export function jsonAuthHeaders() {
  return {
    ...authHeaders(),
    "Content-Type": "application/json",
  };
}

export function buildUrl(base, path) {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  if (!base) return normalizedPath;
  return `${base}${normalizedPath}`;
}

export class ApiError extends Error {
  constructor(message, { status, url, body } = {}) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.url = url;
    this.body = body;
  }
}

function detailFromBody(body) {
  if (!body) return null;
  if (typeof body.detail === "string") return body.detail;
  if (Array.isArray(body.detail)) {
    return body.detail
      .map((item) =>
        typeof item === "string" ? item : item?.msg || JSON.stringify(item)
      )
      .join("; ");
  }
  return null;
}

export function networkErrorMessage(err, label) {
  if (err instanceof ApiError) return err.message;
  const msg = err instanceof Error ? err.message : String(err);
  if (msg === "Failed to fetch" || err instanceof TypeError) {
    return `${label}: network error. If using Docker, ensure the frontend Vite proxy is running (empty VITE_INGESTION_URL) or services are reachable on published ports.`;
  }
  return msg || `${label} failed.`;
}

/**
 * Fetch with retries and structured console logging.
 * @param {string} path - e.g. "/users/me"
 * @param {RequestInit} [options]
 * @param {{ base?: string, retries?: number, retryDelayMs?: number, label?: string }} [config]
 */
export async function apiFetch(path, options = {}, config = {}) {
  const {
    base = API_URL,
    retries = 2,
    retryDelayMs = 600,
    label = path,
  } = config;

  const url = buildUrl(base, path);
  const method = options.method || "GET";
  let lastError;

  for (let attempt = 0; attempt <= retries; attempt += 1) {
    try {
      console.log(`${LOG} → ${label}`, { url, method, attempt: attempt + 1 });
      const response = await fetch(url, options);
      console.log(`${LOG} ← ${label}`, {
        url,
        status: response.status,
        ok: response.ok,
      });
      return response;
    } catch (err) {
      lastError = err;
      console.error(`${LOG} ✗ ${label}`, {
        url,
        attempt: attempt + 1,
        error: err,
      });
      if (attempt < retries) {
        await new Promise((resolve) =>
          setTimeout(resolve, retryDelayMs * (attempt + 1))
        );
      }
    }
  }

  throw lastError instanceof Error
    ? lastError
    : new Error(`${label}: request failed`);
}

export async function parseJsonResponse(response, label = "request") {
  const url = response.url;
  let body = {};
  try {
    body = await response.json();
  } catch {
    body = {};
  }

  if (!response.ok) {
    const detail = detailFromBody(body);
    throw new ApiError(detail || `${label} failed (${response.status})`, {
      status: response.status,
      url,
      body,
    });
  }

  return body;
}

export async function apiJson(path, options = {}, config = {}) {
  const response = await apiFetch(path, options, config);
  return parseJsonResponse(response, config.label || path);
}

export async function ingestHealthData(payload) {
  const path = "/ingest";
  const url = buildUrl(INGESTION_URL, path);

  console.log(`${LOG} → ingestion`, { url, payload });

  const response = await apiFetch(
    path,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    },
    { base: INGESTION_URL, label: "ingestion", retries: 2 }
  );

  const body = await parseJsonResponse(response, "ingestion");
  console.log(`${LOG} ← ingestion response`, body);
  return body;
}

export async function fetchPredictionHealth() {
  if (!PREDICTION_URL) return null;
  try {
    const body = await apiJson("/health", {}, {
      base: PREDICTION_URL,
      label: "prediction-health",
      retries: 1,
    });
    console.log(`${LOG} ← prediction service health`, body);
    return body;
  } catch (err) {
    console.warn(`${LOG} prediction service health check failed`, err);
    return null;
  }
}
