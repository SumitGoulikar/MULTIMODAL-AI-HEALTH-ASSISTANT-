# Multimodal AI Health Assistant

A smart healthcare assistant combining **voice**, **vision**, and **AI-driven medical analysis** to support early symptom evaluation and accessibility in remote environments.

---

## 🚀 Overview

This application enables users to:
- Speak about their symptoms using a microphone
- Upload medical images such as skin photos or X-rays
- Receive AI-generated insights and audio responses in real time

Designed as an **educational research project** in healthcare AI — not a clinical diagnostic tool.

---

## 🧠 Core Capabilities
- **Speech Understanding** – Whisper-based speech recognition
- **Medical Image Analysis** – Llama Vision model for image insights
- **Natural Speech Output** – ElevenLabs / gTTS voice generation
- **Intuitive UI** – Built with Gradio for a smooth experience
- **Fast & Secure** – API-based processing with local privacy handling

---

## 🛠 Tech Stack

| Component | Technology |
|----------|------------|
| UI | Gradio |
| Backend | Python 3.11+ |
| Speech-to-Text | Groq Whisper |
| Vision Model | Meta Llama Scout |
| Text-to-Speech | ElevenLabs + gTTS |
| Media Processing | FFmpeg |

---

## 📦 Project Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/SumitGoulikar/MULTIMODAL-AI-HEALTH-ASSISTANT-.git
cd MULTIMODAL-AI-HEALTH-ASSISTANT-
```

2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
3️⃣ Configure Environment Variables
```bash
cp .env.example .env
```

Add your API keys:
```
GROQ_API_KEY=your_key_here
ELEVENLABS_API_KEY=your_key_here   # Optional
```
4️⃣ Install FFmpeg
```
Windows: choco install ffmpeg
```
```
macOS: brew install ffmpeg
```
```
Linux: sudo apt install ffmpeg
```
5️⃣ Run Application
```
python gradio_app.py
```

Access in browser → http://127.0.0.1:7860
```
📂 Folder Structure
├─ gradio_app.py           # Main application
├─ brain_of_the_doctor.py  # Vision model logic
├─ voice_of_the_patient.py # Speech recognition
├─ voice_of_the_doctor.py  # TTS output
├─ requirements.txt
├─ Dockerfile
└─ .env.example
```
⚠️ Disclaimer

This system is not approved for clinical or emergency medical use.
It is intended only for learning, experimentation, and research.

Always consult a licensed healthcare professional for medical concerns.

🤝 Contributing

Contributions are welcome!
Feel free to:

Open issues

Submit pull requests

Suggest enhancements

📬 Contact

Developer: Sumit Goulikar
Email: sumithgoulikar2004@gmail.com

GitHub: https://github.com/SumitGoulikar

If this project helps you, please ⭐ star the repository to support it!
