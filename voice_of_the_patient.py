# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

import logging
import os
from groq import Groq

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    """
    Transcribe audio file using Groq's Whisper API
    
    Args:
        stt_model (str): Model name (e.g., "whisper-large-v3")
        audio_filepath (str): Path to audio file
        GROQ_API_KEY (str): Groq API key
    
    Returns:
        str: Transcribed text
    """
    try:
        # Validate API key
        if not GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not set. Please check your .env file")
        
        # Validate file exists
        if not os.path.exists(audio_filepath):
            raise FileNotFoundError(f"Audio file not found: {audio_filepath}")
        
        # Check file size
        file_size = os.path.getsize(audio_filepath)
        if file_size == 0:
            raise ValueError("Audio file is empty")
        
        logging.info(f"Transcribing audio file: {audio_filepath} (size: {file_size} bytes)")
        
        # Initialize Groq client
        client = Groq(api_key=GROQ_API_KEY)
        
        # Open and transcribe audio file
        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en",
                response_format="text"  # Get plain text response
            )
        
        logging.info(f"Transcription successful: {transcription}")
        
        # Handle both text and object responses
        if isinstance(transcription, str):
            return transcription
        else:
            return transcription.text
        
    except FileNotFoundError as e:
        logging.error(f"File error: {e}")
        raise
    except ValueError as e:
        logging.error(f"Validation error: {e}")
        raise
    except Exception as e:
        logging.error(f"Error in transcribe_with_groq: {e}")
        import traceback
        traceback.print_exc()
        raise Exception(f"Transcription failed: {str(e)}")


# For testing purposes only
if __name__ == "__main__":
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    if GROQ_API_KEY:
        # Test with an existing audio file
        test_file = "test_audio.wav"
        if os.path.exists(test_file):
            result = transcribe_with_groq(
                stt_model="whisper-large-v3",
                audio_filepath=test_file,
                GROQ_API_KEY=GROQ_API_KEY
            )
            print(f"Transcription: {result}")
        else:
            print(f"Test file not found: {test_file}")
    else:
        print("GROQ_API_KEY not found in environment")