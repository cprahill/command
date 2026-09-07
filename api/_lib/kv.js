// Talks to Vercel KV / Upstash Redis over the REST API that @vercel/kv wraps.
// Accepts either KV_REST_API_* (Vercel KV) or UPSTASH_REDIS_REST_* (Upstash).

export function kvEnv() {
  const url = String(process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL || "").replace(/\/$/, "");
  const token = String(process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN || "");
  if (!url || !token || !allowedKvUrl(url)) return null;
  return { url, token };
}

function allowedKvUrl(url) {
  try {
    const u = new URL(url);
    if (u.protocol !== "https:") return false;
    const host = u.hostname.toLowerCase();
    return host.endsWith(".upstash.io") || host.endsWith(".kv.vercel-storage.com");
  } catch {
    return false;
  }
}

export function getKv() {
  const env = kvEnv();
  if (!env) return null;
  return restKv(env.url, env.token);
}

export function restKv(url, token) {
  async function exec(parts) {
    const res = await fetch(url, {
      method: "POST",
      headers: {
        Authorization: "Bearer " + token,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(parts)
    });
    let data = {};
    try {
      data = await res.json();
    } catch {
      data = {};
    }
    if (!res.ok) {
      const err = new Error("kv-error");
      err.code = "kv-error";
      throw err;
    }
    return data.result;
  }

  function pack(v) {
    return JSON.stringify(v);
  }

  function unpack(r) {
    if (r == null) return null;
    if (typeof r === "object") return r;
    if (typeof r !== "string") return r;
    try {
      return JSON.parse(r);
    } catch {
      return r;
    }
  }

  return {
    async get(key) {
      return unpack(await exec(["GET", key]));
    },
    async set(key, val, ex) {
      const args = ["SET", key, pack(val)];
      if (ex) args.push("EX", String(ex));
      await exec(args);
      return true;
    },
    async setNx(key, val, ex) {
      const args = ["SET", key, pack(val), "NX"];
      if (ex) args.push("EX", String(ex));
      const r = await exec(args);
      return r === "OK";
    }
  };
}
