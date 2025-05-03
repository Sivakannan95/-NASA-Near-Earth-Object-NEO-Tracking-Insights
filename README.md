# 🚀 NASA Near-Earth Object (NEO) Tracking & Insights

![NASA Badge](https://img.shields.io/badge/API-NASA_NEO-blue)
![License Badge](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)

---

## 🔹 Project Overview

A complete end-to-end data pipeline built on top of NASA's Near-Earth Object (NEO) API to monitor and analyze asteroid data.  
The system extracts data via API, transforms and stores it in a relational database, and provides insightful dashboards through Streamlit.

---

## 🎓 Skills Gained

- API Integration & JSON Parsing  
- Data Cleaning & Transformation  
- SQL Table Design and Data Insertion  
- SQL Analytical Query Writing  
- Streamlit Dashboard Development  
- User Interaction with Filters and Visualization  

---

## 🌍 Domain

**Space Research & Astronomical Data Analysis**

---

## 📊 Business Use Cases

- **Threat Monitoring**: Identify potentially hazardous asteroids based on speed, size, and proximity.  
- **Date-Based Exploration**: Analyze approach patterns over time.  
- **Filtering for Insights**: Provide customized filters for users.  
- **Space Data Democratization**: Make astronomical data accessible to non-technical users.  

---

### 📥 Step 2: Data Extraction
- Use start date (e.g., `2024-01-01`) and fetch 7-day batches
- Follow pagination using `data['links']['next']`
- Loop until ~10,000 records are collected

**Extracted Fields:**

| Field | Description |
|-------|-------------|
| id | Asteroid ID |
| neo_reference_id | NASA Reference ID |
| name | Asteroid Name |
| absolute_magnitude_h | Brightness |
| estimated_diameter_min_km | Min diameter (km) |
| estimated_diameter_max_km | Max diameter (km) |
| is_potentially_hazardous_asteroid | True/False |
| close_approach_date | Date of approach |
| relative_velocity_kmph | Speed in km/h |
| astronomical | Distance in AU |
| miss_distance_km | Miss distance (km) |
| miss_distance_lunar | Miss distance (LD) |
| orbiting_body | Usually Earth |

📌 *Note: Multiple entries per asteroid are possible due to repeated close approaches.*

### 🧹 Step 3: Data Cleaning

- Keep only relevant fields  
- Convert data types correctly  
- Handle missing data using `.get()`  
- Convert dates using `datetime.strptime()`  
- Prepare data for SQL insertion  

---

## 👁️ Streamlit UI Features

**Functionalities:**

- Dropdown menu to select queries (1–15)
- Filters:
- Date range
- Velocity range
- Distance (AU/LD)
- Hazardous status
- Diameter range

**Widgets Used:**

- `st.date_input()`  
- `st.slider()`  
- `st.selectbox()`  
- `st.dataframe()`  

---

## 📊 Expected Results

- 10,000+ asteroid records fetched & cleaned  
- Inserted into normalized SQL tables  
- Executed 15+ analytical queries  
- Delivered interactive dashboard for insights  

---

## 🔧 Technologies Used

- Python  
- NASA NEO API  
- **MySQL**  
- Streamlit  
- Pandas  

---

## 🌐 Tags

`API Integration` `JSON Parsing` `Python` `SQL` `Data Extraction` `Streamlit` `Space Research` `Dashboard` `Asteroids` `NASA` `Astronomy`

---

## 🌌 Conclusion

This project empowers users to interact with space data intuitively, making it useful for researchers, educators, and enthusiasts by transforming raw API data into meaningful insights.

---

## 📁 Project Structure (Optional)
```bash
├── api/                  # Scripts to fetch and parse NASA API
├── db/                   # SQL scripts for schema and queries
├── streamlit_app/        # Streamlit UI code
├── requirements.txt      # Dependencies
├── README.md             # Project README


## 📚 Project Approach

### 🔑 Step 1: Get NASA API Key
- Register at [https://api.nasa.gov](https://api.nasa.gov)
- API Format:
