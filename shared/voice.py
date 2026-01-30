import google.cloud.texttospeech as tts
import os

def generate_voice_google(text: str, output_path: str = "response.mp3"):
    """
    Synthesizes speech using Google Cloud 'Journey' voices.
    """
    client = tts.TextToSpeechClient()
    synthesis_input = tts.SynthesisInput(text=text)
    
    # 'Journey-F' is a high-quality, expressive female AI voice
    # Try 'Journey-D' for a male voice
    voice = tts.VoiceSelectionParams(
        language_code="en-US", 
        name="en-US-Journey-F"
    )
    
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3)

    response = client.synthesize_speech(
        input=synthesis_input, 
        voice=voice, 
        audio_config=audio_config
    )

    with open(output_path, "wb") as out:
        out.write(response.audio_content)
    
    return output_path