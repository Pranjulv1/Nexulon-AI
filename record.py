import sounddevice as sd
import wavio
import time

FILE_NAME = "test.mp3" # Saving directly as mp3 for the client to read
DURATION = 5  # Seconds

def record_audio():
    print("---------------------------------------")
    print(f"🎙️  Recording for {DURATION} seconds...")
    print("   SPEAK NOW: 'Check System Performance'")
    print("---------------------------------------")
    
    # Record audio (requires 'pip install sounddevice wavio scipy')
    fs = 44100 
    recording = sd.rec(int(DURATION * fs), samplerate=fs, channels=2)
    sd.wait()  
    
    # Save as WAV first (wavio handles wav) then we rename for the client
    wavio.write("test.wav", recording, fs, sampwidth=2)
    
    # Python trick to rename it to what client.py expects
    import os
    if os.path.exists("test.mp3"):
        os.remove("test.mp3")
    os.rename("test.wav", "test.mp3")
    
    print("✅ Recording Saved! Run 'python client.py' now.")

if __name__ == "__main__":
    try:
        record_audio()
    except Exception as e:
        print("❌ Error: Missing libraries.")
        print("   Run this command: pip install sounddevice wavio scipy")