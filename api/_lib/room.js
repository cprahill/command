import { randomBytes } from "node:crypto";
import { sendEmpty, sendJson } from "./cors.js";
import { one, queryOf, readBody } from "./http.js";

export const ROOM_TTL = 120;
const ICE_MAX = 48;
const PAYLOAD_MAX = 24 * 1024;
const ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

export function roomKey(code) {
  return "baja:room:" + code;
}

export function sanitizeCode(raw) {
  return one(raw).toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, 4);
}

export function randomCode() {
  const buf = randomBytes(4);
  let s = "";
  for (let i = 0; i < 4; i++) s += ABC[buf[i] % ABC.length];
  return s;
}

function payloadOk(v) {
  if (v == null) return false;
  if (typeof v === "string") return v.length > 0 && v.length <= PAYLOAD_MAX;
  if (typeof v === "number" || typeof v === "boolean") return true;
  if (typeof v !== "object") return false;
  try {
    return JSON.stringify(v).length <= PAYLOAD_MAX;
  } catch {
    return false;
  }
}

function emptyRoom(code) {
  return {
    code,
    createdAt: Date.now(),
    updatedAt: Date.now(),
    join: null,
    offer: null,
    answer: null,
    ice: []
  };
}

function publicRoom(room) {
  return {
    ok: true,
    code: room.code,
    createdAt: room.createdAt,
    updatedAt: room.updatedAt,
    join: room.join || null,
    offer: room.offer || null,
    answer: room.answer || null,
    ice: Array.isArray(room.ice) ? room.ice : []
  };
}

async function loadRoom(kv, code) {
  const raw = await kv.get(roomKey(code));
  if (!raw || typeof raw !== "object") return null;
  return raw;
}

async function saveRoom(kv, room) {
  room.updatedAt = Date.now();
  await kv.set(roomKey(room.code), room, ROOM_TTL);
  return room;
}

async function createRoom(kv) {
  for (let i = 0; i < 8; i++) {
    const code = randomCode();
    const room = emptyRoom(code);
    if (await kv.setNx(roomKey(code), room, ROOM_TTL)) return room;
  }
  const err = new Error("busy");
  err.code = "busy";
  throw err;
}

export async function handleRoom(req, res, kv) {
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
      const code = sanitizeCode(queryOf(req).code);
      if (code.length !== 4) {
        sendJson(req, res, 400, { ok: false, error: "bad-code" });
        return;
      }
      const room = await loadRoom(kv, code);
      if (!room) {
        sendJson(req, res, 404, { ok: false, error: "no-room" });
        return;
      }
      sendJson(req, res, 200, publicRoom(room));
      return;
    }

    const body = readBody(req);
    if (!body) {
      sendJson(req, res, 400, { ok: false, error: "bad-json" });
      return;
    }
    const action = one(body.action).toLowerCase();
    if (action === "create") {
      const room = await createRoom(kv);
      sendJson(req, res, 200, { ok: true, code: room.code });
      return;
    }

    const code = sanitizeCode(body.code);
    if (code.length !== 4) {
      sendJson(req, res, 400, { ok: false, error: "bad-code" });
      return;
    }
    const room = await loadRoom(kv, code);
    if (!room) {
      sendJson(req, res, 404, { ok: false, error: "no-room" });
      return;
    }

    if (action === "join") {
      if (!payloadOk(body.sdp)) {
        sendJson(req, res, 400, { ok: false, error: "bad-sdp" });
        return;
      }
      room.join = { sdp: body.sdp };
      await saveRoom(kv, room);
      sendJson(req, res, 200, publicRoom(room));
      return;
    }

    if (action === "offer" || action === "answer" || action === "ice") {
      if (!payloadOk(body.payload)) {
        sendJson(req, res, 400, { ok: false, error: "bad-payload" });
        return;
      }
      if (action === "ice") {
        const ice = Array.isArray(room.ice) ? room.ice.slice() : [];
        ice.push(body.payload);
        room.ice = ice.slice(-ICE_MAX);
      } else {
        room[action] = body.payload;
      }
      await saveRoom(kv, room);
      sendJson(req, res, 200, publicRoom(room));
      return;
    }

    sendJson(req, res, 400, { ok: false, error: "bad-action" });
  } catch (err) {
    if (err && err.code === "busy") {
      sendJson(req, res, 503, { ok: false, error: "busy" });
      return;
    }
    sendJson(req, res, 502, { ok: false, error: "kv-error" });
  }
}
