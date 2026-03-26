# ⚕️ AI Medical Assistant (Voice + Vision)

AI-powered medical assistant that understands **speech, images, and text** to provide quick health insights.

---

## 🌐 Live Demo

👉 https://multimodal-ai-health-assistant-2.onrender.com/app

---

## 🚀 Overview

An intelligent system that allows users to:

* 🎤 Speak symptoms
* 📸 Upload medical images
* 🧠 Get AI-based analysis
* 🔊 Receive voice explanation

---

## 💡 Key Features

* 🎤 **Speech-to-Text** (Groq Whisper)
* 👁️ **Vision AI** (Llama models for image analysis)
* 🔊 **Text-to-Speech** (ElevenLabs / gTTS fallback)
* ⚡ **Fast Response (~3–5 sec)**
* 🌐 **Multi-input support** (mic, upload, webcam)
* 🔒 **Secure & Private (no data storage)**
* 💻 **Cross-platform UI (Gradio + Web UI)**

---

## 🛠️ Tech Stack

* **Frontend:** Gradio + HTML/CSS
* **Backend:** FastAPI + Python
* **AI Models:** Whisper (STT), Llama Vision
* **Audio:** FFmpeg, PyDub
* **TTS:** ElevenLabs / gTTS

---

## 🆕 Recent Updates

* ✅ Integrated **FastAPI + Gradio mounting**
* ✅ Added **dynamic port handling (fix for port 7860 error)**
* ✅ Improved **server logging & debugging**
* ✅ Enhanced **UI structure and frontend fixes**

---

## ⭐ Clone Repository
```bash
git clone https://github.com/SumitGoulikar/MULTIMODAL-AI-HEALTH-ASSISTANT-.git
cd MULTIMODAL-AI-HEALTH-ASSISTANT-
```

## 🚀 Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python server.py
```

👉 Open: http://127.0.0.1:7860

---

## 📂 Project Structure

```
ai-doctor/
├── server.py                 # FastAPI server
├── gradio_app.py             # Gradio UI
├─ brain_of_the_doctor.py     # Vision model logic
├── voice_of_the_doctor.py    # TTS output
├── voice_of_the_patient.py   # Speech recognition
├── frontend/                 # Landing page
├── assets/                   # Static files
├── requirements.txt
└── .env
```

---

## 🔑 API Setup

Create `.env` file:

```
GROQ_API_KEY=your_key
ELEVENLABS_API_KEY=your_key
```

---

## ⚠️ Disclaimer

* Not a replacement for medical professionals
* For **educational use only**
* Always consult a doctor for real diagnosis

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first.

---

## 📧 Contact

* GitHub: https://github.com/SumitGoulikar
* Email: [sumithgoulikar2004@gmail.com](mailto:sumithgoulikar2004@gmail.com)

---
