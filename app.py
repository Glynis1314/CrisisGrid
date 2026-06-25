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

    layout="wide"

)


# =========================
# Professional UI
# =========================

st.markdown(
"""
<style>

.main{
    background-color:#f8fafc;
}

.stButton > button{
    width:100%;
    height:50px;
    border-radius:12px;
    font-weight:bold;
}

div[data-testid="metric-container"]{
    border:1px solid #e2e8f0;
    border-radius:12px;
    padding:15px;
    box-shadow:0 2px 6px rgba(0,0,0,0.1);
}

</style>
""",
unsafe_allow_html=True
)


# =========================
# Header
# =========================

st.title(

    "🚨 CrisisGrid"

)

st.caption(

    "Geospatial Emergency Management Dashboard"

)

st.info(
"""
📌 This dashboard currently uses curated emergency service datasets for demonstration purposes.

The architecture is designed to support integration with live APIs and real-time emergency infrastructure data sources.
"""
)

st.markdown(
"""
### 🌍 Supported Cities

- Mumbai
- Pune
- Delhi

Additional cities can be integrated without modifying the application architecture.
"""
)


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

city = st.text_input(

    "📍 Search Location",

    value="Mumbai"

)

destination = st.text_input(

    "🧭 Destination",

    value="Chhatrapati Shivaji Maharaj International Airport"

)

coordinates = get_coordinates(

    city

)


if coordinates:

    latitude, longitude = coordinates

    # =========================
    # Buttons
    # =========================

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        hospital_button = st.button("🏥 Hospitals", key="hospital")

    with col2:
        police_button = st.button("🚓 Police", key="police")

    with col3:
        fire_button = st.button("🚒 Fire", key="fire")

    with col4:
        heatmap_button = st.button("📊 Service Density", key="heatmap")

    with col5:
        pdf_button = st.button("📄 Generate SITREP", key="pdf")

    with col6:
        reset_button = st.button("🔄 Reset", key="reset")
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

    hospitals = []

    police_stations = []

    fire_stations = []

    

    if st.session_state.show_hospitals:

        hospitals = get_services(

            city,

            "hospital"

        )

    if st.session_state.show_police:

        police_stations = get_services(

            city,

            "police"

        )

    if st.session_state.show_fire:

        fire_stations = get_services(

            city,

            "fire"

        )

    # =========================
    # Analytics
    # =========================

    analytics = calculate_metrics(

        hospitals,

        police_stations,

        fire_stations

    )

    # =========================
    # Route
    # =========================

    # Route feature removed

    # =========================
    # Dashboard
    # =========================

    st.subheader(

        "📊 Emergency Dashboard"

    )

    st.info(
"""
📊 Service Density visualizes the concentration of emergency services within the selected city.

📄 Generate SITREP exports the current emergency infrastructure report as a PDF.
"""
)

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(

        "🏥 Hospitals",

        len(hospitals)

    )

    metric2.metric(

        "🚓 Police",

        len(police_stations)

    )

    metric3.metric(

        "🚒 Fire",

        len(fire_stations)

    )

    metric4.metric(

        "🌍 Location",

        city

    )

    st.subheader(

        "📈 Emergency Insights"

    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "Infrastructure Availability Index",

            f"{analytics['coverage_score']}/10"

        )

    with col2:

        st.metric(

            "Infrastructure Status",

            analytics["risk_level"]

        )

    st.subheader(

        "📋 Emergency Summary"

    )

    for item in analytics["summary"]:

        st.write(

            item

        )

    # =========================
    # Create Map
    # =========================

    crisis_map = create_map(

        latitude,

        longitude,

        city,

        hospitals,

        police_stations,

        fire_stations,

        st.session_state.show_heatmap

    )

    st_folium(

        crisis_map,

        width=1200,

        height=600

    )

    # =========================
    # Map Legend
    # =========================

    st.markdown(
"""

### 🗺️ Map Legend

🔴 Emergency HQ

🟢 Hospitals

🔵 Police Stations

🟠 Fire Stations

📊 Service Density

"""
)

    # =========================
    # PDF Export
    # =========================

    if pdf_button:

        enabled_features = []

        if st.session_state.show_hospitals:

            enabled_features.append(

                "Hospitals"

            )

        if st.session_state.show_police:

            enabled_features.append(

                "Police"

            )

        if st.session_state.show_fire:

            enabled_features.append(

                "Fire"

            )

        if st.session_state.show_heatmap:

            enabled_features.append(

                "Service Density"

            )

        
        
        pdf_path = generate_pdf(

            city,

            destination,

            hospitals,

            police_stations,

            fire_stations,

            ", ".join(

                enabled_features

            )

        )

        st.success(

            "PDF generated successfully."

        )

        with open(

            pdf_path,

            "rb"

        ) as file:

            st.download_button(

                label="⬇️ Download Report",

                data=file,

                file_name="crisis_report.pdf",

                mime="application/pdf"

            )

else:

    st.error(

        "Location not found."

    )