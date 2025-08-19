const BASE = import.meta.env.VITE_API || "http://localhost:8000";

export async function ingestFile(file, title=""){
  const form = new FormData();
  form.append("file", file);
  if (title) form.append("title", title);
  const res = await fetch(`${BASE}/api/ingest`, { method: "POST", body: form });
  return res.json();
}

export async function ingestText(title, text){
  const res = await fetch(`${BASE}/api/ingest-text`, {
    method: "POST",
    headers: { "Content-Type":"application/json" },
    body: JSON.stringify({ title, text })
  });
  return res.json();
}

export async function search(q, k=5){
  const url = new URL(`${BASE}/api/search`);
  url.searchParams.set("q", q);
  url.searchParams.set("k", k);
  const res = await fetch(url);
  return res.json();
}

export async function answer(q, k=5){
  const url = new URL(`${BASE}/api/answer`);
  url.searchParams.set("q", q);
  url.searchParams.set("k", k);
  const res = await fetch(url);
  return res.json();
}
