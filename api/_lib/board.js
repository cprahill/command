import { sendEmpty, sendJson } from "./cors.js";
import { clampInt, one, queryOf, readBody, shortText } from "./http.js";

export const PLANETS = new Set(["mars", "moon", "earth"]);
export const MODES = new Set(["raid", "trial", "tour", "hunt", "free"]);
export const DIFFS = {
  easy: "EASY",
  medium: "MED",
  hard: "HARD",
  extra: "XHARD"
};

const DIFF_ALIASES = {
  easy: "easy",
  medium: "medium",
  med: "medium",
  hard: "hard",
  extra: "extra",
  xhard: "extra",
  "x-hard": "extra"
};

export function parsePlanet(raw) {
  const s = one(raw).toLowerCase();
  return PLANETS.has(s) ? s : "";
}

export function parseMode(raw) {
  const s = one(raw).toLowerCase();
  return MODES.has(s) ? s : "";
}

export function parseDiff(raw) {
  const s = one(raw).toLowerCase();
  return DIFF_ALIASES[s] || "";
}

export function boardKey(planet, mode, diff) {
  return "baja:v1:" + planet + "/" + mode + "/" + diff;
}

export function sanitizeName(raw) {
  return one(raw).toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 4);
}

export function rowBetter(mode, a, b) {
  if (mode === "trial") return (a.time || 9e9) < (b.time || 9e9);
  return (a.score || 0) > (b.score || 0);
}

export function sortBoard(mode, list) {
  const rows = (list || []).slice();
  if (mode === "trial") rows.sort((a, b) => (a.time || 9e9) - (b.time || 9e9));
  else rows.sort((a, b) => (b.score || 0) - (a.score || 0));
  return rows.slice(0, 3);
}

function dedupeNames(mode, list) {
  const best = new Map();
  for (const r of list || []) {
    const k = r && r.name;
    if (!k) continue;
    const prev = best.get(k);
    if (!prev || rowBetter(mode, r, prev)) best.set(k, r);
  }
  return [...best.values()];
}

export function publicRow(r) {
  return {
    name: r.name,
    score: r.score,
    coins: r.coins,
    time: r.time,
    diff: r.diff,
    place: r.place,
    cup: r.cup,
    mode: r.mode,
    planet: r.planet
  };
}

export function insertRow(mode, list, row) {
  const cleaned = dedupeNames(mode, list);
  const i = cleaned.findIndex((r) => r.name === row.name);
  let inserted = false;
  if (i >= 0) {
    if (rowBetter(mode, row, cleaned[i])) {
      cleaned[i] = row;
      inserted = true;
    }
  } else {
    const ranked = sortBoard(mode, cleaned);
    if (ranked.length < 3 || rowBetter(mode, row, ranked[ranked.length - 1])) {
      cleaned.push(row);
      inserted = true;
    }
  }
  return { rows: sortBoard(mode, cleaned).map(publicRow), inserted };
}

export function parseScoreRow(body) {
  if (!body) return { error: "bad-json" };
  const planet = parsePlanet(body.planet);
  const mode = parseMode(body.mode);
  const diff = parseDiff(body.diff);
  const name = sanitizeName(body.name);
  if (!planet || !mode || !diff) return { error: "bad-lane" };
  if (name.length < 1) return { error: "bad-name" };
  return {
    planet,
    mode,
    diff,
    row: {
      name,
      score: clampInt(body.score, 0, 1e9, 0),
      coins: clampInt(body.coins, 0, 1e6, 0),
      time: clampInt(body.time, 0, 1e9, 0),
      diff: DIFFS[diff],
      place: shortText(body.place, 12),
      cup: shortText(body.cup, 12),
      mode,
      planet
    }
  };
}

async function loadRows(kv, key) {
  const raw = await kv.get(key);
  return Array.isArray(raw) ? raw : [];
}

export async function handleBoard(req, res, kv) {
  if (req.method === "OPTIONS") {
    sendEmpty(req, res, 204);
    return;
  }
  if (req.method !== "GET" && req.method !== "POST") {
    sendJson(req, res, 405, { ok: false, error: "method" });
    return;
  }
  if (!kv) {
    sendJson(req, res, 503, { ok: false, error: "no-kv" });
    return;
  }

  try {
    if (req.method === "GET") {
      const q = queryOf(req);
      const planet = parsePlanet(q.planet);
      const mode = parseMode(q.mode);
      const diff = parseDiff(q.diff);
      if (!planet || !mode || !diff) {
        sendJson(req, res, 400, { ok: false, error: "bad-lane" });
        return;
      }
      const key = boardKey(planet, mode, diff);
      const rows = sortBoard(mode, await loadRows(kv, key)).map(publicRow);
      sendJson(req, res, 200, { ok: true, key, rows });
      return;
    }

    const parsed = parseScoreRow(readBody(req));
    if (parsed.error) {
      sendJson(req, res, 400, { ok: false, error: parsed.error });
      return;
    }
    const key = boardKey(parsed.planet, parsed.mode, parsed.diff);
    const current = await loadRows(kv, key);
    const next = insertRow(parsed.mode, current, parsed.row);
    await kv.set(key, next.rows);
    sendJson(req, res, 200, { ok: true, key, rows: next.rows, inserted: next.inserted });
  } catch {
    sendJson(req, res, 502, { ok: false, error: "kv-error" });
  }
}
