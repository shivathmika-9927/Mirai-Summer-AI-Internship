import random
import requests
import streamlit as st
from urllib.parse import quote

st.set_page_config(
    page_title="AI Image Studio",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 AI Image Studio")
st.write("Generate beautiful AI images with different art styles.")

# ------------------------------------------------
# Sidebar
# ------------------------------------------------

st.sidebar.header("⚙ Generation Settings")

art_style = st.sidebar.selectbox(
    "Select Art Style",
    [
        "Photorealistic",
        "Digital Art",
        "Anime",
        "Oil Painting",
        "Cyberpunk"
    ]
)

width = st.sidebar.slider(
    "Image Width",
    256,
    1024,
    768,
    step=64
)

height = st.sidebar.slider(
    "Image Height",
    256,
    1024,
    768,
    step=64
)

# Assignment Task 3
magic_enhance = st.sidebar.checkbox("✨ Enable Magic Enhance")

# ------------------------------------------------

user_prompt = st.text_input(
    "Describe your masterpiece..."
)

# Assignment Task 4

surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A dragon made entirely of stained glass",
    "A treehouse city floating above the clouds",
    "A robot painting a sunset on a canvas"
]

# ------------------------------------------------

def generate_and_display(prompt):

    full_prompt = f"{prompt}, {art_style}"

    if magic_enhance:
        full_prompt += ", masterpiece, 8k resolution, highly detailed, trending on artstation, unreal engine 5 render"

    encoded_prompt = quote(full_prompt)

    # Assignment Task 1
    url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width={width}&height={height}"
    )

    with st.spinner("🎨 Generating Image..."):

        try:

            response = requests.get(
                url,
                timeout=60
            )

            if response.status_code == 200:

                st.success("✅ Image Generated Successfully!")

                st.image(
                    response.content,
                    caption=full_prompt,
                    use_container_width=True
                )

                # Assignment Task 2

                st.download_button(
                    label="⬇ Download Image",
                    data=response.content,
                    file_name=f"{art_style}_image.png",
                    mime="image/png"
                )

            else:

                st.error(f"API Error ({response.status_code})")
                st.write(response.text)

        except Exception as e:

            st.error(f"Error: {e}")

# ------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    if st.button("🎨 Generate Image"):

        if user_prompt.strip() == "":

            st.warning("Please enter a prompt.")

        else:

            generate_and_display(user_prompt)

with col2:

    if st.button("🎲 Surprise Me!"):

        random_prompt = random.choice(surprise_prompts)

        st.success(f"🎲 Prompt: {random_prompt}")

        generate_and_display(random_prompt)