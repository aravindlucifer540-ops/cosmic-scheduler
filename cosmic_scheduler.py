#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════╗
║       COSMIC SCHEDULER — Universe Edition        ║
║   Daily Planner · Stats · Week Comparison        ║
╚══════════════════════════════════════════════════╝
Run: python cosmic_scheduler.py
Requires: pip install flask
"""

from flask import Flask, render_template_string, request, jsonify
import json, os, datetime

app = Flask(__name__)
DATA_FILE = "schedule_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"tasks": {}, "completions": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>COSMIC SCHEDULER</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
  :root {
    --void: #020408;
    --deep: #060d18;
    --nebula1: #0a1628;
    --nebula2: #0d1f3c;
    --star: #e8f4fd;
    --pulsar: #00d4ff;
    --quasar: #7c3aed;
    --nova: #f59e0b;
    --done: #10b981;
    --undone: #ef4444;
    --glow1: rgba(0,212,255,0.15);
    --glow2: rgba(124,58,237,0.15);
    --border: rgba(0,212,255,0.2);
    --glass: rgba(6,13,24,0.85);
  }

  * { margin:0; padding:0; box-sizing:border-box; }

  body {
    background: var(--void);
    color: var(--star);
    font-family: 'Rajdhani', sans-serif;
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* ── STARFIELD ── */
  #cosmos {
    position: fixed; inset: 0; z-index: 0;
    background:
      radial-gradient(ellipse at 20% 20%, rgba(124,58,237,0.08) 0%, transparent 50%),
      radial-gradient(ellipse at 80% 80%, rgba(0,212,255,0.06) 0%, transparent 50%),
      radial-gradient(ellipse at 50% 50%, rgba(245,158,11,0.03) 0%, transparent 70%),
      #020408;
  }

  .star-layer {
    position: absolute; inset: 0;
    background-image:
      radial-gradient(1px 1px at 10% 15%, rgba(232,244,253,0.9) 0%, transparent 100%),
      radial-gradient(1px 1px at 25% 40%, rgba(232,244,253,0.7) 0%, transparent 100%),
      radial-gradient(1.5px 1.5px at 40% 5%, rgba(232,244,253,0.8) 0%, transparent 100%),
      radial-gradient(1px 1px at 55% 70%, rgba(232,244,253,0.6) 0%, transparent 100%),
      radial-gradient(1px 1px at 70% 25%, rgba(232,244,253,0.9) 0%, transparent 100%),
      radial-gradient(1.5px 1.5px at 85% 55%, rgba(232,244,253,0.7) 0%, transparent 100%),
      radial-gradient(1px 1px at 92% 10%, rgba(232,244,253,0.8) 0%, transparent 100%),
      radial-gradient(1px 1px at 15% 80%, rgba(232,244,253,0.5) 0%, transparent 100%),
      radial-gradient(2px 2px at 60% 90%, rgba(0,212,255,0.6) 0%, transparent 100%),
      radial-gradient(1px 1px at 35% 60%, rgba(232,244,253,0.7) 0%, transparent 100%),
      radial-gradient(1px 1px at 78% 78%, rgba(232,244,253,0.6) 0%, transparent 100%),
      radial-gradient(1.5px 1.5px at 5% 50%, rgba(124,58,237,0.7) 0%, transparent 100%),
      radial-gradient(1px 1px at 48% 35%, rgba(232,244,253,0.8) 0%, transparent 100%),
      radial-gradient(1px 1px at 90% 40%, rgba(232,244,253,0.6) 0%, transparent 100%),
      radial-gradient(2px 2px at 20% 95%, rgba(245,158,11,0.5) 0%, transparent 100%);
    animation: twinkle 6s ease-in-out infinite alternate;
  }

  .star-layer:nth-child(2) {
    background-image:
      radial-gradient(1px 1px at 8% 30%, rgba(232,244,253,0.6) 0%, transparent 100%),
      radial-gradient(1px 1px at 30% 20%, rgba(232,244,253,0.8) 0%, transparent 100%),
      radial-gradient(1.5px 1.5px at 52% 48%, rgba(0,212,255,0.5) 0%, transparent 100%),
      radial-gradient(1px 1px at 67% 60%, rgba(232,244,253,0.7) 0%, transparent 100%),
      radial-gradient(1px 1px at 75% 12%, rgba(232,244,253,0.9) 0%, transparent 100%),
      radial-gradient(2px 2px at 88% 85%, rgba(124,58,237,0.6) 0%, transparent 100%),
      radial-gradient(1px 1px at 43% 75%, rgba(232,244,253,0.5) 0%, transparent 100%),
      radial-gradient(1px 1px at 18% 62%, rgba(232,244,253,0.7) 0%, transparent 100%);
    animation-delay: 3s;
    animation-duration: 8s;
  }

  @keyframes twinkle {
    0%   { opacity: 0.4; }
    50%  { opacity: 1; }
    100% { opacity: 0.6; }
  }

  /* ── NEBULA CLOUDS ── */
  .nebula {
    position: fixed; border-radius: 50%; filter: blur(80px);
    animation: drift 20s ease-in-out infinite alternate;
    pointer-events: none; z-index: 0;
  }
  .nebula-1 { width:500px; height:400px; background:rgba(124,58,237,0.07); top:-100px; left:-100px; }
  .nebula-2 { width:600px; height:500px; background:rgba(0,212,255,0.05); bottom:-150px; right:-150px; animation-delay:-10s; }
  .nebula-3 { width:300px; height:300px; background:rgba(245,158,11,0.04); top:40%; left:50%; animation-delay:-5s; }

  @keyframes drift {
    0%   { transform: translate(0,0) scale(1); }
    100% { transform: translate(30px,20px) scale(1.05); }
  }

  /* ── LAYOUT ── */
  #app { position: relative; z-index: 1; max-width: 1400px; margin: 0 auto; padding: 20px; }

  /* ── HEADER ── */
  header {
    text-align: center; padding: 30px 0 20px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 30px;
    position: relative;
  }

  .logo-text {
    font-family: 'Orbitron', monospace;
    font-size: clamp(1.8rem, 4vw, 3rem);
    font-weight: 900;
    background: linear-gradient(135deg, var(--pulsar), var(--quasar), var(--nova));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: 6px;
    text-shadow: none;
    animation: logoGlow 4s ease-in-out infinite alternate;
  }

  @keyframes logoGlow {
    from { filter: drop-shadow(0 0 10px rgba(0,212,255,0.4)); }
    to   { filter: drop-shadow(0 0 25px rgba(124,58,237,0.6)); }
  }

  .tagline {
    font-family: 'Share Tech Mono', monospace;
    color: rgba(0,212,255,0.6);
    font-size: 0.75rem;
    letter-spacing: 4px;
    margin-top: 6px;
  }

  .live-time {
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.4rem;
    color: var(--pulsar);
    margin-top: 10px;
    text-shadow: 0 0 20px var(--pulsar);
  }

  /* ── NAV TABS ── */
  .nav-tabs {
    display: flex; gap: 4px; justify-content: center;
    margin-bottom: 30px; flex-wrap: wrap;
  }

  .tab-btn {
    font-family: 'Orbitron', monospace;
    font-size: 0.7rem;
    letter-spacing: 2px;
    padding: 10px 22px;
    background: transparent;
    border: 1px solid var(--border);
    color: rgba(232,244,253,0.5);
    cursor: pointer;
    transition: all 0.3s;
    clip-path: polygon(8px 0%, 100% 0%, calc(100% - 8px) 100%, 0% 100%);
  }

  .tab-btn:hover, .tab-btn.active {
    background: linear-gradient(135deg, var(--glow1), var(--glow2));
    border-color: var(--pulsar);
    color: var(--pulsar);
    text-shadow: 0 0 10px var(--pulsar);
    box-shadow: 0 0 20px rgba(0,212,255,0.2);
  }

  /* ── PANELS ── */
  .panel { display: none; animation: panelIn 0.4s ease; }
  .panel.active { display: block; }

  @keyframes panelIn {
    from { opacity:0; transform: translateY(15px); }
    to   { opacity:1; transform: translateY(0); }
  }

  /* ── GLASS CARD ── */
  .glass {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: 12px;
    backdrop-filter: blur(20px);
    padding: 24px;
    position: relative;
    overflow: hidden;
  }

  .glass::before {
    content: '';
    position: absolute; top:0; left:0; right:0; height:1px;
    background: linear-gradient(90deg, transparent, var(--pulsar), transparent);
    opacity: 0.5;
  }

  .section-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.75rem;
    letter-spacing: 4px;
    color: var(--pulsar);
    margin-bottom: 20px;
    display: flex; align-items: center; gap: 10px;
  }

  .section-title::after {
    content: ''; flex:1; height:1px;
    background: linear-gradient(90deg, var(--border), transparent);
  }

  /* ── DATE SELECTOR ── */
  .date-nav {
    display: flex; align-items: center; justify-content: center;
    gap: 20px; margin-bottom: 24px;
  }

  .date-nav button {
    background: var(--glow1);
    border: 1px solid var(--border);
    color: var(--pulsar);
    width: 36px; height: 36px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 1.2rem;
    transition: all 0.3s;
    display: flex; align-items: center; justify-content: center;
  }
  .date-nav button:hover { background: rgba(0,212,255,0.3); box-shadow: 0 0 15px var(--pulsar); }

  .current-date {
    font-family: 'Orbitron', monospace;
    font-size: 1.1rem;
    color: var(--star);
    min-width: 200px;
    text-align: center;
  }

  /* ── TASK LIST ── */
  .task-item {
    display: flex; align-items: center; gap: 14px;
    padding: 14px 16px;
    margin-bottom: 10px;
    background: rgba(6,13,24,0.6);
    border: 1px solid var(--border);
    border-radius: 8px;
    transition: all 0.3s;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }

  .task-item::before {
    content: ''; position: absolute; left:0; top:0; bottom:0;
    width: 3px;
    background: var(--undone);
    transition: background 0.3s;
  }

  .task-item.done::before { background: var(--done); }
  .task-item:hover { border-color: var(--pulsar); box-shadow: 0 0 15px rgba(0,212,255,0.1); }

  .task-dot {
    width: 14px; height: 14px;
    border-radius: 50%;
    flex-shrink: 0;
    background: var(--undone);
    box-shadow: 0 0 8px var(--undone);
    transition: all 0.3s;
    border: 2px solid rgba(0,0,0,0.3);
  }

  .task-item.done .task-dot {
    background: var(--done);
    box-shadow: 0 0 12px var(--done);
    animation: pulse-green 2s infinite;
  }

  @keyframes pulse-green {
    0%, 100% { box-shadow: 0 0 8px var(--done); }
    50%       { box-shadow: 0 0 20px var(--done), 0 0 30px rgba(16,185,129,0.3); }
  }

  .task-info { flex: 1; }

  .task-name {
    font-size: 1rem;
    font-weight: 600;
    color: var(--star);
    transition: color 0.3s;
  }

  .task-item.done .task-name { color: rgba(232,244,253,0.4); text-decoration: line-through; }

  .task-time {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    color: rgba(0,212,255,0.6);
    margin-top: 2px;
  }

  .task-category {
    font-size: 0.65rem;
    letter-spacing: 2px;
    padding: 2px 8px;
    border-radius: 20px;
    background: rgba(124,58,237,0.2);
    border: 1px solid rgba(124,58,237,0.3);
    color: rgba(124,58,237,0.9);
  }

  .task-delete {
    background: none; border: none; color: rgba(239,68,68,0.4);
    cursor: pointer; font-size: 1rem; padding: 4px;
    transition: all 0.3s; border-radius: 4px;
  }
  .task-delete:hover { color: var(--undone); background: rgba(239,68,68,0.1); }

  /* ── ADD TASK FORM ── */
  .add-form {
    display: grid;
    grid-template-columns: 1fr 1fr auto;
    gap: 10px;
    margin-top: 20px;
    flex-wrap: wrap;
  }

  .cosmic-input {
    background: rgba(2,4,8,0.8);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 10px 14px;
    color: var(--star);
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.95rem;
    transition: all 0.3s;
    outline: none;
    width: 100%;
  }

  .cosmic-input:focus {
    border-color: var(--pulsar);
    box-shadow: 0 0 15px rgba(0,212,255,0.15);
  }

  .cosmic-input option { background: var(--deep); }

  .cosmic-btn {
    background: linear-gradient(135deg, rgba(0,212,255,0.2), rgba(124,58,237,0.2));
    border: 1px solid var(--pulsar);
    color: var(--pulsar);
    padding: 10px 20px;
    font-family: 'Orbitron', monospace;
    font-size: 0.7rem;
    letter-spacing: 2px;
    cursor: pointer;
    border-radius: 6px;
    transition: all 0.3s;
    white-space: nowrap;
  }

  .cosmic-btn:hover {
    background: linear-gradient(135deg, rgba(0,212,255,0.4), rgba(124,58,237,0.4));
    box-shadow: 0 0 20px rgba(0,212,255,0.3);
    transform: translateY(-1px);
  }

  /* ── PROGRESS RING ── */
  .progress-section {
    display: flex; align-items: center; justify-content: center;
    gap: 40px; margin-bottom: 30px; flex-wrap: wrap;
  }

  .progress-ring-wrap {
    position: relative; display: flex; flex-direction: column; align-items: center; gap: 8px;
  }

  .progress-ring-wrap svg { transform: rotate(-90deg); }

  .ring-track { fill: none; stroke: rgba(232,244,253,0.06); }
  .ring-fill  { fill: none; stroke-linecap: round; transition: stroke-dashoffset 0.8s cubic-bezier(0.4,0,0.2,1); }

  .ring-label {
    position: absolute; top:50%; left:50%;
    transform: translate(-50%,-50%);
    text-align: center;
  }

  .ring-pct {
    font-family: 'Orbitron', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--pulsar);
  }

  .ring-sub { font-size: 0.65rem; color: rgba(232,244,253,0.4); letter-spacing: 2px; }
  .ring-title { font-size: 0.7rem; letter-spacing: 2px; color: rgba(232,244,253,0.5); text-align: center; }

  /* ── STATS GRID ── */
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px,1fr));
    gap: 14px;
    margin-bottom: 30px;
  }

  .stat-card {
    background: rgba(6,13,24,0.7);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
    text-align: center;
    transition: all 0.3s;
  }

  .stat-card:hover { border-color: var(--pulsar); box-shadow: 0 0 20px rgba(0,212,255,0.1); }

  .stat-val {
    font-family: 'Orbitron', monospace;
    font-size: 1.8rem;
    font-weight: 700;
  }

  .stat-val.green { color: var(--done); text-shadow: 0 0 15px var(--done); }
  .stat-val.red   { color: var(--undone); text-shadow: 0 0 15px var(--undone); }
  .stat-val.cyan  { color: var(--pulsar); text-shadow: 0 0 15px var(--pulsar); }
  .stat-val.gold  { color: var(--nova); text-shadow: 0 0 15px var(--nova); }

  .stat-label { font-size: 0.65rem; letter-spacing: 2px; color: rgba(232,244,253,0.4); margin-top: 4px; }

  /* ── WEEK CHART ── */
  .week-chart {
    display: flex; gap: 10px; align-items: flex-end;
    height: 160px; padding: 10px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 14px;
  }

  .day-bar-wrap {
    flex: 1; display: flex; flex-direction: column;
    align-items: center; gap: 6px; height: 100%;
    justify-content: flex-end;
  }

  .day-bar-container {
    width: 100%; flex: 1; display: flex;
    align-items: flex-end; position: relative;
    max-height: 120px;
  }

  .day-bar {
    width: 100%;
    border-radius: 4px 4px 0 0;
    transition: height 0.8s cubic-bezier(0.4,0,0.2,1);
    min-height: 4px;
    position: relative;
    overflow: hidden;
  }

  .day-bar::after {
    content: '';
    position: absolute; top:0; left:0; right:0; bottom:0;
    background: linear-gradient(180deg, rgba(255,255,255,0.15), transparent);
  }

  .bar-done   { background: linear-gradient(180deg, var(--done), rgba(16,185,129,0.5)); box-shadow: 0 -4px 15px rgba(16,185,129,0.3); }
  .bar-undone { background: linear-gradient(180deg, var(--undone), rgba(239,68,68,0.5)); box-shadow: 0 -4px 15px rgba(239,68,68,0.3); }
  .bar-today  { background: linear-gradient(180deg, var(--pulsar), rgba(0,212,255,0.5)); box-shadow: 0 -4px 20px rgba(0,212,255,0.5); }

  .day-label { font-family: 'Share Tech Mono', monospace; font-size: 0.65rem; color: rgba(232,244,253,0.5); }
  .day-pct   { font-family: 'Orbitron', monospace; font-size: 0.6rem; color: rgba(232,244,253,0.7); }

  /* ── WEEK COMPARE ── */
  .compare-grid {
    display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 20px;
  }

  .week-card {
    background: rgba(6,13,24,0.6);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px;
  }

  .week-card-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.65rem;
    letter-spacing: 3px;
    color: var(--nova);
    margin-bottom: 14px;
  }

  .week-dots {
    display: flex; gap: 6px; flex-wrap: wrap;
  }

  .week-dot {
    width: 18px; height: 18px;
    border-radius: 50%;
    transition: all 0.3s;
    position: relative;
  }

  .week-dot.dot-done   { background: var(--done); box-shadow: 0 0 10px rgba(16,185,129,0.5); }
  .week-dot.dot-undone { background: var(--undone); box-shadow: 0 0 8px rgba(239,68,68,0.4); }
  .week-dot.dot-empty  { background: rgba(232,244,253,0.08); border: 1px solid rgba(232,244,253,0.1); }
  .week-dot.dot-today  { ring: 2px solid var(--pulsar); box-shadow: 0 0 12px var(--pulsar); }

  .week-dot:hover::after {
    content: attr(data-tip);
    position: absolute; bottom: 22px; left: 50%;
    transform: translateX(-50%);
    background: var(--nebula2); border: 1px solid var(--border);
    padding: 3px 7px; border-radius: 4px;
    font-size: 0.6rem; white-space: nowrap;
    color: var(--star); z-index: 10;
    font-family: 'Share Tech Mono', monospace;
  }

  /* ── CALENDAR ── */
  .calendar-grid {
    display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px;
  }

  .cal-header {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 2px;
    color: rgba(0,212,255,0.5);
    text-align: center;
    padding: 6px 0;
  }

  .cal-day {
    aspect-ratio: 1;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    border-radius: 6px;
    cursor: pointer;
    border: 1px solid transparent;
    transition: all 0.3s;
    font-size: 0.85rem;
    font-weight: 600;
    position: relative;
    gap: 2px;
  }

  .cal-day:hover { border-color: var(--pulsar); background: rgba(0,212,255,0.05); }
  .cal-day.today { border-color: var(--pulsar); background: rgba(0,212,255,0.1); color: var(--pulsar); }
  .cal-day.selected { background: rgba(0,212,255,0.2); border-color: var(--pulsar); box-shadow: 0 0 12px rgba(0,212,255,0.2); }
  .cal-day.other-month { opacity: 0.25; }

  .cal-indicator {
    width: 5px; height: 5px; border-radius: 50%; flex-shrink: 0;
  }

  /* ── TIMELINE VIEW ── */
  .timeline {
    position: relative;
    padding-left: 30px;
  }

  .timeline::before {
    content: ''; position: absolute; left: 10px; top: 0; bottom: 0;
    width: 1px; background: linear-gradient(180deg, var(--pulsar), transparent);
  }

  .timeline-item {
    position: relative; margin-bottom: 12px; padding: 12px 14px;
    background: rgba(6,13,24,0.6); border: 1px solid var(--border);
    border-radius: 8px; transition: all 0.3s;
    display: flex; align-items: center; gap: 12px;
    cursor: pointer;
  }

  .timeline-item:hover { border-color: var(--pulsar); }

  .timeline-item::before {
    content: ''; position: absolute; left: -25px; top: 50%;
    transform: translateY(-50%);
    width: 10px; height: 10px; border-radius: 50%;
    border: 2px solid var(--void);
    transition: all 0.3s;
  }

  .timeline-item.done::before { background: var(--done); box-shadow: 0 0 10px var(--done); }
  .timeline-item:not(.done)::before { background: var(--undone); box-shadow: 0 0 8px var(--undone); }

  /* ── SCROLLBAR ── */
  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-track { background: var(--void); }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

  /* ── GRID LAYOUT ── */
  .main-grid {
    display: grid;
    grid-template-columns: 1fr 380px;
    gap: 20px;
  }

  @media (max-width: 900px) { .main-grid { grid-template-columns: 1fr; } }

  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  @media (max-width: 700px) { .grid-2 { grid-template-columns: 1fr; } .compare-grid { grid-template-columns: 1fr; } }

  /* ── LEGEND ── */
  .legend { display: flex; gap: 20px; justify-content: center; margin-bottom: 16px; flex-wrap: wrap; }
  .legend-item { display: flex; align-items: center; gap: 6px; font-size: 0.75rem; color: rgba(232,244,253,0.5); }
  .legend-dot { width: 10px; height: 10px; border-radius: 50%; }

  /* ── MODAL ── */
  .modal-backdrop {
    display: none; position: fixed; inset: 0;
    background: rgba(0,0,0,0.7); z-index: 100;
    align-items: center; justify-content: center;
    backdrop-filter: blur(5px);
  }
  .modal-backdrop.open { display: flex; }

  .modal {
    background: var(--nebula1);
    border: 1px solid var(--pulsar);
    border-radius: 16px;
    padding: 30px;
    width: 400px; max-width: 90vw;
    box-shadow: 0 0 60px rgba(0,212,255,0.2);
    animation: modalIn 0.3s ease;
  }

  @keyframes modalIn {
    from { opacity:0; transform: scale(0.9) translateY(-20px); }
    to   { opacity:1; transform: scale(1) translateY(0); }
  }

  .modal-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.85rem;
    letter-spacing: 3px;
    color: var(--pulsar);
    margin-bottom: 20px;
  }

  .form-group { margin-bottom: 14px; }
  .form-label { display: block; font-size: 0.7rem; letter-spacing: 2px; color: rgba(232,244,253,0.5); margin-bottom: 6px; }

  .modal-actions { display: flex; gap: 10px; margin-top: 20px; justify-content: flex-end; }

  .btn-cancel {
    background: none; border: 1px solid rgba(232,244,253,0.2);
    color: rgba(232,244,253,0.5); padding: 8px 18px;
    border-radius: 6px; cursor: pointer;
    font-family: 'Rajdhani', sans-serif; font-size: 0.9rem;
    transition: all 0.3s;
  }
  .btn-cancel:hover { border-color: var(--undone); color: var(--undone); }

  /* ── TOAST ── */
  .toast {
    position: fixed; bottom: 30px; right: 30px;
    background: var(--nebula2);
    border: 1px solid var(--pulsar);
    border-radius: 8px;
    padding: 12px 20px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    color: var(--pulsar);
    z-index: 200;
    transform: translateX(200%);
    transition: transform 0.4s cubic-bezier(0.4,0,0.2,1);
    box-shadow: 0 0 30px rgba(0,212,255,0.2);
  }
  .toast.show { transform: translateX(0); }

  /* ── SCANNING LINE ── */
  .scan-line {
    position: fixed; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg, transparent, var(--pulsar), transparent);
    animation: scan 6s linear infinite;
    opacity: 0.3; z-index: 5; pointer-events: none;
  }
  @keyframes scan { from { top:-2px; } to { top:100vh; } }

  /* ── COMPLETION ANIMATION ── */
  @keyframes completeFlash {
    0%   { box-shadow: 0 0 0 rgba(16,185,129,0); }
    50%  { box-shadow: 0 0 30px rgba(16,185,129,0.5); }
    100% { box-shadow: 0 0 0 rgba(16,185,129,0); }
  }
  .flash { animation: completeFlash 0.6s ease; }

  .empty-state {
    text-align: center; padding: 40px;
    color: rgba(232,244,253,0.2);
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 2px;
  }

  .orbit-icon { font-size: 2rem; margin-bottom: 10px; }
</style>
</head>
<body>

<div id="cosmos">
  <div class="star-layer"></div>
  <div class="star-layer"></div>
</div>
<div class="nebula nebula-1"></div>
<div class="nebula nebula-2"></div>
<div class="nebula nebula-3"></div>
<div class="scan-line"></div>

<div id="app">
  <header>
    <div class="logo-text">◈ COSMIC SCHEDULER ◈</div>
    <div class="tagline">MISSION CONTROL · DAILY ORBIT PLANNER</div>
    <div class="live-time" id="liveTime">--:--:--</div>
  </header>

  <nav class="nav-tabs">
    <button class="tab-btn active" onclick="switchTab('today')">⬡ TODAY</button>
    <button class="tab-btn" onclick="switchTab('stats')">◎ STATS</button>
    <button class="tab-btn" onclick="switchTab('week')">⊕ WEEK VIEW</button>
    <button class="tab-btn" onclick="switchTab('calendar')">◉ CALENDAR</button>
  </nav>

  <!-- TODAY PANEL -->
  <div id="panel-today" class="panel active">
    <div class="main-grid">
      <div>
        <div class="glass">
          <div class="section-title">◈ MISSION TASKS</div>
          <div class="date-nav">
            <button onclick="changeDay(-1)">◀</button>
            <div class="current-date" id="todayLabel">—</div>
            <button onclick="changeDay(+1)">▶</button>
          </div>

          <div class="progress-section">
            <div class="progress-ring-wrap">
              <svg width="110" height="110" viewBox="0 0 110 110">
                <circle class="ring-track" cx="55" cy="55" r="46" stroke-width="7"/>
                <circle class="ring-fill" id="ringFill" cx="55" cy="55" r="46"
                  stroke="url(#ringGrad)" stroke-width="7"
                  stroke-dasharray="289" stroke-dashoffset="289"/>
                <defs>
                  <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="#00d4ff"/>
                    <stop offset="100%" stop-color="#7c3aed"/>
                  </linearGradient>
                </defs>
              </svg>
              <div class="ring-label">
                <div class="ring-pct" id="ringPct">0%</div>
                <div class="ring-sub">DONE</div>
              </div>
              <div class="ring-title">DAILY PROGRESS</div>
            </div>
          </div>

          <div id="taskList"></div>

          <div class="add-form" style="margin-top:20px;">
            <input class="cosmic-input" id="newTaskName" placeholder="New mission task..." type="text" onkeypress="if(event.key==='Enter')addTask()">
            <input class="cosmic-input" id="newTaskTime" placeholder="Time (e.g. 09:00)" type="time">
            <button class="cosmic-btn" onclick="addTask()">＋ ADD</button>
          </div>
          <div style="display:flex;gap:10px;margin-top:8px;">
            <select class="cosmic-input" id="newTaskCat" style="flex:1">
              <option value="WORK">WORK</option>
              <option value="HEALTH">HEALTH</option>
              <option value="LEARNING">LEARNING</option>
              <option value="PERSONAL">PERSONAL</option>
              <option value="SOCIAL">SOCIAL</option>
              <option value="OTHER">OTHER</option>
            </select>
          </div>
        </div>
      </div>

      <div style="display:flex;flex-direction:column;gap:16px;">
        <div class="glass">
          <div class="section-title">◎ ORBIT STATUS</div>
          <div class="stats-grid" style="grid-template-columns:1fr 1fr;">
            <div class="stat-card">
              <div class="stat-val green" id="statDone">0</div>
              <div class="stat-label">COMPLETED</div>
            </div>
            <div class="stat-card">
              <div class="stat-val red" id="statUndone">0</div>
              <div class="stat-label">PENDING</div>
            </div>
            <div class="stat-card" style="grid-column:1/-1">
              <div class="stat-val gold" id="statStreak">0</div>
              <div class="stat-label">DAY STREAK 🔥</div>
            </div>
          </div>
        </div>

        <div class="glass">
          <div class="section-title">⊕ TIMELINE</div>
          <div id="timelineView" class="timeline"></div>
        </div>
      </div>
    </div>
  </div>

  <!-- STATS PANEL -->
  <div id="panel-stats" class="panel">
    <div class="glass" style="margin-bottom:20px;">
      <div class="section-title">◎ WEEKLY PERFORMANCE RADAR</div>
      <div class="week-chart" id="weekChart"></div>
      <div style="display:flex;justify-content:space-between;padding:0 4px;">
        <span style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:rgba(232,244,253,0.3)">MON</span>
        <span style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:rgba(232,244,253,0.3)">TUE</span>
        <span style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:rgba(232,244,253,0.3)">WED</span>
        <span style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:rgba(232,244,253,0.3)">THU</span>
        <span style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:rgba(232,244,253,0.3)">FRI</span>
        <span style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:rgba(232,244,253,0.3)">SAT</span>
        <span style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:rgba(232,244,253,0.3)">SUN</span>
      </div>
    </div>

    <div class="grid-2">
      <div class="glass">
        <div class="section-title">◈ ALL-TIME STATS</div>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-val cyan" id="totalTasks">0</div>
            <div class="stat-label">TOTAL TASKS</div>
          </div>
          <div class="stat-card">
            <div class="stat-val green" id="totalDone">0</div>
            <div class="stat-label">COMPLETED</div>
          </div>
          <div class="stat-card">
            <div class="stat-val gold" id="bestDay">0%</div>
            <div class="stat-label">BEST DAY</div>
          </div>
          <div class="stat-card">
            <div class="stat-val" id="avgRate" style="color:var(--quasar);text-shadow:0 0 15px var(--quasar)">0%</div>
            <div class="stat-label">AVG RATE</div>
          </div>
        </div>
      </div>

      <div class="glass">
        <div class="section-title">⬡ CATEGORY BREAKDOWN</div>
        <div id="categoryBreakdown"></div>
      </div>
    </div>
  </div>

  <!-- WEEK PANEL -->
  <div id="panel-week" class="panel">
    <div class="glass" style="margin-bottom:20px;">
      <div class="section-title">⊕ WEEK-TO-WEEK COMPARISON</div>
      <div style="display:flex;gap:10px;justify-content:center;margin-bottom:20px;">
        <button class="cosmic-btn" onclick="changeWeek(-1)">◀ PREV WEEK</button>
        <div id="weekLabel" style="font-family:'Orbitron',monospace;font-size:0.8rem;color:var(--nova);display:flex;align-items:center;padding:0 20px;"></div>
        <button class="cosmic-btn" onclick="changeWeek(+1)">NEXT WEEK ▶</button>
      </div>
      <div id="weekDotGrid"></div>
    </div>

    <div class="compare-grid">
      <div class="glass">
        <div class="week-card-title">◀ PREVIOUS WEEK</div>
        <div id="prevWeekStats"></div>
      </div>
      <div class="glass">
        <div class="week-card-title">▶ CURRENT WEEK</div>
        <div id="currWeekStats"></div>
      </div>
    </div>
  </div>

  <!-- CALENDAR PANEL -->
  <div id="panel-calendar" class="panel">
    <div class="glass">
      <div class="section-title">◉ MISSION CALENDAR</div>
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;">
        <button class="cosmic-btn" onclick="changeCalMonth(-1)">◀ PREV</button>
        <div id="calTitle" style="font-family:'Orbitron',monospace;font-size:1rem;color:var(--nova);"></div>
        <button class="cosmic-btn" onclick="changeCalMonth(+1)">NEXT ▶</button>
      </div>
      <div class="calendar-grid" id="calGrid"></div>
      <div class="legend" style="margin-top:20px;">
        <div class="legend-item"><div class="legend-dot" style="background:var(--done)"></div>≥80% done</div>
        <div class="legend-item"><div class="legend-dot" style="background:var(--nova)"></div>50–79%</div>
        <div class="legend-item"><div class="legend-dot" style="background:var(--undone)"></div>&lt;50% done</div>
        <div class="legend-item"><div class="legend-dot" style="background:rgba(232,244,253,0.15)"></div>no tasks</div>
      </div>
    </div>
  </div>
</div>

<!-- EDIT MODAL -->
<div class="modal-backdrop" id="editModal">
  <div class="modal">
    <div class="modal-title">◈ EDIT MISSION TASK</div>
    <input type="hidden" id="editTaskKey">
    <input type="hidden" id="editTaskDate">
    <div class="form-group">
      <label class="form-label">TASK NAME</label>
      <input class="cosmic-input" id="editTaskName" type="text">
    </div>
    <div class="form-group">
      <label class="form-label">TIME</label>
      <input class="cosmic-input" id="editTaskTime" type="time">
    </div>
    <div class="form-group">
      <label class="form-label">CATEGORY</label>
      <select class="cosmic-input" id="editTaskCat">
        <option>WORK</option><option>HEALTH</option>
        <option>LEARNING</option><option>PERSONAL</option>
        <option>SOCIAL</option><option>OTHER</option>
      </select>
    </div>
    <div class="modal-actions">
      <button class="btn-cancel" onclick="closeModal()">CANCEL</button>
      <button class="cosmic-btn" onclick="saveEdit()">SAVE MISSION</button>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
let state = { tasks: {}, completions: {} };
let currentDate = new Date();
let calMonth = new Date();
let weekOffset = 0;

const dateKey = d => `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
const today = () => dateKey(new Date());

async function loadState() {
  const r = await fetch('/api/data');
  state = await r.json();
  renderAll();
}

async function saveState() {
  await fetch('/api/save', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify(state)
  });
}

function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2500);
}

// ── TIME ──
function updateTime() {
  const now = new Date();
  document.getElementById('liveTime').textContent =
    now.toLocaleTimeString('en-US', {hour12:false}) +
    ' · ' + now.toLocaleDateString('en-US', {weekday:'long',month:'short',day:'numeric'});
}
setInterval(updateTime, 1000); updateTime();

// ── TABS ──
function switchTab(name) {
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('panel-'+name).classList.add('active');
  event.target.classList.add('active');
  if(name==='stats') renderStats();
  if(name==='week')  renderWeekView();
  if(name==='calendar') renderCalendar();
}

// ── DATE NAV ──
function changeDay(d) {
  currentDate = new Date(currentDate); currentDate.setDate(currentDate.getDate()+d);
  renderToday();
}

// ── TASK OPS ──
function getTasksForDate(dk) { return state.tasks[dk] || []; }
function getCompletionsForDate(dk) { return state.completions[dk] || []; }

function addTask() {
  const name = document.getElementById('newTaskName').value.trim();
  if(!name) { toast('⚠ Enter a task name'); return; }
  const time = document.getElementById('newTaskTime').value || '00:00';
  const cat  = document.getElementById('newTaskCat').value;
  const dk   = dateKey(currentDate);
  if(!state.tasks[dk]) state.tasks[dk] = [];
  const id = Date.now().toString();
  state.tasks[dk].push({id, name, time, cat});
  state.tasks[dk].sort((a,b)=>a.time.localeCompare(b.time));
  document.getElementById('newTaskName').value='';
  document.getElementById('newTaskTime').value='';
  saveState(); renderToday();
  toast('◈ Task added to orbit');
}

function toggleTask(dk, id) {
  if(!state.completions[dk]) state.completions[dk]=[];
  const idx = state.completions[dk].indexOf(id);
  if(idx>-1) state.completions[dk].splice(idx,1);
  else state.completions[dk].push(id);
  saveState(); renderToday();
  if(idx===-1) toast('✓ Mission accomplished!');
}

function deleteTask(dk, id) {
  state.tasks[dk] = (state.tasks[dk]||[]).filter(t=>t.id!==id);
  state.completions[dk] = (state.completions[dk]||[]).filter(i=>i!==id);
  saveState(); renderToday();
  toast('◌ Task removed from orbit');
}

function openEditModal(dk, id) {
  const task = (state.tasks[dk]||[]).find(t=>t.id===id);
  if(!task) return;
  document.getElementById('editTaskKey').value = id;
  document.getElementById('editTaskDate').value = dk;
  document.getElementById('editTaskName').value = task.name;
  document.getElementById('editTaskTime').value = task.time;
  document.getElementById('editTaskCat').value  = task.cat||'OTHER';
  document.getElementById('editModal').classList.add('open');
}

function closeModal() { document.getElementById('editModal').classList.remove('open'); }

function saveEdit() {
  const id   = document.getElementById('editTaskKey').value;
  const dk   = document.getElementById('editTaskDate').value;
  const name = document.getElementById('editTaskName').value.trim();
  if(!name) return;
  const task = (state.tasks[dk]||[]).find(t=>t.id===id);
  if(task) {
    task.name = name;
    task.time = document.getElementById('editTaskTime').value;
    task.cat  = document.getElementById('editTaskCat').value;
    state.tasks[dk].sort((a,b)=>a.time.localeCompare(b.time));
  }
  closeModal(); saveState(); renderToday();
  toast('◈ Mission updated');
}

// ── RENDER TODAY ──
function renderToday() {
  const dk     = dateKey(currentDate);
  const tasks  = getTasksForDate(dk);
  const done   = getCompletionsForDate(dk);
  const doneSet = new Set(done);
  const pct    = tasks.length ? Math.round(doneSet.size/tasks.length*100) : 0;

  const days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  document.getElementById('todayLabel').textContent =
    `${days[currentDate.getDay()].toUpperCase()}, ${months[currentDate.getMonth()]} ${currentDate.getDate()}, ${currentDate.getFullYear()}`;

  // Ring
  const circ = 289;
  document.getElementById('ringFill').style.strokeDashoffset = circ - (pct/100)*circ;
  document.getElementById('ringPct').textContent = pct+'%';

  // Stats
  document.getElementById('statDone').textContent = doneSet.size;
  document.getElementById('statUndone').textContent = tasks.length - doneSet.size;
  document.getElementById('statStreak').textContent = calcStreak();

  // Task list
  const list = document.getElementById('taskList');
  if(!tasks.length) {
    list.innerHTML = '<div class="empty-state"><div class="orbit-icon">○</div>NO MISSIONS SCHEDULED<br>ADD TASKS BELOW</div>';
  } else {
    list.innerHTML = tasks.map(t => {
      const isDone = doneSet.has(t.id);
      return `<div class="task-item ${isDone?'done':''}" id="ti-${t.id}">
        <div class="task-dot" onclick="toggleTask('${dk}','${t.id}')"></div>
        <div class="task-info" onclick="toggleTask('${dk}','${t.id}')">
          <div class="task-name">${t.name}</div>
          <div class="task-time">${t.time||'--:--'}</div>
        </div>
        <span class="task-category">${t.cat||'OTHER'}</span>
        <button class="cosmic-btn" style="padding:5px 10px;font-size:0.6rem;" onclick="openEditModal('${dk}','${t.id}')">EDIT</button>
        <button class="task-delete" onclick="deleteTask('${dk}','${t.id}')">✕</button>
      </div>`;
    }).join('');
  }

  // Timeline
  const tl = document.getElementById('timelineView');
  if(!tasks.length) {
    tl.innerHTML = '<div class="empty-state" style="padding:20px">NO DATA</div>';
  } else {
    tl.innerHTML = tasks.map(t => {
      const isDone = doneSet.has(t.id);
      return `<div class="timeline-item ${isDone?'done':''}" onclick="toggleTask('${dk}','${t.id}')">
        <div style="font-family:'Share Tech Mono',monospace;font-size:0.7rem;color:var(--pulsar);min-width:45px">${t.time}</div>
        <div>
          <div style="font-size:0.9rem;font-weight:600">${t.name}</div>
          <div style="font-size:0.65rem;color:rgba(232,244,253,0.4);letter-spacing:1px">${t.cat}</div>
        </div>
        <div style="margin-left:auto;width:8px;height:8px;border-radius:50%;flex-shrink:0;
          background:${isDone?'var(--done)':'var(--undone)'};
          box-shadow:0 0 8px ${isDone?'var(--done)':'var(--undone)'}">
        </div>
      </div>`;
    }).join('');
  }
}

// ── STREAK ──
function calcStreak() {
  let streak = 0;
  const d = new Date();
  while(true) {
    const dk = dateKey(d);
    const tasks = getTasksForDate(dk);
    if(!tasks.length) break;
    const done = getCompletionsForDate(dk);
    if(done.length === tasks.length && tasks.length > 0) streak++;
    else break;
    d.setDate(d.getDate()-1);
  }
  return streak;
}

// ── RENDER STATS ──
function renderStats() {
  // Week chart (current week Mon–Sun)
  const now = new Date();
  const dayOfWeek = now.getDay();
  const mondayOffset = dayOfWeek === 0 ? -6 : 1 - dayOfWeek;
  const monday = new Date(now);
  monday.setDate(now.getDate() + mondayOffset);

  const chart = document.getElementById('weekChart');
  let html = '';
  let totalT=0,totalD=0,rates=[],bestPct=0;

  for(let i=0;i<7;i++) {
    const d = new Date(monday); d.setDate(monday.getDate()+i);
    const dk = dateKey(d);
    const tasks = getTasksForDate(dk);
    const done = getCompletionsForDate(dk).length;
    const pct = tasks.length ? Math.round(done/tasks.length*100) : 0;
    if(tasks.length) { rates.push(pct); if(pct>bestPct) bestPct=pct; }
    totalT+=tasks.length; totalD+=done;
    const isToday = dk===today();
    const barClass = isToday?'bar-today':(pct>=50?'bar-done':'bar-undone');
    const barH = tasks.length ? Math.max(8, pct*1.1) : 4;
    html += `<div class="day-bar-wrap">
      <div class="day-bar-container">
        <div class="day-bar ${barClass}" style="height:${barH}px" title="${pct}% (${done}/${tasks.length})"></div>
      </div>
      <div class="day-pct">${tasks.length?pct+'%':'-'}</div>
    </div>`;
  }
  chart.innerHTML = html;

  document.getElementById('totalTasks').textContent = totalT;
  document.getElementById('totalDone').textContent  = totalD;
  document.getElementById('bestDay').textContent    = bestPct+'%';
  document.getElementById('avgRate').textContent    = rates.length ? Math.round(rates.reduce((a,b)=>a+b,0)/rates.length)+'%' : '0%';

  // Category
  const catMap = {};
  Object.entries(state.tasks).forEach(([dk,tasks]) => {
    const done = new Set(getCompletionsForDate(dk));
    tasks.forEach(t => {
      if(!catMap[t.cat]) catMap[t.cat]={total:0,done:0};
      catMap[t.cat].total++;
      if(done.has(t.id)) catMap[t.cat].done++;
    });
  });
  const catColors = {WORK:'var(--pulsar)',HEALTH:'var(--done)',LEARNING:'var(--nova)',PERSONAL:'var(--quasar)',SOCIAL:'#f472b6',OTHER:'rgba(232,244,253,0.4)'};
  const cb = document.getElementById('categoryBreakdown');
  if(!Object.keys(catMap).length) {
    cb.innerHTML='<div class="empty-state" style="padding:20px">NO DATA YET</div>';
  } else {
    cb.innerHTML = Object.entries(catMap).map(([cat,{total,done}])=>{
      const p = Math.round(done/total*100);
      const col = catColors[cat]||'var(--pulsar)';
      return `<div style="margin-bottom:12px">
        <div style="display:flex;justify-content:space-between;font-size:0.75rem;margin-bottom:4px">
          <span style="letter-spacing:2px;font-family:'Share Tech Mono',monospace;color:${col}">${cat}</span>
          <span style="color:rgba(232,244,253,0.5)">${done}/${total} · ${p}%</span>
        </div>
        <div style="height:6px;background:rgba(232,244,253,0.06);border-radius:3px;overflow:hidden">
          <div style="height:100%;width:${p}%;background:${col};border-radius:3px;
            box-shadow:0 0 8px ${col};transition:width 0.8s ease"></div>
        </div>
      </div>`;
    }).join('');
  }
}

// ── WEEK VIEW ──
function renderWeekView() {
  const now = new Date();
  const dayOfWeek = now.getDay();
  const mondayOffset = dayOfWeek===0?-6:1-dayOfWeek;

  // Current selected week
  const currMonday = new Date(now);
  currMonday.setDate(now.getDate()+mondayOffset+weekOffset*7);
  const prevMonday = new Date(currMonday);
  prevMonday.setDate(currMonday.getDate()-7);

  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const fmtWeek = m => `${months[m.getMonth()]} ${m.getDate()}`;
  const endCurr = new Date(currMonday); endCurr.setDate(currMonday.getDate()+6);
  const endPrev = new Date(prevMonday); endPrev.setDate(prevMonday.getDate()+6);

  document.getElementById('weekLabel').textContent =
    `${fmtWeek(currMonday)} – ${fmtWeek(endCurr)}, ${currMonday.getFullYear()}`;

  const days = ['M','T','W','T','F','S','S'];
  let dotHtml='<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:8px;margin-bottom:12px;">';
  dotHtml += days.map((d,i)=>`<div style="text-align:center;font-family:\'Share Tech Mono\',monospace;font-size:0.6rem;color:rgba(0,212,255,0.5);padding:4px">${d}</div>`).join('');
  dotHtml += '</div><div style="display:grid;grid-template-columns:repeat(7,1fr);gap:8px;">';

  for(let i=0;i<7;i++) {
    const d = new Date(currMonday); d.setDate(currMonday.getDate()+i);
    const dk = dateKey(d);
    const tasks = getTasksForDate(dk);
    const done = getCompletionsForDate(dk).length;
    const pct = tasks.length ? done/tasks.length : -1;
    const isToday = dk===today();
    let dotClass = 'dot-empty';
    let col = 'rgba(232,244,253,0.08)';
    if(pct>=0) { dotClass=pct>=0.8?'dot-done':pct>=0.5?'':'dot-undone'; col=pct>=0.8?'var(--done)':pct>=0.5?'var(--nova)':'var(--undone)'; }
    const label = tasks.length?`${done}/${tasks.length} (${Math.round(pct*100)}%)`:'No tasks';
    const todayStyle = isToday?'outline:2px solid var(--pulsar);outline-offset:2px;':'';
    dotHtml+=`<div style="display:flex;flex-direction:column;align-items:center;gap:6px">
      <div class="week-dot" style="background:${col};box-shadow:0 0 10px ${col};width:24px;height:24px;border-radius:50%;${todayStyle}" data-tip="${label}"></div>
      <div style="font-family:\'Share Tech Mono\',monospace;font-size:0.58rem;color:rgba(232,244,253,0.3)">${d.getDate()}</div>
    </div>`;
  }
  dotHtml+='</div>';
  document.getElementById('weekDotGrid').innerHTML=dotHtml;

  // Comparison stats
  const calcWeekStats = monday => {
    let total=0,done=0;
    for(let i=0;i<7;i++) {
      const d=new Date(monday); d.setDate(monday.getDate()+i);
      const dk=dateKey(d);
      const tasks=getTasksForDate(dk);
      total+=tasks.length;
      done+=getCompletionsForDate(dk).length;
    }
    return {total,done,pct:total?Math.round(done/total*100):0};
  };

  const curr=calcWeekStats(currMonday);
  const prev=calcWeekStats(prevMonday);
  const diff=curr.pct-prev.pct;
  const diffColor=diff>=0?'var(--done)':'var(--undone)';
  const diffSign=diff>=0?'▲':'▼';

  document.getElementById('prevWeekStats').innerHTML=`
    <div style="text-align:center;margin-bottom:10px">
      <div style="font-family:'Orbitron',monospace;font-size:2rem;color:${prev.pct>=50?'var(--done)':'var(--undone)'}">
        ${prev.pct}%</div>
      <div style="font-size:0.75rem;color:rgba(232,244,253,0.4);margin-top:4px">${prev.done}/${prev.total} tasks</div>
    </div>
    <div style="font-size:0.7rem;color:rgba(232,244,253,0.3);text-align:center;font-family:'Share Tech Mono',monospace">
      ${fmtWeek(prevMonday)} – ${fmtWeek(endPrev)}
    </div>`;

  document.getElementById('currWeekStats').innerHTML=`
    <div style="text-align:center;margin-bottom:10px">
      <div style="font-family:'Orbitron',monospace;font-size:2rem;color:${curr.pct>=50?'var(--done)':'var(--undone)'}">
        ${curr.pct}%</div>
      <div style="font-size:0.75rem;color:rgba(232,244,253,0.4);margin-top:4px">${curr.done}/${curr.total} tasks</div>
    </div>
    <div style="font-size:0.7rem;color:rgba(232,244,253,0.3);text-align:center;font-family:'Share Tech Mono',monospace;margin-bottom:8px">
      ${fmtWeek(currMonday)} – ${fmtWeek(endCurr)}
    </div>
    <div style="text-align:center;font-size:0.8rem;color:${diffColor};font-family:'Orbitron',monospace">
      ${diffSign} ${Math.abs(diff)}% vs prev week
    </div>`;
}

function changeWeek(d) { weekOffset+=d; renderWeekView(); }

// ── CALENDAR ──
function renderCalendar() {
  const months=['January','February','March','April','May','June','July','August','September','October','November','December'];
  document.getElementById('calTitle').textContent=`${months[calMonth.getMonth()]} ${calMonth.getFullYear()}`;
  const grid=document.getElementById('calGrid');
  const days=['SUN','MON','TUE','WED','THU','FRI','SAT'];
  let html=days.map(d=>`<div class="cal-header">${d}</div>`).join('');

  const first=new Date(calMonth.getFullYear(),calMonth.getMonth(),1);
  const last=new Date(calMonth.getFullYear(),calMonth.getMonth()+1,0);
  const startPad=first.getDay();

  // Prev month padding
  for(let i=0;i<startPad;i++) {
    const d=new Date(first); d.setDate(1-startPad+i);
    html+=calDayHTML(d,true);
  }
  for(let i=1;i<=last.getDate();i++) {
    const d=new Date(calMonth.getFullYear(),calMonth.getMonth(),i);
    html+=calDayHTML(d,false);
  }
  // Next month padding
  const endPad=6-last.getDay();
  for(let i=1;i<=endPad;i++) {
    const d=new Date(last); d.setDate(last.getDate()+i);
    html+=calDayHTML(d,true);
  }

  grid.innerHTML=html;
}

function calDayHTML(d,otherMonth) {
  const dk=dateKey(d);
  const tasks=getTasksForDate(dk);
  const done=getCompletionsForDate(dk).length;
  const isToday=dk===today();
  const isSelected=dk===dateKey(currentDate);
  let indColor='rgba(232,244,253,0.15)';
  if(tasks.length) {
    const p=done/tasks.length;
    indColor=p>=0.8?'var(--done)':p>=0.5?'var(--nova)':'var(--undone)';
  }
  let cls='cal-day';
  if(otherMonth)cls+=' other-month';
  if(isToday)cls+=' today';
  if(isSelected)cls+=' selected';
  return `<div class="${cls}" onclick="selectCalDay('${dk}')">
    <span>${d.getDate()}</span>
    ${tasks.length?`<div class="cal-indicator" style="background:${indColor}"></div>`:''}
  </div>`;
}

function selectCalDay(dk) {
  const parts=dk.split('-');
  currentDate=new Date(+parts[0],+parts[1]-1,+parts[2]);
  renderCalendar();
  switchTab('today');
  document.querySelectorAll('.tab-btn').forEach((b,i)=>{if(i===0)b.classList.add('active');else b.classList.remove('active');});
  renderToday();
}

function changeCalMonth(d) { calMonth.setMonth(calMonth.getMonth()+d); renderCalendar(); }

function renderAll() { renderToday(); }

// Close modal on backdrop click
document.getElementById('editModal').addEventListener('click',e=>{ if(e.target===e.currentTarget) closeModal(); });

// Init
loadState();
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/api/data')
def get_data():
    return jsonify(load_data())

@app.route('/api/save', methods=['POST'])
def save():
    data = request.get_json()
    save_data(data)
    return jsonify({"ok": True})

if __name__ == '__main__':
    print("\n" + "═"*55)
    print("  ◈  COSMIC SCHEDULER — Universe Edition  ◈")
    print("═"*55)
    print("  ► Open your browser: http://localhost:5000")
    print("  ► Data saved locally in: schedule_data.json")
    print("  ► Press Ctrl+C to stop the server")
    print("═"*55 + "\n")
    app.run(debug=False, port=5000)
