# app.py
# Main Streamlit Application - Multiple Universes Only

import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from universes import UNIVERSES, get_personality_prompt

# ----------------------------------------
# Load Environment Variables
# ----------------------------------------
load_dotenv()

# Initialize Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ----------------------------------------
# Page Configuration
# ----------------------------------------
st.set_page_config(
    page_title="AI Multiverse",
    page_icon="🌌",
    layout="wide"
)

# ----------------------------------------
# Custom CSS
# ----------------------------------------
st.markdown("""
<style>
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    
    /* Sidebar Styling */
    .css-1d391kg, .css-12oz5g7 {
        background: linear-gradient(180deg, #1a1a2e, #16213e) !important;
        border-right: 2px solid #4a4a6a;
    }
    
    /* Chat Messages - User */
    .user-message {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        max-width: 80%;
        float: right;
        clear: both;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        word-wrap: break-word;
    }
    
    /* Chat Messages - AI */
    .ai-message {
        background: rgba(255, 255, 255, 0.08);
        color: #e0e0e0;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        max-width: 80%;
        float: left;
        clear: both;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        word-wrap: break-word;
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 10px 30px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5) !important;
    }
    
    /* Input Fields */
    .stTextInput > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 25px !important;
        color: white !important;
        padding: 12px 20px !important;
    }
    
    .stTextInput > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px !important;
        color: #a0a0c0 !important;
        font-weight: 600 !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }
    
    /* Dividers */
    hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
        margin: 20px 0 !important;
    }
    
    /* Success Messages */
    .stSuccess {
        background: rgba(46, 204, 113, 0.1) !important;
        border: 1px solid #2ecc71 !important;
        border-radius: 15px !important;
    }
    
    /* Error Messages */
    .stError {
        background: rgba(231, 76, 60, 0.1) !important;
        border: 1px solid #e74c3c !important;
        border-radius: 15px !important;
    }
    
    /* Warning Messages */
    .stWarning {
        background: rgba(241, 196, 15, 0.1) !important;
        border: 1px solid #f1c40f !important;
        border-radius: 15px !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #667eea transparent #764ba2 transparent !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------
# Initialize Session State
# ----------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_ai" not in st.session_state:
    st.session_state.current_ai = "🤖 Select an AI"
if "current_personality" not in st.session_state:
    st.session_state.current_personality = None

# ----------------------------------------
# Helper Functions
# ----------------------------------------
def add_to_chat(role, content):
    """Add a message to chat history"""
    st.session_state.chat_history.append({
        "role": role,
        "content": content
    })

def clear_chat():
    """Clear chat history"""
    st.session_state.chat_history = []

def build_predefined_prompt(personality_name, personality_prompt, user_message):
    """Build prompt for predefined personalities"""
    return f"""
You are acting as: {personality_name}

Follow these instructions STRICTLY:

{personality_prompt}

IMPORTANT RULES:
- Never break character
- Never mention that you are an AI
- Stay in character forever
- Respond naturally

User Message:
{user_message}

Your response:
"""

# ----------------------------------------
# Main Header
# ----------------------------------------
st.markdown("""
<div style="text-align: center; padding: 20px 0;">
    <h1 style="font-size: 3.5rem; margin-bottom: 0;">🌌 AI Multiverse</h1>
    <p style="font-size: 1.2rem; color: #a0a0c0; margin-top: 0;">
        Explore a universe of specialized AI assistants
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ----------------------------------------
# Sidebar
# ----------------------------------------
with st.sidebar:
    st.markdown("## 🌌 AI Universes")
    
    # Prebuilt AI Universes
    selected_personality = None
    
    for universe_name, personalities in UNIVERSES.items():
        with st.expander(universe_name, expanded=False):
            for personality_name in personalities.keys():
                if st.button(f"🤖 {personality_name}", key=f"btn_{personality_name}", use_container_width=True):
                    selected_personality = personality_name
                    st.session_state.current_ai = personality_name
                    st.session_state.current_personality = personality_name
                    st.rerun()
    
    st.divider()
    
    # Current AI Display
    st.markdown("### 🤖 Current AI")
    if st.session_state.current_personality:
        st.info(f"🤖 {st.session_state.current_ai}")
    else:
        st.warning("No AI selected")
    
    # Clear Chat Button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        clear_chat()
        st.rerun()

# ----------------------------------------
# Main Chat Area
# ----------------------------------------
col1, col2 = st.columns([3, 1])

with col1:
    # Chat History Display
    chat_history = st.session_state.chat_history
    
    if not chat_history:
        st.markdown("""
        <div style="text-align: center; padding: 60px 20px; color: #a0a0c0;">
            <h3>💬 Start a Conversation</h3>
            <p>Select an AI from the sidebar to begin!</p>
            <p style="font-size: 0.9rem; opacity: 0.7;">
                Currently using: <strong>{}</strong>
            </p>
        </div>
        """.format(st.session_state.current_ai), unsafe_allow_html=True)
    else:
        # Display chat messages
        chat_container = st.container()
        with chat_container:
            for msg in chat_history:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-end; margin: 10px 0;">
                        <div class="user-message">
                            <strong>👤 You</strong><br>
                            {msg['content']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    ai_name = st.session_state.current_ai
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
                        <div class="ai-message">
                            <strong>🤖 {ai_name}</strong><br>
                            {msg['content']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # User Input
    st.divider()
    
    # Check if an AI is selected
    if not st.session_state.current_personality:
        st.warning("⚠️ Please select an AI from the sidebar first!")
        user_message = st.text_input("💬 Type your message here...", disabled=True, key="user_input")
        send_button = st.button("🚀 Send", disabled=True, use_container_width=True)
    else:
        user_message = st.text_input("💬 Type your message here...", key="user_input")
        send_button = st.button("🚀 Send", use_container_width=True)

with col2:
    # Quick Stats
    st.markdown("### 📊 Chat Stats")
    total_messages = len(chat_history)
    user_messages = sum(1 for msg in chat_history if msg["role"] == "user")
    ai_messages = sum(1 for msg in chat_history if msg["role"] == "ai")
    
    st.metric("Total Messages", total_messages)
    st.metric("User Messages", user_messages)
    st.metric("AI Messages", ai_messages)

# ----------------------------------------
# Process User Input
# ----------------------------------------
if send_button and user_message and user_message.strip():
    # Add user message to history
    add_to_chat("user", user_message)
    
    # Get personality prompt
    personality_prompt = get_personality_prompt(st.session_state.current_personality)
    prompt = build_predefined_prompt(
        st.session_state.current_personality,
        personality_prompt,
        user_message
    )
    
    # Generate response with loading animation
    with st.spinner("🌌 Connecting to AI Multiverse..."):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            
            # Add AI response to chat
            add_to_chat("ai", response.text)
            
            # Rerun to update chat display
            st.rerun()
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            st.info("Please make sure your Gemini API key is valid and you have internet connection.")

# ----------------------------------------
# Footer
# ----------------------------------------
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem; padding: 10px;">
    🌌 AI Multiverse — Built with Streamlit & Gemini AI
</div>
""", unsafe_allow_html=True)