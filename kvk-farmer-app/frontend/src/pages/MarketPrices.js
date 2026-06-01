import React, { useState, useEffect } from 'react';
import { getMarket } from '../services/api';

export default function MarketPrices() {
  const [prices, setPrices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMarket().then(r => setPrices(r.data)).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading-wrap"><div className="spinner"/><span>Loading prices...</span></div>;

  return (
    <div>
      <div className="page-header">
        <h2>📈 Market Prices</h2>
        <p>Current crop prices vs Minimum Support Price (MSP) — West Bengal Mandis</p>
      </div>

      <div className="grid-4" style={{marginBottom:22}}>
        {prices.slice(0,4).map((p, i) => (
          <div className="stat-tile" key={i}>
            <span className="label">{p.crop}</span>
            <span className="value">₹{p.market_price}</span>
            <span className="sub">per quintal</span>
            <span className={`badge badge-${p.trend}`} style={{marginTop:4}}>{p.trend === 'up' ? '↑ Rising' : p.trend === 'down' ? '↓ Falling' : '→ Stable'}</span>
          </div>
        ))}
      </div>

      <div className="card">
        <div className="card-title">💰 Complete Price List</div>
        <table className="data-table">
          <thead>
            <tr>
              <th>Crop</th>
              <th>MSP (₹/quintal)</th>
              <th>Market Price (₹/quintal)</th>
              <th>Difference</th>
              <th>Trend</th>
            </tr>
          </thead>
          <tbody>
            {prices.map((p, i) => {
              const diff = p.msp ? p.market_price - p.msp : null;
              return (
                <tr key={i}>
                  <td><b>{p.crop}</b></td>
                  <td>{p.msp ? `₹${p.msp}` : <span style={{color:'var(--text-light)'}}>No MSP</span>}</td>
                  <td><b>₹{p.market_price}</b></td>
                  <td>
                    {diff !== null ? (
                      <span style={{color: diff >= 0 ? '#2e7d32' : '#c62828', fontWeight:600}}>
                        {diff >= 0 ? '+' : ''}₹{diff.toFixed(0)}
                      </span>
                    ) : '—'}
                  </td>
                  <td><span className={`badge badge-${p.trend}`}>{p.trend}</span></td>
                </tr>
              );
            })}
          </tbody>
        </table>
        <div style={{marginTop:12, fontSize:'0.75rem', color:'var(--text-light)'}}>
          * MSP = Minimum Support Price announced by Government of India. Prices updated periodically.
        </div>
      </div>
    </div>
  );
}
