import React, { useState, useRef, useEffect } from 'react';
import { sendChat } from '../services/api';

const LANGS = [
  { code: 'en-IN', label: 'English', flag: '🇮🇳' },
  { code: 'bn-IN', label: 'বাংলা',  flag: '🔵' },
  { code: 'hi-IN', label: 'हिन्दी', flag: '🟠' },
];

const SUGGESTIONS = [
  'Best crops for Kharif season?',
  'How to control BPH in rice?',
  'What is PM-KISAN scheme?',
  'Potato planting time in WB?',
];

export default function Chatbot() {
  const [messages, setMessages]     = useState([
    { role: 'bot', content: 'Namaskar! 🙏 I am KrishiBot, your AI farming assistant for West Bengal. Ask me anything about crops, pests, schemes, or market prices — in English, Bengali, or Hindi!', time: new Date() }
  ]);
  const [input, setInput]           = useState('');
  const [loading, setLoading]       = useState(false);
  const [recording, setRecording]   = useState(false);
  const [voiceStatus, setVoiceStatus] = useState('');
  const [lang, setLang]             = useState('en-IN');
  const [autoSpeak, setAutoSpeak]   = useState(false);
  const [speaking, setSpeaking]     = useState(false);
  const messagesEndRef = useRef(null);
  const recognitionRef = useRef(null);

  useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);

  const history = messages
    .filter(m => m.role !== 'system')
    .slice(-10)
    .map(m => ({ role: m.role === 'bot' ? 'assistant' : 'user', content: m.content }));

  const send = async (text) => {
    if (!text.trim()) return;
    const userMsg = { role: 'user', content: text, time: new Date() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);
    try {
      const r = await sendChat(text, history);
      const botMsg = {
        role: 'bot',
        content: r.data.response,
        source: r.data.source,
        time: new Date()
      };
      setMessages(prev => [...prev, botMsg]);
      if (autoSpeak) speakText(r.data.response);
    } catch {
      setMessages(prev => [...prev, { role: 'bot', content: 'Sorry, I am having trouble connecting. Please check if the backend is running.', time: new Date() }]);
    } finally {
      setLoading(false);
    }
  };

  const speakText = (text) => {
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const utt = new SpeechSynthesisUtterance(text);
    utt.lang = lang;
    utt.rate = 0.9;
    const voices = window.speechSynthesis.getVoices();
    const preferred = voices.find(v => v.lang === lang) || voices.find(v => v.lang.startsWith('en'));
    if (preferred) utt.voice = preferred;
    utt.onstart  = () => setSpeaking(true);
    utt.onend    = () => setSpeaking(false);
    utt.onerror  = () => setSpeaking(false);
    window.speechSynthesis.speak(utt);
  };

  const stopSpeaking = () => { window.speechSynthesis.cancel(); setSpeaking(false); };

  const startRecording = () => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { setVoiceStatus('Speech recognition not supported. Use Chrome or Edge.'); return; }
    const rec = new SR();
    rec.lang = lang;
    rec.interimResults = true;
    rec.continuous = false;
    rec.onstart = () => { setRecording(true); setVoiceStatus('🎙️ Listening...'); };
    rec.onresult = (e) => {
      const transcript = Array.from(e.results).map(r => r[0].transcript).join('');
      setVoiceStatus(`🎙️ ${transcript}`);
      if (e.results[e.results.length - 1].isFinal) {
        setInput(transcript);
        setVoiceStatus('');
        setRecording(false);
        send(transcript);
      }
    };
    rec.onerror = (e) => { setVoiceStatus(`Error: ${e.error}`); setRecording(false); };
    rec.onend   = () => { setRecording(false); setVoiceStatus(''); };
    recognitionRef.current = rec;
    rec.start();
  };

  const stopRecording = () => {
    recognitionRef.current?.stop();
    setRecording(false);
    setVoiceStatus('');
  };

  const fmt = (d) => d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  return (
    <div>
      <div className="page-header">
        <h2>🤖 KrishiBot — AI Farming Assistant</h2>
        <p>Powered by Groq LLaMA 3.3 70B · Supports English, Bengali & Hindi</p>
      </div>

      {/* Controls row */}
      <div style={{display:'flex', alignItems:'center', gap:14, marginBottom:14, flexWrap:'wrap'}}>
        <div className="lang-pills">
          {LANGS.map(l => (
            <button key={l.code} className={`lang-pill ${lang === l.code ? 'active' : ''}`} onClick={() => setLang(l.code)}>
              {l.flag} {l.label}
            </button>
          ))}
        </div>
        <label style={{display:'flex', alignItems:'center', gap:6, fontSize:'0.82rem', cursor:'pointer'}}>
          <input type="checkbox" checked={autoSpeak} onChange={e => setAutoSpeak(e.target.checked)}/>
          🔊 Auto-speak replies
        </label>
        {speaking && (
          <button className="btn btn-secondary" style={{padding:'5px 12px', fontSize:'0.78rem'}} onClick={stopSpeaking}>
            ⏹ Stop speaking
          </button>
        )}
      </div>

      {voiceStatus && (
        <div className="voice-status" style={{marginBottom:10}}>
          {voiceStatus}
        </div>
      )}

      {/* Chat window */}
      <div className="chat-container">
        <div className="chat-header">
          <div className="bot-avatar">🌾</div>
          <div>
            <h3>KrishiBot</h3>
            <p>West Bengal Agricultural AI Assistant · {loading ? 'Typing...' : 'Online'}</p>
          </div>
        </div>

        <div className="chat-messages">
          {messages.map((m, i) => (
            <div key={i} style={{display:'flex', flexDirection:'column', alignItems: m.role === 'user' ? 'flex-end' : 'flex-start'}}>
              <div className={`msg-bubble ${m.role}`}>
                {m.content}
                {m.role === 'bot' && (
                  <button
                    onClick={() => speakText(m.content)}
                    style={{background:'none', border:'none', cursor:'pointer', marginLeft:6, fontSize:'0.9rem', opacity:0.6, verticalAlign:'middle'}}
                    title="Speak this message"
                  >🔊</button>
                )}
              </div>
              <div className="msg-meta">
                {m.role === 'bot' && <span>KrishiBot</span>}
                <span>{fmt(m.time)}</span>
                {m.source && <span style={{background: m.source==='groq' ? '#e8f5e9' : '#fff9c4', padding:'1px 6px', borderRadius:8, fontSize:'0.65rem', fontWeight:700, color: m.source==='groq' ? 'var(--green-dark)' : '#f57f17'}}>{m.source}</span>}
              </div>
            </div>
          ))}
          {loading && (
            <div className="msg-bubble bot" style={{alignSelf:'flex-start'}}>
              <span style={{letterSpacing:3}}>●●●</span>
            </div>
          )}
          <div ref={messagesEndRef}/>
        </div>

        {/* Suggestions */}
        {messages.length <= 2 && (
          <div style={{padding:'8px 16px', display:'flex', gap:8, flexWrap:'wrap', background:'var(--white)', borderTop:'1px solid var(--border)'}}>
            {SUGGESTIONS.map((s, i) => (
              <button key={i}
                style={{padding:'5px 12px', borderRadius:20, border:'1px solid var(--border)', background:'var(--green-pale)', fontSize:'0.78rem', cursor:'pointer', color:'var(--text-mid)'}}
                onClick={() => send(s)}
              >{s}</button>
            ))}
          </div>
        )}

        {/* Input bar */}
        <div className="chat-input-bar">
          <button
            className={`mic-btn ${recording ? 'recording' : 'idle'}`}
            onClick={recording ? stopRecording : startRecording}
            title={recording ? 'Stop recording' : 'Speak your question'}
          >
            {recording ? '⏹' : '🎙️'}
          </button>
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && !e.shiftKey && send(input)}
            placeholder={`Ask in ${LANGS.find(l=>l.code===lang)?.label || 'English'}...`}
            disabled={loading}
          />
          <button className="btn btn-primary" onClick={() => send(input)} disabled={loading || !input.trim()}>
            {loading ? '⏳' : '➤ Send'}
          </button>
        </div>
      </div>
    </div>
  );
}
