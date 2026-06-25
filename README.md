# 🚨 CrisisGrid

**CrisisGrid** is a geospatial emergency management dashboard built using **Python, Streamlit, and Folium**. It provides an interactive map-based interface for visualizing emergency infrastructure such as hospitals, police stations, and fire stations, helping users quickly assess emergency service availability within supported cities.

---

## ✨ Features

- 📍 Search emergency infrastructure by city
- 🏥 View hospitals on an interactive map
- 🚓 View police stations
- 🚒 View fire stations
- 📊 Service Density Heatmap
- 📈 Infrastructure Availability Analytics
- 📄 Generate SITREP (Situation Report) PDF
- 🗺️ Interactive Folium Map
- 🔄 Reset Dashboard

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### Mapping
- Folium
- Streamlit-Folium
- Geopy

### Data Processing
- Pandas

### PDF Generation
- ReportLab

---

## 📂 Project Structure

```text
CrisisGrid/
│
├── app.py
├── requirements.txt
├── README.md
├── data/
│
├── services/
│   ├── analytics.py
│   ├── data_loader.py
│   └── geocoder.py
│
├── utils/
│   ├── map_generator.py
│   └── pdf_generator.py
│
├── exports/
└── assets/
```

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/Glynis1314/CrisisGrid.git
cd CrisisGrid
```

Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## 🌍 Supported Cities

Currently supported:

- Mumbai
- Pune
- Delhi

The application architecture allows additional cities to be integrated with minimal code changes.

---

## 📊 Dashboard Features

- Hospital Infrastructure Visualization
- Police Station Mapping
- Fire Station Mapping
- Service Density Heatmap
- Infrastructure Availability Index
- Infrastructure Status
- Emergency Summary
- SITREP PDF Export

---

## 📄 SITREP Report

The generated Situation Report includes:

- Report Generation Time
- Selected City
- Emergency Service Statistics
- Infrastructure Availability Index
- Infrastructure Status
- Emergency Summary
- Enabled Dashboard Features

---

## 📸 Screenshots

### Home Dashboard
![Dashboard](assets/dashboard.png)

### Emergency Services Map
![Map](assets/map.png)

### Service Density Heatmap
![Heatmap](assets/heatmap.png)

### SITREP Report
![Report](assets/report.png)

---

## 🔮 Future Enhancements

- Live Emergency Service APIs
- Disaster Monitoring Integration
- Traffic-aware Route Planning
- Incident Reporting
- User Authentication
- Historical Emergency Analytics
- Mobile Responsive Interface

---

## 👨‍💻 Author

**Glynis D'Mello**

- GitHub: https://github.com/Glynis1314
- LinkedIn: *(Add your LinkedIn Profile)*

---

## 📜 License

This project is licensed under the MIT License.

---

⭐ If you found this project useful, consider giving it a star on GitHub!