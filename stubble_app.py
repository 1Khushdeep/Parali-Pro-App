import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import plotly.express as px
import plotly.graph_objects as go
import os
import time
import base64

# ==========================================
# 1. PAGE CONFIGURATION & ADVANCED CSS
# ==========================================
st.set_page_config(page_title="Parali-Pro Dashboard", page_icon="🌾", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp { background-color: #050914; color: #f0f2f6; }
    .title-container { text-align: center; margin-top: 10px; margin-bottom: 0px; }
    .emoji-icon { font-size: 75px; vertical-align: middle; }
    .gradient-text { 
        font-size: 85px !important; font-weight: 900; 
        background: -webkit-linear-gradient(#FFDF00, #FF8C00);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 4px 4px 10px rgba(255, 140, 0, 0.4);
        vertical-align: middle; font-family: 'Arial Black', sans-serif;
    }
    .subtitle { text-align: center; color: #00E5FF; font-size: 24px; font-weight: 600; font-style: italic; margin-bottom: 40px; }
    .glass-card { background: rgba(30, 38, 56, 0.7); padding: 25px; border-radius: 15px; border: 1px solid rgba(255, 215, 0, 0.3); text-align: center; }
    div.row-widget.stRadio > div { flex-direction: column; gap: 18px; font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
@st.cache_data(show_spinner=False)
def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="punjab_enterprise_app")
    try:
        loc = geolocator.geocode(f"{location_name}, Punjab, India", timeout=10)
        if loc: return loc.latitude, loc.longitude
    except: pass
    return None, None

def render_image(image_name, caption_text=""):
    if os.path.exists(image_name):
        with open(image_name, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        
        caption_html = f'<div style="color: #00E5FF; font-size: 24px; font-weight: bold; margin-top: 15px; text-align: center; letter-spacing: 1px;">{caption_text}</div>' if caption_text.strip() != "" else ""
        
        html_code = f"""
        <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; width: 100%; margin-bottom: 40px; margin-top: 20px;">
            <img src="data:image/png;base64,{data}" 
                 style="width: 100%; height: auto; object-fit: cover; border-radius: 15px; box-shadow: 0px 4px 15px rgba(0, 229, 255, 0.1);">
            {caption_html}
        </div>
        """
        st.markdown(html_code, unsafe_allow_html=True)
    else:
        st.error(f"⚠️ Missing Image: '{image_name}'")

# ==========================================
# 3. SIDEBAR
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1892/1892747.png", width=120)
st.sidebar.title("🌐 Command Center")
page = st.sidebar.radio("Select Module:", ["🏠 1. Home / Overview", "👨‍🌾 2. AI Decision Engine", "🏛️ 3. Spatial Analytics", "🏭 4. Biomass Logistics", "📈 5. Impact Projections"])

# ==========================================
# PAGE 1: HOME
# ==========================================
if page == "🏠 1. Home / Overview":
    st.markdown('<div class="title-container"><span class="emoji-icon">🌾</span> <span class="gradient-text">Parali-Pro</span></div>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Next-Generation Crop Residue & Energy Optimization Platform</p>', unsafe_allow_html=True)
    render_image("PARALI.png", "") # कैप्शन खाली, अब कुछ नहीं आएगा
    
    st.divider()
    home_tabs = st.tabs(["🔥 Problem", "💡 Solution", "🎯 Pillars"])
    with home_tabs[0]:
        render_image("CRISIS.png", "The Ground Reality")
    with home_tabs[1]:
        render_image("FARMER.png", "Digital Empowerment")
        render_image("TACKLING.png", "Technological Waste Management")
    with home_tabs[2]:
        render_image("BURNING.png", "Eradicate Field Fires")
        render_image("MONEY.png", "Generate Rural Wealth")

# ==========================================
# PAGE 2: AI ENGINE
# ==========================================
elif page == "👨‍🌾 2. AI Decision Engine":
    st.header("👨‍🌾 Intelligent Decision Support System")
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("⚙️ Analysis Parameters")
        village = st.text_input("Location:", "Sangrur")
        yield_val = st.number_input("Paddy Yield (MT):", value=2500.0)
        analyze_btn = st.button("🔄 Execute Optimization")
    with col2:
        if analyze_btn:
            st.success(f"Analysis Complete! Biomass: {yield_val * 1.5} Tons")

# ==========================================
# PAGE 3: SPATIAL ANALYTICS
# ==========================================
elif page == "🏛️ 3. Spatial Analytics":
    st.header("🏛️ Regional Density")
    uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.info(f"Columns in your file: {list(df.columns)}")
            if {'District_Name', 'Production', 'State_Name'}.issubset(df.columns):
                df_grouped = df.groupby('District_Name')['Production'].sum().reset_index()
                st.plotly_chart(px.bar(df_grouped, x='District_Name', y='Production'), use_container_width=True)
            else:
                st.error("Error: CSV must have 'District_Name', 'Production', 'State_Name'")
        except Exception as e:
            st.error(f"Error: {e}")

# ==========================================
# PAGE 4 & 5: LOGISTICS & IMPACT (Simplified)
# ==========================================
elif page == "🏭 4. Biomass Logistics":
    st.header("🏭 Infrastructure")
elif page == "📈 5. Impact Projections":
    st.header("📈 Impact Projections")
    st.plotly_chart(go.Figure(data=go.Scatter(y=[100, 50, 10])), use_container_width=True)
