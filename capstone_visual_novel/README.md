# 🎭 AI Visual Novel Engine

## MirAI School of Technology | Virtual Summer Internship 2026

An AI-powered "Choose Your Own Adventure" visual novel that generates unique stories, artwork, and narration in real-time.

### 🎬 Demo Video
[![Watch the Demo](https://img.shields.io/badge/🎬-Watch_Demo-667eea?style=for-the-badge)](demo.mp4)

Click the link above or view the `demo.mp4` file in this folder to see the 60-second walkthrough.

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| **📖 Dynamic Storytelling** | Gemini AI generates unique narratives based on your choices |
| **🎨 AI-Generated Art** | Pollinations.ai creates matching artwork for each scene |
| **🔊 Voice Narration** | gTTS provides audio narration for an immersive experience |
| **🎯 Interactive Choices** | Dynamic buttons are generated from AI's structured JSON output |
| **🛡️ Graceful Error Handling** | App continues working even if an API fails |

### 🛠️ Technologies Used

- **[Streamlit](https://streamlit.io/)** - Web application framework
- **[Google Gemini AI](https://ai.google.dev/)** - Story generation with structured JSON output
- **[Pollinations.ai](https://pollinations.ai/)** - Real-time AI image generation
- **[gTTS](https://gtts.readthedocs.io/)** - Google Text-to-Speech for narration

### 📁 Project Structure

```
capstone_visual_novel/
├── app.py                 # Main application code
├── requirements.txt      # Python dependencies
├── demo.mp4              # 60-second screen recording
├── README.md             # Project documentation
└── .streamlit/
    └── secrets.toml      # API keys (excluded from version control)
```

### 🚀 Getting Started

1. **Clone the repository** (or navigate to this folder)
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up your API key:**
   - Create a `.streamlit/secrets.toml` file
   - Add: `GEMINI_API_KEY = "your-key-here"`
4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

### 🎯 How It Works

1. **Configure** your story genre and art style in the sidebar.
2. **Start** the adventure to generate the first scene.
3. **Read** the AI-generated story text.
4. **View** the AI-generated artwork.
5. **Listen** to the voice narration.
6. **Choose** your next action from the dynamic buttons.
7. **Continue** until the story concludes.

### 🤝 Submission Details

- **Student:** [Your Name]
- **Track:** AI Builder
- **Internship:** Virtual Summer Internship 2026
- **Institution:** MirAI School of Technology

### 📄 License
This project was created for educational purposes as part of the MirAI School of Technology internship program.

---

Built with ❤️ for MirAI School of Technology