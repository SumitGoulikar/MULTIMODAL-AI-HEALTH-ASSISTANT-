import warnings
warnings.filterwarnings('ignore')

import os
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
        voice_of_doctor = text_to_speech_with_elevenlabs(
            input_text=doctor_response, 
            output_filepath="final.mp3"
        )
        
        progress(1.0, desc="Done!")

        return speech_to_text_output, doctor_response, voice_of_doctor
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return "❌ Error transcribing audio", f"Error: {str(e)}", None


# Use Blocks with enhanced UI
with gr.Blocks(
    title="AI Doctor",
    theme=gr.themes.Soft(),
    css="""
        .gradio-container {max-width: 1400px !important}
        h1 {text-align: center;}
        """
) as demo:
    
    gr.Markdown("#AI Doctor with Vision and Voice")
    gr.Markdown("### Record your symptoms and provide a medical image for AI-powered diagnosis")
    
    with gr.Row():
        with gr.Column(scale=1):
            # Audio input
            audio_input = gr.Audio(
                sources=["microphone", "upload"],
                type="filepath",
                label="🎤 Record Your Symptoms",
                show_download_button=True
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
                        height=250,
                        mirror_webcam=False
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
                label="👨‍⚕️ Doctor's Diagnosis",
                lines=7,
                interactive=False,
                placeholder="AI doctor's diagnosis will appear here..."
            )
            audio_output = gr.Audio(
                label="🔊 Doctor's Voice Response",
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


if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        quiet=False,  # Show startup info
        show_error=True
    )