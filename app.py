import streamlit as st
from streamlit_folium import st_folium

from services.geocoder import get_coordinates
from services.data_loader import get_services
from services.analytics import calculate_metrics
from utils.map_generator import create_map
from utils.pdf_generator import generate_pdf


# =========================
# Page Config
# =========================

st.set_page_config(
    page_title="CrisisGrid",
    page_icon="🚨",
    layout="wide"
)


# =========================
# Command Center CSS
# =========================

st.markdown("""
<style>

/* ── Reset & Base ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #080C14 !important;
    color: #CBD5E1;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
}

[data-testid="stMain"] { background: #080C14 !important; }
[data-testid="stHeader"] { background: transparent !important; }
#MainMenu, footer, [data-testid="stToolbar"] { display: none !important; visibility: hidden !important; }

/* ── System Status Bar ── */
.cg-statusbar {
    background: #0D1521;
    border: 1px solid #1E3A5F;
    border-radius: 10px;
    padding: 12px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}

.cg-statusbar::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: #F59E0B;
}

.cg-status-left {
    display: flex;
    align-items: center;
    gap: 16px;
}

.cg-pulse-dot {
    width: 10px;
    height: 10px;
    background: #EF4444;
    border-radius: 50%;
    box-shadow: 0 0 0 3px rgba(239,68,68,0.25);
    animation: pulse-ring 1.6s ease-out infinite;
    flex-shrink: 0;
}

@keyframes pulse-ring {
    0%   { box-shadow: 0 0 0 0 rgba(239,68,68,0.5); }
    70%  { box-shadow: 0 0 0 8px rgba(239,68,68,0); }
    100% { box-shadow: 0 0 0 0 rgba(239,68,68,0); }
}

.cg-sys-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #F59E0B;
}

.cg-sys-sub {
    font-size: 11px;
    color: #475569;
    letter-spacing: 0.05em;
}

.cg-status-chips {
    display: flex;
    gap: 8px;
}

.cg-chip {
    background: #0A1628;
    border: 1px solid #1E3A5F;
    border-radius: 6px;
    padding: 4px 12px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.cg-chip.active { border-color: #22D3EE; color: #22D3EE; }
.cg-chip.warn   { border-color: #F59E0B; color: #F59E0B; }

/* ── Page Title Block ── */
.cg-title-block {
    margin-bottom: 24px;
}

.cg-eyebrow {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #EF4444;
    margin-bottom: 6px;
}

.cg-title {
    font-size: 38px !important;
    font-weight: 900 !important;
    color: #F1F5F9 !important;
    letter-spacing: -0.03em;
    line-height: 1;
    margin: 0 !important;
    padding: 0 !important;
}

.cg-title span {
    color: #F59E0B;
}

.cg-tagline {
    font-size: 13px;
    color: #475569;
    margin-top: 6px;
    letter-spacing: 0.03em;
}

/* ── Control Panel ── */
.cg-panel {
    background: #0D1521;
    border: 1px solid #1E2D45;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
}

.cg-panel-label {
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #334155;
    margin-bottom: 14px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1E2D45;
}

/* ── Inputs ── */
[data-testid="stTextInput"] input {
    background: #080C14 !important;
    border: 1px solid #1E3A5F !important;
    border-radius: 8px !important;
    color: #E2E8F0 !important;
    font-size: 13px !important;
    padding: 10px 14px !important;
    font-family: 'Courier New', monospace !important;
    letter-spacing: 0.02em;
}

[data-testid="stTextInput"] input:focus {
    border-color: #22D3EE !important;
    box-shadow: 0 0 0 2px rgba(34,211,238,0.12) !important;
}

[data-testid="stTextInput"] label {
    color: #64748B !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
}

/* ── Layer Toggle Buttons ── */
.stButton > button {
    background: #0A1628 !important;
    color: #94A3B8 !important;
    border: 1px solid #1E3A5F !important;
    border-radius: 8px !important;
    height: 44px !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
}

.stButton > button:hover {
    background: #0F2040 !important;
    border-color: #22D3EE !important;
    color: #22D3EE !important;
    box-shadow: 0 0 12px rgba(34,211,238,0.12) !important;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: #0D1521 !important;
    border: 1px solid #1E2D45 !important;
    border-radius: 10px !important;
    padding: 14px 16px !important;
}

[data-testid="metric-container"] label {
    font-size: 9px !important;
    font-weight: 800 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: #475569 !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 28px !important;
    font-weight: 900 !important;
    color: #22D3EE !important;
    font-family: 'Courier New', monospace !important;
    letter-spacing: -0.02em !important;
}

/* ── Section Headers ── */
.cg-section-head {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 28px 0 14px;
}

.cg-section-line {
    flex: 1;
    height: 1px;
    background: #1E2D45;
}

.cg-section-tag {
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #334155;
    white-space: nowrap;
}

/* ── Insight Cards ── */
.cg-insight-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-bottom: 16px;
}

.cg-insight-card {
    background: #0D1521;
    border: 1px solid #1E2D45;
    border-radius: 10px;
    padding: 16px;
}

.cg-insight-card.amber { border-left: 3px solid #F59E0B; }
.cg-insight-card.cyan  { border-left: 3px solid #22D3EE; }
.cg-insight-card.red   { border-left: 3px solid #EF4444; }
.cg-insight-card.green { border-left: 3px solid #10B981; }

.cg-insight-label {
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 6px;
}

.cg-insight-value {
    font-size: 22px;
    font-weight: 900;
    color: #F1F5F9;
    font-family: 'Courier New', monospace;
    letter-spacing: -0.02em;
    line-height: 1;
}

.cg-insight-sub {
    font-size: 11px;
    color: #475569;
    margin-top: 4px;
}

/* ── Summary Items ── */
.cg-summary-item {
    padding: 9px 0;
    border-bottom: 1px solid #111827;
    font-size: 12px;
    color: #94A3B8;
    display: flex;
    align-items: flex-start;
    gap: 8px;
    line-height: 1.5;
}

.cg-summary-item:last-child { border-bottom: none; }

.cg-summary-dash {
    color: #1E3A5F;
    font-family: monospace;
    flex-shrink: 0;
    margin-top: 1px;
}

/* ── Map Legend ── */
.cg-legend {
    background: #0D1521;
    border: 1px solid #1E2D45;
    border-radius: 10px;
    padding: 16px 20px;
    margin-top: 12px;
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    align-items: center;
}

.cg-legend-title {
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #334155;
    width: 100%;
    margin-bottom: 4px;
}

.cg-legend-item {
    display: flex;
    align-items: center;
    gap: 7px;
    font-size: 11px;
    color: #94A3B8;
    font-weight: 600;
}

.cg-legend-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
}

/* ── Info Notice ── */
.cg-notice {
    background: #0A1628;
    border: 1px solid #1E3A5F;
    border-left: 3px solid #22D3EE;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 12px;
    color: #64748B;
    line-height: 1.6;
    margin-bottom: 16px;
}

/* ── SITREP Export Button ── */
.cg-export-wrap .stButton > button {
    background: linear-gradient(135deg, #92400E, #B45309) !important;
    border-color: #F59E0B !important;
    color: #FEF3C7 !important;
    box-shadow: 0 0 16px rgba(245,158,11,0.2) !important;
    letter-spacing: 0.08em !important;
}

.cg-export-wrap .stButton > button:hover {
    background: linear-gradient(135deg, #B45309, #D97706) !important;
    box-shadow: 0 0 24px rgba(245,158,11,0.35) !important;
    color: #FFFBEB !important;
}

/* ── Reset Button ── */
.cg-reset-wrap .stButton > button {
    background: transparent !important;
    border-color: #1E2D45 !important;
    color: #475569 !important;
}

.cg-reset-wrap .stButton > button:hover {
    border-color: #EF4444 !important;
    color: #EF4444 !important;
    box-shadow: 0 0 10px rgba(239,68,68,0.1) !important;
}

/* ── Alert boxes ── */
[data-testid="stAlert"] {
    background: #0A1628 !important;
    border: 1px solid #1E3A5F !important;
    border-radius: 10px !important;
    color: #64748B !important;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] > button {
    background: #0A1628 !important;
    border: 1px solid #22D3EE !important;
    color: #22D3EE !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    letter-spacing: 0.05em !important;
    width: 100% !important;
}

/* ── Success msg ── */
[data-testid="stSuccess"] {
    background: #052E16 !important;
    border-color: #10B981 !important;
    color: #6EE7B7 !important;
    border-radius: 8px !important;
}

/* ── Error msg ── */
[data-testid="stError"] {
    background: #1C0A0A !important;
    border-color: #EF4444 !important;
    color: #FCA5A5 !important;
    border-radius: 8px !important;
}

/* Column spacing */
[data-testid="column"] { padding: 0 5px !important; }

</style>
""", unsafe_allow_html=True)


# =========================
# System Status Bar
# =========================

st.markdown("""
<div class="cg-statusbar">
    <div class="cg-status-left">
        <div class="cg-pulse-dot"></div>
        <div>
            <div class="cg-sys-label">CrisisGrid — Live Operations</div>
            <div class="cg-sys-sub">Geospatial Emergency Management System</div>
        </div>
    </div>
    <div class="cg-status-chips">
        <div class="cg-chip active">System Online</div>
        <div class="cg-chip warn">Demo Dataset Active</div>
        <div class="cg-chip">v1.0</div>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================
# Title
# =========================

st.markdown("""
<div class="cg-title-block">
    <div class="cg-eyebrow">▸ Emergency Management Platform</div>
    <div class="cg-title">Crisis<span>Grid</span></div>
    <div class="cg-tagline">Command-level visibility into emergency infrastructure across cities</div>
</div>
""", unsafe_allow_html=True)


# =========================
# Notices
# =========================

st.markdown("""
<div class="cg-notice">
    ◈ Operating on curated emergency service datasets. Architecture supports live API integration.
    Supported cities: <strong style="color:#94A3B8">Mumbai · Pune · Delhi</strong>
</div>
""", unsafe_allow_html=True)


# =========================
# Session State
# =========================

defaults = {
    "show_hospitals": False,
    "show_police": False,
    "show_fire": False,
    "show_heatmap": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================
# Inputs
# =========================

col_in1, col_in2 = st.columns(2)

with col_in1:
    city = st.text_input("📍 Grid Location", value="Mumbai")

with col_in2:
    destination = st.text_input("🧭 Target Destination", value="Chhatrapati Shivaji Maharaj International Airport")

coordinates = get_coordinates(city)


if coordinates:
    latitude, longitude = coordinates

    # =========================
    # Layer Controls
    # =========================

    st.markdown("""
    <div class="cg-section-head">
        <div class="cg-section-tag">Layer Controls</div>
        <div class="cg-section-line"></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        hospital_button = st.button("🏥 Hospitals", key="hospital")
    with col2:
        police_button = st.button("🚓 Police", key="police")
    with col3:
        fire_button = st.button("🚒 Fire Stations", key="fire")
    with col4:
        heatmap_button = st.button("📡 Density Map", key="heatmap")
    with col5:
        st.markdown('<div class="cg-export-wrap">', unsafe_allow_html=True)
        pdf_button = st.button("📋 Export SITREP", key="pdf")
        st.markdown('</div>', unsafe_allow_html=True)
    with col6:
        st.markdown('<div class="cg-reset-wrap">', unsafe_allow_html=True)
        reset_button = st.button("↺ Reset Grid", key="reset")
        st.markdown('</div>', unsafe_allow_html=True)


    # =========================
    # Update Session State
    # =========================

    if hospital_button:
        st.session_state.show_hospitals = True
    if police_button:
        st.session_state.show_police = True
    if fire_button:
        st.session_state.show_fire = True
    if heatmap_button:
        st.session_state.show_heatmap = True
    if reset_button:
        for key in defaults:
            st.session_state[key] = False
        st.rerun()


    # =========================
    # Load Data
    # =========================

    hospitals        = []
    police_stations  = []
    fire_stations    = []

    if st.session_state.show_hospitals:
        hospitals = get_services(city, "hospital")
    if st.session_state.show_police:
        police_stations = get_services(city, "police")
    if st.session_state.show_fire:
        fire_stations = get_services(city, "fire")


    # =========================
    # Analytics
    # =========================

    analytics = calculate_metrics(hospitals, police_stations, fire_stations)


    # =========================
    # Metrics Row
    # =========================

    st.markdown("""
    <div class="cg-section-head">
        <div class="cg-section-tag">Infrastructure Readout</div>
        <div class="cg-section-line"></div>
    </div>
    """, unsafe_allow_html=True)

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric("🏥 Hospitals",      len(hospitals))
    metric2.metric("🚓 Police Stations", len(police_stations))
    metric3.metric("🚒 Fire Stations",   len(fire_stations))
    metric4.metric("🌍 Grid Location",   city)


    # =========================
    # Emergency Insights
    # =========================

    st.markdown("""
    <div class="cg-section-head">
        <div class="cg-section-tag">Operational Insights</div>
        <div class="cg-section-line"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="cg-insight-row">
        <div class="cg-insight-card amber">
            <div class="cg-insight-label">Infrastructure Availability Index</div>
            <div class="cg-insight-value">{analytics['coverage_score']}<span style="font-size:14px;color:#475569">/10</span></div>
            <div class="cg-insight-sub">Coverage rating for active city grid</div>
        </div>
        <div class="cg-insight-card cyan">
            <div class="cg-insight-label">Infrastructure Status</div>
            <div class="cg-insight-value" style="font-size:18px">{analytics['risk_level']}</div>
            <div class="cg-insight-sub">Current operational classification</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


    # =========================
    # Emergency Summary
    # =========================

    st.markdown("""
    <div class="cg-section-head">
        <div class="cg-section-tag">Situation Summary</div>
        <div class="cg-section-line"></div>
    </div>
    """, unsafe_allow_html=True)

    summary_html = "".join([
        f'<div class="cg-summary-item"><span class="cg-summary-dash">—</span>{item}</div>'
        for item in analytics["summary"]
    ])

    st.markdown(f"""
    <div class="cg-panel">
        {summary_html}
    </div>
    """, unsafe_allow_html=True)


    # =========================
    # Map
    # =========================

    st.markdown("""
    <div class="cg-section-head">
        <div class="cg-section-tag">Tactical Map</div>
        <div class="cg-section-line"></div>
    </div>
    """, unsafe_allow_html=True)

    crisis_map = create_map(
        latitude, longitude, city,
        hospitals, police_stations, fire_stations,
        st.session_state.show_heatmap
    )

    st_folium(crisis_map, width=1200, height=600)


    # =========================
    # Map Legend
    # =========================

    st.markdown("""
    <div class="cg-legend">
        <div class="cg-legend-title">Map Legend</div>
        <div class="cg-legend-item"><div class="cg-legend-dot" style="background:#EF4444"></div> Emergency HQ</div>
        <div class="cg-legend-item"><div class="cg-legend-dot" style="background:#10B981"></div> Hospitals</div>
        <div class="cg-legend-item"><div class="cg-legend-dot" style="background:#3B82F6"></div> Police Stations</div>
        <div class="cg-legend-item"><div class="cg-legend-dot" style="background:#F97316"></div> Fire Stations</div>
        <div class="cg-legend-item"><div class="cg-legend-dot" style="background:#8B5CF6;border-radius:2px"></div> Service Density</div>
    </div>
    """, unsafe_allow_html=True)


    # =========================
    # PDF Export
    # =========================

    if pdf_button:
        enabled_features = []
        if st.session_state.show_hospitals:
            enabled_features.append("Hospitals")
        if st.session_state.show_police:
            enabled_features.append("Police")
        if st.session_state.show_fire:
            enabled_features.append("Fire")
        if st.session_state.show_heatmap:
            enabled_features.append("Service Density")

        pdf_path = generate_pdf(
            city, destination,
            hospitals, police_stations, fire_stations,
            ", ".join(enabled_features)
        )

        st.success("✅ SITREP generated successfully.")

        with open(pdf_path, "rb") as file:
            st.download_button(
                label="⬇️ Download SITREP Report",
                data=file,
                file_name="crisis_report.pdf",
                mime="application/pdf"
            )

else:
    st.error("⚠ Location not found. Enter a supported city: Mumbai, Pune, or Delhi.")
