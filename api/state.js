const GIST = "1819c5b97dfa701902768af9d1208ce0";

export default async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store, no-cache, must-revalidate");
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Content-Type", "application/json");
  const headers = {
    "User-Agent": "grok-command-live",
    Accept: "application/vnd.github+json",
  };
  if (process.env.GITHUB_TOKEN) {
    headers.Authorization = "Bearer " + process.env.GITHUB_TOKEN;
  }
  try {
    const r = await fetch("https://api.github.com/gists/" + GIST, {
      headers,
      cache: "no-store",
    });
    if (!r.ok) {
      res.status(502).json({ error: "gist", status: r.status });
      return;
    }
    const g = await r.json();
    const file = (g.files || {})["harness-live.json"];
    if (!file || !file.content) {
      res.status(502).json({ error: "empty" });
      return;
    }
    res.status(200).send(file.content);
  } catch (e) {
    res.status(502).json({ error: String(e && e.message ? e.message : e) });
  }
}
