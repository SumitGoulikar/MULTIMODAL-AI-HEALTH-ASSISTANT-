# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

import os
from gtts import gTTS
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

# Get API key from environment
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def text_to_speech_with_gtts(input_text, output_filepath):
    """
    Convert text to speech using Google Text-to-Speech
    
    Args:
        input_text (str): Text to convert
        output_filepath (str): Where to save the MP3 file
    
    Returns:
        str: Path to the saved audio file
    """
    language = "en"

    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    
    print(f"Audio saved successfully to {output_filepath}")
    return output_filepath


def text_to_speech_with_elevenlabs(input_text, output_filepath):
    """
    Convert text to speech using ElevenLabs API (Updated for new API)
    
    Args:
        input_text (str): Text to convert
        output_filepath (str): Where to save the MP3 file
    
    Returns:
        str: Path to the saved audio file
    """
    try:
        # Check if API key is available
        if not ELEVENLABS_API_KEY:
            print("Warning: ELEVENLABS_API_KEY not found. Using gTTS as fallback.")
            return text_to_speech_with_gtts(input_text, output_filepath)
        
        # Initialize ElevenLabs client
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        
        # Generate speech using NEW API
        response = client.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB",  # Adam voice (professional male voice)
            optimize_streaming_latency="0",
            output_format="mp3_22050_32",
            text=input_text,
            model_id="eleven_turbo_v2",
            voice_settings=VoiceSettings(
                stability=0.5,
                similarity_boost=0.8,
                style=0.0,
                use_speaker_boost=True,
            ),
        )
        
        # Save the audio to file
        with open(output_filepath, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)
        
        print(f"Audio saved successfully to {output_filepath}")
        return output_filepath
        
    except Exception as e:
        print(f"Error with ElevenLabs TTS: {e}")
        print("Falling back to gTTS...")
        return text_to_speech_with_gtts(input_text, output_filepath)


# Test the functions if running directly
if __name__ == "__main__":
    test_text = "Hello, I am your AI doctor. How can I help you today?"
    
    print("Testing gTTS...")
    text_to_speech_with_gtts(test_text, "test_gtts.mp3")
    
    print("\nTesting ElevenLabs...")
    text_to_speech_with_elevenlabs(test_text, "test_elevenlabs.mp3")