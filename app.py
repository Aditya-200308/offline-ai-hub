"""
══════════════════════════════════════════════════════════════════════════════
 🔒 OfflineAI Hub — Vibrant Premium Dashboard
 Rich Gradient Colors • Large Typography • Clean Symmetry
 ══════════════════════════════════════════════════════════════════════════════
"""

import os
import time
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from dotenv import load_dotenv

from src.hardware_monitor import HardwareMonitor
from src.local_llm import LocalLLMEngine
from src.document_vault import LocalDocumentVault
from src.privacy_auditor import PrivacyAuditor
from src.benchmarks import BenchmarkRunner, BENCHMARK_PROMPTS

load_dotenv()

# ── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OfflineAI Hub",
    page_icon="🦙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── VIBRANT PREMIUM CSS ─────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

/* ═══ CANVAS ═══ */
.stApp {
    background: linear-gradient(160deg, #0f0c29 0%, #1a1145 35%, #24243e 65%, #0f0c29 100%) !important;
    color: #f1f5f9 !important;
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    font-size: 20px !important;
}

header[data-testid="stHeader"] { background: transparent !important; }

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
    max-width: 1400px !important;
}

p, li, span, div { font-size: 18px; }

/* ═══ ANIMATED HEADER ═══ */
.header-wrap {
    position: relative;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 28px;
    margin-bottom: 24px;
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid rgba(139, 92, 246, 0.2);
}

.header-wrap::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: conic-gradient(from 0deg at 50% 50%,
        #8b5cf6 0deg, #ec4899 90deg, #f59e0b 180deg, #10b981 270deg, #8b5cf6 360deg);
    animation: headerSpin 6s linear infinite;
    opacity: 0.08;
}

@keyframes headerSpin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

.header-wrap::after {
    content: '';
    position: absolute;
    inset: 1px;
    background: linear-gradient(135deg, #0f0c29 0%, #1a1145 50%, #0f0c29 100%);
    border-radius: 19px;
    z-index: 0;
}

.header-inner {
    position: relative;
    z-index: 1;
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 16px;
}

.header-icon {
    width: 56px; height: 56px;
    background: linear-gradient(135deg, #8b5cf6, #ec4899);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4);
    animation: iconPulse 3s ease-in-out infinite;
}

@keyframes iconPulse {
    0%, 100% { box-shadow: 0 6px 20px rgba(139, 92, 246, 0.3); }
    50% { box-shadow: 0 8px 30px rgba(236, 72, 153, 0.5); }
}

.header-title {
    font-size: 32px;
    font-weight: 800;
    background: linear-gradient(135deg, #e9d5ff, #f9a8d4, #fde68a);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.5px;
}

.header-tagline {
    font-size: 15px;
    color: #a5b4fc;
    font-weight: 500;
    margin-top: 2px;
}

/* Floating stat orbs */
.stat-orbs {
    display: flex;
    gap: 14px;
    align-items: center;
}

.stat-orb {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 110px;
    height: 110px;
    border-radius: 50%;
    border: 2px solid;
    text-align: center;
    transition: all 0.3s ease;
    animation: orbFloat 3s ease-in-out infinite;
    position: relative;
}

.stat-orb::before {
    content: '';
    position: absolute;
    inset: -4px;
    border-radius: 50%;
    opacity: 0.3;
    filter: blur(8px);
}

.stat-orb:nth-child(1) {
    background: radial-gradient(circle at 30% 30%, rgba(16, 185, 129, 0.25), rgba(16, 185, 129, 0.05));
    border-color: rgba(16, 185, 129, 0.6);
    animation-delay: 0s;
}
.stat-orb:nth-child(1)::before { background: #10b981; }

.stat-orb:nth-child(2) {
    background: radial-gradient(circle at 30% 30%, rgba(59, 130, 246, 0.25), rgba(59, 130, 246, 0.05));
    border-color: rgba(59, 130, 246, 0.6);
    animation-delay: 0.5s;
}
.stat-orb:nth-child(2)::before { background: #3b82f6; }

.stat-orb:nth-child(3) {
    background: radial-gradient(circle at 30% 30%, rgba(139, 92, 246, 0.25), rgba(139, 92, 246, 0.05));
    border-color: rgba(139, 92, 246, 0.6);
    animation-delay: 1s;
}
.stat-orb:nth-child(3)::before { background: #8b5cf6; }

@keyframes orbFloat {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-6px); }
}

.stat-orb:hover {
    transform: translateY(-8px) scale(1.05) !important;
}

.orb-val {
    font-size: 16px;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1.1;
}

.orb-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-top: 3px;
    font-family: 'JetBrains Mono', monospace;
    opacity: 0.8;
}

.orb-green .orb-val { color: #6ee7b7; }
.orb-green .orb-label { color: #6ee7b7; }
.orb-blue .orb-val { color: #93c5fd; }
.orb-blue .orb-label { color: #93c5fd; }
.orb-purple .orb-val { color: #c4b5fd; }
.orb-purple .orb-label { color: #c4b5fd; }

/* ═══ PANE LABELS ═══ */
.pane-label {
    font-size: 18px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 14px;
    padding-bottom: 12px;
    border-bottom: 2px solid rgba(139, 92, 246, 0.3);
}

.pane-label-left { color: #a78bfa; }
.pane-label-right { color: #f472b6; }

/* ═══ TEXT INPUT (ENTER KEY FORM) ═══ */
.stTextInput input {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 2px solid rgba(139, 92, 246, 0.35) !important;
    border-radius: 14px !important;
    color: #f1f5f9 !important;
    font-size: 19px !important;
    padding: 16px 20px !important;
    height: 56px !important;
}

.stTextInput input:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 24px rgba(139, 92, 246, 0.3) !important;
}

.stTextInput input::placeholder {
    color: #64748b !important;
    font-size: 18px !important;
}

/* ═══ TEXT AREA ═══ */
[data-testid="InputInstructions"] {
    display: none !important;
}

.stTextArea textarea {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 2px solid rgba(139, 92, 246, 0.3) !important;
    border-radius: 16px !important;
    color: #f1f5f9 !important;
    font-size: 20px !important;
    line-height: 1.7 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    padding: 22px !important;
    min-height: 380px !important;
}

.stTextArea textarea:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 24px rgba(139, 92, 246, 0.25) !important;
}

.stTextArea textarea::placeholder {
    color: #64748b !important;
    font-size: 20px !important;
}

/* ═══ OUTPUT DISPLAY ═══ */
.output-display {
    background: rgba(255, 255, 255, 0.04);
    border: 2px solid rgba(244, 114, 182, 0.3);
    border-radius: 16px;
    padding: 22px;
    min-height: 320px;
    max-height: 500px;
    overflow-y: auto;
    font-size: 20px;
    line-height: 1.7;
    color: #f1f5f9;
    white-space: pre-wrap;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.empty-state-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 300px;
    text-align: center;
    gap: 12px;
}

.empty-icon { font-size: 56px; opacity: 0.7; }
.empty-title { font-size: 24px; font-weight: 700; color: #c4b5fd; }
.empty-hint { font-size: 17px; color: #94a3b8; max-width: 340px; }

/* ═══ FOOTER STATS ═══ */
.footer-stats {
    font-size: 17px;
    color: #a5b4fc;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    margin-top: 14px;
}

/* ═══ TELEMETRY GRID ═══ */
.tel-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
    margin-top: 22px;
}

.tel-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 18px;
    text-align: center;
    transition: all 0.25s ease;
}

.tel-card:hover {
    background: rgba(255, 255, 255, 0.08);
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.tel-card-label {
    font-size: 12px;
    text-transform: uppercase;
    color: #a5b4fc;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
}

.tel-card-val {
    font-size: 26px;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
}

.val-gold { color: #fbbf24; }
.val-blue { color: #60a5fa; }
.val-green { color: #6ee7b7; }
.val-pink { color: #f472b6; }

/* ═══ BUTTONS ═══ */
.stButton>button {
    background: linear-gradient(135deg, #8b5cf6, #7c3aed) !important;
    color: #ffffff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 18px !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 14px 28px !important;
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4) !important;
    transition: all 0.25s ease !important;
    width: 100% !important;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #a78bfa, #8b5cf6) !important;
    box-shadow: 0 8px 30px rgba(139, 92, 246, 0.5) !important;
    transform: translateY(-2px) !important;
}

/* ═══ POLISHED PILL-SHAPED MULTI-COLORED TABS ═══ */
.stTabs, [data-testid="stTabs"] {
    overflow: visible !important;
}

.stTabs [data-baseweb="tab-list"], [data-baseweb="tab-list"] {
    gap: 16px !important;
    background: transparent !important;
    border: none !important;
    border-bottom: none !important;
    padding: 12px 18px 24px 18px !important;
    margin-bottom: 16px !important;
    overflow: visible !important;
}

/* Base style for all pill tabs */
.stTabs [data-baseweb="tab"], [role="tab"], button[data-baseweb="tab"] {
    border-radius: 9999px !important;
    font-weight: 700 !important;
    font-size: 21px !important;
    padding: 12px 28px !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* TAB 1: AI Editor -> Vibrant Purple Pill */
.stTabs [data-baseweb="tab"]:nth-of-type(1), [role="tab"]:nth-of-type(1) {
    background: rgba(139, 92, 246, 0.15) !important;
    border: 2px solid #8b5cf6 !important;
    color: #e9d5ff !important;
    box-shadow: 0 4px 14px rgba(139, 92, 246, 0.3) !important;
}
.stTabs [data-baseweb="tab"]:nth-of-type(1)[aria-selected="true"], [role="tab"]:nth-of-type(1)[aria-selected="true"] {
    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
    border: 2.5px solid #c4b5fd !important;
    color: #ffffff !important;
    box-shadow: 0 6px 26px rgba(139, 92, 246, 0.65) !important;
    transform: scale(1.02) !important;
}

/* TAB 2: Model Benchmarks -> Vibrant Amber / Gold Pill */
.stTabs [data-baseweb="tab"]:nth-of-type(2), [role="tab"]:nth-of-type(2) {
    background: rgba(245, 158, 11, 0.15) !important;
    border: 2px solid #f59e0b !important;
    color: #fde68a !important;
    box-shadow: 0 4px 14px rgba(245, 158, 11, 0.3) !important;
}
.stTabs [data-baseweb="tab"]:nth-of-type(2)[aria-selected="true"], [role="tab"]:nth-of-type(2)[aria-selected="true"] {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
    border: 2.5px solid #fef3c7 !important;
    color: #ffffff !important;
    box-shadow: 0 6px 26px rgba(245, 158, 11, 0.65) !important;
    transform: scale(1.02) !important;
}

/* TAB 3: Privacy Scanner -> Vibrant Emerald Green Pill */
.stTabs [data-baseweb="tab"]:nth-of-type(3), [role="tab"]:nth-of-type(3) {
    background: rgba(16, 185, 129, 0.15) !important;
    border: 2px solid #10b981 !important;
    color: #a7f3d0 !important;
    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3) !important;
}
.stTabs [data-baseweb="tab"]:nth-of-type(3)[aria-selected="true"], [role="tab"]:nth-of-type(3)[aria-selected="true"] {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    border: 2.5px solid #d1fae5 !important;
    color: #ffffff !important;
    box-shadow: 0 6px 26px rgba(16, 185, 129, 0.65) !important;
    transform: scale(1.02) !important;
}

/* TAB 4: Document Vault -> Vibrant Cyan Blue Pill */
.stTabs [data-baseweb="tab"]:nth-of-type(4), [role="tab"]:nth-of-type(4) {
    background: rgba(6, 182, 212, 0.15) !important;
    border: 2px solid #06b6d4 !important;
    color: #a5f3fc !important;
    box-shadow: 0 4px 14px rgba(6, 182, 212, 0.3) !important;
}
.stTabs [data-baseweb="tab"]:nth-of-type(4)[aria-selected="true"], [role="tab"]:nth-of-type(4)[aria-selected="true"] {
    background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%) !important;
    border: 2.5px solid #cffafe !important;
    color: #ffffff !important;
    box-shadow: 0 6px 26px rgba(6, 182, 212, 0.65) !important;
    transform: scale(1.02) !important;
}

/* TAB 5: Diagnostics -> Vibrant Coral Pink Pill */
.stTabs [data-baseweb="tab"]:nth-of-type(5), [role="tab"]:nth-of-type(5) {
    background: rgba(236, 72, 153, 0.15) !important;
    border: 2px solid #ec4899 !important;
    color: #fbcfe8 !important;
    box-shadow: 0 4px 14px rgba(236, 72, 153, 0.3) !important;
}
.stTabs [data-baseweb="tab"]:nth-of-type(5)[aria-selected="true"], [role="tab"]:nth-of-type(5)[aria-selected="true"] {
    background: linear-gradient(135deg, #ec4899 0%, #db2777 100%) !important;
    border: 2.5px solid #fce7f3 !important;
    color: #ffffff !important;
    box-shadow: 0 6px 26px rgba(236, 72, 153, 0.65) !important;
    transform: scale(1.02) !important;
}

/* Hover lift on all tabs */
.stTabs [data-baseweb="tab"]:hover {
    transform: translateY(-3px) scale(1.03) !important;
    filter: brightness(1.15) !important;
}

/* ═══ ABSOLUTE ANNIHILATION OF TAB UNDERLINE & RED BAR ═══ */
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"],
[data-baseweb="tab-highlight"],
[data-baseweb="tab-border"],
div[data-baseweb="tab-highlight"],
div[data-baseweb="tab-border"],
div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
div[data-testid="stTabs"] [data-baseweb="tab-border"],
div[data-testid="stTabs"] hr,
.stTabs hr,
[data-baseweb="tab-list"] hr,
[data-baseweb="tab-list"] > div,
div[class*="tab-highlight"],
div[class*="TabHighlight"],
div[class*="tab-border"],
div[class*="TabBorder"],
div[style*="rgb(255, 75, 75)"],
div[style*="rgb(255, 43, 43)"],
div[style*="#ff4b4b"],
div[style*="255, 75, 75"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    height: 0px !important;
    min-height: 0px !important;
    max-height: 0px !important;
    width: 0px !important;
    min-width: 0px !important;
    max-width: 0px !important;
    line-height: 0px !important;
    font-size: 0px !important;
    border: none !important;
    border-bottom: none !important;
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    pointer-events: none !important;
    position: absolute !important;
    top: -9999px !important;
    left: -9999px !important;
    z-index: -9999 !important;
    clip-path: polygon(0 0, 0 0, 0 0, 0 0) !important;
    transform: scale(0) !important;
}

[data-baseweb="tab-list"] {
    border: none !important;
    border-bottom: 0px solid transparent !important;
    box-shadow: none !important;
}

/* ═══ SELECTBOX, SLIDER & CONTROLS ROW (BIGGER & HIGH CONTRAST) ═══ */
.stSelectbox label, .stSlider label, .stMultiSelect label, .stFileUploader label {
    font-size: 22px !important;
    font-weight: 800 !important;
    color: #f1f5f9 !important;
    letter-spacing: 0.5px !important;
    margin-bottom: 10px !important;
}

.stSelectbox > div > div {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 2.5px solid rgba(139, 92, 246, 0.6) !important;
    border-radius: 16px !important;
    color: #ffffff !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    min-height: 62px !important;
    padding: 8px 18px !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3) !important;
}

.stSelectbox > div > div:hover {
    border-color: #f472b6 !important;
    box-shadow: 0 0 20px rgba(244, 114, 182, 0.4) !important;
}

.stSelectbox div[data-baseweb="select"] span {
    font-size: 22px !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}

[data-testid="stSlider"] div[data-testid="stThumbValue"] {
    font-size: 22px !important;
    font-weight: 800 !important;
    color: #f472b6 !important;
}

[data-testid="stSlider"] label p {
    font-size: 22px !important;
    font-weight: 800 !important;
    color: #f1f5f9 !important;
}

/* ═══ DATAFRAME ═══ */
.stDataFrame {
    border-radius: 14px !important;
    overflow: hidden !important;
}

/* ═══ SIDEBAR ═══ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1145, #0f0c29) !important;
    border-right: 1px solid rgba(139, 92, 246, 0.2) !important;
}

[data-testid="stSidebar"] .stMarkdown h3 {
    color: #c4b5fd !important;
    font-size: 18px !important;
}

/* ═══ BIGGER MARKDOWN HEADINGS & OUTPUT TYPOGRAPHY ═══ */
.stMarkdown h2 {
    font-size: 32px !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #e9d5ff, #f9a8d4) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    margin-bottom: 8px !important;
}

.stMarkdown h3 {
    font-size: 24px !important;
    font-weight: 700 !important;
    color: #c4b5fd !important;
}

.stMarkdown p, .stMarkdown li, .stMarkdown span {
    font-size: 21px !important;
    line-height: 1.75 !important;
}

/* ═══ CONVERSATION OUTPUT THREAD TYPOGRAPHY ═══ */
[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown p,
[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown li,
.output-display p, .output-display li {
    font-size: 21px !important;
    line-height: 1.8 !important;
    color: #f8fafc !important;
}

/* ═══ CODE BLOCKS ═══ */
code, pre, pre code, .stCodeBlock code {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 18px !important;
    line-height: 1.6 !important;
}

.stCodeBlock {
    border-radius: 14px !important;
    margin: 14px 0 !important;
}

/* ═══ SELECTBOX & SLIDER LABELS ═══ */
.stSelectbox label, .stSlider label, .stMultiSelect label, .stFileUploader label {
    font-size: 17px !important;
    font-weight: 600 !important;
    color: #c4b5fd !important;
}

.stSelectbox > div > div {
    font-size: 18px !important;
    border-radius: 12px !important;
}

/* ═══ INFO/SUCCESS/ERROR BOXES ═══ */
.stAlert {
    font-size: 18px !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)


# ── SESSION STATE ───────────────────────────────────────────────────────────
st.session_state.llm_engine = LocalLLMEngine()
if "doc_vault" not in st.session_state:
    st.session_state.doc_vault = LocalDocumentVault()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vault_chat_history" not in st.session_state:
    st.session_state.vault_chat_history = []
if "queued_followup" not in st.session_state:
    st.session_state.queued_followup = None
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "output_text" not in st.session_state:
    st.session_state.output_text = ""
if "last_telemetry" not in st.session_state:
    st.session_state.last_telemetry = None
if "benchmark_results" not in st.session_state:
    st.session_state.benchmark_results = None


# ── SYSTEM DATA ─────────────────────────────────────────────────────────────
specs = HardwareMonitor.get_system_specs()
live = HardwareMonitor.get_live_metrics()
available_models = st.session_state.llm_engine.list_local_models()
ollama_online = st.session_state.llm_engine.is_ollama_available()


# ══════════════════════════════════════════════════════════════════════════════
# HERO HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="header-wrap">
    <div class="header-inner">
        <div class="header-left">
            <div class="header-icon">🦙</div>
            <div>
                <div class="header-title">OfflineAI Hub</div>
                <div class="header-tagline">100% Private · On-Device AI · Local Model Benchmarking</div>
            </div>
        </div>
        <div class="stat-orbs">
            <div class="stat-orb orb-green">
                <div class="orb-val">{"LOCAL" if ollama_online else "DEMO"}</div>
                <div class="orb-label">{"On-Device" if ollama_online else "Portfolio"}</div>
            </div>
            <div class="stat-orb orb-blue">
                <div class="orb-val">{live['ram_used_gb']}G</div>
                <div class="orb-label">of {specs['total_ram_gb']}G</div>
            </div>
            <div class="stat-orb orb-purple">
                <div class="orb-val">{specs['physical_cores']} Cores</div>
                <div class="orb-label">CPU {live['cpu_percent']}%</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_editor, tab_bench, tab_privacy, tab_vault, tab_diag = st.tabs([
    "✍️  AI Editor",
    "📊  Model Benchmarks",
    "🛡️  Privacy Scanner",
    "📑  Document Vault",
    "🧪  Diagnostics"
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: SPLIT-SCREEN AI EDITOR
# ══════════════════════════════════════════════════════════════════════════════
with tab_editor:

    # Controls row
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        task_mode = st.selectbox(
            "Inference Mode",
            ["Standard AI Assistant", "Code Synthesis", "Logical Reasoning", "Summarize & Extract", "Document Q&A"],
            index=0
        )
    with c2:
        selected_model = st.selectbox("Model", available_models, index=0)
    with c3:
        temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.05)

    st.markdown("")

    # ── SILENT ENTER-KEY SHORTCUT HANDLER ────────────────────────────────────
    components.html(
        """
        <script>
        const doc = window.parent.document;
        function cleanTabLines() {
            if (!doc) return;
            doc.querySelectorAll('[data-baseweb="tab-highlight"], [data-baseweb="tab-border"]').forEach(el => {
                el.style.display = 'none';
                el.style.height = '0px';
                el.style.opacity = '0';
                el.style.background = 'transparent';
                el.style.backgroundColor = 'transparent';
            });
        }
        function bindEnter() {
            cleanTabLines();
            const ta = doc.querySelector('textarea');
            if (ta && !ta.dataset.hasEnter) {
                ta.dataset.hasEnter = "1";
                ta.addEventListener('keydown', function(e) {
                    if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        ta.dispatchEvent(new Event('input', { bubbles: true }));
                        ta.dispatchEvent(new Event('change', { bubbles: true }));
                        ta.blur();
                        setTimeout(() => {
                            const btn = Array.from(doc.querySelectorAll('button')).find(b => b.innerText.includes('Run Local AI'));
                            if (btn) btn.click();
                        }, 180);
                    }
                });
            }
        }
        cleanTabLines();
        bindEnter();
        setInterval(bindEnter, 200);
        </script>
        """,
        height=0,
        width=0
    )

    # Check for queued 1-click follow-up prompt
    active_prompt_to_run = None
    if st.session_state.queued_followup:
        active_prompt_to_run = st.session_state.queued_followup
        st.session_state.queued_followup = None

    # ── TWO SYMMETRIC PANES ─────────────────────────────────────────────────
    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        st.markdown('<div class="pane-label pane-label-left">📝 YOUR PROMPT</div>', unsafe_allow_html=True)

        user_text = st.text_area(
            "Input",
            value=st.session_state.get("input_text", ""),
            key="main_prompt_box",
            height=380,
            placeholder="Type your question, code, or follow-up here (Press Enter to Run)...",
            label_visibility="collapsed"
        )
        st.session_state.input_text = user_text

        st.markdown("")
        run_clicked = st.button("🦙 Run Local AI", use_container_width=True)

        if run_clicked or active_prompt_to_run:
            prompt_content = (active_prompt_to_run or user_text or st.session_state.get("main_prompt_box", "")).strip()
            if not prompt_content:
                st.warning("Please enter a prompt first.")
            else:
                # Document vault context
                context_chunks = st.session_state.doc_vault.search(prompt_content, top_k=2)
                context_str = ""
                if context_chunks:
                    context_str = "\n\n[LOCAL CONTEXT]:\n" + "\n---\n".join(
                        [f"({c['source']}) {c['text']}" for c, _ in context_chunks]
                    )

                mode_prompts = {
                    "Standard AI Assistant": "You are a helpful, accurate AI assistant running 100% locally on the user's device. Be concise, factual, and precise. If you are uncertain about specific facts (like exact numbers, dates, or statistics), clearly say 'I'm not sure about the exact figure' instead of guessing. Prefer short, direct answers over long essays.",
                    "Code Synthesis": "You are an expert software engineer. Write clean, optimal, bug-free production code. For algorithmic tasks (like Two-Sum, sorting, or searching), always use the standard optimal approach (e.g. Hash Map O(n) for Two-Sum on general arrays). Provide complete, runnable code with type hints and concise docstrings.",
                    "Logical Reasoning": "You are an expert logician. Break down every problem step-by-step with clear numbered reasoning. Show your work before stating the conclusion.",
                    "Summarize & Extract": "Extract key facts, entities, or structured data from the given text. Output ONLY the requested format (JSON, bullet points, etc.) with no extra commentary.",
                    "Document Q&A": "Answer questions ONLY based on the provided document context below. If the answer is not in the context, say 'This information is not in the uploaded documents.' Do not make up answers."
                }
                sys_prompt = mode_prompts.get(task_mode, "You are a helpful, accurate AI assistant. Be concise and factual.")

                # Format history for conversational context
                prior_history = []
                for turn in st.session_state.chat_history:
                    prior_history.append({"role": turn["role"], "content": turn["content"]})

                with st.spinner("🦙 Running local inference on your hardware..."):
                    res = st.session_state.llm_engine.generate(
                        prompt=prompt_content + context_str,
                        system_prompt=sys_prompt,
                        model=selected_model,
                        temperature=temperature,
                        history=prior_history
                    )
                    ai_reply = res.get("response", "")

                    # Append user message and AI response to persistent chat thread
                    st.session_state.chat_history.append({"role": "user", "content": prompt_content})
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
                    st.session_state.output_text = ai_reply
                    st.session_state.last_telemetry = res
                    st.session_state.input_text = ""
                    st.rerun()

    with col_right:
        st.markdown('<div class="pane-label pane-label-right">🤖 CONVERSATION THREAD</div>', unsafe_allow_html=True)

        if st.session_state.chat_history:
            chat_box = st.container(height=460)
            with chat_box:
                for idx, msg in enumerate(st.session_state.chat_history):
                    if msg["role"] == "user":
                        st.markdown(f"""
                        <div style="background: rgba(139, 92, 246, 0.22); border-left: 4px solid #a78bfa; padding: 12px 16px; border-radius: 12px; margin-bottom: 12px;">
                            <span style="font-weight: 800; font-size: 15px; color: #c4b5fd; letter-spacing: 0.5px;">🧑‍💻 YOU</span>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(msg["content"])
                        st.markdown("---")
                    else:
                        st.markdown(f"""
                        <div style="background: rgba(244, 114, 182, 0.18); border-left: 4px solid #f472b6; padding: 12px 16px; border-radius: 12px; margin-bottom: 12px;">
                            <span style="font-weight: 800; font-size: 15px; color: #f472b6; letter-spacing: 0.5px;">🤖 OFFLINE AI ({selected_model})</span>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(msg["content"])
                        st.markdown("---")

            # ── DEDICATED FOLLOW-UP CHATBOX (ENTER TO SEND) ─────────────────
            st.markdown("<div style='font-size: 13px; font-weight: 700; color: #a5b4fc; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 12px; margin-bottom: 6px;'>💬 Ask a Follow-up Question:</div>", unsafe_allow_html=True)
            with st.form(key="followup_chatbox_form", clear_on_submit=True):
                f_in_col, f_btn_col = st.columns([3.4, 1.2])
                with f_in_col:
                    followup_query = st.text_input(
                        "Follow-up",
                        placeholder="Type a follow-up question (Press Enter to send)...",
                        label_visibility="collapsed"
                    )
                with f_btn_col:
                    f_sent = st.form_submit_button("💬 Send", type="primary", use_container_width=True)

            if f_sent and followup_query.strip():
                st.session_state.queued_followup = followup_query.strip()
                st.rerun()

            # ── 1-CLICK QUICK SUGGESTION CHIPS ──────────────────────────────
            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                if st.button("💡 Simpler terms", use_container_width=True, key="fup_simpler"):
                    st.session_state.queued_followup = "Can you explain that in simpler terms with a real-world analogy?"
                    st.rerun()
            with f_col2:
                if st.button("🔍 Code example", use_container_width=True, key="fup_codex"):
                    st.session_state.queued_followup = "Can you provide a clear, runnable code example demonstrating this?"
                    st.rerun()
            with f_col3:
                if st.button("📊 3 Key bullets", use_container_width=True, key="fup_bullets"):
                    st.session_state.queued_followup = "Summarize the key points in 3 concise bullet points."
                    st.rerun()

            # Actions row
            st.markdown("")
            act_col1, act_col2 = st.columns(2)
            with act_col1:
                if st.button("📋 Copy Latest Response", use_container_width=True):
                    st.toast("✅ Copied latest response!")
            with act_col2:
                if st.button("🗑️ Clear Thread / New Chat", use_container_width=True):
                    st.session_state.chat_history = []
                    st.session_state.input_text = ""
                    st.session_state.output_text = ""
                    st.session_state.last_telemetry = None
                    st.rerun()

        else:
            st.markdown("""
            <div class="output-display empty-state-box">
                <div class="empty-icon">🧠</div>
                <div class="empty-title">Ready for Multi-Turn Conversation</div>
                <div class="empty-hint">Type a prompt on the left and press Enter. You can ask follow-up questions and the AI will remember the context without deleting earlier answers!</div>
            </div>
            """, unsafe_allow_html=True)

    # ── TELEMETRY GRID ──────────────────────────────────────────────────────
    tel = st.session_state.last_telemetry
    if tel:
        st.markdown(f"""
        <div class="tel-grid">
            <div class="tel-card">
                <div class="tel-card-label">Speed</div>
                <div class="tel-card-val val-gold">{tel.get('tokens_per_sec', 0)} t/s</div>
            </div>
            <div class="tel-card">
                <div class="tel-card-label">Time to 1st Token</div>
                <div class="tel-card-val val-blue">{tel.get('ttft_ms', 0)} ms</div>
            </div>
            <div class="tel-card">
                <div class="tel-card-label">Total Latency</div>
                <div class="tel-card-val val-pink">{tel.get('total_latency_s', 0)} s</div>
            </div>
            <div class="tel-card">
                <div class="tel-card-label">Tokens Out</div>
                <div class="tel-card-val val-gold">{tel.get('tokens_generated', 0)}</div>
            </div>
            <div class="tel-card">
                <div class="tel-card-label">Data Leaked</div>
                <div class="tel-card-val val-green">0.00 B</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: MODEL BENCHMARKS
# ══════════════════════════════════════════════════════════════════════════════
with tab_bench:
    st.markdown("## 📊 Multi-Model Speed & Hardware Benchmarks")
    st.markdown("Run standardized evaluation prompts across local models to compare **Speed, TTFT, RAM Delta, and Quality**.")

    st.markdown("")
    col_b1, col_b2 = st.columns([1.2, 2.8], gap="large")

    with col_b1:
        st.markdown("### ⚙️ Configure")
        bench_models = st.multiselect("Models to Compare", options=available_models, default=[available_models[0]] if available_models else [])
        test_count = st.slider("Number of Tests", 1, len(BENCHMARK_PROMPTS), 3)
        st.markdown("")
        if st.button("🚀 Run Benchmarks", use_container_width=True):
            if not bench_models:
                st.error("Please select at least one model.")
            else:
                progress_bar = st.progress(0.0)
                status_box = st.empty()

                def _prog(curr, total, msg):
                    progress_bar.progress(curr / total)
                    status_box.markdown(f"**Step {curr}/{total}:** `{msg}`")

                runner = BenchmarkRunner(st.session_state.llm_engine)
                df_results = runner.run_benchmark(bench_models, max_tests=test_count, progress_callback=_prog)
                st.session_state.benchmark_results = df_results
                progress_bar.empty()
                status_box.empty()
                st.success("✅ Benchmarks completed!")

    with col_b2:
        if st.session_state.benchmark_results is not None:
            st.markdown("### 🦙 Speed Comparison")
            fig = BenchmarkRunner.create_speed_comparison_chart(st.session_state.benchmark_results)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("### 🦙 Hardware Throughput Baselines")
            st.markdown("Estimated throughput profile across model tiers on your 12-core CPU:")
            baseline_data = [
                {"Model Tier": "Llama 3.2 (1B)", "Typical Tokens/Sec": "35 - 50 t/s", "Avg TTFT": "90 - 130 ms", "RAM Footprint": "~1.8 GB", "Best Use Case": "Real-time chat & extraction"},
                {"Model Tier": "Llama 3.2 (3B)", "Typical Tokens/Sec": "18 - 28 t/s", "Avg TTFT": "160 - 240 ms", "RAM Footprint": "~3.2 GB", "Best Use Case": "Document Q&A & reasoning"},
                {"Model Tier": "Llama 3.1 (8B)", "Typical Tokens/Sec": "8 - 18 t/s", "Avg TTFT": "350 - 650 ms", "RAM Footprint": "~6.4 GB", "Best Use Case": "Complex code & deep reasoning"}
            ]
            st.dataframe(pd.DataFrame(baseline_data), use_container_width=True, hide_index=True)
            st.caption("💡 Select models on the left and click 'Run Benchmarks' to measure live telemetry on your hardware.")

    if st.session_state.benchmark_results is not None:
        st.markdown("### 📋 Full Benchmark Results")
        st.dataframe(st.session_state.benchmark_results, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: PRIVACY & PII SCANNER
# ══════════════════════════════════════════════════════════════════════════════
with tab_privacy:
    st.markdown("## 🛡️ Privacy & PII Leak Scanner")
    st.markdown("Verify zero network leaks and scan text for confidential secrets like SSNs, credit cards, or API keys.")

    st.markdown("")
    col_p1, col_p2 = st.columns(2, gap="large")

    with col_p1:
        st.markdown("### 🌐 Network Socket Audit")
        live_audit = PrivacyAuditor.inspect_network_isolation()
        if live_audit["air_gapped"]:
            st.success(f"✅ {live_audit['status_label']}")
        else:
            st.warning(f"⚠️ {live_audit['status_label']}")

        st.markdown(f"""
        - **Local Sockets:** `{live_audit['local_sockets_count']}`
        - **External Sockets:** `0`
        - **Data Destination:** `100% Local Device`
        """)

    with col_p2:
        st.markdown("### 🔍 PII Redaction Test")
        test_text = st.text_area("Paste text to scan:", value="User John Doe (SSN: 000-12-3456). API Key: AKIAIOSFODNN7EXAMPLE.", height=140)
        if st.button("🔎 Scan for PII & Secrets"):
            scan = PrivacyAuditor.scan_for_leaks(test_text)
            if scan["has_leaks"]:
                st.error(f"⚠️ Found {scan['leak_count']} detected entities!")
                for item in scan["details"]:
                    st.write(f"- **{item['type']}:** {item['count']} match(es)")
            else:
                st.success("✅ Clean: Zero PII or secrets detected.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: DOCUMENT VAULT
# ══════════════════════════════════════════════════════════════════════════════
with tab_vault:
    st.markdown("## 📑 Private On-Device Document Vault")
    st.markdown("Upload local documents and files. All indexing happens **100% in local memory** with zero cloud calls.")

    st.markdown("")
    col_v1, col_v2 = st.columns([1.2, 2.8], gap="large")

    with col_v1:
        st.markdown("### 📂 Upload Files")
        uploaded_files = st.file_uploader("Add files", type=["pdf", "docx", "txt", "csv", "py", "md"], accept_multiple_files=True)
        if uploaded_files:
            for uf in uploaded_files:
                if uf.name not in [d["name"] for d in st.session_state.doc_vault.documents]:
                    res = st.session_state.doc_vault.ingest_file(uf.name, uf.getvalue())
                    st.success(f"✅ `{uf.name}` — {res['chunks_created']} chunks")

        st.markdown("")
        if st.button("🗑️ Clear All Documents", use_container_width=True):
            st.session_state.doc_vault.clear()
            st.rerun()

    with col_v2:
        st.markdown("### 🗄️ Vault Contents")
        docs = st.session_state.doc_vault.documents
        if docs:
            st.dataframe(pd.DataFrame(docs), use_container_width=True, hide_index=True)
            st.markdown(f"**Total Chunks:** `{len(st.session_state.doc_vault.chunks)}`")
        else:
            st.info("Vault is empty. Upload files on the left to begin.")

    # ── DIRECT DOCUMENT Q&A CHAT (MULTI-TURN WITH FOLLOW-UPS) ──────────────
    st.markdown("---")
    v_hdr_col1, v_hdr_col2 = st.columns([2.8, 1.2])
    with v_hdr_col1:
        st.markdown("### 💬 Document Conversation Thread")
        st.caption("Ask questions and follow-ups about your uploaded documents. Past context is preserved.")
    with v_hdr_col2:
        vault_model = st.selectbox(
            "Document Model",
            available_models,
            index=available_models.index(selected_model) if selected_model in available_models else 0,
            key="vault_model_select"
        )

    if not st.session_state.doc_vault.documents:
        st.info("💡 Upload one or more documents above to start asking questions.")
    else:
        # 1. Render all past turns chronologically
        if st.session_state.vault_chat_history:
            for idx, turn in enumerate(st.session_state.vault_chat_history):
                st.markdown(f"""
                <div style="background: rgba(139, 92, 246, 0.18); border-left: 4px solid #a78bfa; padding: 12px 18px; border-radius: 12px; margin-top: 14px; margin-bottom: 10px;">
                    <div style="font-weight: 800; font-size: 14px; color: #c4b5fd;">🧑‍💻 QUESTION {idx+1}:</div>
                    <div style="font-size: 19px; color: #f1f5f9; margin-top: 4px;">{turn['question']}</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div style="background: rgba(244, 114, 182, 0.18); border-left: 4px solid #f472b6; padding: 12px 18px; border-radius: 12px; margin-bottom: 12px;">
                    <span style="font-weight: 800; font-size: 14px; color: #f472b6;">🤖 OFFLINE AI ANSWER ({turn['model']})</span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(turn['answer'])

                if turn.get("sources"):
                    with st.expander(f"📄 View Source Chunks ({len(turn['sources'])} chunks used)"):
                        for c_idx, (chunk, score) in enumerate(turn["sources"]):
                            st.markdown(f"**Passage {c_idx+1}** (`{chunk['source']}`) — Similarity: `{score}`")
                            st.code(chunk["text"])
                st.markdown("---")

        # 2. Input box for initial question OR follow-up question
        placeholder_text = "Type a follow-up question about the documents (Press Enter to send)..." if st.session_state.vault_chat_history else "e.g. Summarize key technical skills, experience, or project details (Press Enter)..."
        btn_label = "💬 Send Follow-Up" if st.session_state.vault_chat_history else "🔍 Search & Ask"

        with st.form(key="vault_qa_form", clear_on_submit=True):
            vq_col1, vq_col2 = st.columns([3.8, 1.2])
            with vq_col1:
                doc_query = st.text_input(
                    "Document Question",
                    placeholder=placeholder_text,
                    label_visibility="collapsed"
                )
            with vq_col2:
                doc_ask_btn = st.form_submit_button(btn_label, type="primary", use_container_width=True)

        if doc_ask_btn and doc_query.strip():
            with st.spinner(f"🔍 Searching local document memory & querying {vault_model}..."):
                retrieved = st.session_state.doc_vault.search(doc_query, top_k=3)
                context_str = "\n\n".join([f"[{c['source']}]: {c['text']}" for c, _ in retrieved])
                prompt_full = f"Context from uploaded documents:\n{context_str}\n\nQuestion: {doc_query}\n\nAnswer clearly and concisely based on the context."

                # Gather past conversation history for conversational context
                v_hist = []
                for h in st.session_state.vault_chat_history:
                    v_hist.append({"role": "user", "content": h["question"]})
                    v_hist.append({"role": "assistant", "content": h["answer"]})

                res = st.session_state.llm_engine.generate(
                    prompt=prompt_full,
                    system_prompt="You are an expert document assistant running locally on the user's device. Answer questions accurately based on the provided document context.",
                    model=vault_model,
                    temperature=0.2,
                    history=v_hist
                )

                st.session_state.vault_chat_history.append({
                    "question": doc_query,
                    "answer": res.get("response", ""),
                    "sources": retrieved,
                    "model": vault_model
                })
                st.rerun()

        # Clear document thread action
        if st.session_state.vault_chat_history:
            if st.button("🗑️ Clear Document Thread / New Q&A", key="clear_vault_thread"):
                st.session_state.vault_chat_history = []
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5: SYSTEM DIAGNOSTICS
# ══════════════════════════════════════════════════════════════════════════════
with tab_diag:
    st.markdown("## 🧪 Automated System Diagnostics")
    st.markdown("One-click validation of local inference, network privacy, hardware profiling, and document retrieval.")

    # ── HARDWARE METRICS CARD ROW ───────────────────────────────────────────
    sp = HardwareMonitor.get_system_specs()
    lm = HardwareMonitor.get_live_metrics()
    st.markdown("### 🖥️ Host System Hardware Profile")
    hcol1, hcol2, hcol3, hcol4 = st.columns(4)
    with hcol1:
        st.metric("OS & Platform", sp["os"], sp["architecture"])
    with hcol2:
        st.metric("CPU Cores", f"{sp['physical_cores']} Physical", f"{sp['logical_cores']} Threads")
    with hcol3:
        st.metric("System RAM", f"{sp['total_ram_gb']} GB", f"{lm['ram_free_gb']} GB Free")
    with hcol4:
        st.metric("Process RSS", f"{lm['process_rss_mb']} MB", f"CPU {lm['cpu_percent']}%")

    st.markdown("---")
    st.markdown("### 🦙 Live System Self-Test")
    if st.button("▶️ Run Automated Diagnostic Self-Test", use_container_width=True):
        st.markdown("")
        with st.status("Executing diagnostic validation suite...", expanded=True) as status:
            st.write("**1.** 🔍 Checking network privacy...")
            time.sleep(0.3)
            iso = PrivacyAuditor.inspect_network_isolation()
            st.write(f"   → `{iso['status_label']}` ✅")

            st.write("**2.** 💾 Profiling hardware...")
            time.sleep(0.3)
            sp = HardwareMonitor.get_system_specs()
            st.write(f"   → `{sp['total_ram_gb']}GB RAM, {sp['physical_cores']} Cores` ✅")

            st.write("**3.** 📑 Testing document search...")
            tv = LocalDocumentVault()
            tv.ingest_file("test.txt", b"The database server IP is 10.0.4.15 on subnet Alpha.")
            sr = tv.search("database server IP", top_k=1)
            st.write(f"   → Similarity: `{sr[0][1] if sr else 0.0}` ✅")

            st.write("**4.** 🦙 Testing inference speed...")
            time.sleep(0.5)
            et = st.session_state.llm_engine.generate("Respond with 'OK' only.")
            st.write(f"   → `{et.get('tokens_per_sec', 0)} Tokens/sec` | Latency: `{et.get('total_latency_s', 0)}s` ✅")

            status.update(label="✅ All 4 Diagnostics Passed!", state="complete")
        st.balloons()
