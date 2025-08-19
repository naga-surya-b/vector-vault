import { useState } from "react";

export default function SearchPanel({ onSearch }){
  const [q, setQ] = useState("");
  const [k, setK] = useState(5);
  const [useLLM, setUseLLM] = useState(false);

  return (
    <div style={{display:"grid", gap:"0.5rem", marginTop:"1rem"}}>
      <div style={{display:"flex", gap:"0.5rem"}}>
        <input style={{flex:1}} placeholder="Ask a question or search by meaning..." value={q} onChange={e=>setQ(e.target.value)} />
        <button onClick={()=>onSearch({ q, k: Number(k), useLLM })}>Search</button>
      </div>
      <div style={{display:"flex", gap:"1rem", alignItems:"center"}}>
        <label>Top K: <input type="number" min="1" max="10" value={k} onChange={e=>setK(e.target.value)} style={{width:60, marginLeft:6}} /></label>
        <label><input type="checkbox" checked={useLLM} onChange={e=>setUseLLM(e.target.checked)} /> Use LLM (synthesize answer)</label>
      </div>
    </div>
  );
}
