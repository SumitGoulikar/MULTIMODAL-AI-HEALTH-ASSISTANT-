import warnings
warnings.filterwarnings('ignore')

import os
import uuid
from pathlib import Path
import gradio as gr

from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs

system_prompt="""You are to respond as a professional and experienced medical doctor. I understand you are not an actual physician, but this is for educational and learning purposes only. Carefully analyze the given image and provide a concise medical interpretation. If you notice any abnormal findings, describe them professionally and state what condition or concern they may suggest. Formulate a brief differential diagnosis if applicable, and offer general remedial or management advice relevant to those possibilities. Do not use any numbers, bullet points, or special characters. Your entire response should be written as a single, natural paragraph that sounds like a doctor speaking directly to a patient. Avoid phrases like “In the image I see” or “As an AI model”; instead, begin naturally with phrases such as “With what I observe, I think you may have…”. Keep the answer short, empathetic, and medically precise, not exceeding two sentences."""


def process_inputs(audio_filepath, image_upload, image_webcam, image_clipboard, progress=gr.Progress()):
    """Process audio and image inputs with progress tracking"""
    
    if not audio_filepath:
        return "⚠️ No audio recorded", "Please record your voice first", None
    
    # Use whichever image source was provided
    image_filepath = image_upload or image_webcam or image_clipboard
    
    try:
        progress(0.1, desc="Processing audio...")
        print(f"✓ Processing audio: {audio_filepath}")
        
        # Transcribe
        progress(0.3, desc="Transcribing speech...")
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
        
        print(f"✓ Transcription: {speech_to_text_output}")

        # Analyze image
        if image_filepath:
            progress(0.5, desc="Analyzing image...")
            print(f"✓ Analyzing image")
            doctor_response = analyze_image_with_query(
                query=system_prompt + speech_to_text_output, 
                encoded_image=encode_image(image_filepath), 
                model="meta-llama/llama-4-scout-17b-16e-instruct"
            )
        else:
            doctor_response = "No image provided for me to analyze"

        progress(0.8, desc="Generating voice response...")
        print(f"✓ Diagnosis complete")

        # Generate voice
        audio_dir = Path(__file__).resolve().parent / "generated_audio"
        audio_dir.mkdir(parents=True, exist_ok=True)
        output_filepath = str(audio_dir / f"{uuid.uuid4().hex}.mp3")
        voice_of_doctor = text_to_speech_with_elevenlabs(
            input_text=doctor_response, 
            output_filepath=output_filepath,
        )
        
        progress(1.0, desc="Done!")

        return speech_to_text_output, doctor_response, voice_of_doctor
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return "❌ Error transcribing audio", f"Error: {str(e)}", None


# Theme sync: apply the saved theme (or system preference) by toggling `html.dark`.
# This keeps the assistant UI in sync with the landing page's theme preference.
THEME_SYNC_SCRIPT = """
<script>
(function () {
  const THEME_KEY = "theme";
  const root = document.documentElement;

  const stored = window.localStorage.getItem(THEME_KEY);
  const theme =
    stored === "light" || stored === "dark"
      ? stored
      : (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");

  root.classList.toggle("dark", theme === "dark");

  // Optional toggle button (top-right) for the assistant UI.
  const btn = document.getElementById("gradioThemeToggle");
  if (!btn) return;

  function updateLabel() {
    btn.textContent = root.classList.contains("dark") ? "Light" : "Dark";
  }

  updateLabel();

  btn.addEventListener("click", function () {
    const next = root.classList.contains("dark") ? "light" : "dark";
    window.localStorage.setItem(THEME_KEY, next);
    root.classList.toggle("dark", next === "dark");
    updateLabel();
  });
})();
</script>
"""

THEME_TOGGLE_HTML = """
<div id="gradio-theme-toggle-wrapper">
  <button id="gradioThemeToggle" type="button">Switch to Dark</button>
</div>
"""


# Use Blocks with enhanced UI
with gr.Blocks(
    title="AI Doctor",
    theme=gr.themes.Soft(),
    css="""
        .gradio-container {max-width: 1400px !important}
        h1 {text-align: center;}

        html.dark {
          color-scheme: dark;
        }
        html.dark body {
          background: #060a14 !important;
          color: #e5e7eb !important;
        }
        html.dark .gradio-container {
          background: transparent !important;
          color: #e5e7eb !important;
        }
        html.dark .prose, html.dark .markdown-body {
          color: #e5e7eb !important;
        }

        #gradio-theme-toggle-wrapper {
          position: fixed;
          top: 14px;
          right: 14px;
          z-index: 9999;
        }
        #gradioThemeToggle {
          cursor: pointer;
          border-radius: 12px;
          border: 1px solid rgba(229, 231, 235, 0.14);
          background: rgba(255, 255, 255, 0.92);
          color: #0f172a;
          padding: 10px 12px;
          font-weight: 800;
          box-shadow: 0 10px 30px rgba(0,0,0,0.12);
          backdrop-filter: blur(10px);
        }
        html.dark #gradioThemeToggle {
          border-color: rgba(229, 231, 235, 0.14);
          background: rgba(11, 18, 32, 0.85);
          color: #e5e7eb;
          box-shadow: 0 12px 34px rgba(0,0,0,0.55);
        }
    """
) as demo:
    
    gr.HTML(THEME_TOGGLE_HTML + THEME_SYNC_SCRIPT)
    gr.Markdown("<h1 style='text-align:center;'>⚕️ AI Medical Assistant</h1>")
    gr.Markdown("---")
    gr.Markdown("<h3>🎤 Record your symptoms and provide a medical image for AI-powered diagnosis</h3>")
    
    with gr.Row():
        with gr.Column(scale=1):
            # Audio input
            audio_input = gr.Audio(
                sources=["microphone", "upload"],
                type="filepath",
                label="🎤 Record Your Symptoms"
            )
            
            # Image tabs
            gr.Markdown("### 📸 Provide Medical Image:")
            with gr.Tabs():
                with gr.Tab("Upload"):
                    image_upload = gr.Image(
                        sources=["upload"],
                        type="filepath",
                        label="Choose from computer",
                        height=250
                    )
                
                with gr.Tab("Webcam"):
                    image_webcam = gr.Image(
                        sources=["webcam"],
                        type="filepath",
                        label="Take photo",
                        height=250
                    )
                
                with gr.Tab("Paste"):
                    image_clipboard = gr.Image(
                        sources=["clipboard"],
                        type="filepath",
                        label="Paste image (Ctrl+V)",
                        height=250
                    )
            
            with gr.Row():
                submit_btn = gr.Button("🩺 Get Diagnosis", variant="primary", size="lg", scale=2)
                clear_btn = gr.ClearButton(value="🔄 Clear All", variant="secondary", size="lg", scale=1)
        
        with gr.Column(scale=1):
            transcription_output = gr.Textbox(
                label="📝 What You Said (Transcription)",
                lines=3,
                interactive=False,
                placeholder="Your transcribed speech will appear here..."
            )
            diagnosis_output = gr.Textbox(
                label="👨‍⚕️ AI medical assistant Diagnosis",
                lines=7,
                interactive=False,
                placeholder="AI medical assistant's diagnosis will appear here..."
            )
            audio_output = gr.Audio(
                label="🔊 AI medical assistant Voice Response",
                autoplay=True,
                show_download_button=True
            )
    
    gr.Markdown("---")
    gr.Markdown("⚠️ **Disclaimer:** This is an AI-powered educational tool and not a substitute for professional medical advice.")
    
    # Connect buttons
    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_input, image_upload, image_webcam, image_clipboard],
        outputs=[transcription_output, diagnosis_output, audio_output]
    )
    
    clear_btn.add([audio_input, image_upload, image_webcam, image_clipboard, 
                   transcription_output, diagnosis_output, audio_output])

# Note: `demo.launch()` is intentionally omitted so this Gradio app can be mounted
# under FastAPI by `server.py` at `/app`.