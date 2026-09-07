export function one(v) {
  if (Array.isArray(v)) v = v[0];
  if (v == null) return "";
  return String(v).trim();
}

export function queryOf(req) {
  if (req.query && typeof req.query === "object" && !Array.isArray(req.query)) {
    return req.query;
  }
  try {
    const u = new URL(req.url || "", "http://localhost");
    return Object.fromEntries(u.searchParams);
  } catch {
    return {};
  }
}

export function readBody(req) {
  const b = req.body;
  if (b == null || b === "") return {};
  if (typeof b === "string") {
    try {
      const parsed = JSON.parse(b);
      return parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed : null;
    } catch {
      return null;
    }
  }
  if (typeof b === "object" && !Array.isArray(b)) return b;
  return null;
}

export function clampInt(v, min, max, fallback = 0) {
  const n = typeof v === "number" ? v : Number(v);
  if (!Number.isFinite(n)) return fallback;
  return Math.max(min, Math.min(max, Math.round(n)));
}

export function shortText(v, max) {
  return String(v == null ? "" : v).replace(/[^\w .+\-]/g, "").slice(0, max);
}
