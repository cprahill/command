const FIXED = new Set([
  "https://cprahill.github.io",
  "http://127.0.0.1:8766",
  "http://localhost:8766",
  "http://100.92.162.78:8766"
]);

function isLoopback(host) {
  return host === "127.0.0.1" || host === "localhost";
}

function isTailscale(host) {
  const m = /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/.exec(host);
  if (!m) return false;
  return +m[1] === 100;
}

export function allowOrigin(origin) {
  if (!origin || typeof origin !== "string") return "";
  if (FIXED.has(origin)) return origin;
  try {
    const u = new URL(origin);
    if (u.protocol !== "http:") return "";
    if (isLoopback(u.hostname) || isTailscale(u.hostname)) return origin;
    return "";
  } catch {
    return "";
  }
}

export function applyCors(req, res) {
  const origin = allowOrigin(header(req, "origin"));
  if (origin) res.setHeader("Access-Control-Allow-Origin", origin);
  res.setHeader("Vary", "Origin");
  res.setHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Paper-Desk-Token");
  res.setHeader("Access-Control-Max-Age", "86400");
}

export function header(req, name) {
  const h = req.headers || {};
  const v = h[name] || h[name.toLowerCase()] || h[name.toUpperCase()];
  if (Array.isArray(v)) return v[0] || "";
  return v || "";
}

export function sendJson(req, res, status, body) {
  applyCors(req, res);
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  if (typeof res.status === "function" && typeof res.json === "function") {
    return res.status(status).json(body);
  }
  res.statusCode = status;
  res.end(JSON.stringify(body));
}

export function sendEmpty(req, res, status) {
  applyCors(req, res);
  if (typeof res.status === "function") res.status(status);
  else res.statusCode = status;
  if (typeof res.end === "function") res.end();
}
