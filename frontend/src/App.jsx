import { useState } from "react";
import { search, answer } from "./api.js";
import UploadPanel from "./components/UploadPanel.jsx";
import SearchPanel from "./components/SearchPanel.jsx";

export default function App(){
  const [results, setResults] = useState([]);
  const [ans, setAns] = useState("");

  async function handleSearch({ q, k, useLLM }){
    setAns("");
    if (useLLM) {
      const r = await answer(q, k);
      setResults(r.results || []);
      setAns(r.answer || "");
    } else {
      const r = await search(q, k);
      setResults(r.results || []);
    }
  }

  return (
    <div style={{fontFamily:"Inter, system-ui, sans-serif", padding:"1rem", maxWidth:960, margin:"0 auto"}}>
      <h1>VectorVault Pro</h1>
      <p style={{opacity:.8}}>Private, offline document Q&A with citations.</p>

      <UploadPanel onAfterIngest={() => { /* no-op */ }} />
      <SearchPanel onSearch={handleSearch} />

      {ans && (
        <div style={{border:"1px solid #bbb", borderRadius:8, padding:"0.75rem", marginTop:"1rem", background:"#fafafa"}}>
          <strong>Answer</strong>
          <div style={{whiteSpace:"pre-wrap", marginTop:6}}>{ans}</div>
        </div>
      )}

      <div style={{marginTop:"1rem"}}>
        {results.map(r => (
          <div key={r.rank} style={{border:"1px solid #ddd", borderRadius:8, padding:"0.75rem", marginBottom:"0.5rem"}}>
            <div style={{fontSize:12, opacity:.7, display:"flex", gap:"0.5rem"}}>
              <span>#{r.rank}</span>
              <span>score: {r.score.toFixed(3)}</span>
              {"rerank_score" in r ? <span>rr: {r.rerank_score.toFixed(3)}</span> : null}
              <span title="source">{r.title} · chunk {r.chunk_index}</span>
            </div>
            <div style={{whiteSpace:"pre-wrap", marginTop:6}}>{r.text}</div>
          </div>
        ))}
        {results.length === 0 && <p style={{opacity:.7}}>No results yet — upload a PDF or paste text, then search.</p>}
      </div>
    </div>
  );
}
