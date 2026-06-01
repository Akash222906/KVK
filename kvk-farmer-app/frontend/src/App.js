import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import './index.css';
import Dashboard from './pages/Dashboard';
import ReportGenerator from './pages/ReportGenerator';
import Chatbot from './pages/Chatbot';
import MarketPrices from './pages/MarketPrices';
import Schemes from './pages/Schemes';
import { getDistricts } from './services/api';

const NAV = [
  { path: '/',         icon: '🏠', label: 'Dashboard' },
  { path: '/report',   icon: '📋', label: 'Farm Report' },
  { path: '/chat',     icon: '🤖', label: 'KrishiBot AI' },
  { path: '/market',   icon: '📈', label: 'Market Prices' },
  { path: '/schemes',  icon: '🏛️', label: 'Govt Schemes' },
];

export default function App() {
  const [district, setDistrict] = useState('Bardhaman');
  const [districts, setDistricts] = useState([]);

  useEffect(() => {
    getDistricts().then(r => setDistricts(r.data)).catch(() => {});
  }, []);

  return (
    <BrowserRouter>
      <div className="sidebar">
        <div className="sidebar-logo">
          <h1>🌾 KVK Krishak Seva</h1>
          <p>Krishi Vigyan Kendra · ICAR</p>
        </div>
        <div className="district-select-wrap">
          <label>Your District</label>
          <select value={district} onChange={e => setDistrict(e.target.value)}>
            {districts.map(d => <option key={d} value={d}>{d}</option>)}
          </select>
        </div>
        <nav className="sidebar-nav">
          {NAV.map(n => (
            <NavLink key={n.path} to={n.path} end={n.path==='/'} className={({isActive}) => 'nav-link' + (isActive ? ' active' : '')}>
              <span className="nav-icon">{n.icon}</span>
              {n.label}
            </NavLink>
          ))}
        </nav>
        <div className="sidebar-footer">
          <div>West Bengal KVK Network</div>
          <div>All 20 Districts Covered</div>
          <div style={{marginTop:4, color:'rgba(255,255,255,0.3)'}}>v2.0 · Powered by Groq AI</div>
        </div>
      </div>

      <main className="main-content">
        <Routes>
          <Route path="/"        element={<Dashboard district={district} />} />
          <Route path="/report"  element={<ReportGenerator district={district} />} />
          <Route path="/chat"    element={<Chatbot />} />
          <Route path="/market"  element={<MarketPrices />} />
          <Route path="/schemes" element={<Schemes />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}
