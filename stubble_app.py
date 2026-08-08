import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import os
import time

# ==========================================
# 1. PAGE CONFIGURATION & ADVANCED CSS
# ==========================================
st.set_page_config(page_title="Parali-Pro Dashboard", page_icon="🌾", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* Premium Dark Theme */
    .stApp { background-color: #050914; color: #f0f2f6; }
    
    /* 3D Title Fix (Emoji separate from Gradient) */
    .title-container { text-align: center; margin-top: 10px; margin-bottom: 0px; }
    .emoji-icon { font-size: 75px; vertical-align: middle; }
    .gradient-text { 
        font-size: 85px !important; 
        font-weight: 900; 
        background: -webkit-linear-gradient(#FFDF00, #FF8C00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 4px 4px 10px rgba(255, 140, 0, 0.4);
        vertical-align: middle;
        font-family: 'Arial Black', sans-serif;
    }
    
    /* Subtitle Styling */
    .subtitle { text-align: center; color: #00E5FF; font-size: 24px; font-weight: 600; font-style: italic; letter-spacing: 1.5px; margin-bottom: 40px; }
    
    /* Custom Metric Cards */
    .glass-card {
        background: rgba(30, 38, 56, 0.7);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        text-align: center;
        transition: transform 0.3s ease;
    }
    .glass-card:hover { transform: translateY(-5px); border: 1px solid rgba(255, 215, 0, 0.8); }
    
    /* Sidebar styling */
    div.row-widget.stRadio > div { flex-direction: column; gap: 18px; font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HELPER FUNCTIONS (CACHED FOR SPEED)
# ==========================================
@st.cache_data(show_spinner=False)
def get_coordinates(location_name):
    """Geocodes district names into Lat/Lon for spatial mapping."""
    geolocator = Nominatim(user_agent="punjab_enterprise_app")
    try:
        loc = geolocator.geocode(f"{location_name}, Punjab, India", timeout=10)
        if loc: return loc.latitude, loc.longitude
    except: pass
    return None, None

def render_image(image_name, caption_text="", width=800, height=500):
    """Forces images to maintain strict uniform dimensions for professional UI."""
    if os.path.exists(image_name):
        img = Image.open(image_name).resize((width, height))
        st.image(img, caption=caption_text, use_container_width=True)
    else:
        st.error(f"⚠️ System Alert: Graphic asset '{image_name}' missing from directory.")

# ==========================================
# 3. SIDEBAR NAVIGATION & SYSTEM STATUS
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1892/1892747.png", width=120)
st.sidebar.title("🌐 Command Center")
page = st.sidebar.radio(
    "Select Module:",
    ["🏠 1. Home / Overview", 
     "👨‍🌾 2. AI Decision Engine", 
     "🏛️ 3. Spatial Analytics", 
     "🏭 4. Biomass Logistics",
     "📈 5. Impact Projections"]
)
st.sidebar.divider()
st.sidebar.markdown("### 🟢 System Status")
st.sidebar.info("All nodes operational. Connected to spatial database.")

# ==========================================
# PAGE 1: HOME / OVERVIEW
# ==========================================
if page == "🏠 1. Home / Overview":
    # Fixed 3D Title with separate Emoji
    st.markdown('<div class="title-container"><span class="emoji-icon">🌾</span> <span class="gradient-text">Parali-Pro</span></div>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Next-Generation Crop Residue & Energy Optimization Platform</p>', unsafe_allow_html=True)
    
    render_image("PARALI.png", width=1400, height=500)
    st.divider()
    
    home_tabs = st.tabs(["🔥 Problem Statement", "💡 Strategic Solution", "🎯 Core Pillars"])
    
    with home_tabs[0]:
        st.write("### The Ecological & Economic Crisis")
        st.write("Every post-harvest season, the narrow window for field preparation triggers massive stubble burning across North India. This conventional practice annihilates topsoil nutrients and creates severe atmospheric pollution (PM2.5/PM10), resulting in a public health emergency and economic loss.")
        render_image("CRISIS.png", width=1400, height=500)

    with home_tabs[1]:
        st.write("### The Data-Driven Intervention")
        st.write("We architect a bridge between agriculture and the energy sector. Utilizing spatial data and production metrics, Parali-Pro routes crop residue directly to operational Biomass, Paper, and Bio-CNG plants, translating waste into sustainable capital.")
        col1, col2 = st.columns(2)
        with col1: render_image("FARMER.png", "Digital Empowerment of Farmers", width=800, height=600)
        with col2: render_image("TACKLING.png", "Technological Waste Management", width=800, height=600)

    with home_tabs[2]:
        st.write("### Platform Objectives")
        # Changed to 2 columns for symmetry since BIO_CNG image is removed
        col_obj1, col_obj2 = st.columns(2)
        with col_obj1: render_image("BURNING.png", "Eradicate Field Fires", width=800, height=800)
        with col_obj2: render_image("MONEY.png", "Generate Rural Wealth", width=800, height=800)

# ==========================================
# PAGE 2: AI DECISION ENGINE (FARMER PORTAL)
# ==========================================
elif page == "👨‍🌾 2. AI Decision Engine":
    st.header("👨‍🌾 Intelligent Decision Support System")
    st.write("Leveraging algorithmic analysis to compute the most lucrative residue management strategy.")
    
    st.image("https://images.unsplash.com/photo-1592982537447-6f2a6a0c5c13?auto=format&fit=crop&w=1400&h=400&q=80", use_container_width=True)
    st.divider()
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("⚙️ Analysis Parameters")
        village_name = st.text_input("Location (Village/District):", "Sangrur")
        crop_production = st.number_input("Paddy Yield (Metric Tons):", min_value=1.0, value=2500.0, step=100.0)
        dist_factory = st.slider("Logistics Radius to Plant (km):", 0, 150, 35)
        analyze_btn = st.button("🔄 Execute Optimization Algorithm", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        if analyze_btn:
            # Cinematic AI Loading Effect for Video Presentation
            with st.spinner("Initializing geospatial routing and volume calculation..."):
                time.sleep(1)
            with st.spinner("Applying Residue-to-Crop Ratio (RCR) models..."):
                time.sleep(1)
            
            stubble_volume = crop_production * 1.5 
            st.success(f"✅ Analysis Complete! Projected Biomass Volume: **{stubble_volume:,.2f} Tons**")
            
            st.write("### 📊 Algorithmic Recommendation")
            if dist_factory <= 50 and stubble_volume > 500:
                st.metric(label="Primary Directive", value="Supply to Biomass Facility 🏭", delta=f"Projected Revenue: ₹{stubble_volume * 2500:,.2f}")
                st.info("Logistics constraint verified. High volume concentration and optimal proximity make commercial supply highly profitable.")
            else:
                st.metric(label="Primary Directive", value="In-situ Composting 🌱", delta="Optimizes Soil Nutrition")
                st.warning("Logistics threshold exceeded. Transport costs outweigh commercial benefits. Utilizing mechanical integration (Super SMS) is advised.")

# ==========================================
# PAGE 3: SPATIAL ANALYTICS (GOVT)
# ==========================================
elif page == "🏛️ 3. Spatial Analytics":
    st.header("🏛️ Regional Density & Spatial Mapping")
    uploaded_file = st.file_uploader("Initialize System with Crop Data (CSV)", type=['csv'])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if {'District_Name', 'Production', 'State_Name'}.issubset(df.columns):
            df_punjab = df[df['State_Name'].str.upper() == 'PUNJAB']
            df_grouped = df_punjab.groupby('District_Name')['Production'].sum().reset_index()
            df_grouped['Stubble_Volume'] = df_grouped['Production'] * 1.5
            df_grouped = df_grouped.sort_values(by='Stubble_Volume', ascending=False)
            
            st.markdown("### 📈 High-Level Statistical Overview")
            col1, col2 = st.columns(2)
            with col1:
                fig_bar = px.bar(df_grouped.head(10), x='District_Name', y='Stubble_Volume', 
                                 title="Critical Districts by Biomass Volume (MT)",
                                 color='Stubble_Volume', color_continuous_scale='YlOrRd', template="plotly_dark")
                fig_bar.update_layout(xaxis_title="District", yaxis_title="Volume (MT)", hovermode="x unified")
                st.plotly_chart(fig_bar, use_container_width=True)
                
            with col2:
                fig_pie = px.pie(df_grouped.head(10), names='District_Name', values='Stubble_Volume', 
                                 title="Regional Contribution Distribution", hole=0.5, template="plotly_dark",
                                 color_discrete_sequence=px.colors.sequential.YlOrRd[::-1])
                fig_pie.update_traces(textposition='inside', textinfo='percent+label', hovertemplate="%{label}: %{value:,.0f} MT")
                st.plotly_chart(fig_pie, use_container_width=True)
            
            st.divider()
            st.write("### 🔥 Live Spatial Heatmap (Geospatial Render)")
            with st.spinner("Connecting to geocoding servers... mapping vectors..."):
                heat_data = []
                for _, row in df_grouped.iterrows():
                    lat, lon = get_coordinates(str(row['District_Name']))
                    if lat and lon and pd.notnull(row['Stubble_Volume']):
                        heat_data.append([lat, lon, float(row['Stubble_Volume'])])
                
                if heat_data:
                    m = folium.Map(location=[30.9, 75.8], zoom_start=7, tiles="CartoDB dark_matter")
                    HeatMap(heat_data, radius=35, blur=25, max_zoom=1).add_to(m)
                    st_folium(m, width="100%", height=500)
                else:
                    st.error("Spatial mapping failed. Please check network restrictions.")
        else:
            st.error("Invalid Dataset Schema. Requires: State_Name, District_Name, Production")

# ==========================================
# PAGE 4: BIOMASS LOGISTICS (INDUSTRY)
# ==========================================
elif page == "🏭 4. Biomass Logistics":
    st.header("🏭 Infrastructure & Capacity Network")
    uploaded_bio = st.file_uploader("Load Industry Infrastructure Matrix (Excel)", type=['xlsx'])
    
    if uploaded_bio is not None:
        df_bio = pd.read_excel(uploaded_bio).dropna(subset=['Location of the Project'])
        
        if 'Capacity in MW' in df_bio.columns:
            df_bio['Capacity in MW'] = pd.to_numeric(df_bio['Capacity in MW'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce')
            
            st.markdown("### ⚡ Infrastructure KPIs")
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Total Facilities Mapped", len(df_bio))
            col_b.metric("Aggregate Power Capacity", f"{df_bio['Capacity in MW'].sum():.1f} MW")
            col_c.metric("Supply Chain Status", "Active", "Optimized")
            
            st.divider()
            
            fig_cap = px.bar(df_bio, x='Name of the Company', y='Capacity in MW',
                             title="Operational Capacity per Facility (MW)",
                             color='Capacity in MW', color_continuous_scale='Greens', template="plotly_dark")
            fig_cap.update_layout(xaxis={'categoryorder':'total descending'}, hovermode="x unified")
            st.plotly_chart(fig_cap, use_container_width=True)
            
            st.write("### 📍 Node Coordinates Mapping")
            with st.spinner("Extracting coordinates and rendering logistics nodes..."):
                m2 = folium.Map(location=[30.9, 75.8], zoom_start=7, tiles="CartoDB dark_matter")
                for _, row in df_bio.iterrows():
                    search_loc = str(row['Location of the Project']).split(',')[-1].replace('Distt:', '').strip()
                    lat, lon = get_coordinates(search_loc)
                    if lat and lon:
                        company, capacity = row.get('Name of the Company', 'Biomass Plant'), row.get('Capacity in MW', 'Unknown')
                        folium.Marker(
                            location=[lat, lon], popup=f"<b>{company}</b><br>Capacity: {capacity} MW",
                            icon=folium.Icon(color="green", icon="leaf")
                        ).add_to(m2)
                st_folium(m2, width="100%", height=500)
        else:
            st.error("Invalid Schema. Missing 'Capacity in MW' column.")

# ==========================================
# PAGE 5: IMPACT PROJECTIONS
# ==========================================
elif page == "📈 5. Impact Projections":
    st.header("📈 Predictive Environmental Impact")
    st.write("Simulated timeline for emission mitigation and AQI stabilization (2023 - 2028).")
    
    years = ['2023', '2024', '2025', '2026', '2027', '2028']
    bau_emissions = [200, 215, 230, 245, 260, 280] 
    optimized_emissions = [200, 180, 140, 90, 50, 10] 
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=bau_emissions, mode='lines+markers', name='Emissions (Business As Usual)', line=dict(color='#ff4b4b', width=3, dash='dash')))
    fig.add_trace(go.Scatter(x=years, y=optimized_emissions, mode='lines+markers', fill='tozeroy', name='Emissions (Parali-Pro Integrated)', line=dict(color='#00FFCC', width=4)))
    
    fig.update_layout(title="Carbon Emission Trajectory (MtCO2)", xaxis_title="Financial Year", yaxis_title="Emissions (MtCO2)", template="plotly_dark", hovermode="x unified", legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    st.write("### 🎯 5-Year Milestone Targets")
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Peak AQI", "110", "▼ 75% Reduction", delta_color="normal")
    col2.metric("Soil Carbon Recovery", "18%", "▲ Sustained", delta_color="normal")
    col3.metric("Rural Economy Boost", "₹2,150 Cr", "▲ Generated", delta_color="normal")