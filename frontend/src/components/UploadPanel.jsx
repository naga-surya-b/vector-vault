import { useState } from "react";
import { ingestFile, ingestText } from "../api.js";

export default function UploadPanel({ onAfterIngest }){
  const [title, setTitle] = useState("");
  const [text, setText] = useState("");

  async function onFile(e){
    const f = e.target.files?.[0];
    if(!f) return;
    await ingestFile(f, title);
    alert("Ingested " + (title || f.name));
    e.target.value = null;
    onAfterIngest?.();
  }

  async function onPaste(){
    if(!text.trim()) return;
    await ingestText(title || "pasted-text", text);
    alert("Ingested pasted text");
    setText("");
    onAfterIngest?.();
  }

  return (
    <div style={{display:"grid", gap:"0.5rem", border:"1px solid #eee", padding:"0.75rem", borderRadius:8, marginTop:"0.5rem"}}>
      <strong>Ingest</strong>
      <input placeholder="Optional title" value={title} onChange={e=>setTitle(e.target.value)} />
      <input type="file" accept=".pdf,.txt,.md" onChange={onFile} />
      <textarea placeholder="Or paste text here..." rows={5} value={text} onChange={e=>setText(e.target.value)} />
      <button onClick={onPaste}>Ingest Pasted Text</button>
    </div>
  );
}
