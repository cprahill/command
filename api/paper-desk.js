import { getKv } from "./_lib/kv.js";
import { sendJson, sendEmpty, header } from "./_lib/cors.js";
import { readBody } from "./_lib/http.js";

const KEY = "paper-desk:v1:public";

function tokenOk(req) {
  const want = String(process.env.PAPER_DESK_PUBLISH_TOKEN || "");
  if (!want || want.length < 16) return false;
  const auth = header(req, "authorization") || "";
  const m = /^Bearer\s+(.+)$/i.exec(auth);
  const got = (m ? m[1] : header(req, "x-paper-desk-token") || "").trim();
  return got && got === want;
}

export default async function handler(req, res) {
  const method = (req.method || "GET").toUpperCase();
  if (method === "OPTIONS") return sendEmpty(req, res, 204);

  const kv = getKv();
  if (!kv) return sendJson(req, res, 503, { ok: false, error: "no-kv" });

  if (method === "GET") {
    const board = await kv.get(KEY);
    if (!board) return sendJson(req, res, 200, { ok: true, board: null, empty: true });
    // flatten for the static client: include board fields at top level too
    return sendJson(req, res, 200, { ok: true, board, paper: board.paper, signals: board.signals, updated_at: board.updated_at, disclaimer: board.disclaimer });
  }

  if (method === "POST") {
    if (!tokenOk(req)) return sendJson(req, res, 401, { ok: false, error: "unauthorized" });
    const body = readBody(req);
    if (!body || typeof body !== "object") return sendJson(req, res, 400, { ok: false, error: "bad-json" });
    const board = body.board && typeof body.board === "object" ? body.board : body;
    if (!board.paper || typeof board.paper !== "object") {
      return sendJson(req, res, 400, { ok: false, error: "need-paper" });
    }
    delete board.burn;
    delete board.studio_sprint;
    delete board.r1;
    board.paper.live_wallets = false;
    if (board.paper.confidence) board.paper.confidence.live_ready = false;
    await kv.set(KEY, board);
    return sendJson(req, res, 200, { ok: true, updated_at: board.updated_at || null });
  }

  return sendJson(req, res, 405, { ok: false, error: "method" });
}
