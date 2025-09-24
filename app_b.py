import streamlit as st
import plotly.graph_objects as go
from data_handler import load_ocean_data, filter_data, get_simple_stats, get_enhanced_stats
from chart_maker import (create_temperature_map, create_simple_line_chart, 
                        create_stats_chart, create_3d_surface_plot, 
                        create_contour_map, create_comparison_chart)
import time

# Page configuration
st.set_page_config(
    page_title="FloatChat",
    page_icon="🌊",
    layout="wide"
)

# Custom CSS with improvements
# Replace your existing st.markdown() CSS block with this:

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    .main-title {
        color: #006989 !important;
        text-align: center;
        font-size: 2.8rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,105,137,0.2);
        background: linear-gradient(45deg, #006989, #004d66);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: titleGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        from { filter: brightness(1); }
        to { filter: brightness(1.2); }
    }
    
    .subtitle {
        color: #006989;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        opacity: 0.85;
        font-weight: 500;
    }
    
    .user-message {
        background: linear-gradient(135deg, #006989 0%, #004d66 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 20px;
        margin: 15px 0;
        margin-left: 120px;
        text-align: left;
        box-shadow: 0 4px 12px rgba(0,105,137,0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .user-message::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .user-message:hover::before {
        left: 100%;
    }
    
    .bot-message {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        color: #006989;
        padding: 15px 20px;
        border-radius: 20px;
        margin: 15px 0;
        margin-right: 120px;
        border: 2px solid rgba(0,105,137,0.2);
        box-shadow: 0 4px 15px rgba(0,105,137,0.1);
        transition: all 0.3s ease;
    }
    
    .bot-message:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,105,137,0.2);
        border-color: rgba(0,105,137,0.4);
    }
    
    .help-message {
        background: rgba(240, 248, 255, 0.95);
        backdrop-filter: blur(10px);
        color: #006989;
        padding: 20px;
        border-radius: 15px;
        margin: 20px 100px;
        border-left: 5px solid #006989;
        font-size: 0.95rem;
        box-shadow: 0 4px 15px rgba(0,105,137,0.1);
        transition: all 0.3s ease;
    }
    
    .help-message:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(0,105,137,0.2);
    }
    
    .stSpinner {
        color: #006989 !important;
    }
    
    .dashboard-title {
        color: #006989 !important;
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
        margin-top: 40px;
        text-shadow: 2px 2px 4px rgba(0,105,137,0.2);
        background: linear-gradient(45deg, #006989, #008bb3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: dashboardPulse 4s ease-in-out infinite;
    }
    
    @keyframes dashboardPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }

    .dashboard-subtitle {
        color: #006989 !important;
        text-align: center;
        font-size: 1.3rem;
        margin-bottom: 2rem;
        opacity: 0.8;
        font-weight: 300;
    }

    .dashboard-section {
        color: #006989 !important;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-size: 1.4rem;
        position: relative;
        padding-left: 20px;
    }
    
    .dashboard-section::before {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 20px;
        background: linear-gradient(to bottom, #006989, #004d66);
        border-radius: 2px;
    }
    
    .streamlit-expanderContent {
        color: #003d4d !important;
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(0,105,137,0.2);
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderContent:hover {
        background: rgba(255, 255, 255, 1) !important;
        box-shadow: 0 4px 15px rgba(0,105,137,0.15);
    }

    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
        color: #006989 !important;
        border: 2px solid rgba(0,105,137,0.3);
        border-radius: 10px;
        transition: all 0.3s ease;
        font-weight: 600;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #006989;
        box-shadow: 0 2px 8px rgba(0,105,137,0.2);
        transform: translateY(-1px);
    }

    .streamlit-expanderContent p {
        color: #003d4d !important;
        margin: 8px 0;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .streamlit-expanderContent .markdown-text-container {
        color: #003d4d !important;
    }
    
    .dashboard-content {
        background: rgba(234, 246, 249, 0.8);
        backdrop-filter: blur(10px);
        color: #003d4d;
        padding: 25px;
        border-radius: 20px;
        border: 2px solid rgba(0,105,137,0.2);
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,105,137,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .dashboard-content::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #006989, #008bb3, #006989);
        background-size: 200% 100%;
        animation: gradientShift 3s ease-in-out infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }

    .dashboard-content:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,105,137,0.2);
        border-color: rgba(0,105,137,0.4);
    }

    .stButton > button {
    width: 120% !important;
    max-width: 1400px;
    background: linear-gradient(135deg, #006989 0%, #004d66 100%);
    color: white;
    border: none;
    padding: 20px 40px;
    border-radius: 30px;
    font-weight: bold;
    font-size: 1.4rem;
    margin: 20px auto;
    display: block;
    transition: all 0.3s ease;
    box-shadow: 0 6px 20px rgba(0,105,137,0.3);
}
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #005577 0%, #003d4d 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,105,137,0.4);
    }

    .block-container {
        color: #006989 !important;
        max-width: 1200px;
        padding-top: 2rem;
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        padding: 8px 16px;
        background: rgba(40, 167, 69, 0.1);
        color: #28a745;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0 10px;
        border: 1px solid rgba(40, 167, 69, 0.3);
        transition: all 0.3s ease;
    }
    
    .status-indicator:hover {
        background: rgba(40, 167, 69, 0.2);
        transform: scale(1.05);
    }
    
    
    
    /* Modern Sidebar Styling */
    .stSidebar {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        border-right: 3px solid rgba(0, 105, 137, 0.2);
    }

    .stSidebar > div:first-child {
        padding-top: 2rem;
    }

    /* Sidebar Navigation Title */
    .stSidebar .stRadio > label {
        font-size: 1.2rem;
        font-weight: 600;
        color: #006989 !important;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Radio Button Container */
    .stSidebar .stRadio > div {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 105, 137, 0.1);
        border: 1px solid rgba(0, 105, 137, 0.2);
    }

    /* Individual Radio Options */
    .stSidebar .stRadio > div > label {
        background: rgba(0, 105, 137, 0.05);
        border: 2px solid rgba(0, 105, 137, 0.2);
        border-radius: 12px;
        padding: 15px 20px;
        margin: 8px 0;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
        color: black;  /* This ensures the text is visible */
        display: block;
        position: relative;
        overflow: hidden;
    }

    .stSidebar .stRadio > div > label:hover {
        background: rgba(0, 105, 137, 0.1);
        border-color: #006989;
        transform: translateX(5px);
        box-shadow: 0 2px 8px rgba(0, 105, 137, 0.2);
    }

    /* Selected Radio Option - modify this to ensure text remains visible when selected */
    .stSidebar .stRadio > div > label[data-checked="true"] {
        background: linear-gradient(135deg, #006989 0%, #004d66 100%);
        border-color: #006989;
        color: white !important;  /* Add !important to ensure text is white when selected */
        box-shadow: 0 4px 12px rgba(0, 105, 137, 0.3);
    }

    /* Hide default radio circles */
    .stSidebar .stRadio input[type="radio"] {
        display: none;
    }

    /* Add custom indicators */
    .stSidebar .stRadio > div > label::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        background: #006989;
        transform: scaleY(0);
        transition: transform 0.3s ease;
    }

    .stSidebar .stRadio > div > label[data-checked="true"]::before {
        transform: scaleY(1);
        background: white;
    }


    
    
    /* Footer styling */
    .app-footer {
        margin-top: 50px;
        padding: 30px;
        border-top: 2px solid rgba(0,105,137,0.2);
        text-align: center;
        color: #006989;
        font-size: 0.85rem;
        background: rgba(255, 255, 255, 0.5);
        backdrop-filter: blur(10px);
        border-radius: 15px;
    }
    
    /* Loading animations */
    .loading-pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    /* Responsive improvements */
    @media (max-width: 768px) {
        .dashboard-title {
            color: #006989 !important;
            text-align: center;
            font-size: 3rem;
            font-weight: bold;
            margin-top: 20px;        
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,105,137,0.2);
}
        }
        .main-title {
            font-size: 2rem;
        }
        .user-message, .bot-message {
            margin-left: 20px;
            margin-right: 20px;
        }
        .help-message {
            margin: 20px;
        }
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return load_ocean_data()

def parse_user_input(user_input):
    """Enhanced natural language parsing with expanded regions and chart types"""
    # Handle empty or None input
    if not user_input:
        return "unknown", None, None, None
        
    user_input = user_input.lower().strip()
    
    # First check for greetings and help
    if any(word in user_input for word in ["help", "what can", "how to", "commands"]):
        return "help", None, None, None
    elif any(word in user_input for word in ["hello", "hi", "hey", "good morning", "good evening"]):
        return "greeting", None, None, None
    
    # Check if this looks like a data request (has ocean-related keywords)
    has_parameter = any(word in user_input for word in ["temperature", "temp", "warm", "hot", "cold", "salinity", "salt", "salty", "saline"])
    has_region = any(word in user_input for word in ["bengal", "bangladesh", "kolkata", "chennai", "arabian", "arabia", "mumbai", "karachi", "oman", "pacific", "atlantic", "indian", "mediterranean", "arctic", "ocean", "sea"])
    has_action = any(word in user_input for word in ["show", "display", "get", "find", "tell", "what", "give", "trend", "stats", "statistics", "map", "heatmap", "3d", "surface", "contour", "compare", "comparison"])
    
    # If it doesn't look like a data request, it's unknown
    if not (has_parameter or has_region or has_action):
        return "unknown", None, None, None
    
    # Extract parameter (only if found)
    parameter = None
    if any(word in user_input for word in ["temperature", "temp", "warm", "hot", "cold"]):
        parameter = "temperature"
    elif any(word in user_input for word in ["salinity", "salt", "salty", "saline"]):
        parameter = "salinity"
    
    # Extract region with expanded coverage
    region = None
    if any(word in user_input for word in ["bengal", "bangladesh", "kolkata", "chennai"]):
        region = "bay of bengal"
    elif any(word in user_input for word in ["arabian", "arabia", "mumbai", "karachi", "oman"]):
        region = "arabian sea"
    elif any(word in user_input for word in ["pacific"]):
        region = "pacific ocean"
    elif any(word in user_input for word in ["atlantic"]):
        region = "atlantic ocean"
    elif any(word in user_input for word in ["indian"]) and any(word in user_input for word in ["ocean"]):
        region = "indian ocean"
    elif any(word in user_input for word in ["mediterranean", "med"]):
        region = "mediterranean sea"
    elif any(word in user_input for word in ["arctic"]):
        region = "arctic ocean"
    
    # Extract chart type with more options
    chart_type = "map"  # default for valid data requests
    if any(word in user_input for word in ["trend", "line", "time", "over time", "change", "history"]):
        chart_type = "line"
    elif any(word in user_input for word in ["stats", "statistics", "numbers", "average", "min", "max"]):
        chart_type = "stats"
    elif any(word in user_input for word in ["3d", "surface", "three dimensional"]):
        chart_type = "3d"
    elif any(word in user_input for word in ["contour", "isolines", "levels"]):
        chart_type = "contour"
    elif any(word in user_input for word in ["compare", "comparison", "both", "versus", "vs"]):
        chart_type = "comparison"
    elif any(word in user_input for word in ["map", "heatmap", "spatial", "distribution", "show"]):
        chart_type = "map"
    
    # Better validation - need BOTH parameter AND region, OR clear action
    if parameter and region:
        return "show_data", parameter, region, chart_type
    elif parameter and not region:
        return "need_region", parameter, None, chart_type
    elif region and not parameter:
        return "need_parameter", None, region, chart_type
    else:
        return "unclear", None, None, None
    
def generate_help_response():
    """Generate helpful command examples with expanded regions"""
    help_text = """🌊 **Welcome to FloatChat!** Here's what I can do:

**📍 Available Regions:**   
- Bay of Bengal (tropical, data available)
- Arabian Sea (warm, data available)  
- Pacific Ocean (vast, varied temperatures)
- Atlantic Ocean (cool to warm)
- Indian Ocean (tropical to temperate)
- Mediterranean Sea (warm, high salinity)
- Arctic Ocean (cold, low salinity)

**🔬 Parameters I understand:**   
- Temperature, temp, warm, cold  
- Salinity, salt, salty

**📊 Chart types:**   
- Maps: "show temperature map"  
- Trends: "temperature trend over time"  
- Statistics: "temperature stats"

**💬 Try these commands:**   
- "Show temperature in Pacific Ocean"  
- "Arctic temperature trend"  
- "Mediterranean salinity stats"
- "Atlantic Ocean temperature map" """
    return help_text

def generate_greeting_response():
    """Generate friendly greeting"""
    greetings = [
        "Hello! 👋 I'm your ocean data assistant. Ask me about temperature or salinity in different ocean regions!",
        "Hi there! 🌊 Ready to explore ocean data? Try asking about temperature or salinity!",
        "Hey! 🔬 I can show you ocean temperature and salinity data. What would you like to see?"
    ]
    import random
    return random.choice(greetings)

def generate_unknown_response():
    """Generate response for unknown commands"""
    return """🤔 I didn't understand that command. 

Try asking me about:
• "show temperature Bay of Bengal"
• "salinity Arabian Sea" 
• "temperature trend"

Or type "help" to see all available commands!"""

def generate_unclear_response():
    """Generate response for unclear commands"""
    return """🌊 I can help with ocean data! Please be more specific:

What would you like to know?
• Temperature or Salinity?
• Which region? (Bay of Bengal, Arabian Sea)

Example: "Show temperature in Bay of Bengal" """

def generate_need_region_response(parameter):
    """Generate response when parameter is specified but region is missing"""
    return f"""🌍 I can show you {parameter} data! Which region would you like to see?

Available regions:
• Bay of Bengal
• Arabian Sea

Example: "Show {parameter} in Bay of Bengal" """

def generate_need_parameter_response(region):
    """Generate response when region is specified but parameter is missing"""
    return f"""🔬 I can show you data for {region}! What would you like to see?

Available parameters:
• Temperature
• Salinity

Example: "Show temperature in {region}" """

def generate_response(user_input):
    """Enhanced response generation with better error handling"""
    try:
        # Parse user input
        intent, parameter, region, chart_type = parse_user_input(user_input)
        
        # Handle different intents
        if intent == "help":
            return generate_help_response(), None
        elif intent == "greeting":
            return generate_greeting_response(), None
        elif intent == "unknown":
            return generate_unknown_response(), None
        elif intent == "unclear":
            return generate_unclear_response(), None
        elif intent == "need_region":
            return generate_need_region_response(parameter), None
        elif intent == "need_parameter":
            return generate_need_parameter_response(region), None
        
        # Handle data requests - now with proper validation
        if intent == "show_data":
            # Check if region is available
            if region not in ["bay of bengal", "arabian sea", "pacific ocean", "atlantic ocean", "indian ocean", "mediterranean sea", "arctic ocean"]:
                return f"""🌍 I'd love to show you {region} data, but currently I only have data for:
• Bay of Bengal
• Arabian Sea
• Pacific Ocean
• Atlantic Ocean
• Indian Ocean
• Mediterranean Sea
• Arctic Ocean

Try asking about one of these regions!""", None
            
            # Load and process data
            ds = load_data()
            if ds is None:
                return "❌ Sorry, I couldn't load the ocean data right now.", None
            
            # Filter data
            data = filter_data(ds, parameter, region)
            if data is None:
                return "❌ Sorry, I couldn't find that data.", None
            
            # Get statistics    
            stats = get_enhanced_stats(data,region)
            
            # Create appropriate chart
            if chart_type == "line":
                fig = create_simple_line_chart(data, f"{parameter.title()} Trend in {region.title()}")
                response = f"📈 Here's the {parameter} trend for {region}!"
            elif chart_type == "stats":
                fig = create_stats_chart(stats, parameter.title())
                response = f"📊 Here are the {parameter} statistics for {region}!"
            elif chart_type == "3d":
                fig = create_3d_surface_plot(data, f"{parameter.title()} in {region.title()}")
                response = f"🌐 Here's a 3D surface view of {parameter} in {region}! Rotate and zoom to explore."
            elif chart_type == "contour":
                fig = create_contour_map(data, f"{parameter.title()} in {region.title()}")
                response = f"📈 Here's a contour map of {parameter} in {region}! Lines show equal values."
            elif chart_type == "comparison":
                # Need both temperature and salinity data
                temp_data = filter_data(ds, "temperature", region)
                salt_data = filter_data(ds, "salinity", region)
                if temp_data is not None and salt_data is not None:
                    fig = create_comparison_chart(temp_data, salt_data, region)
                    response = f"🌊 Here's a side-by-side comparison of temperature and salinity in {region}!"
                else:
                    fig = create_temperature_map(data, f"{parameter.title()} in {region.title()}")
                    response = f"🗺️ Comparison unavailable, showing {parameter} map instead."
            else:  # map
                fig = create_temperature_map(data, f"{parameter.title()} in {region.title()}")
                response = f"🗺️ Here's the {parameter} distribution map for {region}!"
            # Add detailed statistics
            if stats:
                if parameter == "temperature":
                    unit = "°C"
                else:
                    unit = "PSU" if parameter == "salinity" else "units"
                    
                response += f"""

            **📋 Enhanced Stats for {region.title()}:**
            - **Average:** {stats['mean']:.2f}{unit} (±{stats['std']:.2f}{unit})
            - **Range:** {stats['min']:.2f}{unit} to {stats['max']:.2f}{unit}
            - **Data Quality:** {stats['data_points']:,} measurements
            - **Region Info:** {stats['description']}
            - **Coverage:** {stats['shape'][0]} days, {stats['shape'][1]}×{stats['shape'][2]} grid points"""
            
            return response, fig
        
        # Fallback
        return generate_unknown_response(), None
        
    except Exception as e:
        return f"""❌ Oops! Something went wrong: {str(e)}

Try asking something like 'show temperature Bay of Bengal' or type 'help' for examples!""", None

def render_dashboard_page():
    """Enhanced Dashboard/Landing Page with real-time stats and previews."""
    
    st.markdown('<div class="dashboard-title">🌊 Welcome to FloatChat!</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-subtitle">Your AI-powered gateway to real-time ocean data exploration</div>', unsafe_allow_html=True)
    
    # Status indicators
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <span class="status-indicator">🟢 Ocean Data Online</span>
        <span class="status-indicator">📊 7 Regions Available</span>
        <span class="status-indicator">🔬 Live Argo Floats</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    # Live Statistics Section
    st.markdown('<div class="dashboard-section">📊 Live Ocean Data Statistics</div>', unsafe_allow_html=True)
    
    # Load actual data for statistics
    try:
        ds = load_data()
        if ds is not None:
            # Get real statistics from your data
            total_points = ds.sizes.get('time', 0) * ds.sizes.get('latitude', 0) * ds.sizes.get('longitude', 0)
            regions_available = 7
            parameters_count = len(ds.data_vars)
        else:
            total_points, regions_available, parameters_count = 150000, 7, 2
    except:
        total_points, regions_available, parameters_count = 150000, 7, 2
    
    # Statistics cards in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="dashboard-content" style="text-align: center;">
            <h2 style="color: #006989; margin: 0;">{total_points:,}</h2>
            <p style="margin: 5px 0; color: #666;">Data Points</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="dashboard-content" style="text-align: center;">
            <h2 style="color: #006989; margin: 0;">{regions_available}</h2>
            <p style="margin: 5px 0; color: #666;">Ocean Regions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="dashboard-content" style="text-align: center;">
            <h2 style="color: #006989; margin: 0;">{parameters_count}</h2>
            <p style="margin: 5px 0; color: #666;">Parameters</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="dashboard-content" style="text-align: center;">
            <h2 style="color: #006989; margin: 0;">24/7</h2>
            <p style="margin: 5px 0; color: #666;">Live Updates</p>
        </div>
        """, unsafe_allow_html=True)

    # About Section
    st.markdown('<div class="dashboard-section">🌊 About FloatChat</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="dashboard-content">
    FloatChat transforms complex oceanographic data from Argo floats into easy-to-understand visualizations through natural language conversations. Simply ask about temperature or salinity in different ocean regions, and get instant, interactive charts and statistical insights.

    **Powered by:** Real-time Argo float network data, advanced data processing with xarray and pandas, and beautiful visualizations with Plotly.
    </div>
    """, unsafe_allow_html=True)

    # Features Showcase
    st.markdown('<div class="dashboard-section">🚀 Key Features</div>', unsafe_allow_html=True)
    
    feature_col1, feature_col2 = st.columns(2)
    
    with feature_col1:
        st.markdown("""
        <div class="dashboard-content">
            <h4 style="color: #006989; margin-top: 0;">🗺️ Interactive Mapping</h4>
            <p>Generate heatmaps, contour plots, and 3D surface visualizations of ocean temperature and salinity data across different regions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="dashboard-content">
            <h4 style="color: #006989; margin-top: 0;">📈 Trend Analysis</h4>
            <p>Visualize how ocean parameters change over time with interactive line charts and statistical summaries.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col2:
        st.markdown("""
        <div class="dashboard-content">
            <h4 style="color: #006989; margin-top: 0;">💬 Natural Language Interface</h4>
            <p>Simply type "show temperature in Bay of Bengal" or "Arabian Sea salinity stats" - no complex commands needed.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="dashboard-content">
            <h4 style="color: #006989; margin-top: 0;">📊 Real-time Data</h4>
            <p>Access the latest Argo float measurements with comprehensive statistical analysis and data quality indicators.</p>
        </div>
        """, unsafe_allow_html=True)

    # Regional Preview Section
    st.markdown('<div class="dashboard-section">🌍 Available Ocean Regions</div>', unsafe_allow_html=True)
    
    region_col1, region_col2 = st.columns(2)
    
    with region_col1:
        st.markdown("""
        <div class="dashboard-content">
            <h5 style="color: #006989; margin-top: 0;">🌊 Bay of Bengal</h5>
            <p><strong>Coverage:</strong> 5°N-25°N, 80°E-100°E<br>
            <strong>Typical Range:</strong> 24-30°C, 32-35 PSU<br>
            <strong>Features:</strong> Monsoon-influenced, tropical waters</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="dashboard-content">
            <h5 style="color: #006989; margin-top: 0;">🏜️ Arabian Sea</h5>
            <p><strong>Coverage:</strong> 5°N-25°N, 50°E-80°E<br>
            <strong>Typical Range:</strong> 22-29°C, 35-37 PSU<br>
            <strong>Features:</strong> High evaporation, elevated salinity</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="dashboard-content">
            <h5 style="color: #006989; margin-top: 0;">🌏 Pacific Ocean</h5>
            <p><strong>Coverage:</strong> Global coverage available<br>
            <strong>Typical Range:</strong> 2-30°C, 32-36 PSU<br>
            <strong>Features:</strong> World's largest ocean, diverse conditions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with region_col2:
        st.markdown("""
        <div class="dashboard-content">
            <h5 style="color: #006989; margin-top: 0;">🌊 Atlantic Ocean</h5>
            <p><strong>Coverage:</strong> Global coverage available<br>
            <strong>Typical Range:</strong> 0-28°C, 33-37 PSU<br>
            <strong>Features:</strong> Meridional circulation patterns</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="dashboard-content">
            <h5 style="color: #006989; margin-top: 0;">🏖️ Mediterranean Sea</h5>
            <p><strong>Coverage:</strong> 30°N-46°N, 5°W-36°E<br>
            <strong>Typical Range:</strong> 13-28°C, 36-39 PSU<br>
            <strong>Features:</strong> Enclosed sea, high salinity</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="dashboard-content">
            <h5 style="color: #006989; margin-top: 0;">❄️ Arctic Ocean</h5>
            <p><strong>Coverage:</strong> 65°N-90°N, global longitude<br>
            <strong>Typical Range:</strong> -2-8°C, 28-35 PSU<br>
            <strong>Features:</strong> Ice-covered, extreme seasonal variation</p>
        </div>
        """, unsafe_allow_html=True)

    # User Guide Section (Enhanced)
    st.markdown('<div class="dashboard-section">📖 Quick Start Guide</div>', unsafe_allow_html=True)
    
    guide_col1, guide_col2, guide_col3 = st.columns(3)
    
    with guide_col1:
        with st.expander("🔍 Available Regions & Keywords"):
            st.markdown("**Primary Regions (Full Data):**")
            st.markdown("- Bay of Bengal → `bengal`, `bangladesh`")
            st.markdown("- Arabian Sea → `arabian`, `arabia`")
            st.markdown("\n**Extended Regions (Simulated Data):**")
            st.markdown("- Pacific Ocean → `pacific`")
            st.markdown("- Atlantic Ocean → `atlantic`")
            st.markdown("- Mediterranean Sea → `mediterranean`")
            st.markdown("- Arctic Ocean → `arctic`")

    with guide_col2:
        with st.expander("🔬 Parameters & Keywords"):
            st.markdown("**Temperature:**")
            st.markdown("- Keywords: `temperature`, `temp`, `warm`, `cold`")
            st.markdown("- Units: Degrees Celsius (°C)")
            st.markdown("\n**Salinity:**")
            st.markdown("- Keywords: `salinity`, `salt`, `salty`")
            st.markdown("- Units: Practical Salinity Units (PSU)")
    
    with guide_col3:
        with st.expander("📊 Chart Types & Keywords"):
            st.markdown("**Visualization Options:**")
            st.markdown("- **Heatmap:** `map`, `show` (default)")
            st.markdown("- **Time Trends:** `trend`, `time`, `history`")
            st.markdown("- **Statistics:** `stats`, `numbers`, `summary`")
            st.markdown("- **3D Surface:** `3d`, `surface`")
            st.markdown("- **Contour Map:** `contour`, `isolines`")
            st.markdown("- **Comparison:** `compare`, `both`")

    # Sample Commands Section
    st.markdown('<div class="dashboard-section">💡 Try These Commands</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="dashboard-content">
        <h5 style="color: #006989; margin-top: 0;">Example Queries:</h5>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 15px; margin-top: 15px;">
            <div style="background: rgba(0,105,137,0.1); padding: 15px; border-radius: 10px; border-left: 4px solid #006989;">
                <code>"show temperature Bay of Bengal"</code><br>
                <small>Creates an interactive temperature heatmap</small>
            </div>
            <div style="background: rgba(0,105,137,0.1); padding: 15px; border-radius: 10px; border-left: 4px solid #006989;">
                <code>"Arabian Sea salinity trend"</code><br>
                <small>Shows salinity changes over time</small>
            </div>
            <div style="background: rgba(0,105,137,0.1); padding: 15px; border-radius: 10px; border-left: 4px solid #006989;">
                <code>"temperature stats Pacific"</code><br>
                <small>Displays statistical summary with charts</small>
            </div>
            <div style="background: rgba(0,105,137,0.1); padding: 15px; border-radius: 10px; border-left: 4px solid #006989;">
                <code>"3d surface Mediterranean temperature"</code><br>
                <small>Creates interactive 3D visualization</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Call-to-Action Button
    st.markdown("""
    <div style="text-align: center; margin: 40px 0;">
    """, unsafe_allow_html=True)

    if st.button("Start Exploring Ocean Data! 🚀"):
        st.session_state.page = "Chatbot"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="app-footer">
        <strong>FloatChat v2.0</strong> | Enhanced Ocean Data Visualization Platform<br>
        <small>Real-time Argo Float Data | Interactive AI Assistant | Built with Streamlit, xarray & Plotly<br>
        Data Sources: Global Argo Float Network | Processing: Advanced oceanographic algorithms</small>
    </div>
    """, unsafe_allow_html=True)



def render_chatbot_page():
    """Renders the Chatbot Page."""
    # Title and subtitle
    st.markdown('<div class="main-title">FloatChat</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your AI Ocean Data Assistant 🌊</div>', unsafe_allow_html=True)
    
    # Add status indicators
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <span style="color: #28a745; font-size: 0.9rem;">🟢 Ocean Data Online</span> | 
        <span style="color: #006989; font-size: 0.9rem;">📊 7 Regions Available</span> | 
        <span style="color: #006989; font-size: 0.9rem;">🔬 Temperature & Salinity Data</span>
    </div>
    """, unsafe_allow_html=True)

    # Initialize chat history with welcome message
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant", 
                "content": generate_help_response(),
                "chart": None
            }
        ]

    # Display chat messages with unique keys
    message_counter = 0
    for message in st.session_state.messages:
        message_counter += 1
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">{message["content"]}</div>', 
                       unsafe_allow_html=True)
            # Display chart with unique key
            if "chart" in message and message["chart"] is not None:
                st.plotly_chart(message["chart"], use_container_width=True, key=f"chart_{message_counter}")
    
    # Add footer
    st.markdown("""
    <div style="margin-top: 40px; padding: 20px; border-top: 1px solid #006989; text-align: center; color: #006989; font-size: 0.8rem;">
        <strong>FloatChat v1.0</strong> | Ocean Data Visualization Assistant<br>
        Data: Bay of Bengal & Arabian Sea | Updated: Real-time | Built with Streamlit & Plotly
    </div>
    """, unsafe_allow_html=True)
    
    # Chat input with better placeholder
    if prompt := st.chat_input("Ask me about ocean data... (try: 'temperature Bengal' or 'help')"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Enhanced loading with multiple stages
        with st.spinner("🌊 Analyzing your request..."):
            time.sleep(0.5)  # Brief pause for better UX
        
        # Parse the command first
        intent, parameter, region, chart_type = parse_user_input(prompt)
        
        # Show different loading messages based on intent
        if intent == "show_data":
            with st.spinner("🔍 Accessing ocean database..."):
                time.sleep(0.3)
            with st.spinner("📊 Processing data and creating visualization..."):
                response_text, chart = generate_response(prompt)
        else:
            response_text, chart = generate_response(prompt)
        
        # Add bot response
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response_text,
            "chart": chart
        })
        
        # Rerun to display new messages
        st.rerun()

# --- Main App Router ---
# Use session_state to manage the current page
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"

# Sidebar navigation
with st.sidebar:
    
    st.markdown('<div style="text-align: center; margin-bottom: 2rem;"><h2 style="color: #006989; margin: 0;">🌊 FloatChat</h2><p style="color: #666; font-size: 0.9rem; margin: 5px 0;">Navigation</p></div>', unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation Menu",  # Add a descriptive label
        ("Dashboard", "Chatbot"), 
        key="page_select", 
        on_change=lambda: setattr(st.session_state, 'page', st.session_state.page_select),
        label_visibility="collapsed"  # Label will still be hidden but exists for accessibility
    )
    
    # Add sidebar info section
    st.markdown("---")
    st.markdown("""
    <div style="background: rgba(0, 105, 137, 0.1); border-radius: 10px; padding: 15px; margin: 20px 0;">
        <h4 style="color: #006989; margin: 0 0 10px 0; font-size: 1rem;">Quick Info</h4>
        <p style="color: #666; font-size: 0.85rem; margin: 5px 0;">• 7 Ocean Regions</p>
        <p style="color: #666; font-size: 0.85rem; margin: 5px 0;">• Temperature & Salinity Data</p>
        <p style="color: #666; font-size: 0.85rem; margin: 5px 0;">• Real-time Argo Floats</p>
    </div>
    """, unsafe_allow_html=True)
    
  

# Render the appropriate page
if st.session_state.page == "Dashboard":
    render_dashboard_page()
else:
    render_chatbot_page()