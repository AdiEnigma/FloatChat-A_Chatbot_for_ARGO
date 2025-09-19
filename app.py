import streamlit as st
import plotly.graph_objects as go
from data_handler import load_ocean_data, filter_data, get_simple_stats
from chart_maker import create_temperature_map, create_simple_line_chart, create_stats_chart
import re
import time

# Page configuration
st.set_page_config(
    page_title="FloatChat",
    page_icon="🌊",
    layout="wide"
)

# Custom CSS with improvements
st.markdown("""
<style>
    .stApp {
        background-color: #eaebed;
    }
    
    .main-title {
        color: #006989 !important;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        color: #006989;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 2rem;
        opacity: 0.8;
    }
    
    .user-message {
        background-color: #006989;
        color: white;
        padding: 12px 18px;
        border-radius: 18px;
        margin: 15px 0;
        margin-left: 120px;
        text-align: left;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .bot-message {
        background-color: white;
        color: #006989;
        padding: 12px 18px;
        border-radius: 18px;
        margin: 15px 0;
        margin-right: 120px;
        border: 1px solid #006989;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .help-message {
        background-color: #f0f8ff;
        color: #006989;
        padding: 15px;
        border-radius: 10px;
        margin: 20px 100px;
        border-left: 4px solid #006989;
        font-size: 0.9rem;
    }
    
    .stSpinner {
        color: #006989;
    }
</style>
""", unsafe_allow_html=True)

def render_chatbot_page():
# Title and subtitle
    st.markdown('<div class="main-title">FloatChat</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your AI Ocean Data Assistant 🌊</div>', unsafe_allow_html=True)
# Add after the subtitle
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <span style="color: #28a745; font-size: 0.9rem;">🟢 Ocean Data Online</span> | 
        <span style="color: #006989; font-size: 0.9rem;">📊 2 Regions Available</span> | 
        <span style="color: #006989; font-size: 0.9rem;">🔬 Temperature & Salinity Data</span>
    </div>
""", unsafe_allow_html=True)
# Load ocean data once at startup
@st.cache_data
def load_data():
    return load_ocean_data()

# FIXED: Enhanced command parser with proper unknown command detection
def parse_user_input(user_input):
    """Enhanced natural language parsing with unknown command detection"""
    user_input = user_input.lower().strip()
    
    # First check for greetings and help
    if any(word in user_input for word in ["help", "what can", "how to", "commands"]):
        return "help", None, None, None
    elif any(word in user_input for word in ["hello", "hi", "hey", "good morning", "good evening"]):
        return "greeting", None, None, None
    
    # Check if this looks like a data request (has ocean-related keywords)
    has_parameter = any(word in user_input for word in ["temperature", "temp", "warm", "hot", "cold", "salinity", "salt", "salty", "saline"])
    has_region = any(word in user_input for word in ["bengal", "bangladesh", "kolkata", "chennai", "arabian", "arabia", "mumbai", "karachi", "oman", "pacific", "atlantic", "indian", "ocean", "sea"])
    has_action = any(word in user_input for word in ["show", "display", "get", "find", "tell", "what", "give", "trend", "stats", "statistics", "map", "heatmap"])
    
    # If it doesn't look like a data request, it's unknown
    if not (has_parameter or has_region or has_action):
        return "unknown", None, None, None
    
    # Extract parameter (only if found)
    parameter = None
    if any(word in user_input for word in ["temperature", "temp", "warm", "hot", "cold"]):
        parameter = "temperature"
    elif any(word in user_input for word in ["salinity", "salt", "salty", "saline"]):
        parameter = "salinity"
    
    # Extract region (only if found)  
    region = None
    if any(word in user_input for word in ["bengal", "bangladesh", "kolkata", "chennai"]):
        region = "bay of bengal"
    elif any(word in user_input for word in ["arabian", "arabia", "mumbai", "karachi", "oman"]):
        region = "arabian sea"
    elif any(word in user_input for word in ["pacific"]):
        region = "pacific ocean"
    elif any(word in user_input for word in ["atlantic"]):
        region = "atlantic ocean"
    elif any(word in user_input for word in ["indian"]):
        region = "indian ocean"
    
    # Extract chart type
    chart_type = "map"  # default for valid data requests
    if any(word in user_input for word in ["trend", "line", "time", "over time", "change", "history"]):
        chart_type = "line"
    elif any(word in user_input for word in ["stats", "statistics", "numbers", "average", "min", "max"]):
        chart_type = "stats"
    
    # IMPROVED: Better validation - need BOTH parameter AND region, OR clear action
    if parameter and region:
        # Perfect - has both parameter and region
        return "show_data", parameter, region, chart_type
    elif parameter and not region:
        # Has parameter but no region - ask for region
        return "need_region", parameter, None, chart_type
    elif region and not parameter:
        # Has region but no parameter - ask for parameter
        return "need_parameter", None, region, chart_type
    else:
        # Has some ocean keywords but unclear what they want
        return "unclear", None, None, None


# In app.py, replace the entire function with this

def generate_help_response():
    """Generate helpful command examples"""
    help_text = """🌊 **Welcome to FloatChat!** Here's what I can do:

**📍 Available Regions:**   
• Bay of Bengal (data available)  
• Arabian Sea (data available)  
• Pacific Ocean (limited data)

**🔬 Parameters I understand:**   
• Temperature, temp, warm, cold  
• Salinity, salt, salty

**📊 Chart types:**   
• Maps: "show temperature map"  
• Trends: "temperature trend over time"  
• Statistics: "temperature stats"

**💬 Try these commands:**   
• "Show temperature in Bay of Bengal"  
• "Salinity trend Arabian Sea"  
• "Temperature statistics"  
• "What's the salinity map for Bengal?" """
    return help_text

def render_dashboard_page():
    """Renders the Dashboard/Landing Page."""
    st.title("🌊 Welcome to FloatChat!")
    st.markdown("Your AI assistant for exploring real-time ocean data from Argo floats.")
    
    st.markdown("---")

    st.subheader("About This Project")
    st.write("""
    FloatChat is designed to make oceanographic data accessible to everyone. 
    Using natural language, you can ask the chatbot to generate visualizations for key ocean parameters
    like temperature and salinity in different regions.
    """)

    st.subheader("User Guide")
    with st.expander("📍 Available Regions & Keywords"):
        st.markdown("- **Bay of Bengal** (Use: `bengal`)")
        st.markdown("- **Arabian Sea** (Use: `arabian`)")

    with st.expander("🔬 Available Parameters & Keywords"):
        st.markdown("- **Temperature** (Use: `temperature`, `temp`)")
        st.markdown("- **Salinity** (Use: `salinity`, `salt`)")
    
    with st.expander("📊 Available Chart Types & Keywords"):
        st.markdown("- **Map:** Shows data points on a map. (Use: `map`)")
        st.markdown("- **Trend:** Shows changes over time. (Use: `trend`)")
        st.markdown("- **Statistics:** Shows a statistical box plot. (Use: `stats`)")

    st.markdown("---")
    
    # Session state is used to switch pages
    if st.button("Start Chatting! 🚀"):
        st.session_state.page = "Chatbot"
        st.rerun()
        
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

# FIXED: Enhanced response generation with proper error handling
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
            if region not in ["bay of bengal", "arabian sea"]:
                return f"""🌍 I'd love to show you {region} data, but currently I only have data for:
• Bay of Bengal
• Arabian Sea

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
            stats = get_simple_stats(data)
            
            # Create appropriate chart
            if chart_type == "line":
                fig = create_simple_line_chart(data, f"{parameter.title()} Trend in {region.title()}")
                response = f"📈 Here's the {parameter} trend for {region}! The line shows how {parameter} changes over time."
            elif chart_type == "stats":
                fig = create_stats_chart(stats, parameter.title())
                response = f"📊 Here are the {parameter} statistics for {region}! This shows the minimum, average, and maximum values."
            else:  # map
                fig = create_temperature_map(data, f"{parameter.title()} in {region.title()}")
                response = f"🗺️ Here's the {parameter} distribution map for {region}! Colors show different {parameter} levels across the region."
            
            # Add detailed statistics
            if stats:
                if parameter == "temperature":
                    unit = "°C"
                else:
                    unit = "PSU" if parameter == "salinity" else "units"
                    
                response += f"""

**📋 Quick Stats:**
• **Average:** {stats['mean']:.2f}{unit}
• **Range:** {stats['min']:.2f}{unit} to {stats['max']:.2f}{unit}
• **Data points:** {stats['shape'][0]} days, {stats['shape'][1]}×{stats['shape'][2]} locations"""
            
            return response, fig
        
        # Fallback
        return generate_unknown_response(), None
        
    except Exception as e:
        return f"""❌ Oops! Something went wrong: {str(e)}

Try asking something like 'show temperature Bay of Bengal' or type 'help' for examples!""", None

# Initialize chat history with welcome message
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": generate_help_response(),
            "chart": None
        }
    ]

# FIXED: Display chat messages with unique keys
message_counter = 0
for message in st.session_state.messages:
    message_counter += 1
    if message["role"] == "user":
        st.markdown(f'<div class="user-message">{message["content"]}</div>', 
                   unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">{message["content"]}</div>', 
                   unsafe_allow_html=True)
        # FIXED: Display chart with unique key
        if "chart" in message and message["chart"] is not None:
            st.plotly_chart(message["chart"], use_container_width=True, key=f"chart_{message_counter}")
# Add before the chat input section
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
    loading_placeholder = st.empty()
    
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

page = st.sidebar.radio(
    "Navigation", 
    ("Dashboard", "Chatbot"), 
    key="page_select", 
    on_change=lambda: setattr(st.session_state, 'page', st.session_state.page_select)
)

if st.session_state.page == "Dashboard":
    render_dashboard_page()
else:
    # We will create the render_chatbot_page() function in the next step.
    # For now, this will cause an error, which we will fix immediately.
    render_chatbot_page()