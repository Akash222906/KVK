import React, { useState } from 'react';
import { previewReport, generateReport } from '../services/api';

const CROPS = ['Rice (Aman)','Rice (Boro)','Rice (Aus)','Jute','Potato','Mustard','Wheat','Vegetables','Maize','Sesame','Groundnut','Sugarcane','Tomato','Brinjal','Onion'];
const SEASONS = ['Kharif','Rabi','Summer'];
const SOIL_TYPES = ['Loamy','Sandy Loam','Clay Loam','Alluvial','Red Laterite','Saline'];

export default function ReportGenerator({ district }) {
  const [form, setForm] = useState({
    name: '', district, crop: 'Rice (Aman)', area: '1', season: 'Kharif',
    soil_type: 'Loamy', N: '80', P: '40', K: '40', pH: '6.5',
  });
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [genLoading, setGenLoading] = useState(false);

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  const handlePreview = async () => {
    setLoading(true);
    try {
      const r = await previewReport({ ...form, district });
      setPreview(r.data);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    setGenLoading(true);
    try {
      const r = await generateReport({ ...form, district });
      const url = window.URL.createObjectURL(new Blob([r.data], { type: 'application/pdf' }));
      const a = document.createElement('a');
      a.href = url;
      a.download = `KVK_Report_${form.name || 'farmer'}_${district}.pdf`;
      a.click();
      window.URL.revokeObjectURL(url);
    } finally {
      setGenLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h2>📋 Farm Report Generator</h2>
        <p>Enter farm details to get AI-powered crop recommendations and downloadable PDF report</p>
      </div>

      <div className="grid-2">
        {/* Form */}
        <div className="card">
          <div className="card-title">🧑‍🌾 Farm Details</div>

          <div className="grid-2">
            <div className="form-group">
              <label>Farmer Name</label>
              <input value={form.name} onChange={e => set('name', e.target.value)} placeholder="e.g. Ramesh Mondal"/>
            </div>
            <div className="form-group">
              <label>Farm Area (hectares)</label>
              <input type="number" value={form.area} onChange={e => set('area', e.target.value)} min="0.1" step="0.1"/>
            </div>
          </div>

          <div className="grid-2">
            <div className="form-group">
              <label>Primary Crop</label>
              <select value={form.crop} onChange={e => set('crop', e.target.value)}>
                {CROPS.map(c => <option key={c}>{c}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label>Season</label>
              <select value={form.season} onChange={e => set('season', e.target.value)}>
                {SEASONS.map(s => <option key={s}>{s}</option>)}
              </select>
            </div>
          </div>

          <div className="form-group">
            <label>Soil Type</label>
            <select value={form.soil_type} onChange={e => set('soil_type', e.target.value)}>
              {SOIL_TYPES.map(s => <option key={s}>{s}</option>)}
            </select>
          </div>

          <div style={{marginBottom:8, fontSize:'0.8rem', fontWeight:700, color:'var(--green-dark)', textTransform:'uppercase', letterSpacing:'0.5px'}}>
            🔬 Soil Nutrients (kg/ha)
          </div>
          <div className="grid-2">
            <div className="form-group">
              <label>Nitrogen (N)</label>
              <input type="number" value={form.N} onChange={e => set('N', e.target.value)} min="0" max="300"/>
            </div>
            <div className="form-group">
              <label>Phosphorus (P)</label>
              <input type="number" value={form.P} onChange={e => set('P', e.target.value)} min="0" max="200"/>
            </div>
            <div className="form-group">
              <label>Potassium (K)</label>
              <input type="number" value={form.K} onChange={e => set('K', e.target.value)} min="0" max="200"/>
            </div>
            <div className="form-group">
              <label>Soil pH</label>
              <input type="number" value={form.pH} onChange={e => set('pH', e.target.value)} min="4" max="9" step="0.1"/>
            </div>
          </div>

          <div style={{display:'flex', gap:10}}>
            <button className="btn btn-primary" onClick={handlePreview} disabled={loading}>
              {loading ? '⏳ Analyzing...' : '🔍 Preview Report'}
            </button>
            {preview && (
              <button className="btn btn-gold" onClick={handleDownload} disabled={genLoading}>
                {genLoading ? '⏳ Generating...' : '⬇️ Download PDF'}
              </button>
            )}
          </div>
        </div>

        {/* Preview panel */}
        <div className="card">
          <div className="card-title">📄 Report Preview</div>
          {!preview && !loading && (
            <div style={{color:'var(--text-light)', textAlign:'center', padding:'40px 0'}}>
              <div style={{fontSize:'3rem', marginBottom:10}}>📋</div>
              <p>Fill in the form and click <b>Preview Report</b></p>
            </div>
          )}
          {loading && <div className="loading-wrap"><div className="spinner"/><span>Running ML models...</span></div>}
          {preview && !loading && (
            <div className="report-preview">
              {/* Crop recommendations */}
              <div className="preview-section">
                <h4>🌾 AI Crop Recommendations</h4>
                {preview.recommendations?.map((r, i) => (
                  <div key={i} style={{marginBottom:8}}>
                    <div style={{display:'flex', justifyContent:'space-between', fontSize:'0.85rem', marginBottom:3}}>
                      <span><b>#{i+1}</b> {r.crop}</span>
                      <span style={{color:'var(--green-dark)', fontWeight:700}}>{r.confidence}%</span>
                    </div>
                    <div className="conf-bar-wrap">
                      <div className="conf-bar">
                        <div className="conf-bar-fill" style={{width:`${r.confidence}%`}}/>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Yield */}
              <div className="preview-section">
                <h4>📦 Yield Prediction</h4>
                <div style={{fontSize:'1.2rem', fontWeight:700, color:'var(--green-dark)'}}>
                  {preview.yield_prediction} quintal/ha
                </div>
                <div style={{fontSize:'0.78rem', color:'var(--text-light)'}}>For {form.crop} in {district}</div>
              </div>

              {/* Pest risks */}
              <div className="preview-section">
                <h4>🐛 Pest Risk Assessment</h4>
                {preview.pest_risks?.map((p, i) => (
                  <div key={i} style={{display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom:6, fontSize:'0.82rem'}}>
                    <span>{p.pest}</span>
                    <span className={`badge badge-${p.risk.toLowerCase()}`}>{p.risk}</span>
                  </div>
                ))}
              </div>

              {/* Weather */}
              <div className="preview-section">
                <h4>🌤️ Current Weather</h4>
                <div style={{fontSize:'0.82rem', color:'var(--text-mid)'}}>
                  {preview.weather?.current?.temperature}°C · {preview.weather?.current?.humidity}% humidity · {preview.weather?.current?.season} season
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
