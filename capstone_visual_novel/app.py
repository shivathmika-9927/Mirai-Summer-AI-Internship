"""
app.py
The Multi-Modal Visual Novel — Capstone Mini-Project
MirAI School of Technology | Virtual Summer Internship 2026 | AI Builder Track
"""

import streamlit as st
import google.generativeai as genai
import requests
import json
import os
import tempfile
from gtts import gTTS
from PIL import Image
from io import BytesIO
import time
import random
import urllib.parse
from datetime import datetime
import re

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="AI Visual Novel - MirAI Capstone",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
    
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
        animation: glow 3s ease-in-out infinite;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 3px;
    }
    
    @keyframes glow {
        0%, 100% { filter: drop-shadow(0 0 20px rgba(102, 126, 234, 0.3)); }
        50% { filter: drop-shadow(0 0 40px rgba(118, 75, 162, 0.6)); }
    }
    
    .sub-header {
        text-align: center;
        color: #8892b0;
        font-size: 1.1rem;
        margin-top: -0.5rem;
        margin-bottom: 1rem;
        font-style: italic;
    }
    
    .story-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .story-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 48px rgba(102, 126, 234, 0.15);
    }
    
    .story-text {
        font-size: 1.1rem;
        line-height: 1.8;
        color: #e6e6e6;
        padding: 1.2rem;
        background: rgba(0,0,0,0.2);
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .sidebar-header {
        font-size: 1.3rem;
        font-weight: 600;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(102, 126, 234, 0.3);
    }
    
    .stats-box {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .image-container {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        transition: all 0.5s ease;
    }
    
    .image-container:hover {
        transform: scale(1.02);
        box-shadow: 0 12px 48px rgba(102, 126, 234, 0.3);
    }
    
    .audio-container {
        background: rgba(102, 126, 234, 0.1);
        border: 2px solid rgba(102, 126, 234, 0.4);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .audio-label {
        color: #a78bfa;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .choice-button {
        width: 100%;
        padding: 0.8rem 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 1rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        text-align: center;
        margin: 0.3rem 0;
    }
    
    .choice-button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #764ba2 0%, #f093fb 100%);
    }
    
    .progress-container {
        width: 100%;
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        height: 6px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    .model-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 0.25rem 1rem;
        border-radius: 20px;
        color: white;
        font-size: 0.8rem;
        font-weight: 600;
        text-align: center;
    }
    
    .game-over {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 15px;
        margin: 1rem 0;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .game-over h2 {
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .game-over p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
    }
    
    .welcome-features {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .feature-item {
        text-align: center;
        padding: 1rem;
    }
    
    .feature-item div:first-child {
        font-size: 2.5rem;
    }
    
    .feature-item div:last-child {
        color: #8892b0;
        margin-top: 0.5rem;
    }
    
    .api-status {
        padding: 0.5rem;
        border-radius: 8px;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    
    .api-success {
        background: rgba(0, 255, 0, 0.1);
        color: #00ff88;
        border: 1px solid rgba(0, 255, 0, 0.2);
    }
    
    .api-warning {
        background: rgba(255, 165, 0, 0.1);
        color: #ffa500;
        border: 1px solid rgba(255, 165, 0, 0.2);
    }
    
    .stAudio {
        width: 100% !important;
    }
    
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #f093fb);
    }
    </style>
""", unsafe_allow_html=True)

# ==================== CONSTANTS ====================
GENRES = [
    "Fantasy",
    "Science Fiction", 
    "Mystery",
    "Horror",
    "Romance",
    "Adventure",
    "Cyberpunk",
    "Steampunk",
    "Historical",
    "Comedy",
    "Drama",
    "Thriller"
]

ART_STYLES = {
    "Digital Painting": "Rich colors, smooth gradients, digital art techniques",
    "Watercolor": "Soft edges, flowing colors, artistic brush strokes",
    "Oil Painting": "Rich textures, visible brush strokes, classical feel",
    "Anime": "Bold lines, vibrant colors, anime/manga style",
    "Pixel Art": "Retro gaming style, blocky pixels, vibrant colors",
    "Realistic": "Photorealistic, detailed textures, lifelike",
    "Cartoon": "Bold outlines, bright colors, whimsical style",
    "3D Render": "3D rendered, detailed lighting, modern CG",
    "Sketch": "Pencil or charcoal style, monochromatic, artistic",
    "Abstract": "Abstract shapes, surreal, artistic expression",
}

# ==================== SESSION STATE ====================
def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        'chat_contents': [],
        'story_log': [],
        'story_started': False,
        'story_count': 0,
        'total_choices': 0,
        'choice_made': False,
        'game_over': False,
        'branch_history': [],
        'current_model': None,
        'api_key_loaded': False,
        'available_models': [],
        'audio_debug': []
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

init_session_state()

# ==================== GET API KEY FROM SECRETS ====================
def get_api_key_from_secrets():
    """Try to load API key from Streamlit secrets."""
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
        if api_key:
            st.session_state.api_key_loaded = True
            return api_key
        
        api_key = st.secrets.get("gemini_api_key")
        if api_key:
            st.session_state.api_key_loaded = True
            return api_key
            
        api_key = st.secrets.get("GOOGLE_API_KEY")
        if api_key:
            st.session_state.api_key_loaded = True
            return api_key
            
    except Exception:
        pass
    return None

# ==================== GET AVAILABLE MODELS ====================
@st.cache_data(show_spinner=False)
def get_available_models(api_key):
    """Get list of available Gemini models."""
    try:
        genai.configure(api_key=api_key)
        models = []
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                models.append(model.name)
        return models
    except Exception as e:
        return []

# ==================== PHASE 1: CACHED GEMINI CLIENT ====================
@st.cache_resource(show_spinner=False)
def get_gemini_client(api_key):
    """Initialize and cache Gemini client with automatic model discovery."""
    try:
        if not api_key:
            return None
        
        genai.configure(api_key=api_key)
        
        available_models = get_available_models(api_key)
        
        if not available_models:
            return None
        
        preferred_models = [
            'models/gemini-2.0-flash-exp',
            'models/gemini-2.0-flash',
            'models/gemini-1.5-flash',
            'models/gemini-1.5-pro',
        ]
        
        for model_name in preferred_models:
            if model_name in available_models:
                try:
                    model = genai.GenerativeModel(model_name)
                    test_response = model.generate_content("test")
                    if test_response:
                        return model
                except Exception:
                    continue
        
        if available_models:
            first_model = available_models[0]
            model = genai.GenerativeModel(first_model)
            return model
        
        return None
        
    except Exception as e:
        return None

# ==================== PHASE 2: STRUCTURED JSON ENGINE ====================
def generate_story_scene(client, genre, player_name="Adventurer", chat_history=None):
    """Generate a story scene with structured JSON output."""
    system_prompt = f"""You are an expert visual novelist and storyteller.
You MUST respond with a valid JSON object containing EXACTLY three keys: 'story_text', 'image_prompt', and 'options'.

Story Genre: {genre}
Player Character: {player_name}

CRITICAL RULES:
1. story_text: Write 3-4 immersive, descriptive sentences.
2. image_prompt: Create a DETAILED prompt for Pollinations API.
3. options: Provide EXACTLY 3 distinct choices.

Response MUST be a valid JSON object only, no other text, no markdown.

Example:
{{
    "story_text": "The ancient door creaks open, revealing a chamber...",
    "image_prompt": "A magnificent fantasy chamber with glowing crystals...",
    "options": [
        "Approach the crystal formation",
        "Search for hidden passages",
        "Call out to see if anyone is here"
    ]
}}
"""

    try:
        if chat_history and len(chat_history) > 0:
            response = client.generate_content(
                system_prompt + "\n\nContinue the story based on the previous context."
            )
        else:
            response = client.generate_content(
                system_prompt + "\n\nGenerate the opening scene of the story."
            )
        
        response_text = response.text.strip()
        
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        try:
            data = json.loads(response_text)
        except json.JSONDecodeError:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
            else:
                raise ValueError("No valid JSON found")
        
        required_keys = ['story_text', 'image_prompt', 'options']
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing key: {key}")
        
        if not isinstance(data['options'], list) or len(data['options']) < 2:
            raise ValueError("Options must be a list with at least 2 choices")
        
        return data
        
    except Exception as e:
        st.error(f"⚠️ Story generation error: {str(e)}")
        return None

# ==================== PHASE 4: IMAGE GENERATION ====================
def fetch_scene_image(image_prompt, art_style, max_retries=3):
    """Fetch image from Pollinations.ai with retry logic."""
    art_style_desc = ART_STYLES.get(art_style, "")
    enhanced_prompt = f"{image_prompt}, {art_style} style, {art_style_desc}, high quality"
    
    for attempt in range(max_retries):
        try:
            encoded_prompt = urllib.parse.quote(enhanced_prompt)
            seed = random.randint(1, 1000)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&seed={seed}&enhance=true"
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            img = Image.open(BytesIO(response.content))
            img_bytes = BytesIO()
            img.save(img_bytes, format='PNG')
            return img_bytes.getvalue()
            
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            else:
                st.toast(f"🎨 Image server busy: {str(e)[:50]}...", icon="🎨")
                return None
    
    return None

# ==================== PHASE 4: AUDIO GENERATION (FIXED) ====================
def synthesize_narration(text, language='en', slow=False):
    """Generate audio narration using gTTS with better error handling."""
    try:
        # Clean text for TTS
        clean_text = text.strip()
        if not clean_text:
            st.session_state.audio_debug.append("Empty text for TTS")
            return None
        
        # Limit text length for TTS (gTTS works better with shorter text)
        if len(clean_text) > 500:
            clean_text = clean_text[:500] + "..."
        
        st.session_state.audio_debug.append(f"Generating TTS for: {clean_text[:50]}...")
        
        # Create TTS object
        tts = gTTS(text=clean_text, lang=language, slow=slow)
        
        # Save to bytes
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        
        # Verify audio was created
        audio_data = audio_bytes.read()
        if len(audio_data) < 1000:  # Should be at least 1KB
            st.session_state.audio_debug.append("Audio file too small - likely empty")
            return None
        
        st.session_state.audio_debug.append(f"Audio generated successfully: {len(audio_data)} bytes")
        return audio_data
        
    except Exception as e:
        error_msg = f"TTS Error: {str(e)}"
        st.session_state.audio_debug.append(error_msg)
        st.toast(f"🔊 Audio error: {str(e)[:50]}", icon="⚠️")
        return None

# ==================== CORE: ADVANCE STORY ====================
def advance_story(action_text, api_key, genre, art_style, player_name, 
                  tts_language='en', tts_slow=False, max_scenes=10):
    """Run one full turn of the engine."""
    if not api_key:
        st.error("⚠️ Please add your Gemini API key.")
        return False
    
    client = get_gemini_client(api_key)
    if not client:
        st.error("⚠️ Failed to initialize Gemini client. Please check your API key.")
        return False
    
    # Add user action
    st.session_state.chat_contents.append(
        {"role": "user", "parts": [{"text": action_text}]}
    )
    
    # Generate scene
    with st.spinner("📖 The narrator is weaving your tale..."):
        scene_data = generate_story_scene(
            client, genre, player_name, st.session_state.chat_contents
        )
    
    if not scene_data:
        st.session_state.chat_contents.pop()
        return False
    
    # Add AI response
    st.session_state.chat_contents.append(
        {"role": "model", "parts": [{"text": scene_data["story_text"]}]}
    )
    
    # Generate image
    image_bytes = None
    with st.spinner("🎨 Painting the scene..."):
        try:
            image_bytes = fetch_scene_image(scene_data["image_prompt"], art_style)
            if image_bytes:
                st.toast("🎨 Scene illustrated!", icon="🎨")
        except Exception:
            st.toast("🎨 Image generation skipped", icon="🎨")
    
    # Generate audio - WITH DEBUG INFO
    audio_bytes = None
    st.session_state.audio_debug = []  # Reset debug
    with st.spinner("🔊 Recording narration..."):
        try:
            audio_bytes = synthesize_narration(
                scene_data["story_text"], 
                tts_language, 
                tts_slow
            )
            if audio_bytes:
                st.toast("🔊 Narration ready! Click play to listen.", icon="🔊")
            else:
                st.toast("🔊 Audio generation failed - check console", icon="⚠️")
        except Exception as e:
            st.toast(f"🔊 Audio error: {str(e)[:50]}", icon="⚠️")
    
    # Update stats
    st.session_state.story_count += 1
    
    # Check game over
    game_over = False
    if st.session_state.story_count >= max_scenes:
        game_over = True
        scene_data["options"] = ["🌟 Start a new adventure", "🔄 Explore a different path"]
    
    # Add to log
    st.session_state.story_log.append({
        "story_text": scene_data["story_text"],
        "image": image_bytes,
        "audio": audio_bytes,  # This should now contain the audio data
        "options": scene_data.get("options", []),
        "timestamp": datetime.now().isoformat(),
        "game_over": game_over,
        "audio_debug": st.session_state.audio_debug.copy()  # Save debug info
    })
    
    st.session_state.story_started = True
    
    if game_over:
        st.session_state.game_over = True
        st.balloons()
    
    return True

# ==================== RESET GAME ====================
def reset_game(genre, art_style):
    """Reset all session state variables."""
    if st.session_state.story_started:
        st.session_state.branch_history.append({
            'timestamp': datetime.now().isoformat(),
            'scenes': st.session_state.story_count,
            'choices': st.session_state.total_choices,
            'genre': genre,
            'art_style': art_style
        })
    
    for key in ['chat_contents', 'story_log', 'story_started', 'story_count',
                'total_choices', 'choice_made', 'game_over', 'audio_debug']:
        if key in st.session_state:
            del st.session_state[key]
    
    init_session_state()
    st.rerun()

# ==================== MAIN APPLICATION ====================
def main():
    # ---------- HEADER ----------
    st.markdown('<div class="main-header">✨ AI Visual Novel Engine ✨</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">🎭 Choose Your Own Adventure • Powered by Gemini & Pollinations</div>',
        unsafe_allow_html=True
    )
    
    # ---------- GET API KEY ----------
    secret_api_key = get_api_key_from_secrets()
    
    # ---------- SIDEBAR ----------
    with st.sidebar:
        st.markdown('<div class="sidebar-header">⚙️ Story Configuration</div>', unsafe_allow_html=True)
        
        if secret_api_key:
            st.markdown(
                '<div class="api-status api-success">✅ API Key loaded from secrets</div>',
                unsafe_allow_html=True
            )
            api_key = st.text_input(
                "🔑 Gemini API Key",
                type="password",
                placeholder="Key loaded from secrets",
                value=secret_api_key,
                key="api_key_input"
            )
            if not api_key or api_key == secret_api_key:
                api_key = secret_api_key
        else:
            st.markdown(
                '<div class="api-status api-warning">⚠️ No API key found in secrets</div>',
                unsafe_allow_html=True
            )
            api_key = st.text_input(
                "🔑 Gemini API Key",
                type="password",
                placeholder="Paste your key here",
                key="api_key_input"
            )
            st.caption("Get a free key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)")
        
        st.divider()
        
        player_name = st.text_input(
            "🧙 Character Name",
            value="Adventurer",
            key="player_name_input"
        )
        
        st.divider()
        
        genre = st.selectbox("📖 Story Genre", GENRES, index=0, key="genre_select")
        art_style = st.selectbox(
            "🎨 Art Style",
            list(ART_STYLES.keys()),
            index=0,
            key="art_style_select",
            format_func=lambda x: f"{x} - {ART_STYLES[x].split(',')[0]}"
        )
        
        st.divider()
        
        with st.expander("🔧 Advanced Settings"):
            tts_language = st.selectbox(
                "🗣️ Narration Language",
                ["en", "es", "fr", "de", "it", "ja", "ko", "zh"],
                index=0
            )
            tts_slow = st.checkbox("🐢 Slow Narration", False)
            max_scenes = st.slider("📊 Max Story Length", 3, 20, 10)
        
        st.divider()
        
        if st.button("🚀 New Game", type="primary", use_container_width=True):
            reset_game(genre, art_style)
        
        st.divider()
        
        st.markdown("### 📊 Adventure Stats")
        with st.container():
            st.markdown('<div class="stats-box">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📖 Scenes", st.session_state.story_count)
            with col2:
                st.metric("🎯 Choices", st.session_state.total_choices)
            
            if st.session_state.story_count > 0:
                progress = min(st.session_state.story_count / max_scenes, 1.0)
                st.markdown(f"""
                <div class="progress-container">
                    <div class="progress-bar" style="width: {progress*100}%;"></div>
                </div>
                <div style="text-align: center; color: #8892b0; font-size: 0.9rem;">
                    Progress: {int(progress*100)}%
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Debug section
        with st.expander("🔍 Debug Info"):
            if st.session_state.audio_debug:
                st.write("Audio Debug:")
                for msg in st.session_state.audio_debug:
                    st.code(msg)
            st.write(f"Story Log Entries: {len(st.session_state.story_log)}")
        
        st.divider()
        st.markdown("""
        <div style="font-size: 0.8rem; color: #666; text-align: center;">
            🎯 MirAI School of Technology 2026<br>
            Built with ❤️ using Streamlit
        </div>
        """, unsafe_allow_html=True)
    
    # ---------- MAIN CONTENT ----------
    
    if not st.session_state.story_started:
        st.markdown("""
        <div class="story-container" style="text-align: center; padding: 3rem;">
            <h2 style="color: #667eea; font-size: 2.5rem;">🌟 Begin Your Epic Adventure</h2>
            <p style="font-size: 1.2rem; color: #ccc; margin: 1rem 0;">
                Every choice shapes your destiny. Every path leads to discovery.
            </p>
            <div class="welcome-features">
                <div class="feature-item">
                    <div>📖</div>
                    <div>Rich Storytelling</div>
                </div>
                <div class="feature-item">
                    <div>🎨</div>
                    <div>AI-Generated Art</div>
                </div>
                <div class="feature-item">
                    <div>🔊</div>
                    <div>Voice Narration</div>
                </div>
                <div class="feature-item">
                    <div>🎯</div>
                    <div>Dynamic Choices</div>
                </div>
            </div>
            <p style="color: #8892b0; font-style: italic;">
                Configure your story in the sidebar and begin your journey!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Start Your Adventure", use_container_width=True, type="primary"):
                if not api_key:
                    st.error("⚠️ Please add your Gemini API key in the sidebar.")
                else:
                    with st.spinner("🎬 Creating your world..."):
                        success = advance_story(
                            f"Start a new {genre} story with the player named {player_name}.",
                            api_key, genre, art_style, player_name,
                            tts_language, tts_slow, max_scenes
                        )
                        if success:
                            st.rerun()
    
    # ---------- DISPLAY STORY LOG WITH AUDIO ----------
    for idx, scene in enumerate(st.session_state.story_log):
        st.markdown("<div class='story-container'>", unsafe_allow_html=True)
        
        st.caption(f"📖 Scene {idx + 1}")
        
        if scene.get("image"):
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown('<div class="image-container">', unsafe_allow_html=True)
                st.image(scene["image"], use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f"<div class='story-text'>{scene['story_text']}</div>", unsafe_allow_html=True)
        
        # ---------- AUDIO PLAYER ----------
        if scene.get("audio"):
            st.markdown("""
            <div class="audio-label">🔊 Listen to Narration:</div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="audio-container">', unsafe_allow_html=True)
            st.audio(scene["audio"], format="audio/mp3")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Show audio info
            st.caption(f"Audio size: {len(scene['audio'])} bytes")
        else:
            st.info("🔇 No audio available for this scene")
            # Show debug info if available
            if scene.get("audio_debug"):
                with st.expander("🔍 Audio Debug Info"):
                    for msg in scene["audio_debug"]:
                        st.code(msg)
        
        if scene.get("timestamp"):
            st.caption(f"⏱️ {scene['timestamp'][:19]}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ---------- PHASE 3: DYNAMIC UI GENERATION ----------
    if st.session_state.story_log and not st.session_state.get("game_over", False):
        latest_scene = st.session_state.story_log[-1]
        latest_options = latest_scene.get("options", [])
        
        if latest_options:
            st.markdown("### 🎯 Choose Your Path:")
            st.markdown("*Select one of the options below to continue your adventure*")
            
            cols = st.columns(min(len(latest_options), 3))
            for idx, option in enumerate(latest_options):
                col_idx = idx % 3
                with cols[col_idx]:
                    button_key = f"choice_{len(st.session_state.story_log)}_{idx}_{hash(option)}"
                    if st.button(
                        f"➡️ {option}",
                        key=button_key,
                        use_container_width=True,
                        help=f"Choose: {option}"
                    ):
                        st.session_state.total_choices += 1
                        with st.spinner("🎬 Advancing the story..."):
                            success = advance_story(
                                option, api_key, genre, art_style, player_name,
                                tts_language, tts_slow, max_scenes
                            )
                            if success:
                                st.rerun()
    
    # ---------- GAME OVER SCREEN ----------
    if st.session_state.get("game_over", False):
        st.markdown(f"""
        <div class="game-over">
            <h2>🎉 Congratulations, Hero!</h2>
            <p>You've completed your adventure with <strong>{st.session_state.story_count}</strong> scenes 
            and <strong>{st.session_state.total_choices}</strong> choices made!</p>
            <p style="font-size: 0.9rem; opacity: 0.8;">
                Start a new game in the sidebar to continue your journey.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ==================== RUN APPLICATION ====================
if __name__ == "__main__":
    main()