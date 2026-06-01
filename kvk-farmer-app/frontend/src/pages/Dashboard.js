import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { getWeather, getMarket, getAdvisory } from '../services/api';

export default function Dashboard({ district }) {
  const [weather, setWeather]   = useState(null);
  const [market, setMarket]     = useState([]);
  const [advisory, setAdvisory] = useState([]);
  const [loading, setLoading]   = useState(true);

  useEffect(() => {
    setLoading(true);
    Promise.all([
      getWeather(district),
      getMarket(),
      getAdvisory('Kharif'),
    ]).then(([w, m, a]) => {
      setWeather(w.data);
      setMarket(m.data);
      setAdvisory(a.data);
    }).finally(() => setLoading(false));
  }, [district]);

  if (loading) return <div className="loading-wrap"><div className="spinner"/><span>Loading dashboard...</span></div>;

  const curr = weather?.current || {};
  const forecast = weather?.forecast || [];

  const chartData = market.slice(0, 6).map(m => ({
    name: m.crop,
    MSP: m.msp || 0,
    Market: m.market_price,
  }));

  return (
    <div>
      <div className="page-header">
        <h2>🏠 Dashboard — {district}</h2>
        <p>Real-time farm advisory and weather for your district</p>
      </div>

      {/* Weather tiles */}
      <div className="grid-4" style={{marginBottom:22}}>
        <div className="stat-tile">
          <span className="label">🌡️ Temperature</span>
          <span className="value">{curr.temperature}°C</span>
          <span className="sub">{curr.season} Season</span>
        </div>
        <div className="stat-tile">
          <span className="label">💧 Humidity</span>
          <span className="value">{curr.humidity}%</span>
          <span className="sub">Relative Humidity</span>
        </div>
        <div className="stat-tile">
          <span className="label">🌧️ Rainfall</span>
          <span className="value">{curr.rainfall} mm</span>
          <span className="sub">Monthly Average</span>
        </div>
        <div className="stat-tile">
          <span className="label">💨 Wind</span>
          <span className="value">{curr.wind_speed} km/h</span>
          <span className="sub">{curr.conditions}</span>
        </div>
      </div>

      {/* 7-day forecast */}
      <div className="card" style={{marginBottom:22}}>
        <div className="card-title">📅 7-Day Forecast</div>
        <div className="forecast-strip">
          {forecast.map((f, i) => (
            <div className="forecast-day" key={i}>
              <div className="day-name">{f.day}</div>
              <div className="day-temp">{f.max_temp}°</div>
              <div style={{fontSize:'0.68rem', color:'#546e7a'}}>{f.min_temp}°</div>
              <div className="day-rain">🌧 {f.rain_chance}%</div>
            </div>
          ))}
        </div>
      </div>

      <div className="grid-2">
        {/* Market chart */}
        <div className="card">
          <div className="card-title">📊 MSP vs Market Prices (₹/quintal)</div>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={chartData} margin={{top:5, right:10, bottom:5, left:0}}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e8f5e9"/>
              <XAxis dataKey="name" tick={{fontSize:11}}/>
              <YAxis tick={{fontSize:11}}/>
              <Tooltip/>
              <Bar dataKey="MSP" fill="#a5d6a7" radius={[3,3,0,0]}/>
              <Bar dataKey="Market" fill="#1a6b2e" radius={[3,3,0,0]}/>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Advisory */}
        <div className="card">
          <div className="card-title">🌿 Seasonal Advisory</div>
          <ul className="advisory-list">
            {advisory.map((tip, i) => (
              <li key={i}>{tip}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
