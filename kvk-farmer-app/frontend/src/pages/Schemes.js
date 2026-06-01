import React, { useState, useEffect } from 'react';
import { getSchemes } from '../services/api';

export default function Schemes() {
  const [schemes, setSchemes]   = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading]   = useState(true);

  useEffect(() => {
    getSchemes().then(r => { setSchemes(r.data); setSelected(r.data[0]); }).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading-wrap"><div className="spinner"/><span>Loading schemes...</span></div>;

  return (
    <div>
      <div className="page-header">
        <h2>🏛️ Government Schemes</h2>
        <p>Central & State government schemes for West Bengal farmers</p>
      </div>

      <div className="grid-2">
        {/* Scheme list */}
        <div style={{display:'flex', flexDirection:'column', gap:12}}>
          {schemes.map((s, i) => (
            <div key={i} className={`scheme-card ${selected?.name === s.name ? 'active' : ''}`} onClick={() => setSelected(s)}>
              <h4>{s.name}</h4>
              <div style={{fontSize:'0.82rem', color:'var(--text-mid)', marginTop:4}}>{s.full_name}</div>
              <div style={{marginTop:8, fontSize:'0.82rem', fontWeight:600, color:'var(--green-dark)'}}>
                {s.benefit}
              </div>
              <span className="category">{s.category}</span>
            </div>
          ))}
        </div>

        {/* Detail panel */}
        {selected && (
          <div className="scheme-detail">
            <h3>📜 {selected.full_name}</h3>
            <div style={{
              background: 'var(--green-light)',
              borderRadius: 8,
              padding: '12px 16px',
              marginBottom: 18,
              border: '1px solid var(--border)'
            }}>
              <div style={{fontSize:'0.72rem', color:'var(--green-dark)', fontWeight:700, textTransform:'uppercase', letterSpacing:'0.8px', marginBottom:4}}>Key Benefit</div>
              <div style={{fontSize:'1rem', fontWeight:700, color:'var(--green-dark)'}}>{selected.benefit}</div>
            </div>
            <div className="detail-row">
              <label>Category</label>
              <p><span className="badge badge-low">{selected.category}</span></p>
            </div>
            <div className="detail-row">
              <label>Who Can Apply</label>
              <p>{selected.eligibility}</p>
            </div>
            <div className="detail-row">
              <label>How to Apply</label>
              <p>{selected.how_to_apply}</p>
            </div>
            <div style={{marginTop:18, padding:'12px 16px', background:'#fff8e1', borderRadius:8, border:'1px solid #ffe082', fontSize:'0.82rem', color:'#5d4037'}}>
              💡 <b>Tip:</b> Visit your nearest <b>Block Development Office (BDO)</b> or <b>Common Service Centre (CSC)</b> to apply. Carry your Aadhaar card, land records, and bank passbook.
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
