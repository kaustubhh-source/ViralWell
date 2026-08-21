import os
import sqlite3
import requests
import json
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import folium
from folium.plugins import Fullscreen
from streamlit_folium import st_folium
import math

st.set_page_config(
    page_title="ViralWell | Predictive Climate-Health Analytics",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

def inject_natural_botanical_theme():
    import streamlit as st
    import base64
    import os
    from PIL import Image
    import io
    
    rishi_base64 = ""
    rishi_error = ""
    
    # 1. DIRECT RELATIVE PATH RESOLUTION WITH MULTIPLE EXTENSIONS
    base_dir = os.path.dirname(os.path.abspath(__file__))
    possible_filenames = ["ayurveda-rishi.webp", "ayurveda-rishi.webp.webp"]
    possible_paths = []
    for filename in possible_filenames:
        possible_paths.extend([
            os.path.join(base_dir, "..", filename),
            os.path.join(base_dir, filename),
            filename
        ])
    
    target_path = None
    for p in possible_paths:
        if os.path.exists(p):
            target_path = p
            break
            
    if target_path:
        try:
            # Load and clear out white background pixels dynamically without changing artwork colors
            img = Image.open(target_path).convert("RGBA")
            pixels = img.load()
            
            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    r, g, b, a = pixels[x, y]
                    if r > 230 and g > 230 and b > 230:
                        pixels[x, y] = (255, 255, 255, 0)
            
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            rishi_base64 = base64.b64encode(buffered.getvalue()).decode()
        except Exception as e:
            rishi_error = f"ERROR: Failed to read and process image asset at {target_path} -> {str(e)}"
    else:
        rishi_error = f"ERROR: 'ayurveda-rishi.webp' (or .webp.webp) not found. Checked locations: {possible_paths}"

    # Store in session state for rendering at the absolute bottom of content
    st.session_state["rishi_base64"] = rishi_base64
    st.session_state["rishi_error"] = rishi_error

    # ============================================================
    # PROVEN APPROACH:
    # PROVEN APPROACH:
    # 1. st.markdown() with <style> for CSS (background on .stApp, component styling)
    # 2. st.html() for JS that injects leaf DOM into parent document
    # ============================================================

    # --- STEP 1: Background + Component CSS via st.markdown (proven to work) ---
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap');

    /* Leafy background image directly on .stApp */
    .stApp {
        background-image:
            linear-gradient(rgba(2,13,7,0.85), rgba(1,6,3,0.90)),
            url('https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?auto=format&fit=crop&w=1920&q=80') !important;
        background-size: cover !important;
        background-position: center center !important;
        background-attachment: fixed !important;
        background-repeat: no-repeat !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- STEP 2: Falling leaves via components.html (PROVEN to work in test_visual.py) ---
    import streamlit.components.v1 as components
    components.html("""
    <script>
    (function(){
        var doc = window.parent.document;
        if (!doc) return;

        // Inject leaf CSS into parent head
        if (!doc.getElementById('rishi-leaf-css')) {
            var style = doc.createElement('style');
            style.id = 'rishi-leaf-css';
            style.textContent =
                '@keyframes leafFall { ' +
                '  0% { transform: translateY(-10vh) translateX(0px) rotate(0deg) scale(0.8); opacity: 0; } ' +
                '  10% { opacity: 0.7; } ' +
                '  50% { transform: translateY(50vh) translateX(-30px) rotate(180deg) scale(1.05); opacity: 0.7; } ' +
                '  90% { opacity: 0.7; } ' +
                '  100% { transform: translateY(110vh) translateX(30px) rotate(360deg) scale(1.2); opacity: 0; } ' +
                '} ' +
                '#rishi-falling-leaves { ' +
                '  position: fixed; top: 0; left: 0; ' +
                '  width: 100vw; height: 100vh; ' +
                '  overflow: hidden; pointer-events: none; ' +
                '  z-index: 1; ' +
                '} ' +
                '#rishi-falling-leaves span { ' +
                '  position: absolute; ' +
                '  pointer-events: none; ' +
                '  filter: drop-shadow(0 0 5px rgba(0,200,104,0.5)) drop-shadow(0 0 12px rgba(0,200,104,0.25)); ' +
                '  animation: leafFall linear infinite; ' +
                '} ';
            doc.head.appendChild(style);
        }

        // Inject leaf container into parent body
        if (!doc.getElementById('rishi-falling-leaves')) {
            var c = doc.createElement('div');
            c.id = 'rishi-falling-leaves';
            var leaves = [
                {e:'🍃', l:'2%',  d:'22s', dl:'0s',  s:'20px'},
                {e:'🌿', l:'6%',  d:'28s', dl:'4s',  s:'18px'},
                {e:'🍃', l:'10%', d:'25s', dl:'2s',  s:'22px'},
                {e:'🌿', l:'14%', d:'30s', dl:'7s',  s:'19px'},
                {e:'🍃', l:'4%',  d:'26s', dl:'10s', s:'24px'},
                {e:'🌿', l:'12%', d:'32s', dl:'13s', s:'18px'},
                {e:'🍃', l:'84%', d:'24s', dl:'1s',  s:'22px'},
                {e:'🌿', l:'88%', d:'29s', dl:'5s',  s:'20px'},
                {e:'🍃', l:'92%', d:'23s', dl:'3s',  s:'18px'},
                {e:'🌿', l:'96%', d:'31s', dl:'8s',  s:'24px'},
                {e:'🍃', l:'86%', d:'27s', dl:'11s', s:'20px'},
                {e:'🌿', l:'94%', d:'33s', dl:'6s',  s:'19px'}
            ];
            for (var i = 0; i < leaves.length; i++) {
                var lf = leaves[i];
                var span = doc.createElement('span');
                span.textContent = lf.e;
                span.style.cssText = 'left:' + lf.l + ';font-size:' + lf.s + ';animation-duration:' + lf.d + ';animation-delay:' + lf.dl + ';';
                c.appendChild(span);
            }
            doc.body.appendChild(c);
        }
    })();
    </script>
    """, height=0, scrolling=False)
    
    # 3. Streamlit internal components CSS overrides (tabs, hover, inputs, metrics, buttons)
    botanical_components_css = f"""
    <style>
    /* CUSTOM SMOOTH SCROLLBAR */
    ::-webkit-scrollbar {{
        width: 10px !important;
    }}
    ::-webkit-scrollbar-track {{
        background: #010704 !important;
    }}
    ::-webkit-scrollbar-thumb {{
        background: rgba(0, 200, 104, 0.2) !important;
        border-radius: 10px !important;
        border: 2px solid #010704 !important;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: rgba(0, 200, 104, 0.4) !important;
    }}

    /* IMMERSIVE JUNGLE ASHRAM BANNER */
    .unique-rishi-canopy-container {{
        display: block !important;
        position: relative !important;
        width: 100% !important;
        max-width: 1200px !important;
        height: 260px !important;
        margin: 50px auto 20px auto !important;
        background-image: 
            linear-gradient(rgba(2, 13, 7, 0.45), rgba(1, 6, 3, 0.55)), 
            url("https://images.unsplash.com/photo-1441974231531-c6227db76b6e?auto=format&fit=crop&w=1200&q=80") !important;
        background-size: cover !important;
        background-position: center bottom !important;
        overflow: hidden !important;
        z-index: 1 !important;
        opacity: 0.45 !important;
        text-align: center !important;
        mix-blend-mode: screen !important;
        mask-image: linear-gradient(to right, transparent 0%, #000 20%, #000 80%, transparent 100%), linear-gradient(to bottom, transparent 0%, #000 15%, #000 85%, transparent 100%) !important;
        mask-composite: intersect !important;
        -webkit-mask-image: linear-gradient(to right, transparent 0%, #000 20%, #000 80%, transparent 100%), linear-gradient(to bottom, transparent 0%, #000 15%, #000 85%, transparent 100%) !important;
        -webkit-mask-composite: source-in !important;
    }}
    .unique-rishi-canopy-container img {{
        height: 100% !important;
        width: auto !important;
        object-fit: contain !important;
        display: inline-block !important;
        background: transparent !important;
        vertical-align: bottom !important;
    }}

    /* GLASSMORPHIC APP PANEL CONTAINERS WITH EXPLICIT z-index STACKING & 3D HOVER EFFECT */
    div[data-testid="stVerticalBlockBorderBlock"] {{
        background: rgba(3, 15, 9, 0.6) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border: 1px solid rgba(0, 200, 104, 0.2) !important;
        border-radius: 24px !important;
        padding: 26px !important;
        box-shadow: 0 16px 44px rgba(0, 0, 0, 0.6) !important;
        z-index: 10 !important;
        position: relative !important;
        transition: transform 0.4s cubic-bezier(0.165, 0.84, 0.44, 1), box-shadow 0.4s ease, border-color 0.4s ease !important;
    }}
    div[data-testid="stVerticalBlockBorderBlock"]:hover {{
        transform: translateY(-6px) scale(1.005) !important;
        box-shadow: 0 28px 60px rgba(0, 200, 104, 0.16) !important;
        border-color: rgba(0, 200, 104, 0.4) !important;
    }}

    /* PREMIUM TABS STYLING */
    div[data-testid="stTabBar"] {{
        background: rgba(3, 15, 9, 0.4) !important;
        border-radius: 50px !important;
        padding: 6px !important;
        border: 1px solid rgba(0, 200, 104, 0.15) !important;
        backdrop-filter: blur(10px) !important;
    }}
    button[data-baseweb="tab"] {{
        color: #8fa89b !important;
        background: transparent !important;
        border: none !important;
        padding: 10px 24px !important;
        border-radius: 40px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: #00C868 !important;
        background: rgba(0, 200, 104, 0.12) !important;
        box-shadow: 0 4px 15px rgba(0, 200, 104, 0.15) !important;
    }}

    /* METRICS CARD PREMIUM UPGRADES */
    div[data-testid="stMetric"] {{
        background: rgba(1, 10, 5, 0.3) !important;
        border: 1px solid rgba(0, 200, 104, 0.1) !important;
        border-radius: 16px !important;
        padding: 15px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
    }}
    div[data-testid="stMetric"]:hover {{
        border-color: rgba(0, 200, 104, 0.3) !important;
        box-shadow: 0 8px 25px rgba(0, 200, 104, 0.08) !important;
        transform: translateY(-3px) !important;
    }}

    h1, h2, h3, [data-testid="stHeader"] h1 {{
        font-family: 'Playfair Display', serif !important;
        color: #EAF5EE !important;
    }}
    body, p, span, label, .stMarkdown {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #EAF5EE !important;
    }}
    .stButton > button {{
        background: linear-gradient(135deg, #00C868 0%, #009E52 100%) !important;
        color: #010704 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        border-radius: 30px !important;
        border: none !important;
        padding: 12px 30px !important;
        box-shadow: 0 4px 20px rgba(0, 200, 104, 0.3) !important;
        transition: all 0.3s ease !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 24px rgba(0, 200, 104, 0.45) !important;
    }}
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {{
        background-color: rgba(1, 7, 4, 0.8) !important;
        border: 1px solid rgba(0, 200, 104, 0.3) !important;
        border-radius: 14px !important;
        color: #EAF5EE !important;
        transition: border-color 0.3s ease !important;
    }}
    .stTextInput input:focus, .stSelectbox div[data-baseweb="select"]:focus {{
        border-color: #00C868 !important;
    }}
    [data-testid="stMetricValue"] {{
        color: #00C868 !important;
        font-weight: 700 !important;
    }}
    .stSidebar {{
        background-image: linear-gradient(rgba(1, 7, 4, 0.96), rgba(0, 4, 2, 0.99)) !important;
        border-right: 1px solid rgba(0, 200, 104, 0.15) !important;
    }}
    </style>
    """
    st.markdown(botanical_components_css, unsafe_allow_html=True)


inject_natural_botanical_theme()


def get_offline_neighborhood(lat, lon):
    hubs = {
        "Kurla West": (19.0760, 72.8777),
        "Chembur": (19.0522, 72.8996),
        "Andheri East": (19.1136, 72.8697),
        "Ghatkopar West": (19.0857, 72.9082),
        "Govandi East": (19.0596, 72.9158),
        "Dharavi": (19.0380, 72.8538),
        "Bandra Kurla Complex": (19.0607, 72.8643)
    }
    
    best_name = "Kurla West"
    min_dist = float('inf')
    for name, coords in hubs.items():
        dist = math.sqrt((coords[0] - lat)**2 + (coords[1] - lon)**2)
        if dist < min_dist:
            min_dist = dist
            best_name = name
            
    # Augment with cluster data if available
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.abspath(os.path.join(script_dir, "..", "data", "mumbai_clustered_health_data.csv"))
        if os.path.exists(csv_path):
            import pandas as pd
            cdf = pd.read_csv(csv_path)
            regions = cdf[["Region", "Latitude", "Longitude"]].drop_duplicates().to_dict("records")
            for r in regions:
                dist = math.sqrt((r["Latitude"] - lat)**2 + (r["Longitude"] - lon)**2)
                if dist < min_dist:
                    min_dist = dist
                    best_name = r["Region"]
    except Exception:
        pass

    return best_name


@st.cache_data(ttl=600)
def get_live_metrics_and_location(lat, lon):
    # 1. High-speed offline geocoding (0ms delay)
    place_name = get_offline_neighborhood(lat, lon)

    # Realistic static monsoon fallbacks if network exception hits
    live_temp = 27.5
    live_humidity = 88.0
    live_wind = 18.5
    live_desc = "Moderate Rain"
    live_pm25 = 12.0
    
    # 2. Weather API (strict 1.5s timeout)
    try:
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
        response = requests.get(weather_url, timeout=1.5)
        if response.status_code == 200:
            data = response.json()
            current = data.get("current", {})
            if current.get("temperature_2m") is not None:
                live_temp = float(current.get("temperature_2m"))
            if current.get("relative_humidity_2m") is not None:
                live_humidity = float(current.get("relative_humidity_2m"))
            if current.get("wind_speed_10m") is not None:
                live_wind = float(current.get("wind_speed_10m"))
            
            code = current.get("weather_code", 0)
            wmo_map = {
                0: "Clear Sky",
                1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast",
                45: "Fog", 48: "Depositing Rime Fog",
                51: "Light Drizzle", 53: "Moderate Drizzle", 55: "Dense Drizzle",
                61: "Slight Rain", 63: "Moderate Rain", 65: "Heavy Rain",
                80: "Slight Rain Showers", 81: "Moderate Rain Showers", 82: "Violent Rain Showers",
                95: "Thunderstorm", 96: "Thunderstorm with Slight Hail", 99: "Thunderstorm with Heavy Hail"
            }
            live_desc = wmo_map.get(code, "Unknown")
    except Exception:
        pass

    # 3. Air Quality API (strict 1.5s timeout)
    try:
        aqi_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=pm2_5"
        response = requests.get(aqi_url, timeout=1.5)
        if response.status_code == 200:
            data = response.json()
            current_aqi = data.get("current", {})
            if current_aqi.get("pm2_5") is not None:
                live_pm25 = float(current_aqi.get("pm2_5"))
    except Exception:
        pass

    # Save auxiliary variables directly to session state
    st.session_state.wind_speed = live_wind
    st.session_state.weather_desc = live_desc

    return place_name, live_temp, live_humidity, live_pm25


# 1. Set page config layout to "wide" and custom title removed/relocated to top



def render_rishi_footer(key_suffix):
    import streamlit as st
    
    # 1. Blended Ashram Canopy Banner
    if st.session_state.get("rishi_base64"):
        st.markdown(
            f"""
            <div class="unique-rishi-canopy-container" style="text-align: center; margin-top: 50px;">
                <img src="data:image/png;base64,{st.session_state["rishi_base64"]}" style="max-width: 100%; height: auto; border-radius: 8px;">
            </div>
            """, 
            unsafe_allow_html=True
        )
    elif st.session_state.get("rishi_error"):
        st.error(st.session_state["rishi_error"])

    # 2. Glowing Centered Header with Live Animation Keyframes
    st.markdown(
        """
        <style>
        @keyframes rishiGlow {
            0% { text-shadow: 0 0 10px rgba(212, 175, 55, 0.4); transform: scale(1); }
            50% { text-shadow: 0 0 20px rgba(46, 204, 113, 0.7); transform: scale(1.02); }
            100% { text-shadow: 0 0 10px rgba(212, 175, 55, 0.4); transform: scale(1); }
        }
        .rishi-animated-title {
            text-align: center !important;
            font-size: 32px !important;
            color: #fff !important;
            margin-top: 15px !important;
            margin-bottom: 25px !important;
            animation: rishiGlow 4s ease-in-out infinite;
        }
        </style>
        <h2 class="rishi-animated-title">Ask Rishi</h2>
        """, 
        unsafe_allow_html=True
    )

    # 3. Clean Input Box (Label collapsed/hidden)
    rishi_query = st.text_input(
        "Ask Rishi:",
        label_visibility="collapsed",
        placeholder="Ask Rishi: 'I am experiencing a fever, what natural remedies do you suggest?'",
        autocomplete="off",
        key=f"rishi_query_{key_suffix}"
    )

    # 4. Live Meditation Spinner & LLM Execution Framework
    if rishi_query and rishi_query.strip() != "":
        try:
            # Spinner will clear the exact moment the first chunk of the stream arrives
            with st.spinner("Rishi is in deep silent meditation. Please seek your remedy in a few moments."):
                generator = get_rishi_remedy(rishi_query)
                first_chunk = next(generator, None)
            
            st.markdown(f"""
            <div data-testid="stVerticalBlockBorderBlock" style="margin-top: 15px;">
                <h3 style="font-family: 'Playfair Display', serif !important; color: #00C868 !important; font-weight: 700 !important; margin-bottom: 12px; border-bottom: 1px solid rgba(0,200,104,0.20) !important; padding-bottom: 10px !important;">Ayurvedic Guidance</h3>
            </div>
            """, unsafe_allow_html=True)
            
            def final_stream():
                if first_chunk:
                    yield first_chunk
                for chunk in generator:
                    yield chunk
            
            st.write_stream(final_stream())
        except Exception as e:
            st.error(f"⚠️ {str(e)}")


def get_rishi_remedy(user_query):
    import requests
    import json
    import streamlit as st
    
    # 1. Local Fallback Ayurvedic Remedies
    FALLBACK_REMEDIES = {
        "fever": (
            "🌿 **Ayurvedic Guidance for Fever (Jvara):**\n\n"
            "1. **Herbal Decoction**: Drink a warm infusion of *Tulsi* (Holy Basil) and fresh ginger twice daily to support the immune system and promote healthy sweating.\n"
            "2. **Dietary Rest**: Consume light, warm, and easily digestible foods like *Mung Dal Khichdi* spiced with turmeric and cumin. Avoid dairy, cold water, and heavy meals.\n"
            "3. **Hydration**: Sip on warm water infused with a pinch of dry ginger (*Shunti*) throughout the day.\n\n"
            "*Note: If the fever persists or is high, please consult a qualified Vaidya or physician immediately.*"
        ),
        "cold": (
            "🌿 **Ayurvedic Guidance for Cold (Pratishyaya):**\n\n"
            "1. **Steam Inhalation**: Inhale steam infused with a drop of Eucalyptus oil or wild mint to clear congestion in the sinuses.\n"
            "2. **Herbal Remedy**: Mix 1/2 teaspoon of organic turmeric powder and a pinch of black pepper in warm milk (or almond milk) and drink before bedtime.\n"
            "3. **Daily Habit**: Perform *Pranayama* (breath control exercises) such as Nadi Shodhana to clear the respiratory channels."
        ),
        "cough": (
            "🌿 **Ayurvedic Guidance for Cough (Kasa):**\n\n"
            "1. **Honey & Ginger**: Mix 1 teaspoon of fresh ginger juice with 1 teaspoon of raw organic honey. Take this mixture 2-3 times daily to soothe the throat.\n"
            "2. **Licorice Root (Yashtimadhu)**: Chew on a small piece of licorice root or drink licorice root tea to relieve dry, tickling throat irritation.\n"
            "3. **Warm Gargle**: Gargle with warm water containing a pinch of rock salt (*Saindhava Namak*) and turmeric twice a day."
        ),
        "headache": (
            "🌿 **Ayurvedic Guidance for Headache (Shirasula):**\n\n"
            "1. **Herbal Paste**: Apply a paste of sandalwood or nutmeg powder mixed with water to your forehead. Leave it for 15-20 minutes, then rinse off with lukewarm water.\n"
            "2. **Soothing Herbal Tea**: Brew warm tea with coriander seeds and cumin seeds to calm the Pitta/Vata dosha often associated with headaches.\n"
            "3. **Hydration & Rest**: Ensure adequate hydration with lukewarm water and rest in a dark, quiet room away from screens."
        ),
        "indigestion": (
            "🌿 **Ayurvedic Guidance for Indigestion (Ajiirna):**\n\n"
            "1. **CCF Tea**: Sip warm Coriander-Cumin-Fennel (CCF) tea after meals to ignite your digestive fire (*Agni*).\n"
            "2. **Ginger Appetizer**: Chew a thin slice of fresh ginger with a drop of lemon juice and a pinch of rock salt 15 minutes before lunch.\n"
            "3. **Meal Hygiene**: Eat in a calm environment without distractions. Avoid cold or carbonated beverages during meals."
        ),
        "digestion": (
            "🌿 **Ayurvedic Guidance for Indigestion (Ajiirna):**\n\n"
            "1. **CCF Tea**: Sip warm Coriander-Cumin-Fennel (CCF) tea after meals to ignite your digestive fire (*Agni*).\n"
            "2. **Ginger Appetizer**: Chew a thin slice of fresh ginger with a drop of lemon juice and a pinch of rock salt 15 minutes before lunch.\n"
            "3. **Meal Hygiene**: Eat in a calm environment without distractions. Avoid cold or carbonated beverages during meals."
        ),
        "stomach": (
            "🌿 **Ayurvedic Guidance for Stomach Discomfort:**\n\n"
            "1. **Warm Fennel Water**: Boil a teaspoon of fennel seeds in water, strain, and sip warm to reduce bloating and abdominal gas.\n"
            "2. **Castor Oil Compress**: Apply a warm castor oil pack to the lower abdomen to ease Vata-related spasms and congestion.\n"
            "3. **Light Meals**: Eat fresh, warm, watery soups and rice gruel (*Kanji*) until the stomach settles."
        ),
        "skin": (
            "🌿 **Ayurvedic Guidance for Skin Health (Twacha):**\n\n"
            "1. **Neem & Turmeric Paste**: Apply a paste of neem leaves and turmeric powder to blemishes or irritated skin to detoxify and soothe.\n"
            "2. **Aloe Vera Gel**: Apply fresh aloe vera gel directly to clear heat (Pitta) and moisturize naturally.\n"
            "3. **Blood Purifiers**: Sip on warm tea containing Amalaki or Manjistha to cleanse the blood channels."
        ),
        "acne": (
            "🌿 **Ayurvedic Guidance for Skin Health (Twacha):**\n\n"
            "1. **Neem & Turmeric Paste**: Apply a paste of neem leaves and turmeric powder to blemishes or irritated skin to detoxify and soothe.\n"
            "2. **Aloe Vera Gel**: Apply fresh aloe vera gel directly to clear heat (Pitta) and moisturize naturally.\n"
            "3. **Blood Purifiers**: Sip on warm tea containing Amalaki or Manjistha to cleanse the blood channels."
        ),
        "stress": (
            "🌿 **Ayurvedic Guidance for Stress & Mental Balance (Manas):**\n\n"
            "1. **Ashwagandha**: Consume 1/2 teaspoon of Ashwagandha powder in warm milk or water before bed to support the nervous system.\n"
            "2. **Self-Abhyanga**: Perform a gentle self-massage with warm sesame oil on your head and the soles of your feet before sleeping.\n"
            "3. **Meditation & Breath**: Dedicate 10 minutes to deep slow abdominal breathing (*Pranayama*) daily."
        ),
        "anxiety": (
            "🌿 **Ayurvedic Guidance for Stress & Mental Balance (Manas):**\n\n"
            "1. **Ashwagandha**: Consume 1/2 teaspoon of Ashwagandha powder in warm milk or water before bed to support the nervous system.\n"
            "2. **Self-Abhyanga**: Perform a gentle self-massage with warm sesame oil on your head and the soles of your feet before sleeping.\n"
            "3. **Meditation & Breath**: Dedicate 10 minutes to deep slow abdominal breathing (*Pranayama*) daily."
        ),
        "sleep": (
            "🌿 **Ayurvedic Guidance for Stress & Mental Balance (Manas):**\n\n"
            "1. **Ashwagandha**: Consume 1/2 teaspoon of Ashwagandha powder in warm milk or water before bed to support the nervous system.\n"
            "2. **Self-Abhyanga**: Perform a gentle self-massage with warm sesame oil on your head and the soles of your feet before sleeping.\n"
            "3. **Meditation & Breath**: Dedicate 10 minutes to deep slow abdominal breathing (*Pranayama*) daily."
        ),
    }

    # 2. Check for API key and log a warning if missing (safely catching st.secrets failures on Render)
    import os
    api_key = ""
    try:
        api_key = st.secrets.get("NVIDIA_API_KEY", "")
    except Exception:
        pass
    if not api_key:
        api_key = os.getenv("NVIDIA_API_KEY", "") or os.environ.get("NVIDIA_API_KEY", "")
        
    key_missing = not api_key or api_key.strip() == ""
    
    if key_missing:
        st.error("Missing NVIDIA_API_KEY. Please add it to your environment variables or secrets.toml.")
        
        # ponytail: naive substring matching; upgrade to boundary regex or tokenized parsing to handle negatives/context.
        query_lower = user_query.lower()
        fallback_text = None
        for key, remedy in FALLBACK_REMEDIES.items():
            if key in query_lower:
                fallback_text = remedy + "\n\n*(Note: Rendered from local herbal archives due to missing API Key)*"
                break
        if not fallback_text:
            raise ValueError(
                "NVIDIA_API_KEY is missing and no local fallback remedy was found for your query. "
                "Please configure the key in secrets.toml, or ask about common symptoms like 'fever', 'cold', or 'cough'."
            )
        
        def local_stream():
            import time
            for word in fallback_text.split(" "):
                yield word + " "
                time.sleep(0.04)
        return local_stream()

    # 3. Stream API Request execution
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    system_instruction = (
        "You are an ancient, deeply wise Ayurvedic Rishi and Vedic Physician. The user is asking you a health/lifestyle question. "
        "You must answer exclusively using traditional Ayurvedic principles. Focus on balancing the three Doshas (Vata, Pitta, Kapha), "
        "recommending natural herbs (like Neem, Tulsi, Ashwagandha), dietary changes (Ahar), and daily routines (Vihar/Dincharya). "
        "Completely avoid all modern Western medical jargon, pharmaceutical names, or clinical diagnostics. Maintain a compassionate, "
        "calm, and spiritually grounded tone. If a symptom sounds highly critical or life-threatening, gently advise them to consult "
        "a Vaidya or professional physician alongside your natural lifestyle guidance. "
        "Strict Formatting Rules: You must keep your response extremely concise, highly structured, and strictly under 150 words. "
        "Budget your explanation dynamically so that you always complete your thoughts and never cut off mid-sentence or mid-bullet point. "
        "Do not stop abruptly at a header, list item, or number."
    )
    
    payload = {
        "model": "meta/llama-3.1-8b-instruct",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_query.strip()}
        ],
        "temperature": 0.5,
        "max_tokens": 500,
        "stream": True
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, stream=True)
        if response.status_code != 200:
            raise RuntimeError(f"NVIDIA API Error (Status {response.status_code})")
            
        def sse_generator():
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8').strip()
                    if decoded_line.startswith("data: "):
                        data_content = decoded_line[6:]
                        if data_content == "[DONE]":
                            break
                        try:
                            json_data = json.loads(data_content)
                            delta = json_data.get("choices", [{}])[0].get("delta", {})
                            if "content" in delta:
                                yield delta["content"]
                        except Exception:
                            pass
        return sse_generator()
        
    except Exception as e:
        # Fallback mechanism if API fails, times out or is unreachable
        query_lower = user_query.lower()
        fallback_text = None
        for key, remedy in FALLBACK_REMEDIES.items():
            if key in query_lower:
                fallback_text = remedy + "\n\n*(Note: Rendered from local herbal archives due to connection timeout or API error)*"
                break
        
        if not fallback_text:
            raise RuntimeError(
                "The herbs of wisdom timed out or the connection failed. No local fallback remedy "
                "was found for your query. Try asking about common symptoms like 'fever', 'cold', or 'cough'."
            ) from e
            
        def error_stream():
            import time
            for word in fallback_text.split(" "):
                yield word + " "
                time.sleep(0.04)
        return error_stream()


def get_llama_health_advisory(location, temp, humidity, pm25, risk_score, user_query=None):
    import requests
    import os
    import streamlit as st
    
    api_key = ""
    try:
        api_key = st.secrets.get("NVIDIA_API_KEY", "")
    except Exception:
        pass
    if not api_key:
        api_key = os.getenv("NVIDIA_API_KEY", "") or os.environ.get("NVIDIA_API_KEY", "")
        
    key_missing = not api_key or api_key.strip() == ""
    
    if key_missing:
        st.error("Missing NVIDIA_API_KEY. Please add it to your environment variables or secrets.toml.")
        return "Diagnostics Status: AI advisory offline due to missing API Key configuration."
        
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Conditional prompt generation based on user interaction state
    if user_query and user_query.strip() != "":
        prompt = f"""
        You are an expert clinical epidemiologist assistant answering a citizen's query.
        Context for {location} Ward: Temp={temp}°C, Humidity={humidity}%, PM2.5 AQI={pm25}, Forecast Outbreak Risk={risk_score}%.
        
        User Question: "{user_query}"
        
        Instructions:
        - Answer the question directly, concisely, and professionally in 2-3 sentences.
        - Use standard paragraph format or clean bullet points.
        - Do NOT include generic introductory phrases, headers, or conversational filler.
        - Ground your response in Mumbai's real-world tropical climate realities.
        """
    else:
        prompt = f"""
        You are a Senior Public Health Consultant drafting a citizen safety brief for {location} ward in Mumbai.
        Active Telemetry: Temp={temp}°C, Humidity={humidity}%, AQI={pm25}, Risk Index={risk_score}%.
        
        Generate exactly two clean, original bullet points for the dashboard interface:
        - Point 1 (Threat Factor): Identify the active environmental risk driven by this humidity/AQI (e.g., moisture vectors, stagnant water, mold, or respiratory irritants).
        - Point 2 (Preventative Action): Provide a highly practical, daily lifestyle action local families can take.
        
        Strict Rules:
        - Do NOT repeat the raw numeric statistics back to the user.
        - If the temperature is under 32°C, you are strictly prohibited from mentioning heat stress, sun stroke, sun hours, or heatwaves. Focus entirely on monsoon, dampness, or waterborne/vector profiles.
        - Output ONLY the two bullet points. No introductory text.
        """

    system_instruction = (
        "You are an expert clinical epidemiologist and Senior Public Health Consultant advising citizens on outbreak risks. "
        "Strict Formatting Rules: You must keep your response extremely concise, highly structured, and strictly under 150 words. "
        "Budget your explanation dynamically so that you always complete your thoughts and never cut off mid-sentence or mid-bullet point. "
        "Do not stop abruptly at a header, list item, or number."
    )

    payload = {
        "model": "meta/llama-3.1-8b-instruct",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt.strip()}
        ],
        "temperature": 0.5,
        "max_tokens": 250
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            return f"⚠️ API Connection Syncing (Status: {response.status_code}). Please verify your backend key activation."
    except Exception as e:
        return f"Diagnostics Status: AI epidemiological stream error - {str(e)}"

# Load the trained advanced multi-season machine learning model
@st.cache_resource
def load_model():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, "..", "models", "viralwell_multi_season_model.pkl")
    return joblib.load(model_path)

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# Initialize SQLite Database for Logging Scenarios (Advanced Schema)
def init_db():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_dir = os.path.abspath(os.path.join(script_dir, "..", "database"))
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "viralwell_logs.db")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scenario_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            temp REAL,
            humidity REAL,
            rainfall REAL,
            predicted_cases INT,
            risk_level TEXT,
            location TEXT,
            gastro_cases INT,
            heatstroke_cases INT,
            dengue_cases INT,
            malaria_cases INT,
            influenza_cases INT,
            bronchitis_cases INT,
            pm25 REAL
        )
    """)
    # Migration: Add columns if running on an older database version
    new_cols = [
        "location TEXT",
        "gastro_cases INT",
        "heatstroke_cases INT",
        "dengue_cases INT",
        "malaria_cases INT",
        "influenza_cases INT",
        "bronchitis_cases INT",
        "pm25 REAL"
    ]
    for col_def in new_cols:
        try:
            cursor.execute(f"ALTER TABLE scenario_logs ADD COLUMN {col_def}")
        except sqlite3.OperationalError:
            pass  # Column already exists
        
    conn.commit()
    conn.close()
    return db_path

db_path = init_db()


WIKIPEDIA_LINKS = {
    # ☀️ SUMMER CONDITIONS
    "Dehydration": "https://en.wikipedia.org/wiki/Dehydration",
    "Heatstroke": "https://en.wikipedia.org/wiki/Heat_stroke",
    "Heat exhaustion": "https://en.wikipedia.org/wiki/Heat_exhaustion",
    "Heat cramps": "https://en.wikipedia.org/wiki/Heat_cramps",
    "General fatigue": "https://en.wikipedia.org/wiki/Fatigue",
    "Sunburn": "https://en.wikipedia.org/wiki/Sunburn",
    "Prickly heat": "https://en.wikipedia.org/wiki/Miliaria",
    "Scalp sunburn": "https://en.wikipedia.org/wiki/Sunburn",
    "Scalp folliculitis": "https://en.wikipedia.org/wiki/Folliculitis",
    "Melasma": "https://en.wikipedia.org/wiki/Melasma",
    "Photodermatitis": "https://en.wikipedia.org/wiki/Photodermatitis",
    "Nosebleeds": "https://en.wikipedia.org/wiki/Nosebleed",
    "Dust allergies": "https://en.wikipedia.org/wiki/Dust_mite_allergy",
    "Pollen allergies": "https://en.wikipedia.org/wiki/Allergic_rhinitis",
    "Food poisoning": "https://en.wikipedia.org/wiki/Food_poisoning",
    "Gastroenteritis": "https://en.wikipedia.org/wiki/Gastroenteritis",
    "Diarrhea": "https://en.wikipedia.org/wiki/Diarrhea",
    "Dysentery": "https://en.wikipedia.org/wiki/Dysentery",
    "Typhoid fever": "https://en.wikipedia.org/wiki/Typhoid_fever",
    "Cholera": "https://en.wikipedia.org/wiki/Cholera",
    "Chickenpox": "https://en.wikipedia.org/wiki/Chickenpox",
    "Measles": "https://en.wikipedia.org/wiki/Measles",
    "Mumps": "https://en.wikipedia.org/wiki/Mumps",
    "Pink eye": "https://en.wikipedia.org/wiki/Conjunctivitis",
    "Styes": "https://en.wikipedia.org/wiki/Stye",
    "Heat-induced migraines": "https://en.wikipedia.org/wiki/Migraine",
    "Low blood pressure": "https://en.wikipedia.org/wiki/Hypotension",
    "Stomach Flu": "https://en.wikipedia.org/wiki/Gastroenteritis",
    "Adenoviral Conjunctivitis (Pink Eye)": "https://en.wikipedia.org/wiki/Conjunctivitis",
    "Excess Sweat-Induced Scalp Pruritus": "https://en.wikipedia.org/wiki/Itch",

    # 🌧️ MONSOON CONDITIONS
    "Dengue fever": "https://en.wikipedia.org/wiki/Dengue_fever",
    "Malaria": "https://en.wikipedia.org/wiki/Malaria",
    "Chikungunya": "https://en.wikipedia.org/wiki/Chikungunya",
    "Zika virus": "https://en.wikipedia.org/wiki/Zika_virus",
    "Post-viral arthritis": "https://en.wikipedia.org/wiki/Post-viral_arthritis",
    "Myalgia": "https://en.wikipedia.org/wiki/Myalgia",
    "Calf muscle tenderness": "https://en.wikipedia.org/wiki/Myalgia",
    "Leptospirosis": "https://en.wikipedia.org/wiki/Leptospirosis",
    "Oily dandruff": "https://en.wikipedia.org/wiki/Seborrheic_dermatitis",
    "Scalp ringworm": "https://en.wikipedia.org/wiki/Tinea_capitis",
    "Body ringworm": "https://en.wikipedia.org/wiki/Dermatophytosis",
    "Athlete's foot": "https://en.wikipedia.org/wiki/Athlete%27s_foot",
    "Jock itch": "https://en.wikipedia.org/wiki/Tinea_cruris",
    "Nail fungal infections": "https://en.wikipedia.org/wiki/Onychomycosis",
    "Intertrigo": "https://en.wikipedia.org/wiki/Intertrigo",
    "Scabies": "https://en.wikipedia.org/wiki/Scabies",
    "Humidity-driven eczema": "https://en.wikipedia.org/wiki/Eczema",
    "Mold allergies": "https://en.wikipedia.org/wiki/Mold_health_issues",
    "Allergic rhinitis": "https://en.wikipedia.org/wiki/Allergic_rhinitis",
    "Mold-triggered asthma": "https://en.wikipedia.org/wiki/Asthma",
    "Hepatitis A & E": "https://en.wikipedia.org/wiki/Hepatitis_A",
    "Amebiasis": "https://en.wikipedia.org/wiki/Amoebiasis",
    "Giardiasis": "https://en.wikipedia.org/wiki/Giardiasis",
    "Tapeworm infections": "https://en.wikipedia.org/wiki/Tapeworm_infection",
    "Swimmer's ear": "https://en.wikipedia.org/wiki/Otitis_externa",
    "West Nile Virus": "https://en.wikipedia.org/wiki/West_Nile_virus",
    "Enteroviral Hand, Foot, and Mouth Disease (HFMD)": "https://en.wikipedia.org/wiki/Hand,_foot,_and_mouth_disease",

    # ❄️ WINTER CONDITIONS
    "Common cold": "https://en.wikipedia.org/wiki/Common_cold",
    "Influenza": "https://en.wikipedia.org/wiki/Influenza",
    "RSV": "https://en.wikipedia.org/wiki/Respiratory_syncytial_virus",
    "Viral bronchitis": "https://en.wikipedia.org/wiki/Bronchitis",
    "Pneumonia": "https://en.wikipedia.org/wiki/Pneumonia",
    "Smog-induced asthma": "https://en.wikipedia.org/wiki/Asthma",
    "COPD flare-ups": "https://en.wikipedia.org/wiki/Chronic_obstructive_pulmonary_disease",
    "Sinusitis": "https://en.wikipedia.org/wiki/Sinusitis",
    "Flaky dry dandruff": "https://en.wikipedia.org/wiki/Dandruff",
    "Xerosis": "https://en.wikipedia.org/wiki/Xeroderma",
    "Chapped lips": "https://en.wikipedia.org/wiki/Chapped_lips",
    "Cheilitis": "https://en.wikipedia.org/wiki/Cheilitis",
    "Cold-driven eczema": "https://en.wikipedia.org/wiki/Eczema",
    "Psoriasis worsening": "https://en.wikipedia.org/wiki/Psoriasis",
    "Chilblains": "https://en.wikipedia.org/wiki/Chilblains",
    "Cold urticaria": "https://en.wikipedia.org/wiki/Cold_urticaria",
    "Brittle hair breakage": "https://en.wikipedia.org/wiki/Trichorrhexis_nodosa",
    "Split ends": "https://en.wikipedia.org/wiki/Trichoptilosis",
    "Arthritis joint stiffness": "https://en.wikipedia.org/wiki/Joint_stiffness",
    "Rheumatoid arthritis": "https://en.wikipedia.org/wiki/Rheumatoid_arthritis",
    "Muscle spasms": "https://en.wikipedia.org/wiki/Spasm",
    "Raynaud's phenomenon": "https://en.wikipedia.org/wiki/Raynaud_disease",
    "Rotavirus": "https://en.wikipedia.org/wiki/Rotavirus",
    "Increased heart attack risk": "https://en.wikipedia.org/wiki/Myocardial_infarction",
    "Seasonal Affective Disorder": "https://en.wikipedia.org/wiki/Seasonal_affective_disorder",
    "Winter Diarrhea": "https://en.wikipedia.org/wiki/Rotavirus",
    "Norovirus": "https://en.wikipedia.org/wiki/Norovirus",
    "Rhinovirus (Common Cold)": "https://en.wikipedia.org/wiki/Rhinovirus",
    "Respiratory Syncytial Virus (RSV)": "https://en.wikipedia.org/wiki/Respiratory_syncytial_virus",
    "Pollutant-Driven Sore Throat": "https://en.wikipedia.org/wiki/Sore_throat"
}


# Sidebar: Model Insights & Interpretability
st.sidebar.markdown("""
<div class="sidebar-logo-container" style="padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 1.2rem; display: flex; align-items: center; gap: 8px;">
    <svg width="32" height="32" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="sidebarAyurTechGrad" x1="0%" y1="100%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#10b981" />
                <stop offset="100%" stop-color="#06b6d4" />
            </linearGradient>
            <filter id="sidebarGlow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="2.5" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
        </defs>
        <path d="M50,15 C25,25 15,55 50,85" stroke="url(#sidebarAyurTechGrad)" stroke-width="4.5" stroke-linecap="round" />
        <path d="M50,32 C35,37 30,47 22,44" stroke="url(#sidebarAyurTechGrad)" stroke-width="2.5" stroke-linecap="round" />
        <path d="M50,50 C38,55 32,65 25,62" stroke="url(#sidebarAyurTechGrad)" stroke-width="2.5" stroke-linecap="round" />
        <path d="M50,68 C42,71 38,78 32,75" stroke="url(#sidebarAyurTechGrad)" stroke-width="2.5" stroke-linecap="round" />
        <path d="M50,15 L50,85" stroke="url(#sidebarAyurTechGrad)" stroke-width="5" stroke-linecap="round" />
        <circle cx="65" cy="28" r="5" fill="#06b6d4" filter="url(#sidebarGlow)" />
        <circle cx="78" cy="40" r="5" fill="#06b6d4" filter="url(#sidebarGlow)" />
        <circle cx="82" cy="55" r="5" fill="#06b6d4" filter="url(#sidebarGlow)" />
        <circle cx="70" cy="70" r="5" fill="#06b6d4" filter="url(#sidebarGlow)" />
        <circle cx="58" cy="80" r="4" fill="#06b6d4" />
        <circle cx="58" cy="35" r="4" fill="#10b981" />
        <circle cx="68" cy="50" r="4" fill="#10b981" />
        <line x1="50" y1="15" x2="65" y2="28" stroke="url(#sidebarAyurTechGrad)" stroke-width="2.5" stroke-dasharray="2,2" />
        <line x1="65" y1="28" x2="78" y2="40" stroke="url(#sidebarAyurTechGrad)" stroke-width="2" />
        <line x1="65" y1="28" x2="58" y2="35" stroke="url(#sidebarAyurTechGrad)" stroke-width="2" />
        <line x1="58" y1="35" x2="68" y2="50" stroke="url(#sidebarAyurTechGrad)" stroke-width="2" />
        <line x1="78" y1="40" x2="68" y2="50" stroke="url(#sidebarAyurTechGrad)" stroke-width="2" />
        <line x1="78" y1="40" x2="82" y2="55" stroke="url(#sidebarAyurTechGrad)" stroke-width="2" />
        <line x1="82" y1="55" x2="70" y2="70" stroke="url(#sidebarAyurTechGrad)" stroke-width="2" />
        <line x1="68" y1="50" x2="70" y2="70" stroke="url(#sidebarAyurTechGrad)" stroke-width="2" />
        <line x1="70" y1="70" x2="58" y2="80" stroke="url(#sidebarAyurTechGrad)" stroke-width="2" />
        <line x1="50" y1="85" x2="58" y2="80" stroke="url(#sidebarAyurTechGrad)" stroke-width="2.5" stroke-dasharray="2,2" />
    </svg>
    <span style="font-family: 'Inter', sans-serif; font-weight: 800; font-size: 1.4rem; background: linear-gradient(90deg, #10b981 0%, #06b6d4 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -0.5px;">ViralWell</span>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("### 🧠 Model Insights & Interpretability")
st.sidebar.markdown("""
This section provides transparency into the underlying Random Forest machine learning model used to predict outbreak counts.
""")

# Extract feature importances
if hasattr(model, "estimators_"):
    # Average the feature importances of all 6 estimators of the MultiOutputRegressor
    importances = np.mean([est.feature_importances_ for est in model.estimators_], axis=0)
    features = ["Max_Temperature_C", "Mean_Humidity_Pct", "Daily_Rain_mm", "Rainfall_Lag_21", "Month", "PM25_Index"]
    
    st.sidebar.subheader("Relative Feature Importance")
    # Mapping for user-friendly labels
    label_map = {
        "Max_Temperature_C": "🌡️ Max Temperature",
        "Mean_Humidity_Pct": "💧 Mean Humidity",
        "Daily_Rain_mm": "🌧️ Daily Rain",
        "Rainfall_Lag_21": "🌊 Rainfall Lag (21d)",
        "Month": "📅 Season Month",
        "PM25_Index": "💨 PM2.5 AQI"
    }
    
    for feat, imp in zip(features, importances):
        label = label_map.get(feat, feat)
        st.sidebar.write(f"**{label}**: {imp * 100:.1f}%")
        st.sidebar.progress(float(imp))
elif hasattr(model, "feature_importances_"):
    importances = model.feature_importances_
    features = ["Temperature_C", "Humidity_Pct", "Rainfall_Lag_21"]
    
    st.sidebar.subheader("Relative Feature Importance")
    label_map = {
        "Temperature_C": "🌡️ Temperature",
        "Humidity_Pct": "💧 Humidity",
        "Rainfall_Lag_21": "🌧️ Rainfall Lag (21d)"
    }
    for feat, imp in zip(features, importances):
        label = label_map.get(feat, feat)
        st.sidebar.write(f"**{label}**: {imp * 100:.1f}%")
        st.sidebar.progress(float(imp))
else:
    st.sidebar.warning("Feature importances could not be retrieved from the model.")

st.sidebar.markdown("---")
st.sidebar.caption(
    "💡 **Biological Delay Indicator**: 'Rainfall_Lag_21' represents the 3-week delay required "
    "for stagnant pools created by monsoon rains to complete the mosquito vector breeding cycle "
    "(larvae to adult mosquitoes), leading to disease transmission spikes (Dengue/Malaria)."
)



# Inject custom CSS for premium styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap');
    
    /* Global Cyber-Ayurvedic 3D Theme - DO NOT use background shorthand, it wipes background-image */
    .stApp {
        background-color: transparent !important;
    }
    
    html, body, [data-testid="stMetricLabel"], p, h4, h5, h6, .stTabs button, label {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #EAF5EE !important;
    }
    [data-testid="stMetricValue"], h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #EAF5EE !important;
    }
    
    /* Maintain clean font stack for standard input components */
    .stTextInput input, .stNumberInput input, .stSelectbox div[role="button"] {
        font-family: 'Inter', system-ui, sans-serif !important;
    }
    
    /* Preserve material icon font-family to prevent text layout leaks */
    [data-testid="stIconMaterial"], .material-icons, [class*="Icon"], [class*="icon"] {
        font-family: 'Material Icons', 'Material Symbols Rounded', 'Material Symbols Outlined' !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif !important;
        color: #EAF5EE !important;
        font-weight: 700 !important;
    }
    
    /* Neumorphic Frosted Glass Card Engine */
    .glass-card, div[data-testid="metric-container"], .stExpander {
        background: rgba(3, 15, 9, 0.5) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(0, 200, 104, 0.1) !important;
        border-radius: 16px !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4) !important;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    div[data-testid="stSidebar"] {
        background: rgba(1, 7, 4, 0.95) !important;
    }
    
    /* Sidebar specific styling overrides */
    div[data-testid="stSidebar"] {
        padding: 2rem 1rem !important;
        border-right: 1px solid rgba(255, 255, 255, 0.04) !important;
    }
    
    /* Premium Title Header Container */
    .main-title-container {
        background: rgba(255, 255, 255, 0.01) !important;
        border: 1px solid rgba(16, 185, 129, 0.15) !important;
        padding: 2.2rem;
        border-radius: 16px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.03);
        margin-bottom: 2rem;
        text-align: left;
        backdrop-filter: blur(15px);
    }
    
    .main-title-container p {
        font-weight: 400;
        font-size: 1.1rem;
        color: #9ca3af !important;
        margin-top: 0.5rem;
        margin-bottom: 0;
        opacity: 0.9;
    }
    
    /* Stylized Outbreak Prediction Card with 3D Layers */
    .prediction-card {
        background: linear-gradient(135deg, #071915 0%, #0c0d14 100%) !important;
        border: 1.5px solid #10b981 !important;
        padding: 2.5rem !important;
        border-radius: 16px !important;
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.1) !important;
        color: #e5e7eb;
        text-align: center;
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .prediction-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(16, 185, 129, 0.25) !important;
    }
    
    .prediction-value-high {
        font-size: 5rem;
        font-weight: 800;
        color: #ef4444; /* alarm crimson */
        text-shadow: 0 0 25px rgba(239, 68, 68, 0.5);
        margin: 0.5rem 0;
        line-height: 1;
    }

    .prediction-value-normal {
        font-size: 5rem;
        font-weight: 800;
        color: #10b981; /* forest green */
        text-shadow: 0 0 25px rgba(16, 185, 129, 0.5);
        margin: 0.5rem 0;
        line-height: 1;
    }
    
    .prediction-label {
        font-size: 0.95rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #9ca3af;
        letter-spacing: 1.5px;
    }
    
    /* Glowing accents on input focus */
    .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox div[role="button"]:focus {
        border-color: #06b6d4 !important;
        box-shadow: 0 0 12px rgba(6, 182, 212, 0.4) !important;
    }
    
    /* Red Warning Alert Banner (Alarm Crimson with glows) */
    .alert-banner-warning {
        background-color: rgba(239, 68, 68, 0.05) !important;
        border: 2px solid #ef4444 !important;
        padding: 1.8rem;
        border-radius: 16px;
        color: #fca5a5;
        margin-top: 1rem;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
    }
    
    /* Green Info Alert Banner */
    .alert-banner-info {
        background-color: rgba(16, 185, 129, 0.05) !important;
        border: 1.5px solid #10b981 !important;
        padding: 1.8rem;
        border-radius: 16px;
        color: #a7f3d0;
        margin-top: 1rem;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.15), inset 0 1px 1px rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
    }
    
    /* Sticky Global Disclaimer Footer */
    .sticky-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(1, 7, 4, 0.95) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.05) !important;
        color: #9ca3af !important;
        text-align: center;
        padding: 12px 24px;
        font-size: 0.82rem;
        font-weight: 500;
        z-index: 999999;
        line-height: 1.4;
    }
    
    /* Ensure main app container leaves space for the footer */
    .stApp {
        padding-bottom: 80px !important;
    }
</style>
""", unsafe_allow_html=True)

# Header block
st.markdown("""
<div class="main-title-container">
    <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 0.5rem;">
        <svg width="45" height="45" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0 0 8px rgba(16, 185, 129, 0.4));">
            <defs>
                <linearGradient id="headerAyurTechGrad" x1="0%" y1="100%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#10b981" />
                    <stop offset="100%" stop-color="#06b6d4" />
                </linearGradient>
                <filter id="headerGlow" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="3" result="blur" />
                    <feComposite in="SourceGraphic" in2="blur" operator="over" />
                </filter>
            </defs>
            <path d="M50,15 C25,25 15,55 50,85" stroke="url(#headerAyurTechGrad)" stroke-width="4.5" stroke-linecap="round" />
            <path d="M50,32 C35,37 30,47 22,44" stroke="url(#headerAyurTechGrad)" stroke-width="2.5" stroke-linecap="round" />
            <path d="M50,50 C38,55 32,65 25,62" stroke="url(#headerAyurTechGrad)" stroke-width="2.5" stroke-linecap="round" />
            <path d="M50,68 C42,71 38,78 32,75" stroke="url(#headerAyurTechGrad)" stroke-width="2.5" stroke-linecap="round" />
            <path d="M50,15 L50,85" stroke="url(#headerAyurTechGrad)" stroke-width="5" stroke-linecap="round" />
            <circle cx="65" cy="28" r="5" fill="#06b6d4" filter="url(#headerGlow)" />
            <circle cx="78" cy="40" r="5" fill="#06b6d4" filter="url(#headerGlow)" />
            <circle cx="82" cy="55" r="5" fill="#06b6d4" filter="url(#headerGlow)" />
            <circle cx="70" cy="70" r="5" fill="#06b6d4" filter="url(#headerGlow)" />
            <circle cx="58" cy="80" r="4" fill="#06b6d4" />
            <circle cx="58" cy="35" r="4" fill="#10b981" />
            <circle cx="68" cy="50" r="4" fill="#10b981" />
            <line x1="50" y1="15" x2="65" y2="28" stroke="url(#headerAyurTechGrad)" stroke-width="2.5" stroke-dasharray="2,2" />
            <line x1="65" y1="28" x2="78" y2="40" stroke="url(#headerAyurTechGrad)" stroke-width="2" />
            <line x1="65" y1="28" x2="58" y2="35" stroke="url(#headerAyurTechGrad)" stroke-width="2" />
            <line x1="58" y1="35" x2="68" y2="50" stroke="url(#headerAyurTechGrad)" stroke-width="2" />
            <line x1="78" y1="40" x2="68" y2="50" stroke="url(#headerAyurTechGrad)" stroke-width="2" />
            <line x1="78" y1="40" x2="82" y2="55" stroke="url(#headerAyurTechGrad)" stroke-width="2" />
            <line x1="82" y1="55" x2="70" y2="70" stroke="url(#headerAyurTechGrad)" stroke-width="2" />
            <line x1="68" y1="50" x2="70" y2="70" stroke="url(#headerAyurTechGrad)" stroke-width="2" />
            <line x1="70" y1="70" x2="58" y2="80" stroke="url(#headerAyurTechGrad)" stroke-width="2" />
            <line x1="50" y1="85" x2="58" y2="80" stroke="url(#headerAyurTechGrad)" stroke-width="2.5" stroke-dasharray="2,2" />
        </svg>
        <span style="font-family: 'Inter', sans-serif; font-weight: 800; font-size: 2.5rem; color: white; letter-spacing: -1.5px; text-shadow: 0 2px 10px rgba(0,0,0,0.15);">ViralWell</span>
    </div>
    <p>Predictive Analytics Outbreak Dashboard — Mumbai City Climate & Health Intelligence Platform</p>
</div>
""", unsafe_allow_html=True)

# Helper to convert dataframe to CSV bytes for export
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# Function to fetch live real-time weather from Open-Meteo API
# Geocoding lookup using free Nominatim API scoping inside Mumbai
def geocode_mumbai_location(location_name):
    # ponytail: static lookup with fallback defaults; upgrade to OpenStreetMap/Nominatim API for dynamic, typo-tolerant lookups.
    hubs = {
        "Kurla West": (19.0760, 72.8777),
        "Chembur": (19.0522, 72.8996),
        "Andheri East": (19.1136, 72.8697),
        "Ghatkopar West": (19.0857, 72.9082),
        "Govandi East": (19.0596, 72.9158),
        "Dharavi": (19.0380, 72.8538),
        "Bandra Kurla Complex": (19.0607, 72.8643)
    }
    
    search_lower = location_name.lower().strip()
    for name, coords in hubs.items():
        if search_lower in name.lower() or name.lower() in search_lower:
            return coords[0], coords[1], name
            
    # Try augmenting with cluster data offline
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.abspath(os.path.join(script_dir, "..", "data", "mumbai_clustered_health_data.csv"))
        if os.path.exists(csv_path):
            import pandas as pd
            cdf = pd.read_csv(csv_path)
            regions = cdf[["Region", "Latitude", "Longitude"]].drop_duplicates().to_dict("records")
            for r in regions:
                if search_lower in r["Region"].lower() or r["Region"].lower() in search_lower:
                    return r["Latitude"], r["Longitude"], r["Region"]
    except Exception:
        pass
        
    return 19.0760, 72.8777, "Kurla West"

# Caching historical dataset loader (optimized monthly aggregation)

# Function to fetch recent simulation logs
def load_scenario_logs():
    conn = sqlite3.connect(db_path)
    query = """
        SELECT timestamp AS "Timestamp",
               location AS "Location",
               temp AS "Temperature (°C)",
               humidity AS "Humidity (%)",
               rainfall AS "21-Day Lag Rainfall (mm)",
               pm25 AS "PM2.5 AQI (µg/m³)",
               gastro_cases AS "Gastroenteritis Cases",
               heatstroke_cases AS "Heatstroke Cases",
               dengue_cases AS "Dengue Cases",
               malaria_cases AS "Malaria Cases",
               influenza_cases AS "Influenza Cases",
               bronchitis_cases AS "Bronchitis Cases",
               predicted_cases AS "Total Predicted Cases",
               risk_level AS "Risk Level"
        FROM scenario_logs
        ORDER BY id DESC
        LIMIT 5
    """
    df_logs = pd.read_sql_query(query, conn)
    conn.close()
    return df_logs

# Caching historical dataset loader (optimized monthly aggregation)
@st.cache_data
def load_historical_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.abspath(os.path.join(script_dir, "..", "data", "historical_mumbai_weather.csv"))
    if not os.path.exists(data_path):
        return None
    # Read CSV
    df = pd.read_csv(data_path)
    # Parse Date column and set as index
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.set_index("Date")
    # Compute 21-day rolling rainfall accumulation on daily data before downsampling
    df["Rainfall_Lag_21"] = df["Daily_Rain_mm"].rolling(window=21).sum()
    # Drop NaNs
    df = df.dropna()
    # Resample to Monthly frequency using mean values to optimize browser rendering
    df_monthly = df.resample("ME").mean()
    return df_monthly


# Caching regional vulnerability cluster loader
@st.cache_data
def load_vulnerability_clusters():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    clustered_csv_path = os.path.abspath(os.path.join(script_dir, "..", "data", "mumbai_clustered_health_data.csv"))
    if os.path.exists(clustered_csv_path):
        cdf = pd.read_csv(clustered_csv_path)
        unique_regions = cdf[["Region", "Latitude", "Longitude", "Cluster_ID", "Cluster_Zone"]].drop_duplicates().to_dict("records")
        return unique_regions
    return []


# Create navigation tabs right beneath the title header banner
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Outbreak Predictor", 
    "Historical Trends Explorer", 
    "🤖 GenAI Clinical Advisory Desk", 
    "Simulation Logs Archive", 
    "Advanced ML Analytics"
])

with tab1:
    # Telemetry placeholder at the top of the tab for full-width 3D glassmorphic card display
    telemetry_placeholder = st.container()
    
    # Initialize session state for coordinates to keep search and clicks in sync
    if "lat" not in st.session_state:
        st.session_state.lat = 19.0760
    if "lon" not in st.session_state:
        st.session_state.lon = 72.8777
    if "current_location_name" not in st.session_state:
        st.session_state.current_location_name = "Chembur (Default)"
    if "last_search" not in st.session_state:
        st.session_state.last_search = "Chembur"
    if "temp" not in st.session_state:
        st.session_state.temp = 28.0
    if "humidity" not in st.session_state:
        st.session_state.humidity = 75.0
    if "pm25" not in st.session_state:
        st.session_state.pm25 = 15.0
    if "wind_speed" not in st.session_state:
        st.session_state.wind_speed = 12.0
    if "weather_desc" not in st.session_state:
        st.session_state.weather_desc = "Clear Sky"
    if "pred_cases" not in st.session_state:
        st.session_state.pred_cases = 0
    if "pred_gastro" not in st.session_state:
        st.session_state.pred_gastro = 0
    if "pred_heatstroke" not in st.session_state:
        st.session_state.pred_heatstroke = 0
    if "pred_dengue" not in st.session_state:
        st.session_state.pred_dengue = 0
    if "pred_malaria" not in st.session_state:
        st.session_state.pred_malaria = 0
    if "pred_flu" not in st.session_state:
        st.session_state.pred_flu = 0
    if "pred_bronchitis" not in st.session_state:
        st.session_state.pred_bronchitis = 0
    if "rain_lag" not in st.session_state:
        st.session_state.rain_lag = 0.0

    # Left and Right column layout
    col1, col2 = st.columns([1, 1.1], gap="large")
    
    with col1:
        st.subheader("Climate & Environmental Inputs")
        
        # 1. Location search input
        location_search = st.text_input("🔍 Search Any Location/Ward in Mumbai", value="Chembur")
        
        # If user typed a new query, update coordinates via geocoding Nominatim call
        if location_search != st.session_state.last_search:
            lat_res, lon_res, resolved_res = geocode_mumbai_location(location_search)
            st.session_state.lat = lat_res
            st.session_state.lon = lon_res
            st.session_state.current_location_name = resolved_res
            st.session_state.last_search = location_search
            
        # Checkbox to connect to live real-world weather feed (using coordinates)
        live_feed = st.checkbox("📡 Connect Live Real-World Weather & AQI Feed", value=True)
        
        # Default initialization values
        temp_val = 28.0
        humidity_val = 75.0
        rain_val = 10.0
        month_val = datetime.now().month
        pm25_val = 15.0
        
        if live_feed:
            # Query cached streaming engine for 100% accurate live API metrics
            live_loc, live_temp, live_humidity, live_pm25 = get_live_metrics_and_location(st.session_state.lat, st.session_state.lon)
            
            st.session_state.current_location_name = live_loc
            st.session_state.temp = live_temp
            st.session_state.humidity = live_humidity
            st.session_state.pm25 = live_pm25
            
            temp_val = float(live_temp)
            humidity_val = float(live_humidity)
            pm25_val = float(live_pm25)
            rain_val = 5.0  # Safe real-world baseline fallback rain
            month_val = datetime.now().month
            month = month_val
            st.caption("🟢 **Live weather & AQI connected**: Currently streaming real-world sensor data via Open-Meteo API.")
            st.info(f"📅 **Extracted Season**: {['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][month_val-1]}")
        else:
            st.caption("ℹ️ Adjust sliders manually or click/search to query live weather metrics.")
            month = st.selectbox(
                "Active Analysis Month (Fallback)",
                options=list(range(1, 13)),
                format_func=lambda m: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][m-1],
                index=datetime.now().month - 1,
                help="Outbreak models are heavily seasonal (Summer, Monsoon, Winter)."
            )
            
        st.markdown("Configure the current local weather parameters and biological lags to predict potential daily case surges:")
        
        # 2. Temperature Slider
        temp = st.slider(
            "Current Temperature (°C)",
            min_value=15.0,
            max_value=40.0,
            value=temp_val,
            step=0.1,
            disabled=live_feed,
            help="Average daily temperature in Celsius."
        )
        
        # 3. Humidity Slider
        humidity = st.slider(
            "Relative Humidity (%)",
            min_value=30.0,
            max_value=100.0,
            value=humidity_val,
            step=0.5,
            disabled=live_feed,
            help="Average relative humidity percentage."
        )

        # 4. Daily Rainfall Slider
        rain_daily = st.slider(
            "Daily Rainfall (mm)",
            min_value=0.0,
            max_value=150.0,
            value=rain_val,
            step=0.1,
            disabled=live_feed,
            help="Current day's rainfall volume."
        )
        
        # 5. 21-Day Lagged Rainfall Slider (Rolling sum representation)
        rain_lag = st.slider(
            "21-Day Lagged Rainfall (mm)",
            min_value=0.0,
            max_value=500.0,
            value=min(rain_val * 15.0, 500.0),
            step=1.0,
            disabled=live_feed,
            help="Accumulated rainfall sum over the preceding 21 days."
        )
        
        # 6. PM2.5 Air Quality Index Slider
        pm25 = st.slider(
            "PM2.5 AQI (µg/m³)",
            min_value=5.0,
            max_value=150.0,
            value=pm25_val,
            step=0.1,
            disabled=live_feed,
            help="Particulate Matter 2.5 concentration level. High values trigger respiratory risks."
        )
        
        # 6. Interactive Folium Map selection with Fullscreen and 550px height
        st.markdown("---")
        # Call the new cached function using active lat and lon
        loc_name, live_temp, live_humidity, live_pm25 = get_live_metrics_and_location(st.session_state.lat, st.session_state.lon)
        st.session_state.current_location_name = loc_name
        st.session_state.temp = live_temp
        st.session_state.humidity = live_humidity
        st.session_state.pm25 = live_pm25
        
        st.markdown(f"### 📍 Active Target Zone: **{st.session_state.current_location_name}**")
        st.caption(f"Coordinates: Lat `{st.session_state.lat:.4f}`, Lon `{st.session_state.lon:.4f}`")
        st.caption("🖱️ Click anywhere on the map below to analyze that exact neighborhood's real-time outbreak risk:")
        
        # Center the map at the current coordinate state
        m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=12)
        # Add Fullscreen plugin to map
        Fullscreen().add_to(m)
        # Add marker at the current coordinates
        folium.Marker(
            [st.session_state.lat, st.session_state.lon],
            popup=st.session_state.current_location_name,
            tooltip="Active Outbreak Analysis Area",
            icon=folium.Icon(color="darkblue", icon="info-sign")
        ).add_to(m)
        
        # Add clustered microclimate locations to the map
        unique_regions = load_vulnerability_clusters()
        for r in unique_regions:
            zone = r["Cluster_Zone"]
            if zone == "Urban Heat Island Risk":
                color = "#ef4444" # Crimson Red
                popup_text = f"🔥 {r['Region']}: Urban Heat Island Risk"
            elif zone == "Waterlogging Vectors Risk":
                color = "#2563eb" # Cobalt Blue
                popup_text = f"💧 {r['Region']}: Waterlogging Vectors Risk"
            else:
                color = "#10b981" # Emerald Green
                popup_text = f"🟢 {r['Region']}: Stable Microclimate Risk"
                
            folium.CircleMarker(
                location=[r["Latitude"], r["Longitude"]],
                radius=10,
                popup=popup_text,
                tooltip=r["Region"],
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6
            ).add_to(m)
        
        # Render the map and record interactions (height=550px, responsive width)
        map_output = st_folium(m, height=550, use_container_width=True, key="mumbai_interactive_map")
        
        # Cluster Legend below the map
        st.markdown("""
        <div style="background-color: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 10px; margin-top: 10px; margin-bottom: 10px;">
            <p style="margin: 0; font-size: 0.85rem; font-weight: 600; color: #9ca3af; text-align: center;">
                🔬 <b>K-Means Microclimate Clustering Legend</b>:<br>
                <span style="color: #ef4444; margin-right: 12px;">● Crimson Red: Urban Heat Island Risk</span>
                <span style="color: #2563eb; margin-right: 12px;">● Cobalt Blue: Waterlogging Vectors Risk</span>
                <span style="color: #10b981;">● Emerald Green: Stable Microclimate Risk</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Listen for clicks and update active coordinate state if clicked somewhere new
        if map_output and map_output.get("last_clicked"):
            clicked = map_output["last_clicked"]
            clicked_lat = clicked["lat"]
            clicked_lon = clicked["lng"]
            
            # Simple threshold check to prevent floating-point rerun loops
            if abs(clicked_lat - st.session_state.lat) > 0.0001 or abs(clicked_lon - st.session_state.lon) > 0.0001:
                st.session_state.lat = clicked_lat
                st.session_state.lon = clicked_lon
                # Call cached function for live data
                loc_name, live_temp, live_humidity, live_pm25 = get_live_metrics_and_location(clicked_lat, clicked_lon)
                st.session_state.current_location_name = loc_name
                st.session_state.temp = live_temp
                st.session_state.humidity = live_humidity
                st.session_state.pm25 = live_pm25
                st.rerun()

        # 📡 Live Satellite Weather Telecast & Telemetry Board
        st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-top: 1.5rem; margin-bottom: 0.5rem;">
            <h4 style="margin: 0; color: #f3f4f6;">📡 Live Satellite Weather Telecast & Telemetry Board</h4>
            <span style="color: #10b981; font-weight: 700; font-size: 0.75rem; letter-spacing: 1px; display: inline-flex; align-items: center; gap: 6px;">
                <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background-color: #10b981; animation: pulse-green 1.5s infinite;"></span>
                • LIVE STREAM ACTIVE
            </span>
        </div>
        <style>
        @keyframes pulse-green {
            0% { transform: scale(0.95); opacity: 0.5; }
            50% { transform: scale(1.15); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.5; }
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.5); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 1.2rem; margin-top: 0.5rem; width: 100%;">
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 15px;">
                <div style="flex: 1; min-width: 120px; padding: 0.5rem; background: rgba(255,255,255,0.02); border-radius: 8px; border: 1px solid rgba(255,255,255,0.04); text-align: center;">
                    <div style="font-size: 0.75rem; color: #9ca3af; font-weight: 600; text-transform: uppercase; white-space: nowrap;">Temperature</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #f3f4f6; margin-top: 0.25rem; white-space: nowrap;">{st.session_state.temp:.1f} <span style="font-size: 0.9rem; font-weight: 500; color: #9ca3af;">°C</span></div>
                </div>
                <div style="flex: 1; min-width: 120px; padding: 0.5rem; background: rgba(255,255,255,0.02); border-radius: 8px; border: 1px solid rgba(255,255,255,0.04); text-align: center;">
                    <div style="font-size: 0.75rem; color: #9ca3af; font-weight: 600; text-transform: uppercase; white-space: nowrap;">Relative Humidity</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #f3f4f6; margin-top: 0.25rem; white-space: nowrap;">{st.session_state.humidity:.1f} <span style="font-size: 0.9rem; font-weight: 500; color: #9ca3af;">%</span></div>
                </div>
                <div style="flex: 1; min-width: 120px; padding: 0.5rem; background: rgba(255,255,255,0.02); border-radius: 8px; border: 1px solid rgba(255,255,255,0.04); text-align: center;">
                    <div style="font-size: 0.75rem; color: #9ca3af; font-weight: 600; text-transform: uppercase; white-space: nowrap;">Wind Velocity</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #f3f4f6; margin-top: 0.25rem; white-space: nowrap;">{st.session_state.wind_speed:.1f} <span style="font-size: 0.9rem; font-weight: 500; color: #9ca3af;">km/h</span></div>
                </div>
                <div style="flex: 1; min-width: 120px; padding: 0.5rem; background: rgba(255,255,255,0.02); border-radius: 8px; border: 1px solid rgba(255,255,255,0.04); text-align: center;">
                    <div style="font-size: 0.75rem; color: #9ca3af; font-weight: 600; text-transform: uppercase; white-space: nowrap;">PM2.5 AQI</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: #f3f4f6; margin-top: 0.25rem; white-space: nowrap;">{st.session_state.pm25:.1f} <span style="font-size: 0.9rem; font-weight: 500; color: #9ca3af;">µg/m³</span></div>
                </div>
            </div>
            <div style="margin-top: 1rem; font-size: 0.8rem; color: #9ca3af; border-top: 1px solid rgba(255, 255, 255, 0.05); padding-top: 0.5rem; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                <span>☁️ <b>Atmospheric Conditions</b>: {st.session_state.weather_desc}</span>
                <span>Coordinates: <code>{st.session_state.lat:.4f}°N, {st.session_state.lon:.4f}°E</code></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        
    with col2:
        st.subheader("Outbreak Risk Predictions")
        
        # Read the authentic live API metrics directly from the session state if live feed is enabled
        if live_feed:
            temp = float(st.session_state.temp)
            humidity = float(st.session_state.humidity)
            pm25 = float(st.session_state.pm25)
        
        # Render the telemetry card at the top of the app using the tab1 placeholder
        with telemetry_placeholder:
            st.markdown(f"""
            <div class="glass-card" style="display: flex; justify-content: space-around; align-items: center; text-align: center; gap: 10px; background: rgba(15, 23, 42, 0.45); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 1.5rem; box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.1); backdrop-filter: blur(12px); margin-bottom: 2rem;">
                <div>
                    <div style="font-size: 0.85rem; font-weight: 600; text-transform: uppercase; color: #06b6d4; letter-spacing: 1px;">📡 Temperature</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #f3f4f6; margin-top: 0.25rem;">{temp:.1f} <span style="font-size: 1.2rem; font-weight: 500; color: #9ca3af;">°C</span></div>
                </div>
                <div style="border-left: 1px solid rgba(255,255,255,0.1); height: 50px;"></div>
                <div>
                    <div style="font-size: 0.85rem; font-weight: 600; text-transform: uppercase; color: #06b6d4; letter-spacing: 1px;">💧 Relative Humidity</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #f3f4f6; margin-top: 0.25rem;">{humidity:.1f} <span style="font-size: 1.2rem; font-weight: 500; color: #9ca3af;">%</span></div>
                </div>
                <div style="border-left: 1px solid rgba(255,255,255,0.1); height: 50px;"></div>
                <div>
                    <div style="font-size: 0.85rem; font-weight: 600; text-transform: uppercase; color: #06b6d4; letter-spacing: 1px;">💨 PM2.5 Air Quality</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #f3f4f6; margin-top: 0.25rem;">{pm25:.1f} <span style="font-size: 1.2rem; font-weight: 500; color: #9ca3af;">µg/m³</span></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Construct input dataframe for model prediction with 6 features
        # Columns must match EXACTLY: ["Max_Temperature_C", "Mean_Humidity_Pct", "Daily_Rain_mm", "Rainfall_Lag_21", "Month", "PM25_Index"]
        input_df = pd.DataFrame({
            "Max_Temperature_C": [temp],
            "Mean_Humidity_Pct": [humidity],
            "Daily_Rain_mm": [rain_daily],
            "Rainfall_Lag_21": [rain_lag],
            "Month": [month],
            "PM25_Index": [pm25]
        })
        
        # Predict all 6 disease targets
        pred_out = model.predict(input_df)[0]
        pred_gastro = max(0, int(round(pred_out[0])))
        pred_heatstroke = max(0, int(round(pred_out[1])))
        pred_dengue = max(0, int(round(pred_out[2])))
        pred_malaria = max(0, int(round(pred_out[3])))
        pred_flu = max(0, int(round(pred_out[4])))
        pred_bronchitis = max(0, int(round(pred_out[5])))
        
        # Sum of all predictions
        total_cases = pred_gastro + pred_heatstroke + pred_dengue + pred_malaria + pred_flu + pred_bronchitis
        pred_cases = total_cases  # Alias for backward compatibility
        
        st.session_state.pred_cases = pred_cases
        st.session_state.pred_gastro = pred_gastro
        st.session_state.pred_heatstroke = pred_heatstroke
        st.session_state.pred_dengue = pred_dengue
        st.session_state.pred_malaria = pred_malaria
        st.session_state.pred_flu = pred_flu
        st.session_state.pred_bronchitis = pred_bronchitis
        st.session_state.rain_lag = rain_lag
        
        # 1. Probabilistic Threat Assessment calculations
        # Calculate season-specific base probability factors
        summer_factor = np.clip((temp - 25.0) / 15.0, 0.0, 1.0)
        monsoon_factor = (humidity / 100.0) * np.clip(rain_lag / 300.0, 0.0, 1.0)
        winter_factor = np.clip((34.0 - temp) / 15.0, 0.0, 1.0) * np.clip((100.0 - humidity) / 70.0, 0.0, 1.0)

        # Apply month weights to scale active season risks
        is_summer = month in [3, 4, 5]
        is_monsoon = month in [6, 7, 8, 9]
        is_winter = month in [10, 11, 12, 1, 2]

        # Map specific disease probabilities (0% - 100%)
        # Summer diseases
        p_gastro = (summer_factor * 85.0 + 10.0) if is_summer else (summer_factor * 15.0 + 5.0)
        p_heatstroke = (summer_factor * 90.0) if is_summer and temp > 32 else 0.0
        p_chickenpox = (summer_factor * 70.0 + 15.0) if is_summer else (summer_factor * 10.0)
        p_measles = (summer_factor * 65.0 + 10.0) if is_summer else (summer_factor * 5.0)
        p_prickly_heat = (summer_factor * 95.0) if is_summer else (summer_factor * 20.0)
        p_melasma = (summer_factor * 80.0) if is_summer else (summer_factor * 30.0)
        p_spoilage = (summer_factor * 75.0 + 10.0) if is_summer else (summer_factor * 15.0)

        # Monsoon diseases
        p_dengue = (monsoon_factor * 90.0 + 5.0) if is_monsoon else (monsoon_factor * 15.0)
        p_chikungunya = (monsoon_factor * 80.0 + 5.0) if is_monsoon else (monsoon_factor * 10.0)
        p_zika = (monsoon_factor * 50.0) if is_monsoon else (monsoon_factor * 5.0)
        p_lepto = (monsoon_factor * 85.0 + 5.0) if is_monsoon and rain_daily > 20 else (monsoon_factor * 10.0)
        p_toe_fungus = (monsoon_factor * 95.0) if is_monsoon else (monsoon_factor * 20.0)
        p_oily_dandruff = (monsoon_factor * 85.0) if is_monsoon else (monsoon_factor * 25.0)
        p_eczema = (monsoon_factor * 75.0) if is_monsoon else (monsoon_factor * 30.0)
        p_asthma = (monsoon_factor * 80.0 + 10.0) if is_monsoon else (monsoon_factor * 25.0)
        p_swimmer_ear = (monsoon_factor * 70.0) if is_monsoon else (monsoon_factor * 15.0)

        # Winter diseases
        p_flu = (winter_factor * 85.0 + 10.0) if is_winter else (winter_factor * 15.0)
        p_rsv = (winter_factor * 75.0 + 10.0) if is_winter else (winter_factor * 10.0)
        p_rhinovirus = (winter_factor * 90.0 + 5.0) if is_winter else (winter_factor * 20.0)
        p_dry_dandruff = (winter_factor * 95.0) if is_winter else (winter_factor * 15.0)
        p_xerosis = (winter_factor * 90.0) if is_winter else (winter_factor * 20.0)
        p_lips = (winter_factor * 85.0) if is_winter else (winter_factor * 25.0)
        p_smog_bronchitis = (winter_factor * 80.0 + 10.0) if is_winter else (winter_factor * 15.0)
        p_joints = (winter_factor * 75.0 + 15.0) if is_winter else (winter_factor * 20.0)

        # Helper to compute risk levels
        def compute_risk(base_probability):
            prob = min(100, max(0, int(round(base_probability))))
            if prob >= 70:
                level = "🔴 High Threat"
            elif prob >= 35:
                level = "🟡 Moderate Threat"
            else:
                level = "🟢 Low Risk"
            return prob, level

        # Helper to format disease cards
        def format_disease_item(name, base_prob):
            prob, level = compute_risk(base_prob)
            if "🔴" in level:
                color = "#f87171"
            elif "🟡" in level:
                color = "#fbbf24"
            else:
                color = "#34d399"
            return f"""
            <div style="margin-bottom: 0.8rem; padding: 0.65rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px; border-left: 4px solid {color};">
                <div style="font-weight: 600; font-size: 0.95rem; display: flex; justify-content: space-between; color: #f3f4f6;">
                    <span>{name}</span>
                    <span style="color: {color};">{prob}%</span>
                </div>
                <div style="font-size: 0.8rem; color: #9ca3af; margin-top: 0.25rem; font-weight: 500;">{level}</div>
            </div>
            """

        # Helper to compute probability based on key name
        def compute_prob_for_key(key):
            if is_summer:
                if key in ["Dehydration", "Heat exhaustion", "Gastroenteritis", "Stomach Flu"]:
                    return summer_factor * 85.0 + 10.0
                elif key in ["Heatstroke", "Low blood pressure"]:
                    return summer_factor * 90.0
                elif key in ["Chickenpox", "Measles", "Mumps"]:
                    return summer_factor * 70.0 + 10.0
                elif key in ["Prickly heat", "Sunburn", "Scalp sunburn", "Heat cramps"]:
                    return summer_factor * 95.0
                elif key in ["Melasma", "Photodermatitis", "General fatigue"]:
                    return summer_factor * 80.0
                elif key in ["Scalp folliculitis", "Excess Sweat-Induced Scalp Pruritus"]:
                    return summer_factor * 85.0 + 5.0
                elif key in ["Pink eye", "Styes", "Adenoviral Conjunctivitis (Pink Eye)"]:
                    return summer_factor * 75.0
                elif key in ["Nosebleeds"]:
                    return summer_factor * 50.0 + 10.0 if temp > 33 else 0.0
                else: # Allergies, food poisoning, etc.
                    return summer_factor * 70.0 + 15.0
            elif is_monsoon:
                if key in ["Dengue fever", "Malaria", "Chikungunya"]:
                    return monsoon_factor * 90.0 + 5.0
                elif key in ["Leptospirosis", "Hepatitis A & E"]:
                    return monsoon_factor * 85.0 + 5.0 if rain_daily > 15 else monsoon_factor * 10.0
                elif key in ["Athlete's foot", "Jock itch", "Body ringworm"]:
                    return monsoon_factor * 95.0
                elif key in ["Oily dandruff", "Scalp ringworm", "Nail fungal infections", "Intertrigo", "Scabies", "Humidity-driven eczema"]:
                    return monsoon_factor * 85.0
                elif key in ["Swimmer's ear", "Allergic rhinitis", "Mold-triggered asthma", "Mold allergies"]:
                    return monsoon_factor * 80.0
                else:
                    return monsoon_factor * 60.0
            else: # is_winter
                if key in ["Influenza", "Rhinovirus (Common Cold)", "Respiratory Syncytial Virus (RSV)", "RSV"]:
                    return winter_factor * 90.0 + 5.0
                elif key in ["Viral bronchitis", "Pneumonia", "Smog-induced asthma", "COPD flare-ups"]:
                    return winter_factor * 85.0
                elif key in ["Xerosis", "Chapped lips", "Cheilitis"]:
                    return winter_factor * 95.0
                elif key in ["Flaky dry dandruff", "Brittle hair breakage", "Split ends"]:
                    return winter_factor * 90.0
                elif key in ["Sinusitis", "Pollutant-Driven Sore Throat"]:
                    return winter_factor * 85.0
                else:
                    return winter_factor * 75.0

        # Helper to compute risk levels
        def compute_risk(base_probability):
            prob = min(100, max(0, int(round(base_probability))))
            if prob >= 70:
                level = "🔴 High Threat"
            elif prob >= 35:
                level = "🟡 Moderate Threat"
            else:
                level = "🟢 Low Risk"
            return prob, level

        # Helper to format disease cards with clickable Wikipedia links
        def format_disease_item(name):
            base_prob = compute_prob_for_key(name)
            prob, level = compute_risk(base_prob)
            if "🔴" in level:
                color = "#f87171"
            elif "🟡" in level:
                color = "#fbbf24"
            else:
                color = "#34d399"
            
            wiki_url = WIKIPEDIA_LINKS.get(name, "https://en.wikipedia.org/")
            return f"""
            <div style="margin-bottom: 0.8rem; padding: 0.65rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px; border-left: 4px solid {color};">
                <div style="font-weight: 600; font-size: 0.95rem; display: flex; justify-content: space-between; color: #f3f4f6;">
                    <span><a href="{wiki_url}" target="_blank" style="color: #60a5fa; text-decoration: none; font-weight: 600;">{name}</a></span>
                    <span style="color: {color};">{prob}%</span>
                </div>
                <div style="font-size: 0.8rem; color: #9ca3af; margin-top: 0.25rem; font-weight: 500;">{level}</div>
            </div>
            """

        if is_summer:
            season_name = "Summer Season (Grishma Ritu)"
            # Respiratory & Systemic
            sys_names = [
                "Dehydration", "Heatstroke", "Heat exhaustion", "Heat cramps", 
                "General fatigue", "Food poisoning", "Gastroenteritis", "Diarrhea", 
                "Dysentery", "Typhoid fever", "Cholera", "Chickenpox", "Measles", 
                "Mumps", "Heat-induced migraines", "Low blood pressure", "Stomach Flu"
            ]

            # Dermatological
            skin_names = ["Prickly heat", "Sunburn", "Melasma", "Photodermatitis"]

            # Trichological
            hair_names = ["Scalp folliculitis", "Excess Sweat-Induced Scalp Pruritus", "Scalp sunburn"]

            # Ocular & ENT
            ent_names = [
                "Adenoviral Conjunctivitis (Pink Eye)", "Styes", "Nosebleeds", 
                "Dust allergies", "Pollen allergies", "Pink eye"
            ]

            symptom_title = "🌡️ Summer Active Viral Symptom Tracker"
            symptoms_list = [
                "**Chickenpox/Measles**: Low-grade fever followed by body aches, sore throat, and itchy fluid-filled rash vesicles.",
                "**Heatstroke**: Severe headache, dizziness, hot red dry skin (no sweat), rapid heartbeat, vomiting, or confusion.",
                "**Stomach Flu**: Acute onset of severe watery diarrhea, vomiting, stomach cramps, and moderate dehydration signs."
            ]
            
            ayur_title = "🌿 Grishma Ritu Wellness Guide (Summer)"
            ayur_intro = "Based on authentic Ayurvedic *Ritucharya* principles for Grishma Ritu (Summer):"
            prevention_list = [
                "Drink 3-4 liters of water daily; consume coconut water or buttermilk on a strict 2-hour hydration schedule.",
                "Limit direct solar exposure during peak hours (11 AM to 4 PM) to avoid sunburn and heatstroke vectors.",
                "Wear loose, breathable, light-colored cotton clothing to facilitate sweat evaporation and cool body temp.",
                "Maintain cross-ventilation indoors; utilize sun-reflective curtains or blinds to block hot dry air."
            ]
            ayur_list = [
                "Drink refreshing fennel (Saunf) and coriander seed infusions daily to soothe internal Pitta fire.",
                "Apply fresh Aloe Vera (Kumari) pulp or red sandalwood paste to soothe prickly heat rashes and sunburns.",
                "Take 1-2 teaspoons of Amla juice daily in the morning to build heat-resistance and boost Vitamin C.",
                "Wipe sweat-prone skin folds with vetiver (Khus) infused water to cool down and prevent sweat rash."
            ]
            otc_list = [
                "Keep Oral Rehydration Salts (ORS) packets handy to quickly replenish electrolytes lost through sweating.",
                "Apply Calamine Lotion topically to soothe prickly heat bumps, sunburn peeling, and hives.",
                "Use lubricating artificial tear drops to soothe dry, burning eyes or red conjunctivitis symptoms.",
                "Keep Paracetamol (500mg) to treat mild heat-induced headaches, ensuring you stay hydrated when taking it."
            ]

        elif is_monsoon:
            season_name = "Monsoon Season (Varsha Ritu)"
            # Respiratory & Systemic
            sys_names = [
                "Dengue fever", "Malaria", "Chikungunya", "Zika virus", 
                "Post-viral arthritis", "Myalgia", "Calf muscle tenderness", 
                "Leptospirosis", "Hepatitis A & E", "Amebiasis", "Giardiasis", 
                "Tapeworm infections", "West Nile Virus", "Enteroviral Hand, Foot, and Mouth Disease (HFMD)"
            ]

            # Dermatological
            skin_names = [
                "Athlete's foot", "Humidity-driven eczema", "Jock itch", 
                "Body ringworm", "Nail fungal infections", "Intertrigo", "Scabies"
            ]

            # Trichological
            hair_names = ["Oily dandruff", "Scalp ringworm"]

            # Ocular & ENT
            ent_names = ["Swimmer's ear", "Allergic rhinitis", "Mold allergies", "Mold-triggered asthma"]

            symptom_title = "🌡️ Monsoon Active Viral Symptom Tracker"
            symptoms_list = [
                "**Dengue/Chikungunya**: Sudden extreme high fever, severe retro-orbital pain, severe joint swelling, and body rash.",
                "**Leptospirosis**: Shivering chills, severe muscle aches (calves/back), yellowish skin or eyes (jaundice), and red eyes.",
                "**Mold Asthma**: Dry chest wheezing, tightness, dry coughing fits, and nasal mucosal congestion."
            ]
            
            ayur_title = "🌿 Varsha Ritu Wellness Guide (Monsoon)"
            ayur_intro = "Based on authentic Ayurvedic *Ritucharya* principles for Varsha Ritu (Monsoon):"
            prevention_list = [
                "Boil drinking water completely and store it in clean, covered vessels to prevent waterborne pathogens.",
                "Check and clear stagnant water in flower pots, cooler trays, and gutters every 3 days to halt mosquito breeding.",
                "Apply DEET-based mosquito insect repellents and wear full-sleeve clothes when going outdoors in the evening.",
                "Keep footwear completely dry; avoid wearing wet socks or damp shoes to prevent skin fungal infections."
            ]
            ayur_list = [
                "Consume a warm decoction of Guduchi (Giloy) juice or Samshamani Vati to support platelet count and cellular immunity.",
                "Drink warm water (Ushnodaka) infused with a pinch of dry Ginger to kindle the digestive fire (Agni).",
                "Wash feet and skin folds with Neem (Nimba) and Turmeric (Haridra) infused water to halt fungal activity.",
                "Apply a dry paste of Triphala powder mixed with water to damp intertrigo (athlete's foot) to dry up the skin."
            ]
            otc_list = [
                "Apply Clotrimazole (1%) or Miconazole dusting powder to groin and toe folds to prevent fungal infections.",
                "Keep Zinc tablets (20mg) and ORS on hand to treat acute monsoon gastroenteritis and diarrhea scenarios.",
                "Use safe saline nasal drops or sprays to keep the nasal passages clear of humidity-induced mold allergens.",
                "Keep Paracetamol (500mg) to treat sudden monsoon fever spells or joint aches before visiting a doctor."
            ]

        else: # is_winter
            season_name = "Winter Season (Hemant & Shishir Ritu)"
            # Respiratory & Systemic
            sys_names = [
                "Influenza", "Rhinovirus (Common Cold)", "Respiratory Syncytial Virus (RSV)", 
                "Smog-induced asthma", "Viral bronchitis", "Pneumonia", "COPD flare-ups", 
                "Common cold", "RSV", "Rotavirus", "Winter Diarrhea", "Norovirus", 
                "Increased heart attack risk", "Seasonal Affective Disorder"
            ]

            # Dermatological
            skin_names = [
                "Xerosis", "Chapped lips", "Cheilitis", "Cold urticaria", 
                "Psoriasis worsening", "Cold-driven eczema", "Chilblains"
            ]

            # Trichological
            hair_names = ["Flaky dry dandruff", "Brittle hair breakage", "Split ends"]

            # Ocular & ENT
            ent_names = [
                "Sinusitis", "Pollutant-Driven Sore Throat", "Arthritis joint stiffness", 
                "Rheumatoid arthritis", "Muscle spasms", "Raynaud's phenomenon"
            ]

            symptom_title = "🌡️ Winter Active Viral Symptom Tracker"
            symptoms_list = [
                "**Influenza/RSV**: High fever, dry cough, severe fatigue, sore throat, running nose, and dry body chills.",
                "**Smog Bronchitis**: Tight heavy chest, dry barking cough, shortness of breath, or mucous blockages.",
                "**Rhinovirus**: Nasal congestion, constant sneezing, scratching throat, and mild headache."
            ]
            
            ayur_title = "🌿 Hemant / Shishir Ritu Wellness Guide (Winter)"
            ayur_intro = "Based on authentic Ayurvedic *Ritucharya* principles for Hemant / Shishir Ritu (Winter):"
            prevention_list = [
                "Maintain indoor humidity levels between 40-50% using humidifiers to keep respiratory tracts moist.",
                "Wear layered warm woolen clothing to protect the chest and extremities from direct cold draft exposure.",
                "Gargle with warm salt water twice daily to keep the throat clean of viruses and heavy smog particles.",
                "Wash hands with soap frequently, especially after coughing or returning from crowded public transport."
            ]
            ayur_list = [
                "Take a daily spoonful of authentic Amla-rich Chyawanprash to build a strong immune shield for the lungs.",
                "Drink warm Golden Milk (Haldi Doodh) infused with Ashwagandha and a pinch of black pepper at bedtime.",
                "Take Sitopaladi Churna mixed with raw honey to soothe dry cough tickles and throat irritation.",
                "Practice Nasya by applying 2 drops of warm sesame oil (Til Taila) in each nostril to lubricate nasal pathways."
            ]
            otc_list = [
                "Use saline nasal drops or sprays to soothe nasal dryness and clear winter smog-driven sinus blocks.",
                "Use OTC throat lozenges containing amylmetacresol or cough suppressants for dry, hacking winter coughs.",
                "Apply ceramide-based or urea-rich moisturizing creams to treat dry, cracked winter skin (Xerosis) and eczema.",
                "Use Ketoconazole (2%) or Coal Tar shampoo twice weekly to control severe dry, flaky scalp dandruff."
            ]

        # Generate HTML content strings for columns
        col1_content = "".join([format_disease_item(name) for name in sys_names])
        col2_content = "".join([format_disease_item(name) for name in skin_names])
        col3_content = "".join([format_disease_item(name) for name in hair_names])
        col4_content = "".join([format_disease_item(name) for name in ent_names])

        # Render layout
        st.subheader("📋 Most Likely Seasonal Health Threats Active Today")
        st.caption(f"Based on: **{season_name}** diagnostics at coordinate metrics.")
        
        # 2x2 Grid of columns
        grid_row1_col1, grid_row1_col2 = st.columns(2, gap="large")
        with grid_row1_col1:
            st.markdown(f"<h4 style='color: #a7f3d0; border-bottom: 2px solid rgba(167, 243, 208, 0.2); padding-bottom: 0.4rem;'>🫁 Respiratory & Systemic Health</h4>", unsafe_allow_html=True)
            st.markdown(col1_content, unsafe_allow_html=True)
            
        with grid_row1_col2:
            st.markdown(f"<h4 style='color: #fbcfe8; border-bottom: 2px solid rgba(251, 207, 232, 0.2); padding-bottom: 0.4rem;'>🧴 Dermatological & Skin Health</h4>", unsafe_allow_html=True)
            st.markdown(col2_content, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        grid_row2_col1, grid_row2_col2 = st.columns(2, gap="large")
        with grid_row2_col1:
            st.markdown(f"<h4 style='color: #bfdbfe; border-bottom: 2px solid rgba(191, 219, 254, 0.2); padding-bottom: 0.4rem;'>💇‍♂️ Trichological & Scalp Health</h4>", unsafe_allow_html=True)
            st.markdown(col3_content, unsafe_allow_html=True)
            
        with grid_row2_col2:
            st.markdown(f"<h4 style='color: #fef08a; border-bottom: 2px solid rgba(254, 240, 138, 0.2); padding-bottom: 0.4rem;'>👁️ Ocular & ENT Health</h4>", unsafe_allow_html=True)
            st.markdown(col4_content, unsafe_allow_html=True)
            

    # 3D Glassmorphic Three-Tiered Solution Matrix
    st.markdown("---")
    st.markdown("### 🔬 Three-Tiered Solution Matrix")
    st.caption(f"Personalized preventative, traditional, and medical care protocols mapped dynamically to **{season_name}** threats.")
    
    sol_col1, sol_col2, sol_col3 = st.columns(3)
    
    with sol_col1:
        # Card 1 (🌿 Prevention & Lifestyle)
        prev_html = "".join([f"<li style='margin-bottom: 0.8rem; line-height: 1.5; color: #e5e7eb; font-size: 0.92rem;'>{item}</li>" for item in prevention_list])
        st.markdown(f"""
        <div style="background-color: rgba(6, 182, 212, 0.05); border: 1.5px solid #06b6d4; border-radius: 16px; padding: 20px; box-shadow: 0 15px 35px rgba(6, 182, 212, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); min-height: 480px;">
            <h4 style="color: #06b6d4; margin-top: 0; margin-bottom: 0.8rem; font-size: 1.2rem; font-weight: 700; display: flex; align-items: center; gap: 8px;">
                <span>🌿 Prevention & Lifestyle</span>
            </h4>
            <p style="color: #a5f3fc; font-style: italic; font-size: 0.85rem; margin-top: 0; margin-bottom: 1rem;">Daily routines, hydration schedules, and environmental adjustments:</p>
            <ul style="margin: 0; padding-left: 1.2rem;">
                {prev_html}
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with sol_col2:
        # Card 2 (🥣 Traditional Ayurvedic Care)
        ayur_html = "".join([f"<li style='margin-bottom: 0.8rem; line-height: 1.5; color: #e5e7eb; font-size: 0.92rem;'>{item}</li>" for item in ayur_list])
        st.markdown(f"""
        <div style="background-color: rgba(16, 185, 129, 0.05); border: 1px solid #10b981; border-radius: 16px; padding: 20px; box-shadow: 0 0 20px rgba(16, 185, 129, 0.15), inset 0 1px 1px rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); min-height: 480px;">
            <h4 style="color: #10b981; margin-top: 0; margin-bottom: 0.8rem; font-size: 1.2rem; font-weight: 700; display: flex; align-items: center; gap: 8px;">
                <span>🥣 Traditional Ayurvedic Care</span>
            </h4>
            <p style="color: #a7f3d0; font-style: italic; font-size: 0.85rem; margin-top: 0; margin-bottom: 1rem;">Ritucharya guidelines and easily accessible home remedies:</p>
            <ul style="margin: 0; padding-left: 1.2rem;">
                {ayur_html}
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    with sol_col3:
        # Card 3 (💊 Over-the-Counter OTC Pharmacy)
        otc_html = "".join([f"<li style='margin-bottom: 0.8rem; line-height: 1.5; color: #e5e7eb; font-size: 0.92rem;'>{item}</li>" for item in otc_list])
        st.markdown(f"""
        <div style="background-color: rgba(245, 158, 11, 0.05); border: 1.5px solid #f59e0b; border-radius: 16px; padding: 20px; box-shadow: 0 15px 35px rgba(245, 158, 11, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); min-height: 480px;">
            <h4 style="color: #f59e0b; margin-top: 0; margin-bottom: 0.8rem; font-size: 1.2rem; font-weight: 700; display: flex; align-items: center; gap: 8px;">
                <span>💊 Over-the-Counter OTC Pharmacy</span>
            </h4>
            <p style="color: #fef3c7; font-style: italic; font-size: 0.85rem; margin-top: 0; margin-bottom: 1rem;">Safe medical counter-options and non-prescription home relief:</p>
            <ul style="margin: 0; padding-left: 1.2rem;">
                {otc_html}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Balanced 2-column container system beneath matrix for Symptoms & Warnings
    st.markdown("<br>", unsafe_allow_html=True)
    col_left, col_right = st.columns(2, gap="large")
    
    with col_left:
        st.markdown(f"### {symptom_title}")
        for item in symptoms_list:
            st.markdown(item)
            
    with col_right:
        st.markdown("""
        <div style="background-color: rgba(239, 68, 68, 0.12); border: 2px solid #ef4444; border-radius: 16px; padding: 20px; box-shadow: 0 0 20px rgba(239, 68, 68, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px);">
            <span style="font-weight: 800; color: #f87171; font-size: 1.1rem; display: block; margin-bottom: 0.4rem;">⚠️ Red Flag Symptoms:</span>
            <span style="font-size: 0.95rem; color: #fca5a5; line-height: 1.6; font-weight: 500;">If you are experiencing persistent high fever, breathing difficulties, bleeding gums, or extreme lethargy, do not self-medicate. Seek professional medical treatment from a doctor immediately.</span>
        </div>
        """, unsafe_allow_html=True)
    
    render_rishi_footer("tab1")








with tab2:
    st.markdown("## 📈 Historical Climate vs. Outbreak Trends Analysis")
    historical_df = load_historical_data()
    
    if historical_df is not None:
        st.markdown("""
        This interactive visualization plots historical daily rainfall and climate trends from the **5-year real-world Mumbai Weather Archive (2021–2025)**. 
        It maps weather parameters to dynamic risk curves for all biological systems, proving the seasonal correlations and biological lags.
        """)
        
        # Category Selector for Anatomical Analysis
        trend_system = st.radio(
            "📊 Select Anatomical System for Historical Trend Analysis",
            ["🫁 Respiratory & Systemic", "🧴 Dermatological & Skin", "💇‍♂️ Trichological & Scalp", "👁️ Ocular & ENT"],
            horizontal=True
        )
        
        # Calculate dynamic risk curves on the monthly historical weather dataset
        historical_df["Month"] = historical_df.index.month
        temp = historical_df["Max_Temperature_C"]
        humidity = historical_df["Mean_Humidity_Pct"]
        rain_lag = historical_df["Rainfall_Lag_21"]
        rain_daily = historical_df["Daily_Rain_mm"]
        month = historical_df["Month"]
        
        summer_factor = ((temp - 25.0) / 15.0).clip(lower=0, upper=1)
        monsoon_factor = (humidity / 100.0) * ((rain_lag / 300.0).clip(lower=0, upper=1))
        winter_factor = ((34.0 - temp) / 15.0).clip(lower=0, upper=1) * ((100.0 - humidity) / 70.0).clip(lower=0, upper=1)
        
        is_summer = month.isin([3, 4, 5]).astype(float)
        is_monsoon = month.isin([6, 7, 8, 9]).astype(float)
        is_winter = month.isin([10, 11, 12, 1, 2]).astype(float)
        
        # Systemic/Respiratory
        historical_df["Gastroenteritis Risk (%)"] = (is_summer * (summer_factor * 85.0 + 10.0) + (1.0 - is_summer) * (summer_factor * 15.0 + 5.0)).round(1)
        historical_df["Heatstroke Risk (%)"] = (is_summer * (summer_factor * 90.0) * (temp > 32).astype(float)).round(1)
        historical_df["Dengue Risk (%)"] = (is_monsoon * (monsoon_factor * 90.0 + 5.0) + (1.0 - is_monsoon) * (monsoon_factor * 15.0)).round(1)
        historical_df["Malaria Risk (%)"] = (is_monsoon * (monsoon_factor * 80.0 + 5.0) + (1.0 - is_monsoon) * (monsoon_factor * 10.0)).round(1)
        historical_df["Influenza Risk (%)"] = (is_winter * (winter_factor * 85.0 + 10.0) + (1.0 - is_winter) * (winter_factor * 15.0)).round(1)
        historical_df["Bronchitis Risk (%)"] = (is_winter * (winter_factor * 80.0 + 10.0) + (1.0 - is_winter) * (winter_factor * 15.0)).round(1)
        
        # Skin
        historical_df["Athlete's Foot Risk (%)"] = (is_monsoon * (monsoon_factor * 95.0) + (1.0 - is_monsoon) * (monsoon_factor * 20.0)).round(1)
        historical_df["Xerosis Risk (%)"] = (is_winter * (winter_factor * 95.0) + (1.0 - is_winter) * (winter_factor * 20.0)).round(1)
        
        # Scalp
        historical_df["Oily Dandruff Risk (%)"] = (is_monsoon * (monsoon_factor * 85.0) + (1.0 - is_monsoon) * (monsoon_factor * 25.0)).round(1)
        historical_df["Dry Flaky Dandruff Risk (%)"] = (is_winter * (winter_factor * 95.0) + (1.0 - is_winter) * (winter_factor * 15.0)).round(1)
        
        # Ocular/ENT
        historical_df["Pink Eye Risk (%)"] = (is_summer * (summer_factor * 75.0) + (1.0 - is_summer) * (summer_factor * 15.0)).round(1)
        historical_df["Chronic Sinusitis Risk (%)"] = (is_winter * (winter_factor * 80.0) + (1.0 - is_winter) * (winter_factor * 20.0)).round(1)
        
        # Dynamically set plot columns and descriptive insights based on selection
        if trend_system == "🫁 Respiratory & Systemic":
            plot_cols = [
                "Max_Temperature_C", "Gastroenteritis Risk (%)", "Dengue Risk (%)", 
                "Malaria Risk (%)", "Influenza Risk (%)", "Bronchitis Risk (%)"
            ]
            desc_text = """
            **Anatomical System Insight**: Systemic illnesses track the major seasons of Mumbai. 
            - **☀️ Summer Peak (March–May)**: The rise in Max Temperature triggers immediate gastroenteritis risk, indicating high systemic stress and water-borne food safety threats.
            - **🌧️ Monsoon Peak (June–September)**: Dengue and Malaria risks peak during high humidity monsoons. Notice the **biological breeding delay lag**: the risk builds up gradually over the monsoon months, showing the delay required for accumulated rainwater to generate vectors.
            - **❄️ Winter Peak (October–February)**: Flu and Bronchitis risks rise as temperatures drop, representing cold weather respiratory virus surges.
            """
        elif trend_system == "🧴 Dermatological & Skin":
            plot_cols = ["Mean_Humidity_Pct", "Athlete's Foot Risk (%)", "Xerosis Risk (%)"]
            desc_text = """
            **Anatomical System Insight**: Skin barriers react directly to humidity trends.
            - **🌧️ Monsoon Peak (June–September)**: The high Mean Humidity Pct triggers athlete's foot (fungal) risks, driven by water logging and damp skin friction.
            - **❄️ Winter Peak (October–February)**: Dry xerosis (extreme dry skin) risk curves climb as humidity drops below 50%, dehydrating the lipid barrier.
            """
        elif trend_system == "💇‍♂️ Trichological & Scalp":
            plot_cols = ["Mean_Humidity_Pct", "Oily Dandruff Risk (%)", "Dry Flaky Dandruff Risk (%)"]
            desc_text = """
            **Anatomical System Insight**: Scalp microflora cycles between humidity-driven excess sebum and cold-driven dryness.
            - **🌧️ Monsoon Peak**: Oily Dandruff risks peak during humid monsoon months as high sweat and sebum excretion feeds Malassezia yeast.
            - **❄️ Winter Peak**: Flaky Dry Dandruff risks surge as winter air dries out the stratum corneum, causing skin flaking.
            """
        else: # Ocular & ENT
            plot_cols = ["Max_Temperature_C", "Pink Eye Risk (%)", "Chronic Sinusitis Risk (%)"]
            desc_text = """
            **Anatomical System Insight**: Ocular and sinus paths are sensitive to dust/heat and temperature shifts.
            - **☀️ Summer Peak**: Pink Eye (adenoviral conjunctivitis) risks peak during summer heat and dry dust-storm exposure.
            - **❄️ Winter Peak**: Chronic Sinusitis risks escalate during winter cold, driven by mucus thickening and low air flow.
            """
            
        st.markdown(desc_text)
        st.line_chart(historical_df[plot_cols])
        
        # New section: Model Interpretability & Feature Weights
        st.markdown("---")
        st.markdown("### 🧠 Model Interpretability & Feature Weights")
        
        # Access features and labels
        features = ["Max_Temperature_C", "Mean_Humidity_Pct", "Daily_Rain_mm", "Rainfall_Lag_21", "Month", "PM25_Index"]
        label_map = {
            "Max_Temperature_C": "🌡️ Max Temperature",
            "Mean_Humidity_Pct": "💧 Mean Humidity",
            "Daily_Rain_mm": "🌧️ Daily Rain",
            "Rainfall_Lag_21": "🌊 Rainfall Lag (21d)",
            "Month": "📅 Season Month",
            "PM25_Index": "💨 PM2.5 AQI"
        }
        
        # Extract feature importances
        if hasattr(model, "estimators_"):
            importances = np.mean([est.feature_importances_ for est in model.estimators_], axis=0)
        elif hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
        else:
            importances = np.array([0.16, 0.16, 0.16, 0.16, 0.16, 0.2])
            
        importance_pct = importances * 100.0
        feature_labels = [label_map.get(f, f) for f in features]
        
        importance_df = pd.DataFrame({
            "Feature": feature_labels,
            "Relative Importance (%)": importance_pct
        })
        
        # Sort values for visual readability
        importance_df = importance_df.sort_values(by="Relative Importance (%)", ascending=False)
        
        # Render using Altair for custom styles matching rest of green theme
        import altair as alt
        chart = alt.Chart(importance_df).mark_bar(
            cornerRadiusEnd=4,
            color="#10b981"
        ).encode(
            x=alt.X('Relative Importance (%):Q', title='Relative Mathematical Weight (%)'),
            y=alt.Y('Feature:N', title='Climate Driver Feature', sort='-x'),
            tooltip=['Feature', alt.Tooltip('Relative Importance (%):Q', format='.1f')]
        ).properties(
            height=250
        )
        st.altair_chart(chart, use_container_width=True)
        
        st.caption(
            "💡 **Interpretability Transparency**: This interactive feature weights chart reveals how our "
            "epidemiological Random Forest regressor weights specific environmental parameters. By averaging across "
            "all output estimators, it illustrates how lagging monsoon rainfall parameters (`Rainfall_Lag_21`) "
            "interact with immediate surface metrics (such as `Max_Temperature_C` and `Mean_Humidity_Pct`) to determine "
            "biological risks across Mumbai's distinct seasonal cycles."
        )
    else:
        st.warning("Historical dataset 'data/historical_mumbai_weather.csv' could not be loaded. Please ensure the pipeline scripts have run successfully.")

    render_rishi_footer("tab2")



# Load baseline distribution stats for Z-score drift checks
@st.cache_data
def get_baseline_stats():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    clustered_path = os.path.abspath(os.path.join(script_dir, "..", "data", "mumbai_clustered_health_data.csv"))
    if os.path.exists(clustered_path):
        try:
            df_clust = pd.read_csv(clustered_path)
            stats = {}
            for col in ["Max_Temperature_C", "Daily_Rain_mm", "PM25_Index"]:
                if col in df_clust.columns:
                    stats[col] = {
                        "mean": float(df_clust[col].mean()),
                        "std": float(df_clust[col].std())
                    }
            return stats
        except Exception:
            pass
            
    hist_path = os.path.abspath(os.path.join(script_dir, "..", "data", "historical_mumbai_weather.csv"))
    if os.path.exists(hist_path):
        try:
            df_hist = pd.read_csv(hist_path)
            return {
                "Max_Temperature_C": {"mean": float(df_hist["Max_Temperature_C"].mean()), "std": float(df_hist["Max_Temperature_C"].std())},
                "Daily_Rain_mm": {"mean": float(df_hist["Daily_Rain_mm"].mean()), "std": float(df_hist["Daily_Rain_mm"].std())},
                "PM25_Index": {"mean": 30.0, "std": 15.0}
            }
        except Exception:
            pass
            
    return {
        "Max_Temperature_C": {"mean": 28.0, "std": 3.0},
        "Daily_Rain_mm": {"mean": 10.0, "std": 8.0},
        "PM25_Index": {"mean": 30.0, "std": 15.0}
    }


with tab5:
    st.markdown("## 🔬 Advanced Machine Learning Analytics & Pipeline Reports")
    st.markdown("""
    This dedicated laboratory analytics workspace displays competitive benchmark statistics, hyperparameter tuning 
    logs, and unsupervised regional clustering partitions resolved across Mumbai's microclimates.
    """)
    
    # 1. Model Performance Benchmark Matrix
    st.markdown("### 📊 Model Performance Benchmark Matrix")
    st.markdown("""
    This interactive table shows testing evaluation metrics across our baseline, optimized, and champion 
    epidemiological models. The system automatically promotes the model with the highest testing $R^2$ score 
    to be the active production inference engine.
    """)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    benchmark_json_path = os.path.abspath(os.path.join(script_dir, "..", "models", "benchmark_metrics.json"))
    
    if os.path.exists(benchmark_json_path):
        try:
            with open(benchmark_json_path, "r") as f:
                bench_data = json.load(f)
            # Build DataFrame
            bench_df = pd.DataFrame(bench_data).T
            bench_df.index.name = "Modeling Architecture"
            bench_df.columns = ["Mean Absolute Error (MAE)", "Root Mean Squared Error (RMSE)", "Testing R² Score"]
            st.dataframe(bench_df.style.highlight_max(subset=["Testing R² Score"], color="rgba(16, 185, 129, 0.2)"), use_container_width=True)
        except Exception as e:
            st.error(f"Error loading benchmark metrics: {e}")
    else:
        st.info("Performance benchmarks are loading. Please verify that scripts/train_multi_season_model.py has run successfully.")
        
    # 2. Hyperparameter Tuning Metrics Log
    st.markdown("---")
    st.markdown("### ⚙️ Champion Hyperparameter Optimization Registry")
    st.markdown("""
    The grid parameters listed below represent the mathematically optimal estimator parameters discovered during 
    cross-validation (GridSearchCV) sweeps on the Random Forest tree weights.
    """)
    
    best_params = {}
    if model is not None:
        if hasattr(model, "estimators_") and len(model.estimators_) > 0:
            base_est = model.estimators_[0]
            if hasattr(base_est, "get_params"):
                params = base_est.get_params()
                # 🛠️ Fix 2: Clean mapping for parameter display strings
            criterion_map = {
                "squared_error": "Mean Squared Error (MSE)",
                "absolute_error": "Mean Absolute Error (MAE)",
                "friedman_mse": "Friedman MSE",
                "poisson": "Poisson Reduction"
            }
            raw_criterion = params.get("criterion")
            clean_criterion = criterion_map.get(raw_criterion, str(raw_criterion).replace('_', ' ').title())

            best_params = {
                "Max Depth Limit": params.get("max_depth") or "None (Unlimited)",
                "Optimal Estimators Count": params.get("n_estimators"),
                "Min Samples Split": params.get("min_samples_split"),
                "Tree Split Criterion": clean_criterion
            }
                
    if best_params:
        param_cols = st.columns(len(best_params))
        for idx, (param, val) in enumerate(best_params.items()):
            with param_cols[idx]:
                st.metric(label=param, value=str(val))
    else:
        st.info("Hyperparameter optimization logs are currently loading or unavailable.")
        
    # 3. Unsupervised Regional Vulnerabilities (K-Means)
    st.markdown("---")
    st.markdown("### 🧮 Unsupervised K-Means Regional Vulnerability Report")
    st.markdown("""
    An unsupervised Scikit-Learn **K-Means Clustering** model ($K=3$) was fitted to the geographic coordinates 
    (latitude/longitude) and average temperature/precipitation trends across Mumbai regions to partition the wards 
    into three distinct risk zones:
    
    1. **Urban Heat Island Risk (🔴 Crimson Red)**: Areas showing elevated surface temperatures and industrial exposure (e.g. Chembur).
    2. **Waterlogging Vectors Risk (🔵 Cobalt Blue)**: Wards with high humidity and susceptibility to pooled monsoon precipitation, acting as potential mosquito breeding hubs (e.g. Andheri).
    3. **Stable Microclimate Risk (🟢 Emerald Green)**: Coastal or vegetation-dense zones exhibiting stable microclimates (e.g. Colaba).
    
    The interactive Folium map on the main dashboard overlays these calculated machine learning cluster IDs, color-coding circle markers to indicate active environmental vulnerabilities.
    """)

    # 4. Real-Time Population Data Drift & Anomaly Monitor
    st.markdown("---")
    st.markdown("### 📉 Real-Time Population Data Drift & Anomaly Monitor")
    st.markdown("""
    This utility performs real-time population drift monitoring. By comparing today's live telemetry input vectors 
    against baseline distributions from our 5-year historical records, the monitor calculates current $Z$-scores 
    to flags anomalies and potential data drift scenarios.
    """)
    
    drift_stats = get_baseline_stats()
    
    # Calculate Z-scores
    z_temp = (temp - drift_stats["Max_Temperature_C"]["mean"]) / (drift_stats["Max_Temperature_C"]["std"] or 1.0)
    z_rain = (rain_daily - drift_stats["Daily_Rain_mm"]["mean"]) / (drift_stats["Daily_Rain_mm"]["std"] or 1.0)
    z_pm25 = (pm25 - drift_stats["PM25_Index"]["mean"]) / (drift_stats["PM25_Index"]["std"] or 1.0)
    
    s_z_temp = float(z_temp.iloc[0]) if hasattr(z_temp, 'iloc') else float(z_temp)
    s_z_rain = float(z_rain.iloc[0]) if hasattr(z_rain, 'iloc') else float(z_rain)
    s_z_pm25 = float(z_pm25.iloc[0]) if hasattr(z_pm25, 'iloc') else float(z_pm25)
    
    drift_detected = abs(s_z_temp) > 2.0 or abs(s_z_rain) > 2.0 or abs(s_z_pm25) > 2.0
    
    # Display Notification Badge
    if drift_detected:
        st.markdown("""
        <div class="alert-banner-warning" style="margin-top: 10px; margin-bottom: 20px;">
            <span style="font-weight: 800; font-size: 1.1rem; color: #ef4444; display: flex; align-items: center; gap: 8px;">
                <span>⚠️ Statistical Data Drift Detected</span>
            </span>
            <p style="margin: 0.5rem 0 0 0; color: #fca5a5; font-size: 0.95rem; font-weight: 500;">
                Warning: The active climate telemetry vector deviates by more than 2.0 standard deviations (Z-score threshold) 
                from the baseline 5-year distribution. Today's inputs indicate localized micro-climate anomalies.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-banner-info" style="margin-top: 10px; margin-bottom: 20px;">
            <span style="font-weight: 800; font-size: 1.1rem; color: #10b981; display: flex; align-items: center; gap: 8px;">
                <span>🟢 MLOps telemetry normal</span>
            </span>
            <p style="margin: 0.5rem 0 0 0; color: #a7f3d0; font-size: 0.95rem; font-weight: 500;">
                Today's inputs are within normal statistical baseline bounds. No significant data drift detected.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    # Render interactive selectbox to let users toggle analyzed features
    selected_drift_metric = st.selectbox(
        "Select Telemetry Metric for Z-Score Anomaly Visualization",
        ["Max_Temperature_C", "Daily_Rain_mm", "PM25_Index"],
        format_func=lambda m: {
            "Max_Temperature_C": "🌡️ Temperature (°C)",
            "Daily_Rain_mm": "🌧️ Daily Rainfall (mm)",
            "PM25_Index": "💨 PM2.5 AQI (µg/m³)"
        }.get(m, m)
    )
    
    # Extract values for normal distribution plotting
    mu = drift_stats[selected_drift_metric]["mean"]
    sigma = drift_stats[selected_drift_metric]["std"] or 1.0
    today_val = temp if selected_drift_metric == "Max_Temperature_C" else (rain_daily if selected_drift_metric == "Daily_Rain_mm" else pm25)
    today_val = float(today_val.iloc[0]) if hasattr(today_val, 'iloc') else float(today_val)
    
    # Generate Normal Distribution bell-curve points
    x_range = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 200)
    y_bell = (1.0 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_range - mu) / sigma)**2)
    
    curve_df = pd.DataFrame({
        "Feature Value": x_range,
        "Probability Density": y_bell
    })
    
    # Create point coordinates for today's value
    y_today = (1.0 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((today_val - mu) / sigma)**2)
    point_df = pd.DataFrame({
        "Feature Value": [today_val],
        "Probability Density": [y_today],
        "Metric": [selected_drift_metric]
    })
    
    # Build Altair Chart
    import altair as alt
    base_chart = alt.Chart(curve_df).mark_area(
        color="#06b6d4",
        opacity=0.25
    ).encode(
        x=alt.X('Feature Value:Q', title=f"{selected_drift_metric} Baseline Value"),
        y=alt.Y('Probability Density:Q', title='Probability Density')
    )
    
    # Colored marker based on Z-score deviation
    z_score = (today_val - mu) / sigma
    marker_color = "#ef4444" if abs(z_score) > 2.0 else "#10b981"
    
    line_marker = alt.Chart(point_df).mark_rule(
        color=marker_color,
        strokeWidth=2,
        strokeDash=[4, 4]
    ).encode(
        x='Feature Value:Q'
    )
    
    point_marker = alt.Chart(point_df).mark_circle(
        size=160,
        color=marker_color,
        opacity=1.0
    ).encode(
        x='Feature Value:Q',
        y='Probability Density:Q',
        tooltip=[
            alt.Tooltip('Feature Value:Q', title="Today's Value", format='.2f'),
            alt.Tooltip('Probability Density:Q', title="Probability Density", format='.4f')
        ]
    )
    
    combined_bell = (base_chart + line_marker + point_marker).properties(
        height=320,
        title=f"Anomaly Monitor: Today's Z-Score = {z_score:.2f} (Baseline mean={mu:.1f}, std={sigma:.1f})"
    )
    st.altair_chart(combined_bell, use_container_width=True)

    render_rishi_footer("tab5")


# Helper to convert DB input values to standard Python floats to prevent SQLite errors
def to_float(val):
    import pandas as pd
    import numpy as np
    if val is None:
        return 0.0
    try:
        if isinstance(val, (pd.Series, pd.DataFrame)):
            return float(val.iloc[0])
        elif isinstance(val, np.ndarray):
            return float(val.ravel()[0])
        else:
            return float(val)
    except Exception:
        return 0.0

# Formatter to convert stored cases into string percentages
def format_to_pct(val):
    if pd.isna(val) or val is None:
        return "0%"
    try:
        val_f = float(val)
        if 0.0 < val_f < 1.0:
            val_f = val_f * 100.0
        val_f = min(100.0, max(0.0, val_f))
        return f"{int(round(val_f))}%"
    except Exception:
        return "0%"

# Cell styling rules for pandas styler
def style_risk_cells(val):
    try:
        if isinstance(val, str) and val.endswith("%"):
            num = float(val.replace("%", ""))
        else:
            num = float(val)
            
        if num < 40.0:
            return 'background-color: rgba(16, 185, 129, 0.15); color: #10b981;'
        elif 40.0 <= num <= 70.0:
            return 'background-color: rgba(245, 158, 11, 0.15); color: #f59e0b;'
        else:
            return 'background-color: rgba(239, 68, 68, 0.15); color: #ef4444;'
    except Exception:
        return ''

with tab3:
    st.header("Serverless Epidemiological Diagnostics Center")
    st.caption("Powered by Meta Llama-3.2-3b-Instruct via NVIDIA NIM High-Speed Compute Fabric")
    
    # Check if a location has been actively selected on the main dashboard map/selectbox
    selected_location = st.session_state.get("current_location_name")
    current_temp = st.session_state.get("temp", 27.0)
    current_humidity = st.session_state.get("humidity", 75.0)
    current_pm25 = st.session_state.get("pm25", 35.0)
    pred_cases = st.session_state.get("pred_cases", 0)
    current_risk_score = f"{min(100.0, max(0.0, (pred_cases / 150.0) * 100.0)):.1f}"

    if selected_location:
        st.markdown("---")
        
        # 1. Neat Default Automated Advisory Section
        st.subheader("Automated Clinical Risk Advisory")
        with st.spinner("Analyzing micro-climate vector footprints..."):
            # Fetch the baseline summary from the updated 3B model pipeline
            default_advisory = get_llama_health_advisory(
                selected_location, current_temp, current_humidity, current_pm25, current_risk_score
            )
            
            # Render the advice inside a visually distinct, clean card container
            st.info(default_advisory)
            
        st.markdown("---")
        
        # 2. Neat Interactive Search/Query Section
        st.subheader("Interactive Epidemiological Consultant")
        st.markdown("Ask the AI Assistant any specific health or precautionary question regarding this zone:")
        
        # Keep ONLY the modern consultant input bar inside Tab 3
        epi_query = st.text_input(
            label="e.g., What specific precautions should senior citizens...",
            label_visibility="collapsed",
            placeholder="e.g., What specific precautions should senior citizens or children take here right now?",
            key="epi_consultant_input"
        )
        
        if epi_query:
            with st.spinner("🧠 Querying Llama Core Reasoning Matrix..."):
                custom_response = get_llama_health_advisory(
                    selected_location, current_temp, current_humidity, current_pm25, current_risk_score, user_query=epi_query
                )
                
                # Render the custom question answer inside a clean highlighted block
                st.markdown("##### 💡 Consultation Response:")
                st.success(custom_response)
    else:
        st.warning("📍 Please select a target location ward on the main panel to activate live generative diagnostics.")


with tab4:
    st.markdown("## 📋 Scenario Simulation Log History")
    
    # Log Current Scenario Button placed directly above the tracking table
    if st.button("💾 Log Current Scenario", use_container_width=True):
        risk_str = "HIGH" if pred_cases >= 100 else "NORMAL"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO scenario_logs (
                timestamp, temp, humidity, rainfall, predicted_cases, risk_level, location,
                gastro_cases, heatstroke_cases, dengue_cases, malaria_cases, influenza_cases, bronchitis_cases, pm25
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            to_float(st.session_state.temp),
            to_float(st.session_state.humidity),
            to_float(rain_lag),
            to_float(pred_cases),
            risk_str,
            st.session_state.current_location_name,
            to_float(pred_gastro),
            to_float(pred_heatstroke),
            to_float(pred_dengue),
            to_float(pred_malaria),
            to_float(pred_flu),
            to_float(pred_bronchitis),
            to_float(st.session_state.pm25)
        ))
        conn.commit()
        conn.close()
        st.success("Scenario logged successfully to SQLite database!")
        
    logged_scenarios = load_scenario_logs()
    if not logged_scenarios.empty:
        st.markdown("Below are the past simulation scenarios logged into our tracking database:")
        
        # Rename columns to percentage risk format
        rename_dict = {
            "Gastroenteritis Cases": "Gastroenteritis Risk",
            "Heatstroke Cases": "Heatstroke Risk",
            "Dengue Cases": "Dengue Risk",
            "Malaria Cases": "Malaria Risk",
            "Influenza Cases": "Influenza Risk",
            "Bronchitis Cases": "Bronchitis Risk"
        }
        df_renamed = logged_scenarios.rename(columns=rename_dict)
        
        # Apply the format to string percentage for each of the six columns
        risk_cols = list(rename_dict.values())
        for col in risk_cols:
            if col in df_renamed.columns:
                df_renamed[col] = df_renamed[col].apply(format_to_pct)
                
        # Apply style sheet color mapping conditionally
        styler = df_renamed.style
        if hasattr(styler, "map"):
            styled_df = styler.map(style_risk_cells, subset=risk_cols)
        else:
            styled_df = styler.applymap(style_risk_cells, subset=risk_cols)
            
        st.dataframe(styled_df, use_container_width=True)
        
        # Convert to CSV using cached helper function
        csv_bytes = convert_df_to_csv(logged_scenarios)
        
        # Download button
        st.download_button(
            label="📥 Export Logs as CSV",
            data=csv_bytes,
            file_name="viralwell_simulation_report.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("No scenarios logged yet. Adjust the sliders in the '🔮 Outbreak Predictor' tab and click '💾 Log Current Scenario' here to save simulated data.")

    render_rishi_footer("tab4")








# 5. Global Legal Disclaimer (Absolute End of File)
st.markdown("""
<div class="sticky-footer">
    ⚠️ <b>LEGAL MEDICAL DISCLAIMER:</b> ViralWell is a predictive data science analytics framework intended purely for educational and lifestyle planning support. It does not contain clinical diagnostic algorithms and should never substitute professional medical examination, prescription, or intervention.
</div>
""", unsafe_allow_html=True)


